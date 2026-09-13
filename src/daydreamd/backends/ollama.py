"""Ollama backend: local open-weight models through the native chat API.

Two uses. (1) The second writer family for the v0.2 corpus (a non-Anthropic model writes half
the notes, the shared-priors control). (2) The retrospective track needs an old-cutoff
generator, which must be a local open-weight model. Cost is recorded as 0.0; tokens come from
Ollama's ``prompt_eval_count`` and ``eval_count``. The model id is read back from the response
and, when available, extended with the digest from ``/api/show`` so the record is immutable.
"""

from __future__ import annotations

import os
import time

import httpx

from . import Completion

DEFAULT_HOST = "http://localhost:11434"


class OllamaBackend:
    name = "ollama"

    def __init__(self, host: str | None = None, timeout: float = 600.0) -> None:
        self.host = (host or os.environ.get("OLLAMA_HOST") or DEFAULT_HOST).rstrip("/")
        self.timeout = timeout
        self._digests: dict[str, str] = {}

    def _digest(self, model: str) -> str:
        if model in self._digests:
            return self._digests[model]
        digest = ""
        try:
            with httpx.Client(timeout=30.0) as client:
                r = client.post(f"{self.host}/api/show", json={"model": model})
            if r.status_code == 200:
                details = r.json()
                # Ollama exposes the manifest digest on some versions; fall back to modelfile hash.
                digest = str(details.get("digest") or "")
                if not digest and details.get("modelfile"):
                    import hashlib

                    digest = hashlib.sha256(details["modelfile"].encode()).hexdigest()[:12]
        except httpx.HTTPError:
            digest = ""
        self._digests[model] = digest
        return digest

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
            "stream": False,
            "options": {"temperature": 0.7},
        }
        last: Exception | None = None
        for attempt in range(3):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    r = client.post(f"{self.host}/api/chat", json=payload)
                r.raise_for_status()
                data = r.json()
                model_id = str(data.get("model") or model)
                digest = self._digest(model_id)
                return Completion(
                    text=str((data.get("message") or {}).get("content", "") or ""),
                    model_id=f"ollama/{model_id}@{digest}" if digest else f"ollama/{model_id}",
                    input_tokens=int(data.get("prompt_eval_count", 0) or 0),
                    output_tokens=int(data.get("eval_count", 0) or 0),
                    cost_usd=0.0,
                    raw={k: v for k, v in data.items() if k != "message"},
                )
            except (httpx.HTTPError, ValueError) as exc:
                last = exc
                time.sleep(2**attempt)
        raise RuntimeError(f"ollama failed after 3 attempts: {last}")
