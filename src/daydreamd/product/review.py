"""`daydreamd review morning.md`: read the ticked boxes into an append-only verdict log."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..core.io import append_jsonl, read_jsonl
from ..core.run import now_iso
from . import paths
from .morning import parse


@dataclass
class ReviewSummary:
    reviewed: int
    kept: int
    known: int
    unmarked: int
    log: Path


def review(morning: Path) -> ReviewSummary:
    header, dreams = parse(morning.read_text(encoding="utf-8"))
    if not dreams:
        raise RuntimeError(f"{morning} has no dream blocks; was it written by daydreamd?")
    log = paths.verdicts_path()
    stamp = now_iso()
    for d in dreams:
        append_jsonl(
            log,
            {
                "dream_id": d.dream_id,
                "run_id": header.get("run", d.dream_id.split("/")[0]),
                "corpus": header.get("corpus", ""),
                "corpus_sha": header.get("sha", ""),
                "reviewed_at": stamp,
                "keep": d.keep,
                "known": d.known,
                "connection": d.connection,
                "mechanism": d.mechanism,
                "check": d.check,
                "sources": d.sources,
                "critic": d.critic,
                "reason": d.reason,
            },
        )
    kept = sum(1 for d in dreams if d.keep)
    known = sum(1 for d in dreams if d.known and not d.keep)
    return ReviewSummary(
        reviewed=len(dreams),
        kept=kept,
        known=known,
        unmarked=len(dreams) - kept - known,
        log=log,
    )


def latest_verdicts(log: Path | None = None) -> dict[str, dict]:
    """The last verdict recorded for each dream id."""
    out: dict[str, dict] = {}
    for row in read_jsonl(log or paths.verdicts_path()):
        out[row["dream_id"]] = row
    return out
