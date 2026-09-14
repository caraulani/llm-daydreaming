"""Obsidian vault adapter: a markdown folder with hidden directories (`.obsidian`, `.trash`)
skipped and the note title (file stem) kept so morning.md can link back with `[[wikilinks]]`."""

from __future__ import annotations

from pathlib import Path

from ..core.ingest import Doc, load_markdown_folder

VAULT_EXCLUDES = ["*.excalidraw.md", "*.canvas"]


def load(path: Path, excludes: list[str] | None = None) -> list[Doc]:
    return load_markdown_folder(path, VAULT_EXCLUDES + list(excludes or []), skip_hidden=True)


def wikilink(doc: Doc) -> str:
    """`[[title]]` for the note, which Obsidian resolves by file stem."""
    return f"[[{Path(doc.name).stem}]]"
