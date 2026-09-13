"""Adapter for a Claude Code memory directory (`~/.claude/projects/<slug>/memory`).

Strips YAML frontmatter, excludes MEMORY.md (the index) and any file whose name matches a
secret-like pattern. Add more patterns with `--exclude`. Nothing is uploaded: the run directory
for a private corpus is gitignored, and the manifest can be anonymised."""

from __future__ import annotations

from pathlib import Path

from ..core.ingest import Doc, load_markdown_folder

SECRET_PATTERNS = ["*credential*", "*secret*", "*password*", "*paperwork*", "*token*", "MEMORY.md"]


def load(path: Path, excludes: list[str] | None = None) -> list[Doc]:
    return load_markdown_folder(path, SECRET_PATTERNS + list(excludes or []))
