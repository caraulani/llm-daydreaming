"""Stage orchestration driven by an experiment config (experiments/*/config.yaml)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import yaml

from .adapters import load_corpus
from .backends import Backend, get_backend
from .core import blind as blind_mod
from .core.cards import extract_cards
from .core.critic import run_critic
from .core.dupgate import dupgate
from .core.embed import Embedder, FakeEmbedder, StaticEmbedder, embed_cards
from .core.embed import make_embedder as _make_embedder
from .core.generator import generate
from .core.ingest import Doc, load_snapshot, snapshot
from .core.io import copy_jsonl, read_json, read_jsonl, write_json, write_jsonl
from .core.match import match_gold
from .core.run import RunDir
from .core.sampler import (
    Unit,
    label_units,
    note_pair_key,
    note_units,
    partner_domain_units,
    random_note_pairs,
    sample_anchor_remote,
    sample_banded,
    sample_cross_domain_near,
    sample_random,
    single_units,
)
from .core.stats import human_tables, synthetic_tables

REPO = Path(__file__).resolve().parents[2]


def load_config(path: Path) -> dict[str, Any]:
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    cfg["_path"] = str(path)
    return cfg


def resolve(p: str | Path) -> Path:
    p = Path(p)
    return p if p.is_absolute() else REPO / p


def make_embedder(cfg: dict[str, Any]) -> Embedder | StaticEmbedder | FakeEmbedder:
    """Research runs default to the MiniLM model the committed runs used (`embedder: minilm`);
    a config may say `embedder: static` for the product default. Fake backend, fake embedder."""
    if cfg.get("backend") == "fake":
        return FakeEmbedder()
    return _make_embedder(str(cfg.get("embedder", "minilm")))


def open_run(cfg: dict[str, Any], run_root: Path | None = None, slug: str | None = None) -> RunDir:
    root = run_root or resolve(cfg.get("run_root", "experiments/runs"))
    run = RunDir.create(root, cfg.get("visibility", "public"), slug or cfg.get("slug", "run"))
    run.update_meta(config=str(cfg.get("_path")), seed=cfg.get("seed"), backend=cfg.get("backend"))
    return run


def stage_snapshot(run: RunDir, cfg: dict[str, Any]) -> list[Doc]:
    c = cfg["corpus"]
    docs = load_corpus(c["kind"], resolve(c["path"]), c.get("exclude"))
    manifest = snapshot(
        run,
        docs,
        resolve(c["path"]),
        anonymise=bool(c.get("anonymise", cfg.get("visibility") == "private")),
    )
    if c["kind"] == "synth":
        src = read_json(resolve(c["path"]) / "manifest.json")
        manifest["synthetic"] = {
            k: src[k]
            for k in (
                "n_bridges",
                "n_decoys",
                "leakage_failures",
                "writer_model_ids",
                "corpus_sha256",
            )
        }
        extra = {
            d["id"]: {k: d.get(k) for k in ("kind", "bridge_id", "decoy_id", "writer_family")}
            for d in src.get("docs", [])
        }
        for doc in manifest["docs"]:
            doc.update(extra.get(doc["id"], {}))
        manifest["synthetic"]["writers"] = src.get("writers", {})
        manifest["synthetic"]["leak_judge"] = src.get("leak_judge", {})
        write_json(run.path / "snapshot" / "manifest.json", manifest)
        write_json(run.path / "gold.json", read_json(resolve(c["path"]) / "gold.json"))
        write_json(run.path / "domains.json", read_json(resolve(c["path"]) / "domains.json"))
    return docs


def stage_cards(run: RunDir, cfg: dict[str, Any], backend: Backend) -> list[dict]:
    docs = load_snapshot(run)
    return extract_cards(
        run, backend, docs, model=cfg["models"]["cards"], concurrency=cfg.get("concurrency", 4)
    )


def stage_embed(run: RunDir, cfg: dict[str, Any]) -> np.ndarray:
    cards = list(read_jsonl(run.path / "cards.jsonl"))
    vecs = embed_cards(run.path, cards, make_embedder(cfg))
    run.mark_stage("embed", n=len(cards), model=make_embedder(cfg).model_name)
    return vecs


def _synthetic_context(run: RunDir) -> tuple[dict, dict, dict[str, str]]:
    gold = read_json(run.path / "gold.json") if (run.path / "gold.json").exists() else {}
    domains = read_json(run.path / "domains.json") if (run.path / "domains.json").exists() else {}
    manifest = read_json(run.path / "snapshot" / "manifest.json")
    return gold, manifest, domains


def stage_sample(run: RunDir, cfg: dict[str, Any]) -> list[Unit]:
    cards = list(read_jsonl(run.path / "cards.jsonl"))
    vecs = np.load(run.path / "embeddings.npy")
    seed = int(cfg.get("seed", 0))
    arms = cfg.get("arms", {})
    gold, manifest, domains = _synthetic_context(run)
    planted = {note_pair_key(g["note_a"], g["note_b"]): bid for bid, g in gold.items()}
    src_manifest = (
        read_json(resolve(cfg["corpus"]["path"]) / "manifest.json")
        if cfg["corpus"]["kind"] == "synth"
        else {}
    )
    decoy_notes: dict[str, list[str]] = {}
    for d in src_manifest.get("docs", []):
        if d.get("decoy_id"):
            decoy_notes.setdefault(d["decoy_id"], []).append(d["id"])
    decoys = {note_pair_key(*v): k for k, v in decoy_notes.items() if len(v) == 2}
    units: list[Unit] = []
    if "S0" in arms and gold:
        s0 = arms["S0"]
        pl = list(planted.items())[: s0.get("planted_limit") or None]
        dc = list(decoys.items())[: s0.get("decoy_limit") or None]
        triples = [(a, b, f"planted:{bid}") for (a, b), bid in pl] + [
            (a, b, f"decoy:{did}") for (a, b), did in dc
        ]
        notes = [d["id"] for d in manifest["docs"]]
        rnd = random_note_pairs(
            notes, domains, set(planted) | set(decoys), int(s0.get("random_pairs", 42)), seed
        )
        triples += [(a, b, "random") for a, b in rnd]
        units += note_units(cards, triples, "S0")
    if "S1" in arms and gold:
        notes = [d["id"] for d in manifest["docs"]]
        units += partner_domain_units(cards, gold, domains, notes, seed + 11, "S1")
    if "B1" in arms:
        units += sample_random(cards, vecs, int(arms["B1"].get("n", 100)), seed + 1)
    if "B3" in arms:
        units += sample_banded(cards, vecs, int(arms["B3"].get("per_band", 25)), seed + 3)
    if "B6" in arms:
        units += sample_anchor_remote(cards, vecs, int(arms["B6"].get("n", 50)), seed + 6)
    if "B7" in arms:
        b7 = arms["B7"]
        units += sample_cross_domain_near(
            cards, vecs, domains, int(b7.get("n", 100)), seed + 7, str(b7.get("band", "Q1"))
        )
    if "B4" in arms:
        sel = arms["B4"].get("notes", "bridge")
        if sel == "bridge" and gold:
            notes = sorted(
                {g["note_a"] for g in gold.values()} | {g["note_b"] for g in gold.values()}
            )
        elif sel == "all":
            notes = sorted({c["source_note"] for c in cards})
        else:
            rng = np.random.default_rng(seed + 4)
            all_notes = sorted({c["source_note"] for c in cards})
            notes = [
                all_notes[i]
                for i in rng.choice(
                    len(all_notes),
                    size=min(int(arms["B4"].get("n", 50)), len(all_notes)),
                    replace=False,
                )
            ]
        limit = arms["B4"].get("limit")
        units += single_units(cards, notes[: limit or None], "B4")
    label_units(units, planted, decoys)
    family = {d["id"]: d.get("writer_family") for d in manifest.get("docs", [])}
    for u in units:
        u.writer_family = family.get(u.note_a)
    write_jsonl(run.path / "units.jsonl", (u.to_row() for u in units))
    run.mark_stage(
        "sample",
        n_units=len(units),
        arms={a: sum(1 for u in units if u.arm == a) for a in sorted({u.arm for u in units})},
    )
    return units


def _units_from_disk(run: RunDir) -> list[Unit]:
    return [Unit(**row) for row in read_jsonl(run.path / "units.jsonl")]


def stage_generate(run: RunDir, cfg: dict[str, Any], backend: Backend) -> list[dict]:
    return generate(
        run,
        backend,
        _units_from_disk(run),
        model=cfg["models"]["generator"],
        concurrency=cfg.get("concurrency", 4),
    )


def critic_aliases(cfg: dict[str, Any]) -> list[str]:
    """`models.critic` may be one alias or a list; the first is the primary critic."""
    raw = cfg["models"]["critic"]
    aliases = [str(x) for x in raw] if isinstance(raw, list) else [str(raw)]
    if not aliases:
        raise ValueError("models.critic must name at least one critic")
    return aliases


def stage_critic(run: RunDir, cfg: dict[str, Any], backend: Backend) -> list[dict]:
    """Run one or more critics on the same generations.

    The primary (first) critic writes ``critic.jsonl`` and drives dupgate and the main tables.
    Every critic, including the primary, also writes ``critic_<alias>.jsonl`` and records its
    exact model id under ``models.critic_<alias>`` so table T8 can compare them.
    """
    gens = list(read_jsonl(run.path / "generations.jsonl"))
    aliases = critic_aliases(cfg)
    conc = cfg.get("concurrency", 4)
    primary: list[dict] = []
    for i, alias in enumerate(aliases):
        rows = run_critic(
            run,
            backend,
            gens,
            model=alias,
            concurrency=conc,
            outfile=f"critic_{alias}.jsonl",
            role=f"critic_{alias}",
        )
        if i == 0:
            primary = rows
            copy_jsonl(run.path / f"critic_{alias}.jsonl", run.path / "critic.jsonl")
            meta = run.read_meta()
            run.record_model(
                "critic", alias, meta["models"].get(f"critic_{alias}", {}).get("model_id", "")
            )
            run.mark_stage(
                "critic",
                primary=alias,
                critics=aliases,
                n_judged=len(rows),
                n_keep=sum(1 for r in rows if r["verdict"] == "keep"),
            )
    return primary


def stage_dupgate(run: RunDir, cfg: dict[str, Any]) -> list[dict]:
    gens = list(read_jsonl(run.path / "generations.jsonl"))
    critic = list(read_jsonl(run.path / "critic.jsonl"))
    cards = list(read_jsonl(run.path / "cards.jsonl"))
    docs = {d.id: d.text for d in load_snapshot(run)}
    return dupgate(
        run,
        make_embedder(cfg),
        gens,
        critic,
        cards,
        docs,
        threshold=float(cfg.get("dupgate_threshold", 0.85)),
    )


def stage_match(run: RunDir, cfg: dict[str, Any], backend: Backend) -> list[dict]:
    gold, _, _ = _synthetic_context(run)
    if not gold:
        run.mark_stage("match_gold", skipped="no gold.json in run")
        return []
    gens = list(read_jsonl(run.path / "generations.jsonl"))
    return match_gold(
        run,
        backend,
        make_embedder(cfg),
        gens,
        gold,
        model=cfg["models"].get("match", "haiku"),
        concurrency=cfg.get("concurrency", 4),
    )


def stage_blind(run: RunDir, cfg: dict[str, Any]) -> Path:
    gens = list(read_jsonl(run.path / "generations.jsonl"))
    return blind_mod.build_pack(run, gens, seed=int(cfg.get("seed", 0)))


def stage_stats(run: RunDir, cfg: dict[str, Any], out_dir: Path | None = None) -> dict[str, Any]:
    out = out_dir or (run.path / "tables")
    n_perm = int(cfg.get("stats", {}).get("n_perm", 10_000))
    summary = synthetic_tables(
        run,
        out,
        n_perm=n_perm,
        seed=int(cfg.get("seed", 0)),
        prereg=str(cfg.get("prereg", "v0.1")),
    )
    human = human_tables(run, out, n_perm=n_perm, seed=int(cfg.get("seed", 0)))
    if out_dir is None:
        # Only an in-run stats pass touches the run's metadata. `make reproduce` writes tables
        # to results/ and must leave committed run directories byte-identical.
        try:
            tables = str(out.resolve().relative_to(Path.cwd().resolve()))
        except ValueError:
            tables = out.name
        run.mark_stage("stats", tables=tables, human_track=bool(human))
    return summary


def run_all(
    cfg: dict[str, Any],
    run_root: Path | None = None,
    slug: str | None = None,
    backend_name: str | None = None,
) -> RunDir:
    backend = get_backend(backend_name or cfg.get("backend", "claude-cli"))
    run = open_run(cfg, run_root, slug)
    stage_snapshot(run, cfg)
    stage_cards(run, cfg, backend)
    stage_embed(run, cfg)
    stage_sample(run, cfg)
    stage_generate(run, cfg, backend)
    stage_critic(run, cfg, backend)
    stage_dupgate(run, cfg)
    stage_match(run, cfg, backend)
    if cfg.get("blind", {}).get("enabled"):
        stage_blind(run, cfg)
    stage_stats(run, cfg)
    return run
