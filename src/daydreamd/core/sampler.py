"""Pair sampling. Every arm produces `units`: the generator's input records.

Card-level arms (B1 random, B3 banded, B6 anchor+remote) draw card pairs from different notes.
Note-level arms (S0 oracle, B4 reflection) hand the generator every card of the note(s), so they
test the generator and critic independently of the sampler.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Any

import numpy as np

BANDS = ("Q1", "Q2-3", "Q4", "top5")


@dataclass
class Unit:
    unit_id: str
    arm: str
    kind: str  # "pair" | "single"
    note_a: str
    note_b: str | None
    claims_a: list[str]
    claims_b: list[str] = field(default_factory=list)
    card_a: str | None = None
    card_b: str | None = None
    band: str | None = None
    distance: float | None = None
    label: str | None = None  # "planted:<bridge>" | "decoy:<id>" | "random" | None

    def to_row(self) -> dict[str, Any]:
        return self.__dict__.copy()


def note_pair_key(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a <= b else (b, a)


def candidate_pairs(cards: list[dict], vecs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Indices (i, j) with i<j from different notes, and cosine distances."""
    n = len(cards)
    notes = np.array([c["source_note"] for c in cards])
    iu, ju = np.triu_indices(n, k=1)
    mask = notes[iu] != notes[ju]
    iu, ju = iu[mask], ju[mask]
    sims = np.einsum("ij,ij->i", vecs[iu], vecs[ju])
    dist = 1.0 - sims
    return np.stack([iu, ju], axis=1), dist


def band_edges(dist: np.ndarray) -> dict[str, tuple[float, float]]:
    q25, q75, q95 = np.quantile(dist, [0.25, 0.75, 0.95])
    return {
        "Q1": (float(dist.min()) - 1e-9, float(q25)),
        "Q2-3": (float(q25), float(q75)),
        "Q4": (float(q75), float(q95)),
        "top5": (float(q95), float(dist.max()) + 1e-9),
    }


def band_of(d: float, edges: dict[str, tuple[float, float]]) -> str:
    for name, (lo, hi) in edges.items():
        if lo <= d < hi:
            return name
    return "top5"


def _unit_from_pair(
    cards: list[dict], i: int, j: int, d: float, arm: str, k: int, edges: dict
) -> Unit:
    a, b = cards[i], cards[j]
    return Unit(
        unit_id=f"{arm}-{k:04d}",
        arm=arm,
        kind="pair",
        note_a=a["source_note"],
        note_b=b["source_note"],
        claims_a=[a["claim"]],
        claims_b=[b["claim"]],
        card_a=a["id"],
        card_b=b["id"],
        band=band_of(d, edges),
        distance=round(float(d), 4),
    )


def sample_random(cards: list[dict], vecs: np.ndarray, n: int, seed: int) -> list[Unit]:
    pairs, dist = candidate_pairs(cards, vecs)
    edges = band_edges(dist)
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(pairs), size=min(n, len(pairs)), replace=False)
    return [
        _unit_from_pair(cards, int(pairs[t, 0]), int(pairs[t, 1]), float(dist[t]), "B1", k, edges)
        for k, t in enumerate(idx)
    ]


def sample_banded(cards: list[dict], vecs: np.ndarray, per_band: int, seed: int) -> list[Unit]:
    pairs, dist = candidate_pairs(cards, vecs)
    edges = band_edges(dist)
    rng = np.random.default_rng(seed)
    units: list[Unit] = []
    k = 0
    for name, (lo, hi) in edges.items():
        pool = np.where((dist >= lo) & (dist < hi))[0]
        take = rng.choice(pool, size=min(per_band, len(pool)), replace=False)
        for t in take:
            u = _unit_from_pair(
                cards, int(pairs[t, 0]), int(pairs[t, 1]), float(dist[t]), "B3", k, edges
            )
            u.band = name
            units.append(u)
            k += 1
    return units


def density_scores(vecs: np.ndarray, k: int = 10) -> np.ndarray:
    sims = vecs @ vecs.T
    np.fill_diagonal(sims, -1.0)
    k = min(k, vecs.shape[0] - 1)
    top = np.sort(sims, axis=1)[:, -k:]
    return top.mean(axis=1)


def sample_anchor_remote(cards: list[dict], vecs: np.ndarray, n: int, seed: int) -> list[Unit]:
    """Uzzi-shaped: anchor from the densest 20% of cards, remote at Q4 or farther."""
    pairs, dist = candidate_pairs(cards, vecs)
    edges = band_edges(dist)
    q75 = edges["Q4"][0]
    rng = np.random.default_rng(seed)
    dens = density_scores(vecs)
    dense = np.where(dens >= np.quantile(dens, 0.8))[0]
    notes = [c["source_note"] for c in cards]
    units: list[Unit] = []
    seen: set[tuple[int, int]] = set()
    attempts = 0
    while len(units) < n and attempts < n * 50:
        attempts += 1
        i = int(rng.choice(dense))
        d_row = 1.0 - vecs @ vecs[i]
        far = [j for j in np.where(d_row >= q75)[0] if notes[j] != notes[i]]
        if not far:
            continue
        j = int(rng.choice(far))
        key = (min(i, j), max(i, j))
        if key in seen:
            continue
        seen.add(key)
        units.append(_unit_from_pair(cards, i, j, float(d_row[j]), "B6", len(units), edges))
    return units


def cards_by_note(cards: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for c in cards:
        out.setdefault(c["source_note"], []).append(c)
    return out


def note_units(cards: list[dict], note_pairs: list[tuple[str, str, str]], arm: str) -> list[Unit]:
    """S0 oracle units: (note_a, note_b, label) triples, every card of each note."""
    by_note = cards_by_note(cards)
    units = []
    for k, (a, b, label) in enumerate(note_pairs):
        units.append(
            Unit(
                unit_id=f"{arm}-{k:04d}",
                arm=arm,
                kind="pair",
                note_a=a,
                note_b=b,
                claims_a=[c["claim"] for c in by_note.get(a, [])],
                claims_b=[c["claim"] for c in by_note.get(b, [])],
                label=label,
            )
        )
    return units


def single_units(cards: list[dict], notes: list[str], arm: str = "B4") -> list[Unit]:
    by_note = cards_by_note(cards)
    return [
        Unit(
            unit_id=f"{arm}-{k:04d}",
            arm=arm,
            kind="single",
            note_a=n,
            note_b=None,
            claims_a=[c["claim"] for c in by_note.get(n, [])],
        )
        for k, n in enumerate(notes)
    ]


def random_note_pairs(
    notes: list[str], domains: dict[str, str], excluded: set[tuple[str, str]], n: int, seed: int
) -> list[tuple[str, str]]:
    """Cross-domain note pairs that are neither planted nor decoys."""
    rng = np.random.default_rng(seed)
    pool = [
        note_pair_key(a, b)
        for a, b in itertools.combinations(sorted(notes), 2)
        if domains.get(a) != domains.get(b) and note_pair_key(a, b) not in excluded
    ]
    idx = rng.choice(len(pool), size=min(n, len(pool)), replace=False)
    return [pool[int(t)] for t in idx]


def label_units(
    units: list[Unit], planted: dict[tuple[str, str], str], decoys: dict[tuple[str, str], str]
) -> None:
    for u in units:
        if u.kind != "pair" or u.note_b is None:
            continue
        key = note_pair_key(u.note_a, u.note_b)
        if key in planted:
            u.label = f"planted:{planted[key]}"
        elif key in decoys:
            u.label = f"decoy:{decoys[key]}"
        elif u.label is None:
            u.label = "random"
