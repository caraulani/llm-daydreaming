"""daydreamd command line. Stage commands operate on a run directory; `run-all` chains them."""

from __future__ import annotations

from pathlib import Path

import typer

from . import pipeline
from .backends import get_backend
from .core.run import RunDir

app = typer.Typer(
    help="Recombine distant concepts from a corpus; keep what survives selection.",
    no_args_is_help=True,
)


def _run(path: Path) -> RunDir:
    if not (path / "metadata.yaml").exists():
        raise typer.BadParameter(f"{path} is not a run directory")
    return RunDir(path)


def _cfg(config: Path) -> dict:
    return pipeline.load_config(config)


@app.command()
def synth(
    out: Path = typer.Option(Path("data/synth/v0.1")),
    model: str = "haiku",
    backend: str = "claude-cli",
    concurrency: int = 4,
    writers: Path | None = typer.Option(
        None, help="writers.yaml with families: {A: {backend, model}, B: {backend, model}}"
    ),
    judge_model: str = typer.Option("haiku", help="Paraphrase-leak judge alias (oblique specs)"),
    max_tries: int | None = typer.Option(None, help="Override the regeneration cap"),
    min_words: int = typer.Option(150, help="Notes shorter than this are regenerated"),
    one_side_gate: bool = typer.Option(
        False,
        "--one-side-gate",
        help="ADR-014: run the generator on each bridge note alone; list bridges it recovers",
    ),
    gate_model: str = typer.Option("sonnet", help="Generator alias for the one-side gate"),
    resume: bool = typer.Option(
        False, "--resume", help="Keep notes that already pass every check; rebuild the rest"
    ),
) -> None:
    """Write the synthetic corpus from the hand-authored specs (bridges, decoys, fillers)."""
    from .synth.generate import build_corpus, load_writers
    from .synth.spec import load_spec

    out = pipeline.resolve(out)
    manifest = build_corpus(
        load_spec(out),
        get_backend(backend),
        out,
        model=model,
        concurrency=concurrency,
        writers=load_writers(pipeline.resolve(writers)) if writers else None,
        judge_model=judge_model,
        one_side=(gate_model, judge_model) if one_side_gate else None,
        max_tries=max_tries,
        min_words=min_words,
        resume=resume,
    )
    typer.echo(
        f"wrote {manifest['n_notes']} notes to {out} (reused {manifest['reused_notes']}, "
        f"writers {manifest['writer_model_ids']}, "
        f"cost ${manifest['cost_usd']}, leakage failures {manifest['leakage_failures']}, "
        f"leak-judge failures {manifest['leak_judge']['failures']})"
    )


@app.command("run-all")
def run_all(
    config: Path, run_root: Path | None = None, slug: str | None = None, backend: str | None = None
) -> None:
    """Run every stage from a config: snapshot, cards, embed, sample, generate, critic, dupgate, match-gold, stats."""
    run = pipeline.run_all(_cfg(config), run_root, slug, backend)
    typer.echo(f"run complete: {run.path}")


@app.command()
def snapshot(config: Path, run_root: Path | None = None, slug: str | None = None) -> None:
    """Freeze the corpus into a new run directory."""
    cfg = _cfg(config)
    run = pipeline.open_run(cfg, run_root, slug)
    docs = pipeline.stage_snapshot(run, cfg)
    typer.echo(f"{len(docs)} docs frozen at {run.path}")


def _stage(name: str):  # noqa: ANN202
    def cmd(run: Path, config: Path, backend: str | None = None) -> None:
        cfg = _cfg(config)
        r = _run(run)
        needs_backend = name in {"cards", "generate", "critic", "match-gold"}
        fn = {
            "cards": lambda: pipeline.stage_cards(r, cfg, get_backend(backend or cfg["backend"])),
            "embed": lambda: pipeline.stage_embed(r, cfg),
            "sample": lambda: pipeline.stage_sample(r, cfg),
            "generate": lambda: pipeline.stage_generate(
                r, cfg, get_backend(backend or cfg["backend"])
            ),
            "critic": lambda: pipeline.stage_critic(r, cfg, get_backend(backend or cfg["backend"])),
            "dupgate": lambda: pipeline.stage_dupgate(r, cfg),
            "match-gold": lambda: pipeline.stage_match(
                r, cfg, get_backend(backend or cfg["backend"])
            ),
            "blind": lambda: pipeline.stage_blind(r, cfg),
        }[name]
        _ = needs_backend
        out = fn()
        n = len(out) if hasattr(out, "__len__") else out
        typer.echo(f"{name}: {n}")

    cmd.__name__ = name.replace("-", "_")
    cmd.__doc__ = f"Run the `{name}` stage on an existing run directory."
    return cmd


