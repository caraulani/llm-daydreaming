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
make synth          # build the v0.1 corpus (do NOT do this after the prereg is sealed)
make synth SPEC=data/synth/v0.2 WRITERS=experiments/micro-v0.2/writers.yaml   # v0.2, two writer families
make smoke          # tiny end-to-end run with real model calls
make micro          # the pre-registered v0.1 run (only after PREREGISTRATION.md is sealed)
make micro CONFIG=experiments/micro-v0.2/config.yaml   # the v0.2 run (after PREREGISTRATION-v0.2.md is sealed)
make reproduce      # rebuild results/ from committed runs, no model calls
uv run daydreamd dream <folder> --kind obsidian   # product: one night over a corpus -> morning.md
uv run daydreamd review morning.md                 # ticked boxes -> ~/.daydreamd/verdicts.jsonl
uv run daydreamd skill                             # -> SKILL.md + ~/.daydreamd/learnings.md
uv run daydreamd mcp                               # MCP server over stdio (mcp extra)
uv run daydreamd schedule install --path <folder>  # nightly launchd/cron job
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
| `src/daydreamd/backends/` | `Completion` protocol; `claude_cli.py` is the default (with a usage-window circuit breaker); `ollama.py` and `openrouter.py` are the non-Anthropic writer families for v0.2 |
| `src/daydreamd/core/run.py` | `RunDir`, `metadata.yaml`, prompt loading + hashing |
| `src/daydreamd/core/sampler.py` | `Unit` records (with `writer_family` and `note_kind`); arms S0/S1/B1/B3/B6/B7/B4; B4 selects `bridge`, `all`, `bridge+filler` (v0.3) or a random n; labels planted/decoy/random/partner |
| `src/daydreamd/core/generator.py` | one frozen prompt for every pair arm; single units use `generate_single` or the file named by `arms.B4.prompt` (v0.3: `generate_single_strict`), SHA recorded under that name; `NONE` handling |
| `src/daydreamd/core/critic.py` | binary keep/kill with reason; `models.critic` may be a list, the first is primary (`critic.jsonl`), each writes `critic_<alias>.jsonl` |
| `src/daydreamd/core/dupgate.py` | retrieval-based corpus-novelty gate (cosine > 0.85) |
| `src/daydreamd/core/match.py` | grounded gold match + cosine to gold |
| `src/daydreamd/core/blind.py` | owner-blind pack, sealed key, unseal |
| `src/daydreamd/core/stats.py` | tables T1..T9 (synthetic; T9 = single-note abstention by note kind), DECISION.md (v0.1 rule, v0.2 rule, or the v0.3 rule with the filler-abstention precondition when the config says `prereg: v0.3`), H1..H4 (owner-blind) |
| `src/daydreamd/synth/` | spec loader (v0.2 fields: `forbidden_phrases_a/b`, `one_side_test`), 6-gram leakage check, paraphrase-leak judge (`prompts/leak_judge.md`, bridge notes, oblique specs only), note writer with writer families by parity |
| `src/daydreamd/eval/recovery.py` | enrichment (B1/B3/B6/B7), recall, specificity, per-critic comparison, recall by writer family, exploratory finds |
| `src/daydreamd/product/` | the product front door: `dream.py` (cache, sampler policy, critic with learnings, morning.md), `morning.py` (render and parse), `review.py`, `skill.py`, `schedule.py`, `mcp_server.py`, `paths.py` (`~/.daydreamd`, override `DAYDREAMD_HOME`) |
| `src/daydreamd/core/embed.py` | `StaticEmbedder` (model2vec, product default, no PyTorch), `Embedder` (MiniLM, research runs, `research` extra), `FakeEmbedder` (tests); `make_embedder(kind)` |
| `prompts/*.md` | versioned prompts; header comment carries version and role; `critic_with_learnings.md` is the product critic once the owner has reviewed something |
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
   The same applies to `experiments/micro-v0.2/config.yaml`, `prompts/leak_judge.md` and
   `data/synth/v0.2/` once `PREREGISTRATION-v0.2.md` is sealed.
6. **Private runs stay private.** `experiments/runs/private/` and `data/private/` are gitignored.
7. **No estimates in tables.** Cost and token columns come from logged usage only.
8. **Writer families are fixed by parity, never by hand.** `assign_writers()` decides which
   family writes which note; the exact model id per note is read back from the provider and
   recorded in `manifest.json` (`writer_model_id`). A writers file with a `TBD` model is refused.
9. **Several critics judge the same generations.** Only the first (primary) critic feeds dupgate
   and the main tables; the others exist so T8 can compare them. Never swap the primary after
   a run without a logged deviation.
10. **Product runs never touch the corpus.** `daydreamd dream` reads notes, writes `morning.md`
    and `~/.daydreamd/`, nothing else. Endorsed dreams go into a SKILL.md, never back into the
    notes (ADR-009). The critic's kills stay visible in morning.md (research/06, research/07).

## Conventions

- Python 3.12, `uv`, ruff (line length 100, E501 delegated to the formatter), typed signatures.
- Small functions, one module per stage, no hidden global state; every stage is re-runnable
  from its inputs on disk.
- No em dashes in any prose or docstring. Plain words over jargon.
- Tests run offline with the `fake` backend and `FakeEmbedder`; anything needing a real model
  is a smoke test, not a unit test.
- Commit messages: imperative mood, one change per commit.
