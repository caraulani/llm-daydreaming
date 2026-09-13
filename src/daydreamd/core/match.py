"""Grounded match against planted gold: binary LLM entailment with the gold in context, plus the
cosine between the generated connection and the gold connection, reported side by side."""

from __future__ import annotations

from ..backends import Backend
from ..core.embed import Embedder, FakeEmbedder
from ..core.io import write_jsonl
from ..core.llm import complete_json, pmap, usage_record
from ..core.run import RunDir, load_prompt
from ..core.sampler import note_pair_key


def bridge_for_unit(gen: dict, gold: dict, note_to_bridge: dict[str, str]) -> str | None:
    if gen["kind"] == "single":
        return note_to_bridge.get(gen["note_a"])
    label = gen.get("label") or ""
    if label.startswith(("planted:", "partner:")):
        return label.split(":", 1)[1]
    key = note_pair_key(gen["note_a"], gen["note_b"])
    for bid, g in gold.items():
        if note_pair_key(g["note_a"], g["note_b"]) == key:
            return bid
    return None


def match_one(backend: Backend, model: str, template: str, gen: dict, g: dict) -> dict:
    out = gen["output"]
    prompt = (
        template.replace("{{gold_connection}}", g["gold_connection"])
        .replace("{{gold_implication}}", g["gold_implication"])
        .replace("{{connection}}", out["connection"])
        .replace("{{mechanism}}", out["mechanism"])
        .replace("{{testable_implication}}", out["testable_implication"])
    )
    try:
        parsed, comp = complete_json(backend, prompt, model)
    except Exception as exc:  # noqa: BLE001
        return {
            "unit_id": gen["unit_id"],
            "bridge_id": None,
            "match": False,
            "reason": f"error: {exc}"[:200],
            "usage": None,
        }
    return {
        "unit_id": gen["unit_id"],
        "match": bool((parsed or {}).get("match", False)),
        "reason": str((parsed or {}).get("reason", ""))[:200],
        "usage": usage_record(comp),
    }


def match_gold(
    run: RunDir,
    backend: Backend,
    embedder: Embedder | FakeEmbedder,
    generations: list[dict],
    gold: dict,
    model: str = "haiku",
    concurrency: int = 4,
) -> list[dict]:
    template, sha = load_prompt("match_gold")
    run.record_prompt("match_gold", sha)
    note_to_bridge = {g["note_a"]: bid for bid, g in gold.items()} | {
        g["note_b"]: bid for bid, g in gold.items()
    }
    todo = []
    for gen in generations:
        if gen["status"] != "ok":
            continue
        bid = bridge_for_unit(gen, gold, note_to_bridge)
        if bid:
            todo.append((gen, bid))
    rows = pmap(
        lambda t: {**match_one(backend, model, template, t[0], gold[t[1]]), "bridge_id": t[1]},
        todo,
        concurrency,
    )
    if todo:
        gvecs = embedder.encode([gold[bid]["gold_connection"] for _, bid in todo])
        cvecs = embedder.encode([gen["output"]["connection"] for gen, _ in todo])
        for row, gv, cv in zip(rows, gvecs, cvecs, strict=True):
            row["cosine_to_gold"] = round(float(gv @ cv), 4)
    write_jsonl(run.path / "match_gold.jsonl", rows)
    cost = sum((r["usage"] or {}).get("cost_usd", 0.0) for r in rows)
    ids: set[str] = {r["usage"]["model_id"] for r in rows if r["usage"]}
    if ids:
        run.record_model("match_gold", model, sorted(ids)[0])
    run.add_cost(cost)
    run.mark_stage(
        "match_gold",
        n_judged=len(rows),
        n_match=sum(r["match"] for r in rows),
        cost_usd=round(cost, 4),
    )
    return rows
