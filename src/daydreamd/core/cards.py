"""Concept cards: one cheap-model pass per note, cached by note sha, schema-validated."""

from __future__ import annotations

from typing import Any

from ..backends import Backend
from .ingest import Doc
from .io import append_jsonl, read_jsonl, write_jsonl
from .llm import complete_json, pmap, usage_record
from .run import RunDir, load_prompt

MAX_NOTE_CHARS = 9000
VALID_CONFIDENCE = {"high", "med", "low"}


def validate_card(raw: dict[str, Any]) -> dict[str, Any] | None:
    claim = str(raw.get("claim", "")).strip()
    if not claim or len(claim.split()) > 34:
        return None
    why = str(raw.get("why_it_matters", "")).strip()
    if len(why.split()) > 24:
        why = " ".join(why.split()[:24])
    conf = str(raw.get("confidence", "med")).lower()
    if conf not in VALID_CONFIDENCE:
        conf = "med"
    entities = raw.get("entities") or []
    if not isinstance(entities, list):
        entities = [str(entities)]
    return {
        "claim": claim,
        "entities": [str(e) for e in entities][:8],
        "why_it_matters": why,
        "confidence": conf,
    }


def cards_for_doc(backend: Backend, model: str, prompt: str, doc: Doc) -> dict[str, Any]:
    filled = prompt.replace("{{note_id}}", doc.id).replace(
        "{{note_text}}", doc.text[:MAX_NOTE_CHARS]
    )
    parsed, comp = complete_json(backend, filled, model)
    items = parsed if isinstance(parsed, list) else []
    cards = [c for c in (validate_card(x) for x in items if isinstance(x, dict)) if c]
    out = []
    for i, c in enumerate(cards[:6]):
        out.append({"id": f"{doc.id}-c{i + 1}", "source_note": doc.id, **c})
    return {"doc": doc.id, "doc_sha": doc.sha, "cards": out, "usage": usage_record(comp)}


def extract_cards(
    run: RunDir, backend: Backend, docs: list[Doc], model: str = "haiku", concurrency: int = 4
) -> list[dict[str, Any]]:
    prompt, sha = load_prompt("cards")
    run.record_prompt("cards", sha)
    cache_path = run.path / "cards_cache.jsonl"
    cached = {row["doc_sha"]: row for row in read_jsonl(cache_path)}
    todo = [d for d in docs if d.sha not in cached]
    results = pmap(lambda d: cards_for_doc(backend, model, prompt, d), todo, concurrency)
    # A note that yields zero cards (a parse failure or a refusal) is retried once; a note that
    # still has none is recorded that way and excluded from note-level arms by the sampler.
    retry = [d for d, row in zip(todo, results, strict=True) if not row["cards"]]
    if retry:
        again = pmap(lambda d: cards_for_doc(backend, model, prompt, d), retry, concurrency)
        fixed = {d.sha: row for d, row in zip(retry, again, strict=True)}
        results = [fixed.get(row["doc_sha"], row) if not row["cards"] else row for row in results]
    cost = 0.0
    model_id = None
    for row in results:
        append_jsonl(cache_path, row)
        cached[row["doc_sha"]] = row
        cost += row["usage"]["cost_usd"]
        model_id = row["usage"]["model_id"]
    cards = [c for d in docs for c in cached[d.sha]["cards"]]
    write_jsonl(run.path / "cards.jsonl", cards)
    if model_id:
        run.record_model("cards", model, model_id)
    run.add_cost(cost)
    run.mark_stage("cards", n_cards=len(cards), n_docs=len(docs), cost_usd=round(cost, 4))
    return cards
