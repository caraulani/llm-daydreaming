"""`daydreamd dream <path>`: one night over a corpus, ending in morning.md.

Stages are the research pipeline's own (snapshot, cards, embed, sample, generate, critic,
dupgate) with product defaults: a global card cache keyed by note sha so nightly runs only pay
for changed notes, the near-in-embedding, far-in-folder sampler the v0.1 post-hoc pointed at
(plus a quarter random pairs), the critic on but every kill kept visible, and a run directory
under `~/.daydreamd/runs/` in the research schema so a run can later feed Track C.
"""

from __future__ import annotations

import datetime as dt
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..adapters import load_corpus
from ..adapters.obsidian import wikilink
from ..backends import get_backend
from ..core.cards import extract_cards
from ..core.critic import run_critic
from ..core.dupgate import dupgate
from ..core.embed import embed_cards, make_embedder
from ..core.generator import generate
from ..core.ingest import Doc, snapshot
from ..core.io import append_jsonl, read_jsonl, write_jsonl
from ..core.run import RunDir, now_iso, today
from ..core.sampler import Unit, sample_cross_domain_near, sample_random
from . import paths
from .morning import Dream, render

KINDS = ("markdown", "obsidian", "claude-memory")


@dataclass
class DreamConfig:
    path: Path
    kind: str = "markdown"
    n: int = 40
    backend: str = "claude-cli"
    model: str = "sonnet"
    cards_model: str = "haiku"
    critic_model: str = "haiku"
    critic: bool = True
    embedder: str = "static"
    out: Path | None = None
    concurrency: int = 4
    seed: int | None = None
    exclude: list[str] = field(default_factory=list)
    compact: bool = False  # collapse the killed section; everything is still in the file


@dataclass
class DreamResult:
    morning: Path
    run: Path
    counts: dict[str, int]
    cost_usd: float
    models: dict[str, str]


def _slug_for(path: Path) -> str:
    return paths.slugify(path.resolve().name)


def _open_run(path: Path) -> RunDir:
    stamp = dt.datetime.now().strftime("%H%M%S")
    run = RunDir.create(paths.runs_root(), "", f"{_slug_for(path)}-{stamp}")
    run.update_meta(product=True, corpus=str(path), created=now_iso())
    return run


def _seed_cache(run: RunDir, docs: list[Doc]) -> int:
    """Copy cached cards for these notes into the run so extract_cards skips them."""
    wanted = {d.sha for d in docs}
    rows = [r for r in read_jsonl(paths.cards_cache()) if r.get("doc_sha") in wanted]
    write_jsonl(run.path / "cards_cache.jsonl", rows)
    return len(rows)


def _merge_cache(run: RunDir) -> int:
    known = {r["doc_sha"] for r in read_jsonl(paths.cards_cache())}
    added = 0
    for row in read_jsonl(run.path / "cards_cache.jsonl"):
        if row["doc_sha"] not in known and row.get("cards"):
            append_jsonl(paths.cards_cache(), row)
            known.add(row["doc_sha"])
            added += 1
    return added


def sample_units(
    cards: list[dict], vecs: Any, domains: dict[str, str], n: int, seed: int
) -> list[Unit]:
    """Three quarters near-in-embedding across folders, one quarter random. Deduplicated."""
    if len({c["source_note"] for c in cards}) < 2:
        raise RuntimeError("need at least two notes with concept cards to pair anything")
    n_near = max(1, round(n * 0.75))
    n_rand = max(0, n - n_near)
    distinct = len(set(domains.values())) > 1
    near = sample_cross_domain_near(
        cards, vecs, domains if distinct else {}, n_near, seed, "Q1", arm="near"
    )
    rand = sample_random(cards, vecs, n_rand, seed + 1) if n_rand else []
    seen: set[tuple[str, str]] = set()
    out: list[Unit] = []
    for u in near + rand:
        key = (min(u.card_a or "", u.card_b or ""), max(u.card_a or "", u.card_b or ""))
        if key in seen or u.note_a == u.note_b:
            continue
        seen.add(key)
        u.arm = "near" if u in near else "random"
        u.unit_id = f"dream-{len(out) + 1:04d}"
        u.label = None
        out.append(u)
    return out


def _source_label(doc: Doc | None, kind: str) -> str:
    if doc is None:
        return "unknown"
    return wikilink(doc) if kind == "obsidian" else f"`{doc.path or doc.name}`"


