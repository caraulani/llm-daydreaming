"""Planted-bridge recovery metrics over a run directory.

Inputs are the stage outputs (units, generations, critic, dupgate, match_gold) plus gold.json.
Outputs are plain dicts that stats.py renders into tables T1 to T6.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import numpy as np

from ..core.sampler import candidate_pairs, note_pair_key
from .metrics import hypergeom_sf, wilson
from .permutation_null import permutation_p_concentration, permutation_p_gap

PAIR_ARMS = ("S0", "B1", "B3", "B6")
SAMPLER_ARMS = ("B1", "B3", "B6", "B7")


def _index(rows: list[dict], key: str = "unit_id") -> dict[str, dict]:
    return {r[key]: r for r in rows}


def unit_status(gen: dict, critic: dict[str, dict], dup: dict[str, dict]) -> str:
    """none | malformed | error | killed | duplicate | survivor"""
    if gen["status"] != "ok":
        return gen["status"]
    c = critic.get(gen["unit_id"])
    if c is None or c["verdict"] != "keep":
        return "killed"
    d = dup.get(gen["unit_id"])
    if d and d["already_in_corpus"]:
        return "duplicate"
    return "survivor"


def sampler_enrichment(
    units: list[dict], cards: list[dict], vecs: np.ndarray, planted: dict[tuple[str, str], str]
) -> dict[str, Any]:
    """Planted card pairs in each sampled set vs the hypergeometric base rate over all
    cross-note card pairs."""
    pairs, _ = candidate_pairs(cards, vecs)
    notes = [c["source_note"] for c in cards]
    population = int(len(pairs))
    successes = int(sum(1 for i, j in pairs if note_pair_key(notes[i], notes[j]) in planted))
    out: dict[str, Any] = {
        "population_pairs": population,
        "planted_pairs": successes,
        "base_rate": successes / population if population else 0.0,
        "arms": {},
    }
    for arm in SAMPLER_ARMS:
        arm_units = [u for u in units if u["arm"] == arm and u["kind"] == "pair"]
        if not arm_units:
            continue
        draws = len(arm_units)
        hits = [u for u in arm_units if (u.get("label") or "").startswith("planted:")]
        distinct = {u["label"] for u in hits}
        expected = draws * out["base_rate"]
        out["arms"][arm] = {
            "draws": draws,
            "planted_hits": len(hits),
            "distinct_bridges": len(distinct),
            "expected": round(expected, 3),
            "p_hypergeom": hypergeom_sf(len(hits), population, successes, draws),
        }
    return out


def arm_summary(
    units: list[dict],
    generations: list[dict],
    critic: list[dict],
    dup: list[dict],
    match: list[dict],
) -> dict[str, dict[str, Any]]:
    cidx, didx, midx = _index(critic), _index(dup), _index(match)
    gidx = _index(generations)
    out: dict[str, dict[str, Any]] = {}
    for arm in sorted({u["arm"] for u in units}):
        us = [u for u in units if u["arm"] == arm]
        gens = [gidx[u["unit_id"]] for u in us if u["unit_id"] in gidx]
        statuses = [unit_status(g, cidx, didx) for g in gens]
        n = len(gens)
        n_none = statuses.count("none")
        n_ok = sum(1 for g in gens if g["status"] == "ok")
        n_killed = statuses.count("killed")
        n_dup = statuses.count("duplicate")
        n_surv = statuses.count("survivor")
        planted = [
            g
            for g in gens
            if (g.get("label") or "").startswith(("planted:", "partner:")) or (arm == "B4")
        ]
        planted_matched = {
            midx[g["unit_id"]]["bridge_id"]
            for g in planted
            if g["unit_id"] in midx and midx[g["unit_id"]]["match"]
        }
        planted_bridges = {
            (g.get("label") or "").split(":", 1)[1]
            for g in planted
            if (g.get("label") or "").startswith(("planted:", "partner:"))
        }
        if arm == "B4":
            planted_bridges = {
                midx[g["unit_id"]]["bridge_id"] for g in gens if g["unit_id"] in midx
            }
        cost = sum((g["usage"] or {}).get("cost_usd", 0.0) for g in gens)
        cost += sum(
            (cidx[g["unit_id"]]["usage"] or {}).get("cost_usd", 0.0)
            for g in gens
            if g["unit_id"] in cidx
        )
        tokens_in = sum((g["usage"] or {}).get("input_tokens", 0) for g in gens)
        tokens_out = sum((g["usage"] or {}).get("output_tokens", 0) for g in gens)
        out[arm] = {
            "units": n,
            "none": n_none,
            "none_rate": wilson(n_none, n),
            "ok": n_ok,
            "critic_killed": n_killed,
            "kill_rate": wilson(n_killed, n_ok),
            "duplicates": n_dup,
            "survivors": n_surv,
            "planted_units": len(planted) if arm != "B4" else n,
            "bridges_reachable": len(planted_bridges),
            "bridges_recovered": len(planted_matched),
            "recall": wilson(len(planted_matched), len(planted_bridges)),
            "cost_usd": round(cost, 4),
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost_per_recovered": round(cost / len(planted_matched), 4)
            if planted_matched
            else None,
        }
    return out


def oracle_specificity(
    generations: list[dict],
    critic: list[dict],
    dup: list[dict],
    match: list[dict],
    n_perm: int = 10_000,
    seed: int = 0,
) -> dict[str, Any]:
    cidx, didx, midx = _index(critic), _index(dup), _index(match)
    s0 = [g for g in generations if g["arm"] == "S0"]
    groups: dict[str, list[dict]] = defaultdict(list)
    for g in s0:
        label = (g.get("label") or "random").split(":")[0]
        groups[label].append(g)
    out: dict[str, Any] = {"groups": {}}
    for label, gens in groups.items():
        statuses = [unit_status(g, cidx, didx) for g in gens]
        n = len(gens)
        out["groups"][label] = {
            "units": n,
            "none_rate": wilson(statuses.count("none"), n),
            "nonnone_rate": wilson(sum(1 for g in gens if g["status"] == "ok"), n),
            "survivor_rate": wilson(statuses.count("survivor"), n),
        }
    planted = [g for g in groups.get("planted", [])]
    matched = [g for g in planted if g["unit_id"] in midx and midx[g["unit_id"]]["match"]]
    out["recall_planted"] = wilson(len(matched), len(planted))
    out["mean_cosine_to_gold"] = (
        float(
            np.mean(
                [
                    midx[g["unit_id"]].get("cosine_to_gold", 0.0)
                    for g in planted
                    if g["unit_id"] in midx
                ]
            )
        )
        if planted
        else 0.0
    )
    is_planted = np.array([(g.get("label") or "").startswith("planted:") for g in s0])
    hit = np.array([unit_status(g, cidx, didx) == "survivor" for g in s0])
    observed, expected, p = permutation_p_concentration(is_planted, hit, n_perm=n_perm, seed=seed)
    out["permutation"] = {
        "statistic": "survivors among planted S0 units",
        "observed": observed,
        "expected_under_null": round(expected, 3),
        "p": p,
        "n_perm": n_perm,
    }
    return out


def exploratory_finds(generations: list[dict], critic: list[dict], dup: list[dict]) -> list[dict]:
    cidx, didx = _index(critic), _index(dup)
    return [
        {
            "unit_id": g["unit_id"],
            "arm": g["arm"],
            "note_a": g["note_a"],
            "note_b": g.get("note_b"),
            "label": g.get("label"),
            "output": g["output"],
        }
        for g in generations
        if unit_status(g, cidx, didx) == "survivor"
        and not (g.get("label") or "").startswith("planted:")
        and g["kind"] == "pair"
    ]


def sampler_gap_permutation(
    units: list[dict], arm_a: str, arm_b: str, n_perm: int = 10_000, seed: int = 0
) -> dict[str, Any]:
    """Permutation test on arm labels: is the planted-pair rate in arm_a above arm_b?

    Shuffles the arm label across the pooled card-pair units of the two arms and recomputes
    the gap in planted rate. Used for H2(a) in the v0.2 rule (B7 vs B1)."""
    pool = [u for u in units if u["arm"] in (arm_a, arm_b) and u["kind"] == "pair"]
    if not pool:
        return {"observed_gap": 0.0, "p": 1.0, "n_perm": n_perm}
    labels = np.array([u["arm"] for u in pool])
    planted = np.array([(u.get("label") or "").startswith("planted:") for u in pool])
    gap, p = permutation_p_gap(labels, planted, arm_a, arm_b, n_perm=n_perm, seed=seed)
    return {"observed_gap": round(float(gap), 5), "p": float(p), "n_perm": n_perm}


def critic_comparison(
    generations: list[dict], critics: dict[str, list[dict]], match: list[dict]
) -> dict[str, dict[str, Any]]:
    """Per critic: how many correct planted recoveries survive it, how many decoy answers
    survive it, and its kill rate on random S0 pairs. Before the duplicate gate."""
    midx = _index(match)
    s0 = [g for g in generations if g["arm"] == "S0" and g["status"] == "ok"]
    planted_ok = [
        g
        for g in s0
        if (g.get("label") or "").startswith("planted:")
        and g["unit_id"] in midx
        and midx[g["unit_id"]]["match"]
    ]
    decoy_ok = [g for g in s0 if (g.get("label") or "").startswith("decoy:")]
    random_ok = [g for g in s0 if (g.get("label") or "random") == "random"]
    out: dict[str, dict[str, Any]] = {}
    for alias, rows in critics.items():
        cidx = _index(rows)

        def keep(g: dict, idx: dict[str, dict] = cidx) -> bool:
            return idx.get(g["unit_id"], {}).get("verdict") == "keep"

        pl_surv = sum(1 for g in planted_ok if keep(g))
        dc_surv = sum(1 for g in decoy_ok if keep(g))
        rd_kill = sum(1 for g in random_ok if not keep(g))
        out[alias] = {
            "correct_recoveries": len(planted_ok),
            "correct_recoveries_surviving": pl_surv,
            "correct_recoveries_killed": len(planted_ok) - pl_surv,
            "decoy_answers": len(decoy_ok),
            "decoy_answers_surviving": dc_surv,
            "random_answers": len(random_ok),
            "random_kill_rate": wilson(rd_kill, len(random_ok)),
            "model_id": next((r["usage"]["model_id"] for r in rows if r.get("usage")), None),
        }
    return out


def recall_by_family(
    generations: list[dict], match: list[dict], arm: str = "S0"
) -> dict[str, dict[str, Any]]:
    """Planted-bridge recall split by the writer family of the notes (v0.2 H5)."""
    midx = _index(match)
    by: dict[str, dict[str, set[str]]] = {}
    for g in generations:
        label = g.get("label") or ""
        if g["arm"] != arm or not label.startswith("planted:"):
            continue
        fam = str(g.get("writer_family") or "unknown")
        bid = label.split(":", 1)[1]
        d = by.setdefault(fam, {"bridges": set(), "recovered": set()})
        d["bridges"].add(bid)
        if g["unit_id"] in midx and midx[g["unit_id"]]["match"]:
            d["recovered"].add(bid)
    return {
        fam: {
            "bridges": len(d["bridges"]),
            "recovered": len(d["recovered"]),
            "recall": wilson(len(d["recovered"]), len(d["bridges"])),
        }
        for fam, d in sorted(by.items())
    }
