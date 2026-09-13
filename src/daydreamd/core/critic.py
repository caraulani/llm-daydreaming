"""Binary critic: kill if restates a claim, implication not checkable, or generic."""

from __future__ import annotations

from ..backends import Backend
from .io import write_jsonl
from .llm import complete_json, pmap, usage_record
from .run import RunDir, load_prompt

REASONS = {"restates_claim", "not_checkable", "generic", "ok"}


def critic_prompt(template: str, gen: dict) -> str:
    claims = [f"A: {c}" for c in gen["claims_a"]] + [f"B: {c}" for c in gen.get("claims_b") or []]
    out = gen["output"]
    return (
        template.replace("{{claims}}", "\n".join(claims))
        .replace("{{connection}}", out["connection"])
        .replace("{{mechanism}}", out["mechanism"])
        .replace("{{testable_implication}}", out["testable_implication"])
    )


def judge_one(backend: Backend, model: str, template: str, gen: dict) -> dict:
    try:
        parsed, comp = complete_json(backend, critic_prompt(template, gen), model)
    except Exception as exc:  # noqa: BLE001
        return {
            "unit_id": gen["unit_id"],
            "verdict": "error",
            "reason": str(exc)[:200],
            "usage": None,
        }
    verdict = str((parsed or {}).get("verdict", "kill")).lower()
    reason = str((parsed or {}).get("reason", "generic")).lower()
    if verdict not in {"keep", "kill"}:
        verdict = "kill"
    if reason not in REASONS:
        reason = "generic"
    return {
        "unit_id": gen["unit_id"],
        "verdict": verdict,
        "reason": reason,
        "usage": usage_record(comp),
    }


def run_critic(
    run: RunDir,
    backend: Backend,
    generations: list[dict],
    model: str = "haiku",
    concurrency: int = 4,
) -> list[dict]:
    template, sha = load_prompt("critic")
    run.record_prompt("critic", sha)
    todo = [g for g in generations if g["status"] == "ok"]
    rows = pmap(lambda g: judge_one(backend, model, template, g), todo, concurrency)
    write_jsonl(run.path / "critic.jsonl", rows)
    cost = sum((r["usage"] or {}).get("cost_usd", 0.0) for r in rows)
    ids: set[str] = {r["usage"]["model_id"] for r in rows if r["usage"]}
    if ids:
        run.record_model("critic", model, sorted(ids)[0])
    run.add_cost(cost)
    run.mark_stage(
        "critic",
        n_judged=len(rows),
        n_keep=sum(1 for r in rows if r["verdict"] == "keep"),
        cost_usd=round(cost, 4),
    )
    return rows
