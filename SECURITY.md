# Security and privacy policy

## Reporting

Email caraulani@gmail.com with the subject line `daydreamd security`. Do not open a public issue for anything that could expose a user's corpus.

You will get an acknowledgement within 7 days. Fixes for confirmed issues are released as a patch version and noted in `CHANGELOG.md` with credit, unless you ask to stay anonymous.

## The promise this policy protects

daydreamd is local-first:

- The corpus is read from local paths only.
- Embeddings are computed on the machine (`sentence-transformers`), never sent to an embedding API.
- The only network calls are the generator, critic, and judge calls the user configured (by default, headless `claude -p` on their own account, or the API key they supplied).
- No telemetry. No analytics. No crash reporting. Nothing phones home.
- Private runs live under gitignored paths and are never published by any command in this repo.

## What counts as a privacy bug

Any of the following is a security issue, even if no attacker is involved:

- Corpus text, concept cards, dreams, or verdicts written outside the configured output directory.
- Corpus text sent to any endpoint other than the configured model backend.
- A default that sends data to a third party without an explicit config value.
- A command that adds `experiments/runs/private/`, `data/private/`, or `results/private/` to git.
- A registry entry or example that leaks secrets (API keys, passwords, tokens) from a corpus. The ingest step strips files matching a secret pattern, and a miss there is a bug.
- Prompt injection from corpus content that causes the generator or critic to take an action other than returning text.

## Model backends

The default backend runs the `claude` CLI headless. Text you dream over is sent to Anthropic under your own account's data terms. Swap the backend (see `docs/extending.md`) to run fully offline with a local model.

## Supported versions

Only the latest minor release receives fixes.
