"""Anthropic Messages API backend. Requires ANTHROPIC_API_KEY and the `anthropic` extra."""

from __future__ import annotations

import os

from . import Completion

ALIASES = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-5",
    "opus": "claude-opus-5",
}


class AnthropicBackend:
    name = "anthropic"

    def __init__(self, max_tokens: int = 1200) -> None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        try:
            import anthropic
        except ImportError as exc:
            raise RuntimeError("install with `uv sync --extra anthropic`") from exc
        self._client = anthropic.Anthropic()
        self.max_tokens = max_tokens

    def complete(self, prompt: str, *, model: str) -> Completion:
        model_id = ALIASES.get(model, model)
        msg = self._client.messages.create(
            model=model_id,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(
            getattr(b, "text", "") for b in msg.content if getattr(b, "type", "") == "text"
        )
        return Completion(
            text=text,
            model_id=msg.model,
            input_tokens=msg.usage.input_tokens,
            output_tokens=msg.usage.output_tokens,
            cost_usd=0.0,
            raw={"stop_reason": msg.stop_reason, "id": msg.id},
        )
