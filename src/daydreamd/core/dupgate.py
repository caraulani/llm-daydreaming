"""Corpus-novelty gate by retrieval, not opinion: a survivor too close to an existing card or
note chunk is marked `already_in_corpus`."""

from __future__ import annotations

import numpy as np

from .embed import Embedder, FakeEmbedder
from .io import write_jsonl
from .run import RunDir

THRESHOLD = 0.85
CHUNK_WORDS = 80


def chunk_text(text: str, size: int = CHUNK_WORDS) -> list[str]:
    words = text.split()
    return [" ".join(words[i : i + size]) for i in range(0, len(words), size)] or [text]


def dupgate(
    run: RunDir,
    embedder: Embedder | FakeEmbedder,
    generations: list[dict],
    critic: list[dict],
    cards: list[dict],
    docs_text: dict[str, str],
    threshold: float = THRESHOLD,
) -> list[dict]:
    kept = {c["unit_id"] for c in critic if c["verdict"] == "keep"}
    survivors = [g for g in generations if g["status"] == "ok" and g["unit_id"] in kept]
    if not survivors:
        write_jsonl(run.path / "dupgate.jsonl", [])
        run.mark_stage("dupgate", n_checked=0, n_dup=0)
        return []
    corpus = [c["claim"] for c in cards] + [ch for t in docs_text.values() for ch in chunk_text(t)]
    corpus_vecs = embedder.encode(corpus)
    surv_vecs = embedder.encode([g["output"]["connection"] for g in survivors])
    sims = surv_vecs @ corpus_vecs.T
    rows = []
    for g, row in zip(survivors, sims, strict=True):
        best = int(np.argmax(row))
        rows.append(
            {
                "unit_id": g["unit_id"],
                "max_cosine": round(float(row[best]), 4),
                "nearest": corpus[best][:160],
                "already_in_corpus": bool(row[best] > threshold),
            }
        )
    write_jsonl(run.path / "dupgate.jsonl", rows)
    run.mark_stage(
        "dupgate",
        n_checked=len(rows),
        n_dup=sum(r["already_in_corpus"] for r in rows),
        threshold=threshold,
    )
    return rows
