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
) -> None:
    """Write the synthetic corpus from the hand-authored specs (bridges, decoys, fillers)."""
    from .synth.generate import build_corpus
    from .synth.spec import load_spec

    out = pipeline.resolve(out)
    manifest = build_corpus(
        load_spec(out), get_backend(backend), out, model=model, concurrency=concurrency
    )
    typer.echo(
        f"wrote {manifest['n_notes']} notes to {out} (writer {manifest['writer_model_ids']}, cost ${manifest['cost_usd']}, leakage failures {manifest['leakage_failures']})"
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


if __name__ == "__main__":
    app()