for _name in ("cards", "embed", "sample", "generate", "critic", "dupgate", "match-gold", "blind"):
    app.command(_name)(_stage(_name))


@app.command()
def score(
    run: Path,
    unseal: bool = typer.Option(False, help="Verify the key hash and join verdicts to arms."),
) -> None:
    """Read checked boxes from blind/items.md. Without --unseal, only reports counts."""
    from .core import blind as blind_mod

    r = _run(run)
    if not unseal:
        rows = blind_mod.parse_scores(r.path / "blind" / "items.md")
        typer.echo(
            f"scored {sum(1 for x in rows if x['keep'] or x['known'])} of {len(rows)} items (key still sealed)"
        )
        return
    verdicts = blind_mod.unseal(r)
    typer.echo(f"unsealed {len(verdicts)} verdicts into {r.path / 'verdicts.jsonl'}")


@app.command()
def stats(run: Path, config: Path, out: Path | None = None) -> None:
    """Rebuild every table from stage outputs. Makes no model calls."""
    summary = pipeline.stage_stats(_run(run), _cfg(config), out)
    typer.echo(f"tables written; total cost ${summary['cost_usd_total']}")


@app.command("fetch-arxiv")
def fetch_arxiv(out: Path = typer.Option(Path("data/public/arxiv-cs-2026")), n: int = 40) -> None:
    """Fetch a small public corpus of arXiv abstracts (metadata CC0) and pin the ids."""
    from .adapters.arxiv_abstracts import fetch

    m = fetch(pipeline.resolve(out), n)
    typer.echo(f"fetched {m['n_docs']} abstracts into {out}")


# ---------------------------------------------------------------------------------------------
# Product commands: dream, review, skill, mcp, schedule. State lives in ~/.daydreamd (or
# $DAYDREAMD_HOME). Nothing leaves the machine except prompts to the backend you chose.


@app.command()
def dream(
    path: Path = typer.Argument(
        ...,
        help="Folder of notes: an Obsidian vault, a Claude Code memory dir, any markdown folder",
    ),
    out: Path = typer.Option(Path("morning.md"), help="Where to write the morning file"),
    kind: str = typer.Option("markdown", help="markdown | obsidian | claude-memory"),
    n: int = typer.Option(40, help="How many pairs to ask about"),
    backend: str = typer.Option("claude-cli", help="claude-cli | anthropic | ollama"),
    model: str = typer.Option("sonnet", help="Generator model alias or id"),
    cards_model: str = typer.Option("haiku", help="Concept-card extractor alias or id"),
    critic_model: str = typer.Option("haiku", help="Critic alias or id"),
    no_critic: bool = typer.Option(
        False, "--no-critic", help="Skip the critic; everything non-NONE survives"
    ),
    embedder: str = typer.Option("static", help="static (default, no PyTorch) | minilm | fake"),
    concurrency: int = typer.Option(4),
    exclude: list[str] = typer.Option([], help="Extra filename patterns to skip"),
    compact: bool = typer.Option(
        False, "--compact", help="Collapse the killed section (everything stays in the file)"
    ),
) -> None:
    """One night over your notes: pairs distant concepts, asks the model, keeps what survives, writes morning.md."""
    from .product.dream import DreamConfig
    from .product.dream import dream as _dream

    r = _dream(
        DreamConfig(
            path=path,
            kind=kind,
            n=n,
            backend=backend,
            model=model,
            cards_model=cards_model,
            critic_model=critic_model,
            critic=not no_critic,
            embedder=embedder,
            out=out,
            concurrency=concurrency,
            exclude=list(exclude),
            compact=compact,
        )
    )
    c = r.counts
    typer.echo(
        f"{r.morning}: {c['survivors']} survivors of {c['asked']} pairs "
        f"(NONE {c['none']}, killed {c['killed']}, cached cards {c['cached_cards']}/{c['notes']} notes); "
        f"measured cost ${r.cost_usd:.4f}; run {r.run}"
    )


