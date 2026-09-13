"""Headless Claude Code backend: `claude -p --output-format json`.

Zero marginal cost on a Claude subscription. A minimal system prompt replaces the Claude Code
one (measured: 18k vs 50k+ cached prefix tokens per call); `--bare` is avoided because it
skips keychain auth. The JSON envelope carries the exact model id
under `modelUsage`, which is what gets recorded in every run record.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time

from . import Completion

SYSTEM_PROMPT = (
    "You are a careful assistant completing one text task. Do not use any tools. "
    "Follow the output format in the message exactly."
)


class ClaudeCliBackend:
    name = "claude-cli"

    def __init__(self, binary: str = "claude", retries: int = 3, timeout_s: int = 300) -> None:
        if shutil.which(binary) is None:
            raise RuntimeError("`claude` CLI not found on PATH")
        self.binary = binary
        self.retries = retries
        self.timeout_s = timeout_s

    def complete(self, prompt: str, *, model: str) -> Completion:
        last: Exception | None = None
        for attempt in range(self.retries):
            try:
                return self._once(prompt, model)
            except Exception as exc:  # noqa: BLE001
                last = exc
                time.sleep(2**attempt)
        raise RuntimeError(f"claude-cli failed after {self.retries} attempts: {last}")

    def _once(self, prompt: str, model: str) -> Completion:
        cmd = [
            self.binary,
            "-p",
            "--output-format",
            "json",
            "--model",
            model,
            "--system-prompt",
            SYSTEM_PROMPT,
            "--no-session-persistence",
        ]
        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, timeout=self.timeout_s, check=False
        )
        if proc.returncode != 0:
            raise RuntimeError(f"claude exited {proc.returncode}: {proc.stderr[:500]}")
        return parse_envelope(json.loads(proc.stdout), model)


def pick_model_entry(usage: dict, requested: str) -> tuple[str, dict]:
    """The envelope lists every model the CLI touched, including an internal Haiku side-call.
    Pick the entry whose id contains the requested alias; otherwise the one with the most output."""
    if not usage:
        return "unknown", {}
    for model_id, entry in usage.items():
        if requested.lower() in model_id.lower():
            return model_id, entry
    model_id = max(usage, key=lambda k: int(usage[k].get("outputTokens", 0)))
    return model_id, usage[model_id]


def parse_envelope(env: dict, requested: str) -> Completion:
    if env.get("is_error"):
        raise RuntimeError(f"claude returned error: {str(env.get('result', ''))[:300]}")
    usage = env.get("modelUsage", {})
    model_id, u = pick_model_entry(usage, requested)
    return Completion(
        text=str(env.get("result", "")),
        model_id=model_id,
        input_tokens=int(u.get("inputTokens", 0))
        + int(u.get("cacheReadInputTokens", 0))
        + int(u.get("cacheCreationInputTokens", 0)),
        output_tokens=int(u.get("outputTokens", 0)),
        cost_usd=float(env.get("total_cost_usd", 0.0)),
        raw={
            "session_id": env.get("session_id"),
            "stop_reason": env.get("stop_reason"),
            "all_model_ids": sorted(usage),
        },
    )
