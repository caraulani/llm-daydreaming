# ADR-007: Track A uses an old-cutoff generator with a 6-month margin, inherited not claimed

**Status:** Accepted, 2026-07-24.

## Context

Temporal holdout with an old-cutoff generator is already published: MOOSE-Chem (ICLR 2025, 51 post-January-2024 chemistry papers, pre-2024-cutoff models), HindSight (arXiv:2603.15164, Llama-3.3-70B with a June 2023 cutoff and a 6-month safety margin), BioDisco (arXiv:2508.01285). Claiming it as novel invites an easy reviewer kill.

## Decision

Track A (retrospective evaluation) uses an open-weight generator whose training cutoff predates the corpus window by at least 6 months, following HindSight. A modern model does hit matching only, as entailment between two in-context texts, with no reliance on its own memory. The inversion, freezing the model and letting the world move forward, is stated as our framing; the hygiene is cited as inherited.

## Consequences

- The generator interface must be pluggable (see ADR-011).
- Every Track A run records generator snapshot, stated cutoff, margin, and corpus date range in `metadata.yaml`.
- Report strict (mechanism matches) and loose (pair co-occurs as a topic) hit rates, always as lift over B1 and a matched-decoy null, with a false-positive rate and a Wilson interval.
- Report a lead-time distribution, not a point estimate (CKM: mean 404 days, median 399, range 66 to 757), and a future-neighbourhood rate.

## Sources

- BRIEF.md, design decision 1 and METRIC SHAPE.
- HindSight arXiv:2603.15164; MOOSE-Chem ICLR 2025; CKM arXiv:2604.12243; pArticleMap neighbourhood rate.
