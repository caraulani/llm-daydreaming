"""Corpus adapters. The engine never knows where notes came from; an adapter returns Docs."""

from __future__ import annotations

from pathlib import Path

from ..core.ingest import Doc


def load_corpus(kind: str, path: Path, excludes: list[str] | None = None) -> list[Doc]:
    if kind == "synth":
        from .synth_corpus import load

        return load(path)
    if kind == "claude-memory":
        from .claude_memory import load as load_memory

        return load_memory(path, excludes)
    if kind == "markdown":
        from .markdown_folder import load as load_markdown

        return load_markdown(path, excludes)
    if kind == "arxiv":
        from .arxiv_abstracts import load as load_arxiv

        return load_arxiv(path)
    raise ValueError(f"unknown corpus kind: {kind}")
