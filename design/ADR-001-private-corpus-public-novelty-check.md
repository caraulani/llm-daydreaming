# ADR-001: Generate from a private corpus, check novelty against public literature

**Status:** Accepted, 2026-07-24. Confirmed 2026-09-13.

## Context

Every serious idea-generation system runs on published literature: SciMON, ResearchAgent, Nova, Chain-of-Ideas, MOOSE-Chem, Deep Ideation, BioDisco, Co-Scientist, FARS, Alien Space, SciMuse. SciMuse personalises, but from the researcher's published record. Zero literature-based-discovery papers touch personal corpora; an arXiv search for "personal informatics" AND "large language model" returned no hits in July 2026. The refresh of 2026-09-13 found the gap still open. Discovery by Dreaming (arXiv:2607.16256) recombines over public OpenAlex and LMSYS data.

The obvious objection: a private corpus destroys the field's only credible evaluation, because you cannot do future-paper matching on ideas nobody else can see.

## Decision

Generation runs over the owner's private corpus. Novelty checking and temporal validation run against public literature. Novelty-vs-corpus is a retrieval check inside the private corpus; novelty-vs-world is a retrieval check against a public index.

## Consequences

- The system needs two indexes: the private corpus (local embeddings) and a public literature index (Semantic Scholar, arXiv, or web search).
- The owner is the ground-truth judge for usefulness, which is the only setting where a competent human ground truth is free (see ADR-002).
- Generalisation claims require more than one owner. Until a multi-owner study exists, every result is "a single-owner case study".
- Contamination: the generator may have seen the owner's public writing. Every run carries a contamination statement (`docs/contamination.md`).

## Sources

- BRIEF.md, SETTLED POSITION and POSITIONING sections.
- HindSight, arXiv:2603.15164. CKM, arXiv:2604.12243. MOOSE-Chem, ICLR 2025.
- Discovery by Dreaming, arXiv:2607.16256 (public corpora only).
