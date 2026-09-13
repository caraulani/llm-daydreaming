# ADR-013: v0.1 runs over a synthetic corpus with planted ground truth

**Status:** Accepted, 2026-09-13. Scopes ADR-001 for the first experiment only.

## Context

Three problems with running the first experiment over the owner's private memory: privacy (36 of 73 files contain secrets or personal details, and the dreams would expose project names and plans), reproducibility (nobody else can rerun it), and ground truth (the owner's KEEP decisions are the right usefulness signal, but they do not tell us whether the pipeline recovered structure that was actually there).

A synthetic corpus solves all three. If the bridges are written by hand before any note exists, recovery of a planted bridge is a fact, not an opinion.

## Decision

v0.1 runs over `data/synth/v0.1/`: 60 LLM-written markdown notes describing the work of a fictional solo builder, into which 12 hand-authored cross-domain bridges are hidden (each bridge is a real connection between two notes whose surface topics differ), plus 6 decoy pairs (note pairs that share surface vocabulary but have no bridge). The bridges and decoys are authored by the experimenter, with Claude as a disclosed writing assistant, and are fixed under the preregistration seal before the notes are generated; the notes are written by a model instructed to express each bridge's two halves without stating the bridge. A 6-gram leakage check confirms no note contains any six-word run of a gold connection or gold implication; notes that fail are regenerated. `gold.json` lists the planted pairs. The corpus is released under CC BY 4.0 with a datasheet.

Primary v0.1 metric: recovery rate of planted bridges per arm (a dream whose sources are a planted pair and whose `connection` the critic accepts), against the decoy false-positive rate and the B1 random-pairing baseline, with the ADR-006 permutation null.

## Consequences

- v0.1 measures recovery of planted structure, not real-world novelty. The paper says so in the abstract.
- Shared-imagination risk: the notes were written by a model, and the generator may be the same model family, which could inflate recovery. Mitigation in v0.1: report which model wrote the notes and which generated the dreams (see `docs/contamination.md`). Mitigation in v0.2: regenerate the notes with a second model family and rerun.
- Owner-blind KEEP / KNOWN scoring over a private corpus (ADR-005, `docs/human-eval-protocol.md`) is unchanged in design but moves to Track C, a later version.
- Anyone can rerun v0.1 with no private data and no owner. That is the point.

## Sources

- ADR-001, ADR-005, ADR-006.
- Shared Imagination, arXiv:2407.16604 (models hallucinate alike).
- Co-Scientist and Penadés, Cell 188:6654 (2025): ground truth that exists in no corpus, the design this imitates by construction.
