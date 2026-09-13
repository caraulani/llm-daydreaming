"""Render tables T1 to T6 (synthetic track) and the owner-blind tables (Track C) from a run.
No model calls: `make reproduce` runs this over committed outputs."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import numpy as np

from ..eval.metrics import cochran_armitage, cohen_kappa, fisher_one_sided, wilson
from ..eval.permutation_null import permutation_p_gap
from ..eval.recovery import (
    arm_summary,
    critic_comparison,
    exploratory_finds,
    oracle_specificity,
    recall_by_family,
    sampler_enrichment,
    sampler_gap_permutation,
)
from .io import read_json, read_jsonl, write_jsonl
from .run import RunDir


def _fmt_rate(t: tuple[float, float, float]) -> str:
    return f"{100 * t[0]:.1f}% [{100 * t[1]:.0f}, {100 * t[2]:.0f}]"


def _write_table(
    out_dir: Path, name: str, header: list[str], rows: list[list[Any]], caption: str
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / f"{name}.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    md = [
        f"**{name}. {caption}**",
        "",
        "| " + " | ".join(header) + " |",
        "|" + "---|" * len(header),
    ]
    md += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    (out_dir / f"{name}.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def load_run(run: RunDir) -> dict[str, Any]:
    p = run.path
    data = {
        "meta": run.read_meta(),
        "cards": list(read_jsonl(p / "cards.jsonl")),
        "units": list(read_jsonl(p / "units.jsonl")),
        "generations": list(read_jsonl(p / "generations.jsonl")),
        "critic": list(read_jsonl(p / "critic.jsonl")),
        "dup": list(read_jsonl(p / "dupgate.jsonl")),
        "match": list(read_jsonl(p / "match_gold.jsonl")),
        "verdicts": list(read_jsonl(p / "verdicts.jsonl")),
        "critics": {
            f.stem.removeprefix("critic_"): list(read_jsonl(f))
            for f in sorted(p.glob("critic_*.jsonl"))
        },
    }
    data["vecs"] = np.load(p / "embeddings.npy") if (p / "embeddings.npy").exists() else None  # type: ignore[assignment]
    gold_path = p / "gold.json"
    data["gold"] = read_json(gold_path) if gold_path.exists() else {}
    manifest = (
        read_json(p / "snapshot" / "manifest.json")
        if (p / "snapshot" / "manifest.json").exists()
        else {}
    )
    data["manifest"] = manifest
    return data


def synthetic_tables(
    run: RunDir, out_dir: Path, n_perm: int = 10_000, seed: int = 0, prereg: str = "v0.1"
) -> dict[str, Any]:
    d = load_run(run)
    gold = d["gold"]
    planted = {tuple(sorted((g["note_a"], g["note_b"]))): bid for bid, g in gold.items()}
    m = d["manifest"]
    synth = m.get("synthetic", {})
    _write_table(
        out_dir,
        "T1",
        [
            "notes",
            "cards",
            "cards_per_note",
            "bridges",
            "decoys",
            "leakage_failures",
            "corpus_sha256",
        ],
        [
            [
                m.get("n_docs"),
                len(d["cards"]),
                round(len(d["cards"]) / max(1, m.get("n_docs", 1)), 2),
                len(gold),
                synth.get("n_decoys", "n/a"),
                len(synth.get("leakage_failures", [])) if synth else "n/a",
                m.get("corpus_sha256", "")[:12],
            ]
        ],
        "Corpus",
    )
    enrich = (
        sampler_enrichment(d["units"], d["cards"], d["vecs"], planted)
        if d["vecs"] is not None
        else {"arms": {}}
    )
    _write_table(
        out_dir,
        "T2",
        ["arm", "draws", "planted_hits", "distinct_bridges", "expected_hits", "p_hypergeom"],
        [
            [
                a,
                v["draws"],
                v["planted_hits"],
                v["distinct_bridges"],
                v["expected"],
                f"{v['p_hypergeom']:.3g}",
            ]
            for a, v in enrich["arms"].items()
        ],
        f"Sampler enrichment; base rate {100 * enrich.get('base_rate', 0):.2f}% of {enrich.get('population_pairs', 0)} cross-note card pairs are planted",
    )
    spec = oracle_specificity(
        d["generations"], d["critic"], d["dup"], d["match"], n_perm=n_perm, seed=seed
    )
    rows = [
        [
            lab,
            v["units"],
            _fmt_rate(v["none_rate"]),
            _fmt_rate(v["nonnone_rate"]),
            _fmt_rate(v["survivor_rate"]),
        ]
        for lab, v in spec["groups"].items()
    ]
    rows.append(
        [
            "recall on planted (gold match)",
            spec["groups"].get("planted", {}).get("units", 0),
            "",
            "",
            _fmt_rate(spec["recall_planted"]),
        ]
    )
    _write_table(
        out_dir,
        "T3",
        [
            "S0 group",
            "units",
            "NONE rate",
            "non-NONE rate",
            "survivor rate (post critic + dupgate)",
        ],
        rows,
        f"Oracle set: generator and critic without the sampler; mean cosine to gold on planted = {spec['mean_cosine_to_gold']:.3f}",
    )
    arms = arm_summary(d["units"], d["generations"], d["critic"], d["dup"], d["match"])
    _write_table(
        out_dir,
        "T4",
        [
            "arm",
            "units",
            "NONE",
            "critic kill",
            "dup",
            "survivors",
            "bridges reachable",
            "bridges recovered",
            "recall",
            "cost usd",
            "usd per recovered",
        ],
        [
            [
                a,
                v["units"],
                _fmt_rate(v["none_rate"]),
                _fmt_rate(v["kill_rate"]),
                v["duplicates"],
                v["survivors"],
                v["bridges_reachable"],
                v["bridges_recovered"],
                _fmt_rate(v["recall"]),
                v["cost_usd"],
                v["cost_per_recovered"] if v["cost_per_recovered"] is not None else "n/a",
            ]
            for a, v in arms.items()
        ],
        "Per arm: NONE rate, critic kill rate, survivors, recovered planted bridges, measured cost",
    )
    pm = spec["permutation"]
    _write_table(
        out_dir,
        "T5",
        ["statistic", "observed", "expected under null", "p", "shuffles"],
        [
            [
                pm["statistic"],
                pm["observed"],
                pm["expected_under_null"],
                f"{pm['p']:.4f}",
                pm["n_perm"],
            ]
        ],
        "Label-permutation null over the S0 oracle set",
    )
    b4, s0 = arms.get("B4"), arms.get("S0")
    if b4 and s0:
        p = fisher_one_sided(
            s0["bridges_recovered"],
            max(1, s0["bridges_reachable"]),
            b4["bridges_recovered"],
            max(1, b4["bridges_reachable"]),
        )
        _write_table(
            out_dir,
            "T6",
            ["arm", "bridges reachable", "recovered", "recall", "fisher p (S0 > B4)"],
            [
                [
                    "S0 two notes",
                    s0["bridges_reachable"],
                    s0["bridges_recovered"],
                    _fmt_rate(s0["recall"]),
                    f"{p:.3g}",
                ],
                [
                    "B4 one note",
                    b4["bridges_reachable"],
                    b4["bridges_recovered"],
                    _fmt_rate(b4["recall"]),
                    "",
                ],
            ],
            "Recombination vs single-note reflection on the same bridge notes",
        )
    s1 = arms.get("S1")
    if s1 and s0:
        p_s1 = fisher_one_sided(
            s0["bridges_recovered"],
            max(1, s0["bridges_reachable"]),
            s1["bridges_recovered"],
            max(1, s1["bridges_reachable"]),
        )
        rows7 = [
            [
                "S0 bridge note + true partner",
                s0["bridges_reachable"],
                s0["bridges_recovered"],
                _fmt_rate(s0["recall"]),
                f"{p_s1:.3g}",
            ],
            [
                "S1 bridge note + partner-domain filler",
                s1["bridges_reachable"],
                s1["bridges_recovered"],
                _fmt_rate(s1["recall"]),
                "",
            ],
        ]
        if b4:
            rows7.append(
                [
                    "B4 bridge note alone",
                    b4["bridges_reachable"],
                    b4["bridges_recovered"],
                    _fmt_rate(b4["recall"]),
                    "",
                ]
            )
        _write_table(
            out_dir,
            "T7",
            ["arm", "bridges reachable", "recovered", "recall", "fisher p (S0 > S1)"],
            rows7,
            "Exploratory control (not preregistered): does the gold mechanism appear when the partner note is replaced by a mechanism-free filler from the same domain?",
        )
    critics = critic_comparison(d["generations"], d["critics"], d["match"]) if d["critics"] else {}
    if critics:
        _write_table(
            out_dir,
            "T8",
            [
                "critic",
                "model id",
                "correct recoveries",
                "surviving",
                "killed",
                "decoy answers",
                "decoy surviving",
                "kill rate on random",
            ],
            [
                [
                    alias,
                    v["model_id"],
                    v["correct_recoveries"],
                    v["correct_recoveries_surviving"],
                    v["correct_recoveries_killed"],
                    v["decoy_answers"],
                    v["decoy_answers_surviving"],
                    _fmt_rate(v["random_kill_rate"]),
                ]
                for alias, v in critics.items()
            ],
            "Recall after critic, per critic (same generations, before the duplicate gate)",
        )
    finds = exploratory_finds(d["generations"], d["critic"], d["dup"])
    write_jsonl(out_dir / "exploratory_finds.jsonl", finds)
    if prereg == "v0.2":
        decision = _decision_v02(spec, enrich, arms, d, n_perm=n_perm, seed=seed)
    else:
        decision = _decision(spec, enrich, arms)
    (out_dir / "DECISION.md").write_text(decision["md"], encoding="utf-8")
    summary = {
        "prereg": prereg,
        "critics": critics,
        "decision": {k: v for k, v in decision.items() if k != "md"},
        "enrichment": enrich,
        "oracle": spec,
        "arms": arms,
        "n_exploratory": len(finds),
        "cost_usd_total": d["meta"].get("cost_usd_total"),
        "models": d["meta"].get("models"),
    }
    (out_dir / "summary.md").write_text(_summary_md(summary), encoding="utf-8")
    return summary


def _summary_md(s: dict[str, Any]) -> str:
    lines = ["# Run summary", "", f"Total measured cost: ${s['cost_usd_total']}", "", "Models:"]
    for role, m in (s.get("models") or {}).items():
        lines.append(f"- {role}: `{m['model_id']}` (alias `{m['alias']}`)")
    lines += [
        "",
        f"Exploratory finds (non-planted survivors, manual review only): {s['n_exploratory']}",
        "",
    ]
    lines.append(
        f"Oracle recall on planted: {_fmt_rate(s['oracle']['recall_planted'])}; permutation p = {s['oracle']['permutation']['p']:.4f}"
    )
    return "\n".join(lines) + "\n"


def human_tables(
    run: RunDir, out_dir: Path, n_perm: int = 10_000, seed: int = 0
) -> dict[str, Any] | None:
    """Track C tables from owner-blind verdicts. Returns None if the pack was not scored."""
    d = load_run(run)
    v = [x for x in d["verdicts"] if x["repeat_of"] is None]
    if not v:
        return None
    labels = np.array([x["arm"] for x in v])
    keep = np.array([x["keep"] for x in v])
    arms = sorted(set(labels))
    rows = []
    for arm in arms:
        idx = labels == arm
        rows.append(
            [
                arm,
                int(idx.sum()),
                _fmt_rate(wilson(int(keep[idx].sum()), int(idx.sum()))),
                _fmt_rate(wilson(sum(x["known"] for x in v if x["arm"] == arm), int(idx.sum()))),
            ]
        )
    _write_table(
        out_dir,
        "H1",
        ["arm", "scored", "KEEP rate", "KNOWN rate"],
        rows,
        "Owner-blind keep and known rates by arm",
    )
    tests = []
    for a, b in (("B3", "B1"), ("B6", "B1"), ("B3", "B4")):
        if a in arms and b in arms:
            ka, na = int(keep[labels == a].sum()), int((labels == a).sum())
            kb, nb = int(keep[labels == b].sum()), int((labels == b).sum())
            gap, pp = permutation_p_gap(labels, keep, a, b, n_perm=n_perm, seed=seed)
            tests.append(
                [
                    f"{a} vs {b}",
                    f"{100 * gap:+.1f} pts",
                    f"{fisher_one_sided(ka, na, kb, nb):.4f}",
                    f"{pp:.4f}",
                ]
            )
    _write_table(
        out_dir,
        "H2",
        ["comparison", "keep-rate gap", "fisher p", "permutation p"],
        tests,
        "Arm comparisons",
    )
    b3 = [x for x in v if x["arm"] == "B3"]
    if b3:
        bands = ["Q1", "Q2-3", "Q4", "top5"]
        counts = [
            (sum(x["keep"] for x in b3 if x["band"] == b), sum(1 for x in b3 if x["band"] == b))
            for b in bands
        ]
        z, p = cochran_armitage(counts)
        _write_table(
            out_dir,
            "H3",
            ["band", "n", "KEEP rate"],
            [[b, n, _fmt_rate(wilson(k, n))] for b, (k, n) in zip(bands, counts, strict=True)],
            f"Keep rate by distance band; Cochran-Armitage z = {z:.2f}, p = {p:.3g}",
        )
    reps = [x for x in d["verdicts"] if x["repeat_of"] is not None]
    if reps:
        first = {x["item"]: x for x in d["verdicts"]}
        kappa = cohen_kappa(
            [first[r["repeat_of"]]["keep"] for r in reps], [r["keep"] for r in reps]
        )
        (out_dir / "H4.md").write_text(
            f"**H4. Intra-rater consistency on {len(reps)} repeats: Cohen's kappa = {kappa:.2f}**\n",
            encoding="utf-8",
        )
    return {"arms": arms, "n": len(v)}


def _decision(spec: dict[str, Any], enrich: dict[str, Any], arms: dict[str, Any]) -> dict[str, Any]:
    """Apply the preregistered decision rule (PREREGISTRATION.md section 5) to the run."""
    groups = spec.get("groups", {})
    s0, b4 = arms.get("S0"), arms.get("B4")
    n_pl = groups.get("planted", {}).get("units", 0)
    n_dc = groups.get("decoy", {}).get("units", 0)
    rec = s0["bridges_recovered"] if s0 else 0
    # decoy false positives after critic and dupgate (survivor rate x units, rounded)
    dc_rate = groups.get("decoy", {}).get("survivor_rate", (0.0, 0.0, 0.0))[0]
    fp = int(round(dc_rate * n_dc))
    h1_p = fisher_one_sided(rec, max(1, n_pl), fp, max(1, n_dc))
    h1 = h1_p < 0.05
    h2_ps = {a: v["p_hypergeom"] for a, v in enrich.get("arms", {}).items() if a in ("B3", "B6")}
    h2 = any(p < 0.05 for p in h2_ps.values())
    h3_p = None
    h3 = False
    if s0 and b4:
        h3_p = fisher_one_sided(
            s0["bridges_recovered"],
            max(1, s0["bridges_reachable"]),
            b4["bridges_recovered"],
            max(1, b4["bridges_reachable"]),
        )
        h3 = h3_p < 0.05
    signal = h1 and h2
    md = "\n".join(
        [
            "# Preregistered decision rule (PREREGISTRATION.md section 5)",
            "",
            f"- H1 (planted recall {rec}/{n_pl} vs decoy false positives {fp}/{n_dc}, Fisher one-sided): p = {h1_p:.4f} -> {'PASS' if h1 else 'FAIL'}",
            "- H2 (sampler enrichment, hypergeometric): "
            + ", ".join(f"{a} p = {p:.3f}" for a, p in sorted(h2_ps.items()))
            + f" -> {'PASS' if h2 else 'FAIL'}",
            (
                f"- H3 (S0 two-note recall vs B4 one-note recall, Fisher one-sided): p = {h3_p:.4f} -> {'PASS' if h3 else 'FAIL'}"
                if h3_p is not None
                else "- H3: not computable (missing S0 or B4)"
            ),
            "",
            f"**Decision: {'SIGNAL' if signal else 'NULL'}** (signal requires H1 and H2 both passing).",
            "",
        ]
    )
    return {
        "h1": {
            "p": h1_p,
            "pass": h1,
            "recovered": rec,
            "planted": n_pl,
            "decoy_fp": fp,
            "decoys": n_dc,
        },
        "h2": {"p": h2_ps, "pass": h2},
        "h3": {"p": h3_p, "pass": h3},
        "signal": signal,
        "md": md,
    }


def _h1(spec: dict[str, Any], arms: dict[str, Any]) -> dict[str, Any]:
    groups = spec.get("groups", {})
    s0 = arms.get("S0")
    n_pl = groups.get("planted", {}).get("units", 0)
    n_dc = groups.get("decoy", {}).get("units", 0)
    rec = s0["bridges_recovered"] if s0 else 0
    dc_rate = groups.get("decoy", {}).get("survivor_rate", (0.0, 0.0, 0.0))[0]
    fp = int(round(dc_rate * n_dc))
    p = fisher_one_sided(rec, max(1, n_pl), fp, max(1, n_dc))
    return {
        "p": p,
        "pass": p < 0.05,
        "recovered": rec,
        "planted": n_pl,
        "decoy_fp": fp,
        "decoys": n_dc,
    }


def _decision_v02(
    spec: dict[str, Any],
    enrich: dict[str, Any],
    arms: dict[str, Any],
    d: dict[str, Any],
    n_perm: int = 10_000,
    seed: int = 0,
) -> dict[str, Any]:
    """Apply the v0.2 decision rule (PREREGISTRATION-v0.2.md section 5): signal iff H1 and H4."""
    s0, s1, b4 = arms.get("S0"), arms.get("S1"), arms.get("B4")
    b1, b7 = arms.get("B1"), arms.get("B7")
    h1 = _h1(spec, arms)
    # H2(a): B7 planted enrichment, hypergeometric plus arm-label permutation vs B1
    e7 = enrich.get("arms", {}).get("B7")
    perm = sampler_gap_permutation(d["units"], "B7", "B1", n_perm=n_perm, seed=seed)
    h2a_p = e7["p_hypergeom"] if e7 else None
    h2a = h2a_p is not None and h2a_p < 0.05
    # H2(b): non-NONE rate B7 > B1
    h2b_p = None
    h2b = False
    if b1 and b7:
        h2b_p = fisher_one_sided(b7["ok"], max(1, b7["units"]), b1["ok"], max(1, b1["units"]))
        h2b = h2b_p < 0.05
    h3_p = None
    h3 = False
    if s0 and b4:
        h3_p = fisher_one_sided(
            s0["bridges_recovered"],
            max(1, s0["bridges_reachable"]),
            b4["bridges_recovered"],
            max(1, b4["bridges_reachable"]),
        )
        h3 = h3_p < 0.05
    h4_p = None
    h4 = False
    h4_txt = "- H4: not computable (missing S0 or S1)"
    if s0 and s1:
        h4_p = fisher_one_sided(
            s0["bridges_recovered"],
            max(1, s0["bridges_reachable"]),
            s1["bridges_recovered"],
            max(1, s1["bridges_reachable"]),
        )
        h4 = h4_p < 0.05
        h4_txt = (
            f"- H4 (S0 recall {s0['bridges_recovered']}/{s0['bridges_reachable']} vs S1 "
            f"partner-domain-filler recall {s1['bridges_recovered']}/{s1['bridges_reachable']}, "
            f"Fisher one-sided): p = {h4_p:.4f} -> {'PASS' if h4 else 'FAIL'}"
        )
    h2b_txt = "- H2b: not computable (missing B1 or B7)"
    if b1 and b7 and h2b_p is not None:
        h2b_txt = (
            f"- H2b (non-NONE rate B7 {b7['ok']}/{b7['units']} vs B1 {b1['ok']}/{b1['units']}, "
            f"Fisher one-sided): p = {h2b_p:.4f} -> {'PASS' if h2b else 'FAIL'}"
        )
    fam = recall_by_family(d["generations"], d["match"])
    signal = h1["pass"] and h4
    fam_lines = [
        f"  - {f}: {v['recovered']}/{v['bridges']} = {_fmt_rate(v['recall'])}"
        for f, v in fam.items()
    ]
    md = "\n".join(
        [
            "# Preregistered decision rule, v0.2 (PREREGISTRATION-v0.2.md section 5)",
            "",
            f"- H1 (planted recall {h1['recovered']}/{h1['planted']} vs decoy false positives {h1['decoy_fp']}/{h1['decoys']}, Fisher one-sided): p = {h1['p']:.4f} -> {'PASS' if h1['pass'] else 'FAIL'}",
            (
                f"- H2a (B7 planted card pairs {e7['planted_hits']} in {e7['draws']} draws, expected {e7['expected']}, hypergeometric): p = {h2a_p:.4f}; arm-label permutation vs B1: gap = {perm['observed_gap']:+.4f}, p = {perm['p']:.4f} -> {'PASS' if h2a else 'FAIL'}"
                if e7
                else "- H2a: not computable (no B7 arm)"
            ),
            h2b_txt,
            (
                f"- H3 (S0 two-note recall vs B4 one-note recall, Fisher one-sided): p = {h3_p:.4f} -> {'PASS' if h3 else 'FAIL'}"
                if h3_p is not None
                else "- H3: not computable (missing S0 or B4)"
            ),
            h4_txt,
            "- H5 (recall by writer family, estimation only, no pass/fail):",
            *(fam_lines or ["  - no writer families recorded"]),
            "",
            f"**Decision: {'SIGNAL' if signal else 'NULL'}** (signal requires H1 and H4 both passing; H2, H3, H5 are reported and do not enter the rule).",
            "",
        ]
    )
    return {
        "h1": h1,
        "h2a": {"p": h2a_p, "permutation": perm, "pass": h2a},
        "h2b": {"p": h2b_p, "pass": h2b},
        "h3": {"p": h3_p, "pass": h3},
        "h4": {"p": h4_p, "pass": h4},
        "h5": fam,
        "signal": signal,
        "md": md,
    }
