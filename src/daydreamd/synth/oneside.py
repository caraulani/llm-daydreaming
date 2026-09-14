"""The one-side gate (ADR-014): a planted bridge is accepted only if neither of its two notes,
read alone by the generator under a strict NONE-permitted prompt, yields the gold mechanism.

The v0.2 run showed single-note reflection recovering more planted mechanisms than two-note
recombination, because the bridges were general principles that one note's ingredient set
already cued (research/07). This gate runs the generator itself on each side, then asks the
match judge (two votes) whether the output is the gold. A bridge with a recovered side is
listed in the manifest for the experimenter to rewrite or drop before the answer key is sealed;
the builder never edits the answer key.
"""

from __future__ import annotations

from typing import Any

from ..backends import Backend
from ..core.llm import complete_json, usage_record
from ..core.match import match_one
from ..core.run import load_prompt


def gate_one_side(
    backend: Backend,
    gen_model: str,
    judge_model: str,
    note_text: str,
    gold: dict[str, str],
    *,
    votes: int = 2,
    single_template: str | None = None,
    match_template: str | None = None,
) -> dict[str, Any]:
    """Return {status: clean|recovered|error, output, votes, usage}.

    ``clean``: the generator said NONE, or produced something the judge did not accept as the
    gold on a majority of ``votes``. ``recovered``: a majority of judge votes said MATCH.
    """
    single = single_template or load_prompt("generate_single_strict")[0]
    match = match_template or load_prompt("match_gold")[0]
    prompt = single.replace("{{claim}}", note_text)
    try:
        parsed, comp = complete_json(backend, prompt, gen_model)
    except ValueError as exc:  # no JSON and not NONE: count as an error, not as clean
        return {
            "status": "error",
            "output": None,
            "votes": [],
            "usage": None,
            "error": str(exc)[:200],
        }
    usage = [usage_record(comp)]
    if parsed is None:
        return {"status": "clean", "output": None, "votes": [], "usage": usage}
    if not isinstance(parsed, dict) or "connection" not in parsed:
        return {
            "status": "error",
            "output": parsed,
            "votes": [],
            "usage": usage,
            "error": "malformed",
        }
    gen = {
        "unit_id": "gate",
        "output": {
            "connection": str(parsed.get("connection", "")),
            "mechanism": str(parsed.get("mechanism", "")),
            "testable_implication": str(parsed.get("testable_implication", "")),
        },
    }
    verdicts = [match_one(backend, judge_model, match, gen, gold) for _ in range(votes)]
    usage += [v["usage"] for v in verdicts if v.get("usage")]
    yes = sum(1 for v in verdicts if v["match"])
    # majority says MATCH => recovered; a tie fails closed so the bridge gets reviewed
    status = "recovered" if yes * 2 >= votes else "clean"
    return {
        "status": status,
        "output": gen["output"],
        "votes": [{"match": v["match"], "reason": v["reason"]} for v in verdicts],
        "usage": usage,
    }


def gate_bridges(
    backend: Backend,
    gen_model: str,
    judge_model: str,
    notes: dict[str, str],
    gold: dict[str, dict[str, Any]],
    *,
    votes: int = 2,
) -> dict[str, Any]:
    """Run the gate on both sides of every bridge. Returns per-bridge results and the failure list."""
    single, single_sha = load_prompt("generate_single_strict")
    match, match_sha = load_prompt("match_gold")
    out: dict[str, Any] = {}
    failures: list[str] = []
    cost = 0.0
    for bid, g in sorted(gold.items()):
        sides: dict[str, Any] = {}
        for side, nid in (("a", g["note_a"]), ("b", g["note_b"])):
            text = notes.get(nid, "")
            r = gate_one_side(
                backend,
                gen_model,
                judge_model,
                text,
                g,
                votes=votes,
                single_template=single,
                match_template=match,
            )
            for u in r.get("usage") or []:
                cost += float((u or {}).get("cost_usd", 0.0))
            sides[side] = {k: v for k, v in r.items() if k != "usage"}
        failed = any(s["status"] != "clean" for s in sides.values())
        out[bid] = {"sides": sides, "passed": not failed}
        if failed:
            failures.append(bid)
    return {
        "bridges": out,
        "failures": failures,
        "votes": votes,
        "prompt_sha256": {"generate_single_strict": single_sha, "match_gold": match_sha},
        "cost_usd": round(cost, 4),
    }
