from __future__ import annotations

import numpy as np

from daydreamd.core.sampler import (
    BANDS,
    band_edges,
    candidate_pairs,
    sample_anchor_remote,
    sample_banded,
    sample_random,
)


def test_candidate_pairs_exclude_same_note(cards, vecs):
    pairs, dist = candidate_pairs(cards, vecs)
    notes = [c["source_note"] for c in cards]
    assert all(notes[i] != notes[j] for i, j in pairs)
    assert len(pairs) == len(dist) > 0


def test_banded_covers_every_band_and_is_seeded(cards, vecs):
    a = sample_banded(cards, vecs, per_band=2, seed=1)
    b = sample_banded(cards, vecs, per_band=2, seed=1)
    assert [u.unit_id for u in a] == [u.unit_id for u in b]
    assert {u.band for u in a} == set(BANDS)
    _, dist = candidate_pairs(cards, vecs)
    edges = band_edges(dist)
    for u in a:
        lo, hi = edges[u.band]
        assert lo - 1e-4 <= u.distance < hi + 1e-4


def test_random_and_anchor_remote_sizes(cards, vecs):
    assert len(sample_random(cards, vecs, 10, seed=3)) == 10
    ar = sample_anchor_remote(cards, vecs, 5, seed=3)
    assert len(ar) == 5
    _, dist = candidate_pairs(cards, vecs)
    q75 = float(np.quantile(dist, 0.75))
    assert all(u.distance >= q75 - 1e-6 for u in ar)
    assert all(u.note_a != u.note_b for u in ar)
