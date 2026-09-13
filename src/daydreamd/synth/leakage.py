"""Leakage check: no 6-gram of any gold connection may appear in any note."""

from __future__ import annotations

import re

N = 6
STOP_TOKENS = {"the", "a", "an", "of", "to", "and", "in", "on", "is", "are", "that", "it", "for"}


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def ngrams(text: str, n: int = N) -> set[tuple[str, ...]]:
    t = tokens(text)
    return {tuple(t[i : i + n]) for i in range(len(t) - n + 1)}


def leaked_ngrams(note_text: str, gold_texts: list[str], n: int = N) -> list[str]:
    note_grams = ngrams(note_text, n)
    hits = []
    for g in gold_texts:
        for gram in ngrams(g, n) & note_grams:
            if set(gram) - STOP_TOKENS:
                hits.append(" ".join(gram))
    return sorted(set(hits))
