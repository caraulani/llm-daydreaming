"""Write the synthetic notes with a model, one call per note, with regeneration on leakage."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ..backends import Backend, get_backend
from ..core.io import sha256_text, write_json
from ..core.llm import complete_json, pmap, usage_record
from ..core.run import load_prompt, now_iso
from .leakage import leaked_ngrams
from .spec import NoteSpec, Spec, assign_writers

MAX_TRIES = 3  # v0.1 behaviour; oblique (v0.2) specs use MAX_TRIES_OBLIQUE
MAX_TRIES_OBLIQUE = 5


@dataclass
class Writer:
    """One note-writer family: which backend and which model alias writes its notes."""

    family: str
    backend: Backend
    model: str


def load_writers(path: Path) -> list[Writer]:
    """Read a writers file: ``families: {A: {backend, model}, B: {backend, model}}``."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    fams = raw.get("families") or {}
    out = []
    for name, cfg in fams.items():
        model = str(cfg.get("model", "haiku"))
        if model.upper() == "TBD":
            raise RuntimeError(f"writer family {name}: model id is still TBD in {path}")
        out.append(Writer(str(name), get_backend(str(cfg.get("backend", "claude-cli"))), model))
    return out


def judge_leak(
    backend: Backend, model: str, template: str, note_text: str, gold: dict[str, str]
) -> dict[str, Any]:
    """Paraphrase-leak judge: does this ONE note already state or imply the hidden connection?

    Returns {verdict: LEAK|CLEAN|ERROR, evidence, usage}. Any verdict other than CLEAN counts as
    a failed check, so the note is regenerated (an error burns one attempt rather than passing).
    """
    prompt = (
        template.replace("{{note_text}}", note_text)
        .replace("{{gold_connection}}", gold["gold_connection"])
        .replace("{{gold_implication}}", gold["gold_implication"])
    )
    try:
        parsed, comp = complete_json(backend, prompt, model)
    except Exception as exc:  # noqa: BLE001
        return {"verdict": "ERROR", "evidence": str(exc)[:200], "usage": None}
    verdict = str((parsed or {}).get("verdict", "ERROR")).upper()
    if verdict not in {"LEAK", "CLEAN"}:
        verdict = "ERROR"
    return {
        "verdict": verdict,
        "evidence": str((parsed or {}).get("evidence", ""))[:300],
        "usage": usage_record(comp),
    }


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
    backend: Backend,
    model: str,
    template: str,
    spec: Spec,
    note: NoteSpec,
    golds: list[str],
    max_tries: int = MAX_TRIES,
    leak_judge: tuple[Backend, str, str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Write one note, regenerating on a 6-gram leak, an em dash, or (bridge notes with a
    judge) a LEAK verdict from the paraphrase-leak judge. ``leak_judge`` is
    (backend, model, template, gold-for-this-bridge) or None."""
    prompt = render(template, spec, note)
    tries: list[dict[str, Any]] = []
    for attempt in range(1, max_tries + 1):
        comp = backend.complete(prompt, model=model)
        text = clean_note(comp.text)
        if not text.startswith("---"):
            text = "---\nname: " + note.note_id + "\n---\n" + text
        leaks = leaked_ngrams(text, golds)
        style = ["em_dash"] if "\u2014" in text else []
        if len(text.split()) < 150:
            style.append("short")
        words = len(text.split())
        record: dict[str, Any] = {
            "attempt": attempt,
            "leaks": leaks,
            "style": style,
            "words": words,
            "usage": usage_record(comp),
        }
        judged: dict[str, Any] | None = None
        if leak_judge is not None and not leaks and not style:
            jb, jm, jt, gold = leak_judge
            judged = judge_leak(jb, jm, jt, text, gold)
            record["leak_judge"] = judged
        tries.append(record)
        clean = not leaks and not style and (judged is None or judged["verdict"] == "CLEAN")
        if clean:
            return {"note": note, "text": text, "tries": tries, "ok": True}
    return {"note": note, "text": text, "tries": tries, "ok": False}


def build_corpus(
    spec: Spec,
    backend: Backend,
    out_dir: Path,
    model: str = "haiku",
    concurrency: int = 4,
    writers: list[Writer] | None = None,
    judge_model: str = "haiku",
    max_tries: int | None = None,
) -> dict[str, Any]:
    """Write every note in the plan and freeze the corpus manifest.

    v0.1 behaviour (single writer, 6-gram check, 3 tries) is unchanged when the spec has no
    obliqueness fields and no writers are given. Oblique specs add the paraphrase-leak judge on
    bridge notes and allow 5 tries. Writers, when given, assign note-writer families by parity.
    """
    template, prompt_sha = load_prompt("synth_note")
    gold = spec.gold()
    golds = [g["gold_connection"] for g in gold.values()] + [
        g["gold_implication"] for g in gold.values()
    ]
    plan = spec.note_plan()
    families = {w.family: w for w in (writers or [])}
    plan = assign_writers(plan, list(families))
    tries_cap = max_tries or (MAX_TRIES_OBLIQUE if spec.oblique else MAX_TRIES)
    judge_template, judge_sha = load_prompt("leak_judge") if spec.oblique else ("", "")

    def _write(n: NoteSpec) -> dict[str, Any]:
        w = families.get(n.writer_family or "")
        be, mo = (w.backend, w.model) if w else (backend, model)
        lj = None
        if spec.oblique and n.kind == "bridge" and n.bridge_id:
            lj = (backend, judge_model, judge_template, gold[n.bridge_id])
        return write_note(be, mo, template, spec, n, golds, max_tries=tries_cap, leak_judge=lj)

    results = pmap(_write, plan, concurrency)
    notes_dir = out_dir / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    manifest_docs = []
    cost = 0.0
    model_ids: set[str] = set()
    judge_ids: set[str] = set()
    failed = []
    leak_failed = []
    for r in results:
        n: NoteSpec = r["note"]
        (notes_dir / f"{n.note_id}.md").write_text(r["text"], encoding="utf-8")
        for t in r["tries"]:
            cost += t["usage"]["cost_usd"]
            model_ids.add(t["usage"]["model_id"])
            lj = t.get("leak_judge")
            if lj and lj.get("usage"):
                cost += lj["usage"]["cost_usd"]
                judge_ids.add(lj["usage"]["model_id"])
        last = r["tries"][-1]
        if not r["ok"]:
            failed.append(n.note_id)
            if last.get("leak_judge") and last["leak_judge"]["verdict"] != "CLEAN":
                leak_failed.append(n.note_id)
        doc: dict[str, Any] = {
            "id": n.note_id,
            "domain": n.domain,
            "kind": n.kind,
            "bridge_id": n.bridge_id,
            "decoy_id": n.decoy_id,
            "sha256": sha256_text(r["text"]),
            "words": len(r["text"].split()),
            "tries": len(r["tries"]),
            "leaks_final": last["leaks"],
            "writer_family": n.writer_family,
            "writer_model_id": last["usage"]["model_id"],
        }
        if spec.oblique and n.kind == "bridge":
            doc["leak_judge"] = {
                "final": (last.get("leak_judge") or {}).get("verdict"),
                "evidence": (last.get("leak_judge") or {}).get("evidence"),
                "verdicts": [(t.get("leak_judge") or {}).get("verdict") for t in r["tries"]],
            }
        manifest_docs.append(doc)
    manifest = {
        "version": out_dir.name,
        "generated_at": now_iso(),
        "writer_model_ids": sorted(model_ids),
        "writers": {f: {"backend": w.backend.name, "model": w.model} for f, w in families.items()},
        "prompt_sha256": {
            "synth_note": prompt_sha,
            **({"leak_judge": judge_sha} if judge_sha else {}),
        },
        "n_notes": len(manifest_docs),
        "n_bridges": len(spec.bridges),
        "n_decoys": len(spec.decoys),
        "leakage_ngram": 6,
        "leakage_failures": failed,
        "leak_judge": {
            "enabled": bool(spec.oblique),
            "model_ids": sorted(judge_ids),
            "failures": leak_failed,
        },
        "max_tries": tries_cap,
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
