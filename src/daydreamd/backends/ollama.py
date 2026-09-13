"""Ollama backend stub. Local open-weight models are required for the retrospective track
(old-cutoff generator); this is the seam. Not implemented in v0.1."""

from __future__ import annotations

from . import Completion


class OllamaBackend:
    name = "ollama"

    def complete(self, prompt: str, *, model: str) -> Completion:
        raise NotImplementedError(
            "Ollama backend is a v0.2 item; see ROADMAP.md. "
            "Implement by POSTing to http://localhost:11434/api/generate."
        )
