"""Freeze a corpus: copy notes into the run, hash each file and the whole set.

The manifest is the only thing a private run ever needs to publish: file names are replaced by
sha-prefixed ids when `--anonymise` is set, so aggregate statistics can be reported without
revealing what the notes were about.
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass
from pathlib import Path

from .io import sha256_text, write_json
from .run import RunDir, now_iso

DEFAULT_EXCLUDES = ["*credential*", "*secret*", "*password*", "*paperwork*", "MEMORY.md"]


@dataclass
class Doc:
    id: str
    name: str
    text: str
    sha: str
    path: str = ""  # relative posix path inside the corpus (empty for legacy snapshots)

    @property
    def domain(self) -> str:
        """Top-level folder of the note, or "" at the corpus root. The product sampler treats
        notes in different top-level folders as different domains."""
        parts = self.path.split("/")
        return parts[0] if len(parts) > 1 else ""


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def load_markdown_folder(
    source: Path,
    excludes: list[str] | None = None,
    min_words: int = 20,
    skip_hidden: bool = True,
) -> list[Doc]:
    patterns = list(DEFAULT_EXCLUDES) + list(excludes or [])
    docs: list[Doc] = []
    for path in sorted(source.rglob("*.md")):
        rel = path.relative_to(source)
        if skip_hidden and any(part.startswith(".") for part in rel.parts):
            continue  # .obsidian, .trash, .git and friends
        if any(fnmatch.fnmatch(path.name, p) for p in patterns):
            continue
        text = strip_frontmatter(path.read_text(encoding="utf-8", errors="replace")).strip()
        if len(text.split()) < min_words:
            continue
        sha = sha256_text(text)
        docs.append(
            Doc(id=f"doc-{sha[:10]}", name=path.name, text=text, sha=sha, path=rel.as_posix())
        )
    return docs


def _portable(source: Path) -> str:
    """Record the corpus location relative to the working directory, never an absolute path."""
    try:
        return str(source.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return source.name


def snapshot(run: RunDir, docs: list[Doc], source: Path, anonymise: bool) -> dict:
    snap = run.path / "snapshot"
    (snap / "docs").mkdir(parents=True, exist_ok=True)
    for d in docs:
        (snap / "docs" / f"{d.id}.md").write_text(d.text, encoding="utf-8")
    corpus_sha = sha256_text("\n".join(sorted(d.sha for d in docs)))
    manifest = {
        "source": "<private>" if anonymise else _portable(source),
        "frozen_at": now_iso(),
        "n_docs": len(docs),
        "corpus_sha256": corpus_sha,
        "docs": [
            {
                "id": d.id,
                "name": "<redacted>" if anonymise else d.name,
                "path": "<redacted>" if anonymise else d.path,
                "sha256": d.sha,
                "words": len(d.text.split()),
            }
            for d in docs
        ],
    }
    write_json(snap / "manifest.json", manifest)
    run.update_meta(corpus_sha256=corpus_sha, n_docs=len(docs))
    run.mark_stage("snapshot", n_docs=len(docs))
    return manifest


def load_snapshot(run: RunDir) -> list[Doc]:
    from .io import read_json

    manifest = read_json(run.path / "snapshot" / "manifest.json")
    docs = []
    for entry in manifest["docs"]:
        text = (run.path / "snapshot" / "docs" / f"{entry['id']}.md").read_text(encoding="utf-8")
        docs.append(
            Doc(
                id=entry["id"],
                name=entry["name"],
                text=text,
                sha=entry["sha256"],
                path=entry.get("path", ""),
            )
        )
    return docs
