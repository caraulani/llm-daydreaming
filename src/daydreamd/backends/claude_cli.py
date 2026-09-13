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
import threading
import time

from . import Completion

SYSTEM_PROMPT = (
    "You are a careful assistant completing one text task. Do not use any tools. "
    "Follow the output format in the message exactly."
)


# Backoff for a call that fails outright (typically the subscription's usage window is spent).
# Every thread shares one breaker: the first failure trips it, one probe per interval tests
# recovery, and every waiting call resumes together. The pipeline records the pause.
PROBE_INTERVAL_S = 300
MAX_PAUSE_S = 6 * 3600


class ClaudeCliBackend:
    name = "claude-cli"
    _lock = threading.Lock()
    _tripped = False
    _paused_total_s = 0.0

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
        # Three quick failures in a row: assume the usage window is spent and wait for it.
        self._wait_for_recovery(str(last))
        return self._once(prompt, model)

    def _wait_for_recovery(self, reason: str) -> None:
        """Block until a cheap probe succeeds, at most MAX_PAUSE_S. One prober per process."""
        started = time.time()
        while True:
            with ClaudeCliBackend._lock:
                if not ClaudeCliBackend._tripped:
                    ClaudeCliBackend._tripped = True
                    prober = True
                else:
                    prober = False
            if prober:
                try:
                    while time.time() - started < MAX_PAUSE_S:
                        time.sleep(PROBE_INTERVAL_S)
                        try:
                            self._once("Reply with the single word OK.", "haiku")
                            return
                        except Exception:  # noqa: BLE001
                            continue
                    raise RuntimeError(
                        f"claude-cli paused {MAX_PAUSE_S}s without recovery; last error: {reason}"
                    )
                finally:
                    with ClaudeCliBackend._lock:
                        ClaudeCliBackend._tripped = False
                        ClaudeCliBackend._paused_total_s += time.time() - started
            else:
                # another thread is probing; wait for it to clear the breaker
                while ClaudeCliBackend._tripped and time.time() - started < MAX_PAUSE_S:
                    time.sleep(5)
                if time.time() - started >= MAX_PAUSE_S:
                    raise RuntimeError(
                        f"claude-cli paused {MAX_PAUSE_S}s without recovery: {reason}"
                    )
                return

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
