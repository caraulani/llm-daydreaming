# ADR-008: Default sampler is anchor plus remote; banded distance is an ablation

**Status:** Accepted, 2026-07-24. Resolves three coexisting sampler designs in BRIEF.md.

## Context

The raw "fertile zone at intermediate distance" claim is falsified. Liu, Dubova and Griffiths (arXiv:2603.19087, 140 humans, 2,800 ideas, 7 LLMs) find distance-to-originality linear and positive with no quadratic term. Shen, Druckmann and Zou (arXiv:2605.11258) get their best results by maximising distance. Uzzi (Science 2013, 17.9M papers) is two-dimensional: high-impact work combines a conventional core with an atypical injection, and work high on both is about twice as likely to reach the top 5% of citations. Feasibility falls with distance, so usable yield (novelty and feasibility) may still be single-peaked; nobody has plotted it.

## Decision

Default sampler (B6): draw an anchor from dense, familiar territory in the embedding space and one remote element. Banded distance sampling (B3) is kept as an ablation arm and is the instrument for the yield-vs-distance curve, including the far tail above the 95th percentile of pair distances. Random pairing (B1) is the control. Pairs never come from the same source note.

## Consequences

- B6 versus B3 is an A/B inside every run, cheap.
- If the yield curve is flat or monotone, that is reported as the finding.
- Kauffman's adjacent possible is cited as framing only; it is a near-distance prior and cuts against far transfer.
- Mednick's flat-hierarchy mechanism is not cited (refuted, Benedek and Neubauer 2013).

## Sources

- BRIEF.md, design decision 3 and SAMPLER DESIGN CHANGE.
- Uzzi et al., Science 2013. Liu et al. arXiv:2603.19087. Shen et al. arXiv:2605.11258.
