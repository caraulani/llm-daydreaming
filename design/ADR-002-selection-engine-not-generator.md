# ADR-002: The contribution is selection, not generation

**Status:** Accepted, 2026-07-24.

## Context

Generation is not the bottleneck. Si, Yang and Hashimoto (ICLR 2025) found 4,000 generated ideas collapse to about 200 unique ones, and that plain over-generate-and-rank already beat 100 expert researchers on rated novelty. Both prior implementations of Gwern's day-dreaming loop stopped at the verifier: Goedecke's idea-mill could not scale past what the operator could judge; zby's DayDreamingDayDreaming stated that "a domain-agnostic novelty verifier is the fundamental research bottleneck". Ríos-García et al. (arXiv:2604.18805, over 25,000 agent runs) attribute 41.4% of outcome variance to the base model and 1.5% to the scaffold. Anthropic's Schwartz ("Vibe physics", March 2026): LLMs "lack a sense of which paths might be fruitful before walking them."

## Decision

daydreamd is a selection engine for machine-generated ideas, deployed where a competent ground-truth judge is available for free: the owner of a private corpus. The generator is a commodity. The value must come from the corpus (private, unexploited) and the evaluation (grounded, null-tested), never from orchestration.

## Consequences

- The README leads with the evaluation protocol, not the daemon. The daemon is packaging.
- The experiment matrix must include a base-model axis, and the paper reports a variance decomposition. If the sampler effect is under 5% of the model effect, that is the reported finding.
- "Our ideas score higher on novelty" is never claimed. The Ideation-Execution Gap (arXiv:2506.20803) killed that framing.
- Cheap generator plus strict selection is the cost model. Cost per kept idea is a first-class metric, measured from logs.

## Sources

- BRIEF.md, THE REFRAME and THREE NUMBERS sections.
- Si et al., arXiv:2409.04109. Ríos-García et al., arXiv:2604.18805. FARS automated review inflation (5.00 vs 3.23).
