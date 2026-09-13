"""OpenRouter backend (OpenAI-compatible chat completions) for non-Anthropic model families.

Used for the v0.2 corpus so that half the notes are written by a model outside the Anthropic
family (the shared-priors control). Needs ``OPENROUTER_API_KEY`` in the environment. The exact
model id is read back from the response envelope, never from the alias requested. Cost is read
from OpenRouter's usage accounting when present.
"""

from __future__ import annotations

import os
import time

import httpx

from . import Completion

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterBackend:
    name = "openrouter"

    def __init__(self, api_key: str | None = None, timeout: float = 120.0) -> None:
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set")
        self.timeout = timeout

    def complete(self, prompt: str, *, model: str) -> Completion:
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a careful assistant completing one text task. "
                    "Follow the output format exactly.",
                },
                {"role": "user", "content": prompt},
            ],
            "usage": {"include": True},
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/caraulani/llm-daydreaming",
            "X-Title": "daydreamd",
        }
        last: Exception | None = None
        for attempt in range(3):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    r = client.post(ENDPOINT, json=payload, headers=headers)
                if r.status_code in (429, 500, 502, 503, 504):
                    raise httpx.HTTPStatusError(
                        f"status {r.status_code}", request=r.request, response=r
                    )
                r.raise_for_status()
                data = r.json()
                choice = data["choices"][0]
                usage = data.get("usage", {}) or {}
                return Completion(
                    text=(choice.get("message", {}) or {}).get("content", "") or "",
                    model_id=str(data.get("model") or model),
                    input_tokens=int(usage.get("prompt_tokens", 0) or 0),
                    output_tokens=int(usage.get("completion_tokens", 0) or 0),
                    cost_usd=float(usage.get("cost", 0.0) or 0.0),
                    raw=data,
                )
            except (httpx.HTTPError, KeyError, ValueError) as exc:  # transport or envelope
                last = exc
                time.sleep(2**attempt)
        raise RuntimeError(f"openrouter failed after 3 attempts: {last}")
