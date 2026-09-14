# ADR-014: A planted bridge is accepted only if one side alone does not yield it

**Status:** accepted 2026-09-14, applies from corpus v0.3.

## Context

Two preregistered runs on synthetic corpora (v0.1, v0.2) supported the selection step (H1 in both: the generator answers on planted pairs and abstains or is killed on decoys) and failed to demonstrate recombination. In v0.2 the single-note arm recovered 8 of 16 planted mechanisms against 6 of 16 for the two-note oracle, and the exploratory control X5 showed the single-note prompt answers on every filler and decoy note even with NONE permitted. The adversarial review (`research/07`) read all eight single-note recoveries: each is a general principle (regression to the mean, sampling interval versus event duration, a device step, relative schedule drift) read off one note's full ingredient set. The paraphrase-leak judge passed those notes because it models a naive reader; the generator is not one. Only two v0.2 bridges (br09, sequential identifiers across supposedly independent entities; br17, expectation-lag dropout at the third cycle) required both sides, and the pipeline missed both.

## Decision

From v0.3, a bridge enters the answer key only if all of the following hold at build time:

1. **One-side generator test.** The generator itself, given either side's cards alone under a NONE-permitted prompt whose abstention gate is shown to work on fillers, does not produce an output the match judge accepts as the gold mechanism. Two votes from the match judge. A bridge that fails on either side is rewritten or dropped; it is never kept.
2. **Fact, not principle.** Each side's ingredients are specific facts about this builder's situation (an identifier pattern, a dated event, a measured number) rather than instances of a named principle a model would state from one cue. br09 and br17 are the template.
3. **Decoys mirror the accepted bridges' shapes** (unchanged from v0.2).

The single-note arm keeps its role as the incubation control, but its abstention behaviour is reported on fillers in every run, so a "recall" from one note is interpretable.

## Consequences

- Recovery numbers will fall; that is the point. A corpus whose bridges pass the one-side test measures recombination rather than pattern recognition.
- Corpus construction costs more calls (two generator calls and two judge calls per bridge side).
- The finding that principle-type bridges are one-note recoverable is reported in the paper as a property of synthetic ground truth, and is one reason the next headline experiment moves to execution-verified findings on real repositories (`research/05`), where ground truth does not depend on what a model already knows.

## Sources

`research/06`, `research/07`, `results/public/2026-09-14_micro_v0_2/`, `results/public/2026-09-14_x5_single_note_all/`, Chen, Zhao and Cohan (arXiv:2607.01233) on LLM over-production of bridge-like syntheses.
