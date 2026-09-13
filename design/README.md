# Architecture decision records

One file per load-bearing decision. Each record has Status, Context, Decision, Consequences, and Sources. A record is never edited after acceptance; a later record supersedes it and both say so.

The first thirteen records were derived from the founding brief (`~/Desktop/I/dreaming/BRIEF.md`, v3, 2026-07-25) and the adversarial review of 2026-09-13. They are the positions that were decided by default so that future work does not re-litigate them.

| ADR | Title | Status |
|---|---|---|
| [001](ADR-001-private-corpus-public-novelty-check.md) | Generate from a private corpus, check novelty against public literature | Accepted |
| [002](ADR-002-selection-engine-not-generator.md) | The contribution is selection, not generation | Accepted |
| [003](ADR-003-generator-may-say-none.md) | The generator is permitted to output NONE, with structured output | Accepted |
| [004](ADR-004-judge-is-retrieval-not-opinion.md) | Novelty is a retrieval and entailment check, never an LLM opinion | Accepted |
| [005](ADR-005-binary-keep-discard.md) | Ground truth is binary keep or discard, never a Likert scale | Accepted |
| [006](ADR-006-stimulus-control-vs-statistical-null.md) | Stimulus control is random pairing; the statistical null is label permutation | Accepted |
| [007](ADR-007-old-cutoff-generator-track-a.md) | Track A uses an old-cutoff generator with a 6-month margin, inherited not claimed | Accepted |
| [008](ADR-008-sampler-anchor-plus-remote.md) | Default sampler is anchor plus remote; banded distance is an ablation | Accepted |
| [009](ADR-009-writeback-segregated-with-lineage.md) | Writeback is segregated, unverified until endorsed, with lineage | Accepted |
| [010](ADR-010-local-first-no-telemetry.md) | Local-first, bring your own key, local embeddings, no telemetry | Accepted |
| [011](ADR-011-headless-claude-default-backend.md) | Default backend is headless `claude -p`; generators are pluggable | Accepted |
| [012](ADR-012-claim-discipline-erdos-taxonomy.md) | Every hit is classified on Tao's Erdős taxonomy before it is called novel | Accepted |
| [013](ADR-013-synthetic-corpus-with-planted-bridges.md) | v0.1 runs over a synthetic corpus with planted ground truth | Accepted |

To add one: copy the format, number it, open an issue first (see `CONTRIBUTING.md`).
