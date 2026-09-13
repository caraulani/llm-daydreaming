# AGENTS.md

Working notes for coding agents (and humans) on this repo. `CLAUDE.md` points here.

## What this is

daydreamd recombines distant concepts from a corpus and keeps what survives a strict, blind,
pre-registered selection test. v0.1 runs over a synthetic corpus with planted bridges
(`data/synth/v0.1/`). Track C (owner-blind scoring over a real private corpus) is scaffolded but
not the primary path.

## Commands

```bash
make setup          # uv sync --all-extras
make test           # pytest, offline (fake backend + fake embedder)
make lint           # ruff check + format --check
make synth          # regenerate the synthetic corpus (do NOT do this after the prereg is sealed)
make smoke          # tiny end-to-end run with real model calls
make micro          # the pre-registered run (only after PREREGISTRATION.md is sealed)
make reproduce      # rebuild results/ from committed runs, no model calls
uv run daydreamd --help
```

## Architecture

```
adapters → core.ingest (snapshot) → core.cards → core.embed → core.sampler
   → core.generator → core.critic → core.dupgate → core.match (gold) | core.blind (owner)
   → eval.recovery + eval.metrics + eval.permutation_null → core.stats (tables)
```

| File | Purpose |
|---|---|
| `src/daydreamd/pipeline.py` | stage orchestration from a config; `run_all` |
| `src/daydreamd/cli.py` | typer CLI; one command per stage |
| `src/daydreamd/backends/` | `Completion` protocol; `claude_cli.py` is the default |
| `src/daydreamd/core/run.py` | `RunDir`, `metadata.yaml`, prompt loading + hashing |
| `src/daydreamd/core/sampler.py` | `Unit` records; arms S0/B1/B3/B6/B4; labels planted/decoy/random |
| `src/daydreamd/core/generator.py` | one prompt for every pair arm; `NONE` handling |
| `src/daydreamd/core/critic.py` | binary keep/kill with reason |
| `src/daydreamd/core/dupgate.py` | retrieval-based corpus-novelty gate (cosine > 0.85) |
| `src/daydreamd/core/match.py` | grounded gold match + cosine to gold |
| `src/daydreamd/core/blind.py` | owner-blind pack, sealed key, unseal |
| `src/daydreamd/core/stats.py` | tables T1..T6 (synthetic) and H1..H4 (owner-blind) |
| `src/daydreamd/synth/` | spec loader, 6-gram leakage check, note writer |
| `src/daydreamd/eval/recovery.py` | enrichment, recall, specificity, exploratory finds |
| `prompts/*.md` | versioned prompts; header comment carries version and role |
| `experiments/*/config.yaml` | arm sizes, seed, models, backend |

## Invariants (do not break)

1. **Generated text never becomes ground truth.** Gold lives in `data/synth/v0.1/bridges.yaml`,
   hand-authored. Survivors are never folded back into the corpus in v0.1.
2. **Never open `blind/key.json` before scoring.** `score --unseal` verifies `key.sha256` first.
3. **Always record exact model ids.** Backends return `model_id` from the provider envelope;
   stages write it into `metadata.yaml`. Aliases (`haiku`, `sonnet`) are never the record.
4. **Prompts are files.** Change a prompt by bumping the version header; the SHA is logged.
5. **After the preregistration is sealed**, `experiments/micro/config.yaml`, `prompts/`, and
   `data/synth/v0.1/` are frozen. Changes go to a new experiment directory and a new prereg.
6. **Private runs stay private.** `experiments/runs/private/` and `data/private/` are gitignored.
7. **No estimates in tables.** Cost and token columns come from logged usage only.

## Conventions

- Python 3.12, `uv`, ruff (line length 100, E501 delegated to the formatter), typed signatures.
- Small functions, one module per stage, no hidden global state; every stage is re-runnable
  from its inputs on disk.
- No em dashes in any prose or docstring. Plain words over jargon.
- Tests run offline with the `fake` backend and `FakeEmbedder`; anything needing a real model
  is a smoke test, not a unit test.
- Commit messages: imperative mood, one change per commit.
