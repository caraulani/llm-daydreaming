# ADR-009: Writeback is segregated, unverified until endorsed, with lineage

**Status:** Accepted, 2026-07-24.

## Context

The compounding loop (endorsed dreams become concept cards and seed later dreams) is the same loop Shumailov et al. (Nature 2024) showed destroys distributional tails first under recursive self-training. Remote associations are the tails. DreamCoder is the existence proof of doing it right: it trains on fantasies and replays of real solved tasks, and every fantasy is grounded by an actual solver run.

## Decision

Generated material is never silently folded into ground truth. Dreams are stored in a separate namespace, marked unverified until the owner endorses them in a review. Every dream carries a provenance lineage (source cards, prompt version, model snapshot, run ID). A dream built on a later-rejected dream is flagged. Every cycle is anchored in fresh real inputs from the corpus.

## Consequences

- Concept cards from dreams carry `origin: dream` and are excluded from the corpus-duplicate gate's reference set until endorsed.
- Track B measures tail diversity (embedding dispersion of dreams per night) over at least 14 nights, writeback on versus off. Nobody has that curve.
- Cross-run and cross-model diversity are mandatory metrics (Argument Collapse: humans 65.3% unique arguments, LLMs 3.4%; models hallucinate alike, so multi-model ensembling is not a diversity fix).

## Sources

- BRIEF.md, Architecture (writeback risk) and CREATIVITY-SCIENCE CORRECTIONS (model collapse).
- Shumailov et al., Nature 2024. DreamCoder. Shared Imagination arXiv:2407.16604.