@app.command()
def gate(
    corpus: Path = typer.Argument(..., help="A synthetic corpus dir with notes/ and gold.json"),
    backend: str = typer.Option("claude-cli", help="claude-cli | anthropic | ollama"),
    gen_model: str = typer.Option("sonnet", help="Generator alias or id for the one-side gate"),
    judge_model: str = typer.Option("haiku", help="Match judge alias or id"),
    votes: int = typer.Option(2, help="Judge votes per side; a tie fails closed"),
) -> None:
    """ADR-014 one-side gate over an existing corpus: which planted bridges does one note alone give away?"""
    import json

    from .backends import get_backend
    from .synth.oneside import gate_bridges

    gold = json.loads((corpus / "gold.json").read_text(encoding="utf-8"))
    notes = {p.stem: p.read_text(encoding="utf-8") for p in sorted((corpus / "notes").glob("*.md"))}
    res = gate_bridges(get_backend(backend), gen_model, judge_model, notes, gold, votes=votes)
    out = corpus / f"one_side_gate.{gen_model.replace('/', '_').replace(':', '_')}.json"
    out.write_text(json.dumps(res, indent=2), encoding="utf-8")
    typer.echo(
        f"gate: {len(res['failures'])} of {len(gold)} bridges recovered from one side "
        f"({', '.join(res['failures']) or 'none'}); measured cost ${res['cost_usd']}; written {out}"
    )


@app.command()
def review(morning: Path = typer.Argument(Path("morning.md"))) -> None:
    """Read the KEEP and KNOWN boxes you ticked into ~/.daydreamd/verdicts.jsonl."""
    from .product.review import review as _review

    s = _review(morning)
    typer.echo(
        f"reviewed {s.reviewed}: kept {s.kept}, known {s.known}, unmarked {s.unmarked}; log {s.log}"
    )


@app.command()
def skill(
    out: Path | None = typer.Option(
        None, help="Defaults to .claude/skills/daydreamd-<corpus>/SKILL.md"
    ),
) -> None:
    """Write a SKILL.md of the connections you endorsed, and the learnings the critic reads next time."""
    from .product.skill import build_skill

    r = build_skill(out)
    typer.echo(
        f"wrote {r.skill} ({r.endorsed} endorsed, {r.known} known, {r.rejected} rejected); learnings {r.learnings}"
    )


@app.command()
def mcp() -> None:
    """Serve dream, review, skill and status as MCP tools over stdio (needs the mcp extra)."""
    from .product.mcp_server import main as _main

    _main()


schedule_app = typer.Typer(
    help="Run `daydreamd dream` every night (launchd on macOS, cron on Linux)."
)
app.add_typer(schedule_app, name="schedule")


@schedule_app.command("install")
def schedule_install(
    path: Path = typer.Option(..., "--path", help="Folder of notes to dream over"),
    at: str = typer.Option("03:00", help="Local time HH:MM"),
    kind: str = typer.Option("markdown"),
    out: Path = typer.Option(Path("morning.md")),
    n: int = typer.Option(40),
    no_load: bool = typer.Option(False, "--no-load", help="Write the file but do not register it"),
) -> None:
    """Install the nightly job. The plist or crontab line is printed before it is installed."""
    from .product import paths
    from .product.schedule import install

    target, _ = install(path, kind, out, n, at, load=not no_load, home=paths.home())
    typer.echo(f"installed: {target or 'crontab'} (runs daily at {at})")


@schedule_app.command("remove")
def schedule_remove(no_load: bool = typer.Option(False, "--no-load")) -> None:
    """Remove the nightly job."""
    from .product.schedule import remove

    typer.echo(remove(load=not no_load))


if __name__ == "__main__":
    app()
