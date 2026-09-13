"""obsidian adapter (v0.2). Not implemented in v0.1; see ROADMAP.md and docs/extending.md."""

from __future__ import annotations

from pathlib import Path

from ..core.ingest import Doc


def load(path: Path, excludes: list[str] | None = None) -> list[Doc]:
    raise NotImplementedError("obsidian adapter is planned for v0.2")
