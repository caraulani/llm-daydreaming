# ADR-010: Local-first, bring your own key, local embeddings, no telemetry

**Status:** Accepted, 2026-07-24. Non-negotiable.

## Context

The corpus is a person's accumulated private thinking. "Your notes never leave your machine" has to hold for the embedding step too, not only for storage, or the promise is hollow. Napkin, the most connection-forward PKM product, shut down; trust in what a tool does with your notes is part of why people run one at all.

## Decision

- Corpus is read from local paths only.
- Embeddings are computed on-device with a small sentence-transformer.
- The only network calls are to the model backend the user configured (ADR-011), under their own key or account.
- No telemetry, analytics, or crash reporting. Ever.
- Private runs live under gitignored paths, and no command in the repo publishes them.
- Ingest strips files that match secret patterns before anything is embedded or sent.

## Consequences

- A privacy miss is a security bug (see `SECURITY.md`).
- Fully offline operation must be possible via a local model backend.
- Published artifacts from private runs are aggregates, redacted raw outputs (hashes in place of text), and owner-approved examples only.

## Sources

- BRIEF.md, daemon spec and Risks (privacy optics).
