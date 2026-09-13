# ADR-003: The generator is permitted to output NONE, with structured output

**Status:** Accepted, 2026-07-24.

## Context

"Find a connection between A and B" forces confabulation. An audit of 14,922 LLM explanations over personal sensor data (arXiv:2605.08590) found models "routinely attribute anomalous days to causes without sufficient support", and richer context did not reduce the overreach. Most sampled pairs from a distance-forced sampler are, in fact, unrelated.

## Decision

The generator prompt states that most pairs are unrelated and that the correct output for an unrelated pair is exactly `NONE`. Non-NONE output is JSON with four required fields: `connection` (at most 40 words), `mechanism` (why it holds), `testable_implication` (one concrete thing the owner could check or do this week), `needs` (which claim supplies what). Restating either claim, or inventing facts absent from the claims, is a critic kill.

## Consequences

- The NONE rate is logged per arm and per distance band. It is a free honesty metric per model, and it is expected to rise with distance.
- Requiring a falsifiable implication is itself a novelty filter: vague resemblance cannot produce one.
- Prompts are committed verbatim under `prompts/` with a version header and their SHA recorded in every run's metadata.

## Sources

- BRIEF.md, design decision 4.
- arXiv:2605.08590 (overreach audit).
