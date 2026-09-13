# Contributing to daydreamd

Thanks for looking. This is a solo research project with a published protocol, so contributions are welcome in a specific shape. Read this before opening anything.

## The one rule: issue first

Open an issue before you write code. Say what you want to change and why. Wait for a reply (target: within 7 days) before starting. Pull requests that arrive without a prior issue are closed, with two exceptions: typo fixes, and replication runs (see below).

This rule exists because most of the value of this repo is the preregistered protocol and the committed results. A change that looks harmless can invalidate a table.

## Extensions live outside core

Core is `src/daydreamd/core/` and `src/daydreamd/eval/`. It changes rarely and only after an ADR in `design/`.

Everything else extends through interfaces:

- New corpus source: implement the `Adapter` protocol. Publish it as your own package (`daydreamd-<source>`), and open an issue so we link it. Adapters land in-tree only when `ROADMAP.md` lists them.
- New model backend: implement the `Backend` protocol. Same policy.
- New sampler or critic: run it as a new experiment arm under `experiments/`, with a config and a run script, and report it as a replication. If the result holds up we discuss promoting it.

See `docs/extending.md` for the protocols and a worked example.

## Adding an adapter (in-tree, roadmap items only)

1. Issue titled `adapter: <source>` using the template.
2. One module under `src/daydreamd/adapters/<source>.py` implementing `Adapter`.
3. A fake-backend test under `tests/adapters/` that ingests a fixture and checks the document count and the secret-stripping pass.
4. A page under `docs/adapters/<source>.md`: what becomes one document, where output lands, what gets stripped.
5. `CHANGELOG.md` entry under Unreleased.

## Submitting a replication run

You ran the protocol in `PREREGISTRATION.md` on your own corpus. We want it, positive or null.

1. Open an issue with the replication template. Fill in the results table.
2. Open a PR adding one directory: `experiments/runs/<YYYY-MM-DD>_<model-snapshot>/` containing
   - `metadata.yaml`: corpus description (no text), arms, pair counts, every model snapshot ID with access date, sampling parameters, prompt file SHAs, rater description, deviations from the preregistration.
   - `raw_outputs.jsonl`: every generation, critic, and gate decision. If the corpus is private, redact the `connection` and `mechanism` fields to their SHA-256 and keep every label, band, and verdict. Aggregates must still be recomputable.
   - `verdicts.jsonl`: the blind KEEP / KNOWN decisions with the unsealed key.
   - `cost.json`: tokens and cost per arm, read from logs.
3. `make reproduce` must regenerate your table from those files with no API key.

Model snapshot IDs must be immutable IDs, never aliases. `claude-sonnet-4-6` is an alias; use the dated snapshot your backend reports.

## Submitting a registry entry

See `registry/README.md`. Short version: one directory per entry, an OpenTimestamps proof on `dreams.jsonl`, PR-based, CC BY 4.0.

## Changing a prompt

Prompts are versioned artifacts. Every file under `prompts/` has a version header. Bump it, and note in `CHANGELOG.md` which experiment arms the change affects. Results produced with an older prompt version are not overwritten; they are kept and the new run is added beside them.

## Agent-generated pull requests

Pull requests written by AI coding agents are fine if a human read every line and can explain every change. State it in the PR template. We close PRs that:

- touch files unrelated to the issue,
- rewrite formatting across files they did not need to change,
- add abstractions "for later",
- change numbers in `results/` without a run directory that regenerates them,
- arrive without the prior issue.

Agent-generated issues that do not describe a reproducible problem are closed without reply.

## Style

- Python: `ruff` clean, type hints on public functions, no bare `except`.
- Prose (docs, ADRs, paper): short sentences, concrete numbers, no em dashes.
- Never commit corpus text, dreams, or secrets. CI runs gitleaks on every push and pull request; do not rely on it.

## Developer certificate of origin

Sign off every commit (`git commit -s`). By signing off you certify the [Developer Certificate of Origin 1.1](https://developercertificate.org/): you wrote the change or have the right to submit it under the license of the path it lands in (see `LICENSING.md`).

## Running locally

```bash
uv sync --all-extras
DAYDREAMD_BACKEND=fake uv run pytest -q
uv run ruff check .
make reproduce
```

Real runs need a backend. The default is the `claude` CLI in headless mode; see `README.md`.
