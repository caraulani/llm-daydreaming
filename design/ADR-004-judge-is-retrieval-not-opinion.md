# ADR-004: Novelty is a retrieval and entailment check, never an LLM opinion

**Status:** Accepted, 2026-07-24. Strengthened 2026-09-13.

## Context

HindSight (arXiv:2603.15164) found LLM-judged novelty negatively correlated with anticipating real future research (rho = -0.29, p < 0.01). RQ-Bench (arXiv:2606.12071) named the "novelty mirage": judges rate model-generated questions as highly novel while experts prefer author-anchored ones. RINoBench (arXiv:2603.10303, 1,381 expert-judged ideas) found automated novelty metrics do not reliably match expert judgment. Ideation Arena (arXiv:2608.29696) measured 72.56% judge-expert alignment. In October 2025, GPT-5 was publicised as solving open Erdős problems; it had located existing literature solutions.

The founding brief's first rubric included "novel vs the world (recall probe)", which is exactly the LLM-opinion judge these results discredit. The adversarial review of 2026-09-13 flagged it.

## Decision

Novelty-vs-corpus: embed each survivor's `connection`; if cosine similarity to any existing concept card or note chunk exceeds the preregistered threshold (0.85 in v0.1), mark "already in corpus" and kill. Novelty-vs-world: retrieval over a public literature index, reported as nearest-neighbour similarity with a threshold, plus the ADR-012 classification per hit. Retrieval traces are published. The LLM's role in judging is limited to verifying grounding (does the mechanism follow from the two claims) and running a binary coherence critic. It never votes on novelty.

## Consequences

- The judge slot that "scores novelty" is deleted from the architecture.
- The owner's blind KEEP / KNOWN decisions are the primary ground truth for usefulness (ADR-005).
- Track A hit detection is retrieval over post-cutoff literature plus an entailment matcher between two in-context texts, never recall.

## Sources

- BRIEF.md, FORCED DESIGN CHANGE and CLAIM DISCIPLINE sections.
- HindSight arXiv:2603.15164; RQ-Bench arXiv:2606.12071; RINoBench arXiv:2603.10303; Ideation Arena arXiv:2608.29696.
