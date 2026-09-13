# ADR-012: Every hit is classified on Tao's Erdős taxonomy before it is called novel

**Status:** Accepted, 2026-07-24.

## Context

Terence Tao's community ledger for AI contributions to Erdős problems classifies each as: 1(a) AI-independent with no comparable literature; 1(b) AI solution with literature found afterwards; 1(c) AI building on known literature; 1(d) AI plus human; 2(a) literature search; 2(b) formalisation; 2(c) rewriting; 2(d) computation. The cautionary case: in October 2025 GPT-5 was publicised as solving about 10 open Erdős problems; it had located existing solutions in the literature. Tao's read: AI is "becoming capable enough to pick off the lowest hanging fruit, precisely the category most likely to have been solved in the literature already."

## Decision

No dream is called novel in any published artifact until it carries a taxonomy class, assigned after the ADR-004 retrieval checks, and the retrieval trace is published beside it. Only 1(a) and 1(b) may be described as novel; 1(b) must name what was found afterwards.

## Consequences

- `dreams.jsonl` and registry entries carry a `claim_class` field.
- The paper reports counts per class, not a single "novel ideas" number.
- A personal corpus is a long tail of under-examined material, which is where Tao expects the capability trend to pay off; that is the framing, not a result.

## Sources

- BRIEF.md, CLAIM DISCIPLINE section.
- github.com/teorth/erdosproblems wiki.
