"""Write the synthetic notes with a model, one call per note, with regeneration on leakage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..backends import Backend
from ..core.io import sha256_text, write_json
from ..core.llm import pmap, usage_record
from ..core.run import load_prompt, now_iso
from .leakage import leaked_ngrams
from .spec import NoteSpec, Spec

MAX_TRIES = 3


def render(template: str, spec: Spec, note: NoteSpec) -> str:
    ing = ""
    if note.ingredients:
        ing = (
            "Work these facts in, obliquely, as ordinary observations (do not list them as a set, do not explain them):\n"
            + "\n".join(f"- {x}" for x in note.ingredients)
            + "\n"
        )
    forbidden = ", ".join(note.forbidden) if note.forbidden else "(none)"
    return (
        template.replace("{{persona}}", spec.persona)
        .replace("{{topic}}", note.topic)
        .replace("{{domain_label}}", spec.domains[note.domain])
        .replace("{{ingredients_block}}", ing)
        .replace("{{forbidden}}", forbidden)
    )


TRAILER_PREFIXES = ("Co-Authored-By:", "Claude-Session:", "🤖 Generated with")


def clean_note(text: str) -> str:
    """Drop harness trailers (attribution lines) and trailing separators the writer may append."""
    lines = [ln for ln in text.strip().splitlines() if not ln.strip().startswith(TRAILER_PREFIXES)]
    while lines and lines[-1].strip() in {"", "---"}:
        lines.pop()
    return "\n".join(lines).strip() + "\n"


def write_note(
    backend: Backend, model: str, template: str, spec: Spec, note: NoteSpec, golds: list[str]
) -> dict[str, Any]:
    prompt = render(template, spec, note)
    tries: list[dict[str, Any]] = []
    for attempt in range(1, MAX_TRIES + 1):
        comp = backend.complete(prompt, model=model)
        text = clean_note(comp.text)
        if not text.startswith("---"):
            text = "---\nname: " + note.note_id + "\n---\n" + text
        leaks = leaked_ngrams(text, golds)
        style = ["em_dash"] if "\u2014" in text else []
        words = len(text.split())
        tries.append(
            {
                "attempt": attempt,
                "leaks": leaks,
                "style": style,
                "words": words,
                "usage": usage_record(comp),
            }
        )
        if not leaks and not style:
            return {"note": note, "text": text, "tries": tries, "ok": True}
    return {"note": note, "text": text, "tries": tries, "ok": False}


def build_corpus(
    spec: Spec, backend: Backend, out_dir: Path, model: str = "haiku", concurrency: int = 4
) -> dict[str, Any]:
    template, prompt_sha = load_prompt("synth_note")
    gold = spec.gold()
    golds = [g["gold_connection"] for g in gold.values()] + [
        g["gold_implication"] for g in gold.values()
    ]
    plan = spec.note_plan()
    results = pmap(
        lambda n: write_note(backend, model, template, spec, n, golds), plan, concurrency
    )
    notes_dir = out_dir / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    manifest_docs = []
    cost = 0.0
    model_ids: set[str] = set()
    failed = []
    for r in results:
        n: NoteSpec = r["note"]
        (notes_dir / f"{n.note_id}.md").write_text(r["text"], encoding="utf-8")
        for t in r["tries"]:
            cost += t["usage"]["cost_usd"]
            model_ids.add(t["usage"]["model_id"])
        if not r["ok"]:
            failed.append(n.note_id)
        manifest_docs.append(
            {
                "id": n.note_id,
                "domain": n.domain,
                "kind": n.kind,
                "bridge_id": n.bridge_id,
                "decoy_id": n.decoy_id,
                "sha256": sha256_text(r["text"]),
                "words": len(r["text"].split()),
                "tries": len(r["tries"]),
                "leaks_final": r["tries"][-1]["leaks"],
            }
        )
    manifest = {
        "version": "v0.1",
        "generated_at": now_iso(),
        "writer_model_ids": sorted(model_ids),
        "prompt_sha256": {"synth_note": prompt_sha},
        "n_notes": len(manifest_docs),
        "n_bridges": len(spec.bridges),
        "n_decoys": len(spec.decoys),
        "leakage_ngram": 6,
        "leakage_failures": failed,
        "cost_usd": round(cost, 4),
        "corpus_sha256": sha256_text("\n".join(sorted(d["sha256"] for d in manifest_docs))),
        "docs": sorted(manifest_docs, key=lambda d: d["id"]),
    }
    write_json(out_dir / "manifest.json", manifest)
    write_json(out_dir / "gold.json", gold)
    (out_dir / "domains.json").write_text(
        json.dumps({d["id"]: d["domain"] for d in manifest_docs}, indent=2) + "\n"
    )
    return manifest
