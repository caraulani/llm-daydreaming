"""Where the product keeps its state: `~/.daydreamd/` (override with `DAYDREAMD_HOME`)."""

from __future__ import annotations

import os
import re
from pathlib import Path


def home() -> Path:
    root = Path(os.environ.get("DAYDREAMD_HOME") or (Path.home() / ".daydreamd"))
    root.mkdir(parents=True, exist_ok=True)
    return root


def cards_cache() -> Path:
    return home() / "cache" / "cards.jsonl"


def runs_root() -> Path:
    return home() / "runs"


def verdicts_path() -> Path:
    return home() / "verdicts.jsonl"


def learnings_path() -> Path:
    return home() / "learnings.md"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "corpus"
