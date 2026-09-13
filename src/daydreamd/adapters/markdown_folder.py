"""Generic markdown folder adapter (the base for the Obsidian adapter)."""

from __future__ import annotations

from pathlib import Path

from ..core.ingest import Doc, load_markdown_folder


def load(path: Path, excludes: list[str] | None = None) -> list[Doc]:
    return load_markdown_folder(path, excludes)
