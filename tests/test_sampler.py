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


def test_partner_domain_units_use_fillers_from_partner_domain(cards):
    from daydreamd.core.sampler import partner_domain_units

    gold = {"br01": {"note_a": "n1", "note_b": "n2"}}
    domains = {"n1": "ecom", "n2": "fraud", "fl01": "fraud", "fl02": "ecom", "fl03": "iot"}
    notes = list(domains)
    cards = [
        {"id": f"{n}-c1", "source_note": n, "claim": f"claim of {n}"} for n in notes
    ]  # every note needs at least one card; zero-card notes are skipped by design
    units = partner_domain_units(cards, gold, domains, notes, seed=1)
    assert [u.note_b for u in units] == ["fl01", "fl02"]
    assert all(u.label == "partner:br01" for u in units)
    assert all(u.arm == "S1" for u in units)


def test_cross_domain_near_stays_in_band_and_crosses_domains(cards, vecs):
    from daydreamd.core.sampler import band_edges, candidate_pairs, sample_cross_domain_near

    notes = sorted({c["source_note"] for c in cards})
    domains = {n: ("even" if i % 2 == 0 else "odd") for i, n in enumerate(notes)}
    units = sample_cross_domain_near(cards, vecs, domains, n=5, seed=3)
    _, dist = candidate_pairs(cards, vecs)
    lo, hi = band_edges(dist)["Q1"]
    assert units and all(lo <= u.distance < hi for u in units)
    assert all(domains[u.note_a] != domains[u.note_b] for u in units)