def dream(cfg: DreamConfig) -> DreamResult:
    if cfg.kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    corpus = cfg.path.expanduser().resolve()
    docs = load_corpus(cfg.kind, corpus, cfg.exclude or None)
    if len(docs) < 2:
        raise RuntimeError(f"found {len(docs)} usable notes under {corpus}; need at least two")
    by_id = {d.id: d for d in docs}
    backend = get_backend(cfg.backend)
    embedder = make_embedder(cfg.embedder)
    seed = cfg.seed if cfg.seed is not None else random.SystemRandom().randrange(1 << 30)
    run = _open_run(corpus)
    run.update_meta(seed=seed, backend=cfg.backend, kind=cfg.kind, embedder=embedder.model_name)

    manifest = snapshot(run, docs, corpus, anonymise=False)
    cached = _seed_cache(run, docs)
    cards = extract_cards(run, backend, docs, model=cfg.cards_model, concurrency=cfg.concurrency)
    _merge_cache(run)
    if not cards:
        raise RuntimeError("no concept cards could be extracted from this corpus")
    vecs = embed_cards(run.path, cards, embedder)
    run.mark_stage("embed", n=len(cards), model=embedder.model_name)

    domains = {d.id: d.domain for d in docs}
    units = sample_units(cards, vecs, domains, cfg.n, seed)
    write_jsonl(run.path / "units.jsonl", (u.to_row() for u in units))
    run.mark_stage("sample", n_units=len(units), policy="near-cross-folder 0.75 + random 0.25")

    gens = generate(run, backend, units, model=cfg.model, concurrency=cfg.concurrency)
    if cfg.critic:
        learnings = ""
        prompt_name = "critic"
        if paths.learnings_path().exists():
            learnings = "\n".join(paths.learnings_path().read_text().splitlines()[-30:])
            prompt_name = "critic_with_learnings"
        critic_rows = run_critic(
            run,
            backend,
            gens,
            model=cfg.critic_model,
            concurrency=cfg.concurrency,
            prompt_name=prompt_name,
            learnings=learnings,
        )
    else:
        critic_rows = [
            {"unit_id": g["unit_id"], "verdict": "keep", "reason": "critic_off", "usage": None}
            for g in gens
            if g["status"] == "ok"
        ]
        write_jsonl(run.path / "critic.jsonl", critic_rows)
        run.mark_stage("critic", skipped="--no-critic")
    dup_rows = dupgate(run, embedder, gens, critic_rows, cards, {d.id: d.text for d in docs})

    verdict = {r["unit_id"]: r for r in critic_rows}
    dup = {r["unit_id"]: r for r in dup_rows}
    survivors: list[Dream] = []
    killed: list[Dream] = []
    for g in gens:
        if g["status"] != "ok":
            continue
        v = verdict.get(g["unit_id"], {"verdict": "kill", "reason": "error"})
        out = g["output"]
        d = Dream(
            dream_id=f"{run.path.name}/{g['unit_id']}",
            connection=out["connection"],
            mechanism=out["mechanism"],
            check=out["testable_implication"],
            sources=[
                _source_label(by_id.get(g["note_a"]), cfg.kind),
                _source_label(by_id.get(g["note_b"]), cfg.kind),
            ],
            critic=str(v["verdict"]),
            reason=str(v["reason"]),
            distance=g.get("distance"),
            already_in_corpus=bool(dup.get(g["unit_id"], {}).get("already_in_corpus")),
        )
        (survivors if v["verdict"] == "keep" else killed).append(d)
    meta = run.read_meta()
    models = {role: m["model_id"] for role, m in (meta.get("models") or {}).items()}
    models["embeddings"] = embedder.model_name
    counts = {
        "notes": len(docs),
        "cards": len(cards),
        "cached_cards": cached,
        "asked": len(gens),
        "none": sum(1 for g in gens if g["status"] == "none"),
        "error": sum(1 for g in gens if g["status"] == "error"),
        "killed": len(killed),
        "dup": sum(1 for d in survivors if d.already_in_corpus),
        "survivors": len(survivors),
    }
    cost = float(meta.get("cost_usd_total", 0.0))
    declined = [
        (
            _source_label(by_id.get(g["note_a"]), cfg.kind),
            _source_label(by_id.get(g["note_b"]), cfg.kind) if g.get("note_b") else "(single note)",
            g.get("distance"),
        )
        for g in gens
        if g["status"] == "none"
    ]
    text = render(
        run_id=run.path.name,
        corpus=str(corpus),
        corpus_sha=manifest["corpus_sha256"],
        date=today(),
        survivors=survivors,
        killed=killed,
        counts=counts,
        models=models,
        cost_usd=cost,
        declined=declined,
        compact=cfg.compact,
    )
    out_path = (cfg.out or Path("morning.md")).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    (run.path / "morning.md").write_text(text, encoding="utf-8")
    run.mark_stage("dream", morning=str(out_path), **counts)
    return DreamResult(morning=out_path, run=run.path, counts=counts, cost_usd=cost, models=models)
