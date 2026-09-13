"""Generator stage: identical prompt for every pair arm, NONE permitted, structured JSON."""

from __future__ import annotations

from typing import Any

from ..backends import Backend
from .io import write_jsonl
from .llm import complete_json, guard_error_rate, pmap, usage_record
from .run import RunDir, load_prompt
from .sampler import Unit

FIELDS = ("connection", "mechanism", "testable_implication", "needs")


def render_claims(claims: list[str]) -> str:
    if len(claims) == 1:
        return claims[0]
    return "\n".join(f"- {c}" for c in claims)


def render_prompt(unit: Unit, pair_prompt: str, single_prompt: str) -> str:
    if unit.kind == "single":
        return single_prompt.replace("{{claim}}", render_claims(unit.claims_a))
    return pair_prompt.replace("{{claim_a}}", render_claims(unit.claims_a)).replace(
        "{{claim_b}}", render_claims(unit.claims_b)
    )


def normalise_output(parsed: Any) -> dict[str, str] | None:
    if not isinstance(parsed, dict):
        return None
    out = {k: str(parsed.get(k, "")).strip() for k in FIELDS}
    if not out["connection"]:
        return None
    return out


def generate_one(
    backend: Backend, model: str, unit: Unit, pair_prompt: str, single_prompt: str
) -> dict:
    prompt = render_prompt(unit, pair_prompt, single_prompt)
    try:
        parsed, comp = complete_json(backend, prompt, model)
        output = None if parsed is None else normalise_output(parsed)
        status = "none" if parsed is None else ("ok" if output else "malformed")
    except Exception as exc:  # noqa: BLE001
        return {
            **unit.to_row(),
            "status": "error",
            "error": str(exc)[:300],
            "output": None,
            "usage": None,
        }
    return {**unit.to_row(), "status": status, "output": output, "usage": usage_record(comp)}


def generate(
    run: RunDir, backend: Backend, units: list[Unit], model: str = "sonnet", concurrency: int = 4
) -> list[dict]:
    pair_prompt, pair_sha = load_prompt("generate_pair")
    single_prompt, single_sha = load_prompt("generate_single")
    run.record_prompt("generate_pair", pair_sha)
    run.record_prompt("generate_single", single_sha)
    rows = pmap(
        lambda u: generate_one(backend, model, u, pair_prompt, single_prompt), units, concurrency
    )
    write_jsonl(run.path / "generations.jsonl", rows)
    guard_error_rate(rows, "generate")
    cost = sum((r["usage"] or {}).get("cost_usd", 0.0) for r in rows)
    ids: set[str] = {r["usage"]["model_id"] for r in rows if r["usage"]}
    if ids:
        run.record_model("generator", model, sorted(ids)[0])
    run.add_cost(cost)
    counts = {
        s: sum(1 for r in rows if r["status"] == s) for s in ("ok", "none", "malformed", "error")
    }
    run.mark_stage("generate", n_units=len(units), cost_usd=round(cost, 4), **counts)
    return rows
