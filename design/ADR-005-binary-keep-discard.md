# ADR-005: Ground truth is binary keep or discard, never a Likert scale

**Status:** Accepted, 2026-07-24.

## Context

Expert agreement collapses at fine granularity. LLM judges score 43% to 53% self-consistency on 1-to-10 scales against 50% for random. The founding brief's primary curve, "usable-idea yield = novelty x feasibility", implied two graded scores, which contradicts the binary rule. The CHI 2024 study by Strömel et al. (N = 273) moved engagement, attention and reward, and got a flat null on insight (F(2,270) = 0.43, p = .64): self-report cannot separate enjoyment from insight.

## Decision

Every human verdict is two binary marks per item: KEEP (I would act on this or write it down) and KNOWN (I already had this thought). Yield per arm or per band is P(KEEP and not KNOWN and not already-in-corpus). No scale, no "did you like it", no "huh" moments as a success criterion. An internal score may exist for triage only, never as a fitness function for iteration.

## Consequences

- The blind-scoring pack is markdown checkboxes, two per item.
- Intra-rater consistency is measured by repeating 30 items across two sittings and reporting kappa.
- The v0.1 success criterion is a discrimination statistic (see `PREREGISTRATION.md`), not a feeling.

## Sources

- BRIEF.md, UPDATED EXPERIMENT MATRIX (selection rule) and SOBERING FACT sections.
- Strömel et al., CHI 2024.
