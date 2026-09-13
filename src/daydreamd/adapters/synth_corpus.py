"""Adapter for the committed synthetic corpus (data/synth/<version>/)."""

from __future__ import annotations

from pathlib import Path

from ..core.ingest import Doc, strip_frontmatter
from ..core.io import read_json, sha256_text


def load(path: Path) -> list[Doc]:
    manifest = read_json(path / "manifest.json")
    docs = []
    for entry in manifest["docs"]:
        raw = (path / "notes" / f"{entry['id']}.md").read_text(encoding="utf-8")
        if sha256_text(raw) != entry["sha256"]:
            raise RuntimeError(f"note {entry['id']} does not match manifest sha; corpus was edited")
        text = strip_frontmatter(raw).strip()
        docs.append(Doc(id=entry["id"], name=f"{entry['id']}.md", text=text, sha=entry["sha256"]))
    return docs
