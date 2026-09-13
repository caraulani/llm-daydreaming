# Contamination statement

Every run directory under `experiments/runs/` contains a `CONTAMINATION.md` built from this template. A run without one is not citable. Fill every field; write "unknown" where it is unknown, never leave a field blank.

## Template

```markdown
# Contamination statement: <run id>

## Models
| Role | Snapshot ID (immutable) | Stated training cutoff | Access date | Provider |
|---|---|---|---|---|
| note writer (synthetic corpora only) | | | | |
| concept-card extractor | | | | |
| generator | | | | |
| critic | | | | |
| entailment / hit matcher | | | | |

## Corpus
- Corpus: <name, version, manifest SHA-256>
- Date range of the content: <earliest, latest>
- Corpus origin: <human-written private / human-written public / model-written synthetic>
- For public corpora: could the generator have seen these texts in training? <yes / plausibly / no, with reasoning and the cutoff comparison>
- For private corpora: does the owner publish (blog, X, LinkedIn, talks) on the same topics? <yes / no> If yes, estimate the share of notes with a public counterpart, and list the channels.
- For synthetic corpora: which model wrote the notes, and is it the same family as the generator? <state both IDs> Leakage check result: maximum cosine similarity between any planted bridge and any note chunk = <value>, threshold = <value>.

## Prompts
- Prompt files and SHAs: <generator, critic, extractor, note writer>
- Did any prompt contain examples drawn from the corpus? <yes / no>

## Track A only
- Generator cutoff minus corpus window start: <months>. Must be at least 6 (ADR-007).
- Hit-detection index: <source, snapshot date>
- Were any hits found in documents the generator could have seen? <count, listed>

## Other leakage paths considered
- Embedding model training data overlap: <model, note>
- Reused runs: were any outputs cached from an earlier run with different settings? <yes / no>
- Human raters: did any rater see arm labels, the key, or other raters' verdicts before scoring? <yes / no>

## Statement
<Two or three sentences, plain language, stating what this run's results can and cannot be attributed to given the above.>
```

## The synthetic case (v0.1)

The v0.1 corpus is model-written (ADR-013). Two contamination paths matter:

1. **Shared imagination.** If the note writer and the generator share a model family, the generator may find the planted bridges easier than it would in human prose, because both models draw the same associations. The statement must name both snapshot IDs. The v0.2 rerun with a second model family bounds the effect.
2. **Leakage of the bridge into the notes.** If a note states its bridge outright, recovery is retrieval, not recombination. The build script's leakage check (bridge text against every note chunk, maximum similarity below the corpus-duplicate threshold) is reported in the datasheet and repeated here.

The hand-authored bridges are not in any model's training data because they were written for this corpus in September 2026. State that, with the authoring date.

## The private case (Track C)

The owner's notes overlap their public writing, which may be in the generator's training data. Estimate the overlap, name the channels, and add the Co-Scientist-style check where possible: three to five questions whose answers the owner knows but has never written anywhere, scored the same way.
