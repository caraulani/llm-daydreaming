"""Post-hoc, exploratory: where do the planted bridges sit in the embedding-distance distribution?

Written 2026-09-13 while the sealed micro run was still generating. Inputs read: the run's
``cards.jsonl``, ``embeddings.npy``, ``gold.json`` and ``domains.json`` (all produced before the
generator stage). No generation, critic or match output had been read when this was written.

Usage: ``uv run python -m daydreamd.eval.distance_posthoc experiments/runs/public/<run>``
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np


def analyse(run: Path) -> dict:
    cards = [json.loads(line) for line in (run / "cards.jsonl").open(encoding="utf-8")]
    vecs = np.load(run / "embeddings.npy")
    vecs = vecs / np.linalg.norm(vecs, axis=1, keepdims=True)
    gold = json.loads((run / "gold.json").read_text(encoding="utf-8"))
    domains = json.loads((run / "domains.json").read_text(encoding="utf-8"))
    dist = 1.0 - vecs @ vecs.T
    by_note: dict[str, list[int]] = {}
    for i, c in enumerate(cards):
        by_note.setdefault(c["source_note"], []).append(i)
    notes = sorted(by_note)
    all_pairs: list[float] = []
    cross_min: list[float] = []
    for a, b in itertools.combinations(notes, 2):
        sub = dist[np.ix_(by_note[a], by_note[b])]
        all_pairs.extend(sub.ravel().tolist())
        if domains.get(a) != domains.get(b):
            cross_min.append(float(sub.min()))
    arr = np.array(all_pairs)
    q25, q75, q95 = np.quantile(arr, [0.25, 0.75, 0.95])
    rows = []
    for bid, g in sorted(gold.items()):
        sub = dist[np.ix_(by_note[g["note_a"]], by_note[g["note_b"]])]
        mn, mean = float(sub.min()), float(sub.mean())
        band = "Q1" if mn < q25 else ("Q4" if mn >= q75 else "Q2-3")
        rows.append(
            {
                "bridge": bid,
                "min_card_distance": round(mn, 4),
                "min_quantile": round(float((arr < mn).mean()), 4),
                "mean_card_distance": round(mean, 4),
                "mean_quantile": round(float((arr < mean).mean()), 4),
                "closest_pair_band": band,
            }
        )
    planted_min = np.array([r["min_card_distance"] for r in rows])
    return {
        "n_cards": len(cards),
        "n_cross_note_card_pairs": int(len(arr)),
        "band_edges": {
            "q25": round(float(q25), 4),
            "q75": round(float(q75), 4),
            "q95": round(float(q95), 4),
        },
        "planted": rows,
        "planted_min_median": round(float(np.median(planted_min)), 4),
        "random_cross_domain_min_median": round(float(np.median(cross_min)), 4),
        "planted_closest_pair_in_Q1": int(sum(r["closest_pair_band"] == "Q1" for r in rows)),
        "n_planted": len(rows),
    }


def main(argv: list[str]) -> None:
    run = Path(argv[1])
    out = analyse(run)
    dest = run / "distance_posthoc.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "planted"}, indent=2))
    print(f"written: {dest}")


if __name__ == "__main__":
    main(sys.argv)
