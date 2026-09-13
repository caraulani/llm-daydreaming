"""Model backends. Every backend returns a Completion with the exact model id and token usage."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class Completion:
    text: str
    model_id: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    raw: dict[str, Any] = field(default_factory=dict)


class Backend(Protocol):
    name: str

    def complete(self, prompt: str, *, model: str) -> Completion: ...


def get_backend(name: str) -> Backend:
    if name == "claude-cli":
        from .claude_cli import ClaudeCliBackend

        return ClaudeCliBackend()
    if name == "anthropic":
        from .anthropic_api import AnthropicBackend

        return AnthropicBackend()
    if name == "ollama":
        from .ollama import OllamaBackend

        return OllamaBackend()
    if name == "openrouter":
        from .openrouter import OpenRouterBackend

        return OpenRouterBackend()
    if name == "fake":
        from .fake import FakeBackend

        return FakeBackend()
    raise ValueError(f"unknown backend: {name}")
