# Preregistration: daydreamd v0.1 planted-bridge recovery experiment

**Status: FROZEN before any generation run.** The SHA-256 of this file is committed to git and stamped with OpenTimestamps before the first call to any language model in this experiment (see "Sealing"). Any later edit to any section above "DEVIATIONS" is a deviation and must be logged there with a reason and a date.

Template: OSF Preregistration, open-ended form. Written 2026-09-13.

---

## 1. Title

Can a generate-then-select pipeline recover planted cross-domain connections in a private-style note corpus, and does distance-forced pair sampling surface them more often than random pairing?

## 2. Authors

Julian Caraulani (caraulani@gmail.com). Design assistance from Claude Fable 5.1 (Anthropic), disclosed in `paper/CHECKLIST.md`.

## 3. Study type

Computational experiment with synthetic ground truth. No human participants. No human rating in v0.1. Owner-blind rating over a real private corpus is deferred to Track C (Section 13).

## 4. Background and motivation

The founding brief (`research/BRIEF-v3-2026-07-25.md`) and the adversarial review (`research/02-sanity-review-2026-09-13.md`) agree on one thing: generation is cheap and selection is the wall. Prior systems that generate connections over a corpus (Gwern's day-dreaming loop, idea-mill, Vault Daydream, zby/DayDreamingDayDreaming) report no measurement of whether their pipelines find connections that are actually there. LLM-judged novelty is known to be unreliable (HindSight, arXiv:2603.15164, reports ρ = −0.29 between LLM-judged novelty and later real research; RQ-Bench, arXiv:2606.12071, and Ideation Arena, arXiv:2608.29696, report the same direction).

Before any claim about real-world usefulness, the pipeline must pass a recovery test with a known answer key. This experiment plants a small number of connections in a synthetic corpus and measures whether the sampler surfaces the planted pairs and whether the generator plus critic recovers the planted mechanism while declining to invent connections where none was planted.

## 5. Hypotheses (pre-committed)

- **H1 (generator and critic recover planted structure).** On the oracle set S0, recall on planted pairs exceeds the false-positive rate on decoy pairs. Test: Fisher exact, one-sided, α = .05.
- **H2 (distance-forced sampling enriches planted pairs).** Arm B3 and/or arm B6 include more planted pairs in their sampled set than arm B1 (random pairing) does. Test: hypergeometric base rate for each arm plus a 10,000-shuffle permutation test on the B3 vs B1 and B6 vs B1 differences, α = .05, one-sided.
- **H3 (recombination beats single-note reflection).** Recall of planted mechanisms in arm B4 (single-note reflection over the 24 bridge notes) is below recall in the pair arms on the same bridges. Test: Fisher exact, one-sided, α = .05.

**Decision rule.** "Signal" is declared if and only if H1 and H2 both pass. Any other outcome is reported as a null result, in full, with the same tables.

## 6. Corpus

**Synthetic private-style corpus, committed and public.** Sixty markdown notes written by a language model in the voice of one fictional solo builder, across six domains (ten notes per domain), each 150 to 300 words, in the style of memory notes (a project fact, a lesson, a plan). The corpus, its manifest with per-file SHA-256, and the answer key `gold.json` are committed to `data/synth/v0.1/` and are public.

**Planted bridges (12).** Each bridge is a pair of notes in two different domains that carry, obliquely, the ingredients of one hidden mechanism. For each bridge the answer key holds a `gold_connection` (at most 40 words) and a `gold_implication`. Both are authored by the experimenter before any run, with Claude as a disclosed writing assistant, and are fixed in `data/synth/v0.1/bridges.yaml` under the seal (Section 15). They are never produced by the note-writer call or by the pipeline's generator. The notes themselves are drafted by a language model from a per-note spec that lists the ingredients to include and forbids naming the mechanism or the partner domain; the experimenter may edit a note so that the ingredients are present but the connection is not stated.

**Decoy pairs (6).** Pairs of notes in different domains that share vocabulary but carry no mechanism. A correct pipeline outputs NONE on these.

**Filler notes (36).** Notes with no planted role. Sixty notes total: 24 bridge notes, 36 filler. Decoys are drawn from the filler set.

**Leakage check.** No 6-gram of any `gold_connection` may appear in any note. The check is run by `make leakage-check` and its output is committed. A failure is fixed by editing the note, and the corpus manifest is regenerated before freezing.

**Freezing.** The corpus is frozen when its manifest SHA-256 is recorded in `data/synth/v0.1/MANIFEST.sha256` and committed. Generation runs read only the frozen corpus.

## 7. Design

### 7.1 Concept cards

One card-extraction pass per note with the model alias `haiku` (exact snapshot ID recorded from the run log). Schema:

```
{id, source_note, claim (≤30 words, atomic), entities[], why_it_matters (≤20 words), confidence: high|med|low}
```

Three to six cards per note. Card fidelity is not human-rated in v0.1 (synthetic corpus); the card text is committed so anyone can rate it.

### 7.2 Embeddings

`sentence-transformers/all-MiniLM-L6-v2`, run locally, over the note text (for pair sampling at note level) and over card `claim` text (for the duplicate gate). Cosine distance. Pairs within the same note are excluded. The number of cross-note pairs is 60 × 59 / 2 = 1,770, of which 12 are planted.

### 7.3 Arms

| Arm | What is sampled | N | Purpose |
|---|---|---|---|
| S0 | Oracle set: 12 planted pairs + 6 decoy pairs + 42 random non-planted cross-domain pairs, labels hidden from the pipeline | 60 | Tests generator plus critic independent of any sampler |
| B1 | Random cross-note pairs, uniform | 100 | Sampler control |
| B3 | Banded by quantile of the cross-note cosine-distance distribution: Q1 (near), Q2 to Q3 (mid), Q4 (far), top 5 percent (tail); 25 pairs per band | 100 | Distance-forced sampling |
| B6 | Anchor from the densest embedding cluster plus one remote note from Q4 | 50 | Uzzi-style conventional core plus one atypical element |
| B4 | Single-note reflection over each of the 24 bridge notes, no pairing | 24 | Incubation control: can the mechanism be produced from one side alone |

All pair arms use the same generator prompt. B4 uses the single-note prompt. Prompts are committed verbatim in `prompts/` and their SHA-256 is recorded in every run's metadata.

### 7.4 Generator

Model alias `sonnet`, exact snapshot ID recorded from the run log, default temperature. Prompt contract: most pairs are unrelated; if no genuine, non-obvious connection exists, output exactly `NONE`; otherwise output JSON with fields `connection` (≤40 words), `mechanism`, `testable_implication`, `needs`. No restating of either claim. No facts absent from the inputs.

### 7.5 Critic

Model alias `haiku`, binary. Kill if the output restates a claim, if the implication is not checkable, or if the connection is generic. Kill rate is reported per arm.

### 7.6 Duplicate gate

Embed each surviving `connection`; if cosine similarity to any card claim or note chunk exceeds 0.85, mark "already in corpus" and remove. Rate reported per arm.

### 7.7 Recovery judge

For each generation on a planted pair, a binary grounded-entailment judgment: does the generated `connection` plus `mechanism` state the same mechanism as `gold_connection`? Model alias `haiku`, with the gold text in context, output `MATCH` or `NO_MATCH`. Cosine similarity between generated `connection` and `gold_connection` is reported alongside, never used as the criterion. The judge prompt is committed verbatim. The judge never sees the arm label.

## 8. Variables and measures

- **Sampler enrichment.** For each pair arm: number of planted pairs in the sampled set, against the hypergeometric expectation for that arm's N drawn from 1,770 pairs with 12 planted.
- **Recall on planted pairs.** A planted pair counts as recovered if the generator output is non-NONE AND the recovery judge returns MATCH. Reported per arm as a proportion with a Wilson 95 percent interval.
- **Specificity.** NONE rate on decoy pairs and on random non-planted pairs, per arm.
- **False-positive rate after critic.** Proportion of decoy pairs on which a non-NONE output survives the critic and the duplicate gate.
- **B4 recall.** Proportion of the 12 mechanisms recovered from either bridge note alone (MATCH on gold). Expected near zero.
- **NONE rate by distance band** (arm B3).
- **Cost.** Input and output tokens, and USD at list price, per arm and per recovered bridge, read from run logs. No cost number is published that is not read from a log.
- **Exploratory finds.** Non-NONE outputs on non-planted pairs that survive critic and duplicate gate. Reported separately as a count and released as text. Never counted as hits.

## 9. Sampling plan and power

With 12 planted pairs and 6 decoys in S0, H1 compares recall on 12 items to false positives on 6 items. Fisher exact with these sizes detects a difference of roughly 8 of 12 recovered versus 0 or 1 of 6 false positives at α = .05. Smaller effects will not reach significance and will be reported as such. For H2, arm B1 with N = 100 expects 100 × 12 / 1,770 = 0.68 planted pairs; arm B3 and B6 enrichment is tested against that base rate and against permutation. For H3, B4 recall on 12 mechanisms is compared with pair-arm recall on the same 12.

The sample sizes are fixed by the corpus design and are not increased after seeing results. If any arm produces zero non-NONE outputs, that is reported as the result.

## 10. Analysis plan

1. `make reproduce` regenerates every table from committed raw outputs without API access.
2. H1: Fisher exact, one-sided, on the 2 × 2 table (planted recovered / not, decoy false positive / not) for S0.
3. H2: for B3 and B6, hypergeometric survival probability of observing at least the found number of planted pairs; plus permutation: shuffle the planted labels across the 1,770 cross-note pairs 10,000 times, recompute each arm's planted count, report the proportion of shuffles at or above the observed count. Report both.
4. H3: Fisher exact, one-sided, B4 recall versus the best pair arm's recall on the same 12 bridges.
5. Permutation null over S0: shuffle the planted / decoy / random labels across the 60 S0 pairs 10,000 times, recompute the recall-minus-false-positive gap, report the permutation p.
6. Wilson 95 percent intervals on every proportion.
7. Cost from logs.

## 11. Exclusion criteria

- Generator outputs that fail JSON parsing after one repair attempt are counted as NONE and logged as parse failures with their raw text.
- API errors are retried three times; a pair that still fails is excluded and listed by ID.
- No pair is excluded for its content.

## 12. What we will report regardless of outcome

Tables T1 to T6 in `paper/paper.md`, every raw output, every prompt, every model snapshot ID, the corpus, the answer key, the leakage-check output, the run logs, the cost. A null on any hypothesis is written into the abstract.

## 13. Threats to validity, stated before the run

- **Shared priors.** The notes are drafted by a language model, the bridge specs were written with a language model as assistant, and the generator is a language model of the same family; they may share associations, inflating recovery. Mitigations in v0.1: bridges and gold text are fixed under the seal before any run and are not produced by the note-writer or the generator; the leakage check; decoy pairs. Planned mitigation: a second corpus and a second set of bridges written by a different model family or by an independent human.
- **Synthetic ground truth measures recovery of planted structure, not real-world novelty or usefulness.** The abstract template below says this.
- **Judge dependence.** The recovery judge is a language model. It is given the answer and asked a grounded entailment question, which is the narrow use the literature supports; it is not asked to rate novelty. Its prompt is published and all judgments are released for inspection.
- **Single corpus, single generator.** No claim about other corpora or other models is made.

**Track C (future).** Owner-blind scoring over a real private corpus, with a sealed answer key: pool survivors, shuffle, strip arm labels, present in batches of 20; the owner marks KEEP and KNOWN as binary decisions; 30 repeated items for intra-rater kappa; key file SHA committed before scoring and revealed after. Not part of v0.1.

## 14. Pre-committed abstract template

"We plant 12 cross-domain connections in a 60-note synthetic corpus written in the style of one builder's private notes, and measure whether a generate-then-select pipeline recovers them. On the oracle set, the pipeline recovered [x] of 12 planted connections and produced [y] false positives on 6 decoy pairs (Fisher p = [p1]). Distance-forced sampling included [a] planted pairs in 100 draws against a random-pairing expectation of 0.68 (permutation p = [p2]); the anchor-plus-remote sampler included [b] in 50 draws. Single-note reflection recovered [c] of 12. The generator declined to connect [d] percent of decoy pairs and [e] percent of random pairs. Synthetic ground truth measures recovery of planted structure, not real-world novelty or usefulness; we release the corpus, answer key, prompts, raw outputs and a reproduction script so the protocol can be run on any corpus."

Claims not permitted in v0.1 text: "novel ideas", "discovers", "anticipates", any lead time, any cost headline not read from logs, "first", "benchmark", generalization beyond this corpus, any sleep-biology claim.

## 15. Sealing

1. Write this file and the answer key (`data/synth/v0.1/bridges.yaml`, `data/synth/v0.1/decoys.yaml`). Do not run any model call for the experiment before step 5. Development smoke tests on a throwaway corpus are not the experiment; they are logged under `experiments/runs/public/*_smoke/` and never enter a table.
2. Compute `shasum -a 256` of this file and of both answer-key files, and commit the three files together.
3. Stamp: `ots stamp PREREGISTRATION.md data/synth/v0.1/bridges.yaml data/synth/v0.1/decoys.yaml`; commit the `.ots` proofs. Upgrade the proofs later with `ots upgrade`.
4. Record the commit hash here after commit: `PREREG_COMMIT = 056b30e37a3e9f72e7977b190a0f7f13a22903fb` (tag `v0.1.0-prereg`).
5. Build the notes from the sealed specs (`make synth`), run the leakage check, freeze the corpus manifest (Section 6) and record `CORPUS_MANIFEST_SHA256 = 2401e2b842072ed5f71f57523c89386d95fb58d8cc7904869ed2cba9de45f2b2` (corpus sha256 f17c4f0864305f54ce92f3a3422b3ccf65acfbcd84d072ec87e334e2b8b4c571).
6. Only then run `make micro` (cards, embed, sample, generate, critic, dupgate, judge) and `make reproduce`.

**Answer-key hashes at seal time (SHA-256):**

```
8d15420e08f7ac7042b07b26e9f971d61a76bb49074cc38027bd157dd88bf8b7  data/synth/v0.1/bridges.yaml
41c1a00ec8bd06e44dc735e01424387e8b48ae4d9ebd1569dfa4c7141c53b5a1  data/synth/v0.1/decoys.yaml
68eb8523c88f2bac5e81c301cc2083f8d23cf66dfa011a1b11c045586d9ae375  data/synth/v0.1/fillers.yaml
```

The hash of this file itself is the git blob recorded by the sealed commit and by its `.ots` proof.


---

## DEVIATIONS

Format: date, section, what changed, why, who decided.

1. 2026-09-13, Section 6 (corpus). Four of the 60 generated notes are 119 to 149 words, below the 150-word floor; none exceed 300. Kept as generated because regeneration for length was not in the plan and the notes pass the leakage check. Decided by the experimenter.
2. 2026-09-13, Section 8 (measures). Recall is computed as preregistered (non-NONE AND gold match, before the critic). The run shows the critic killed three correct recoveries (S0-0005, S0-0006, S0-0011; reasons "restates_claim", "generic", "generic"), so post-critic survival on planted pairs (5 of 12) is lower than recall (8 of 12). Both numbers are reported; the analysis plan is unchanged.
3. 2026-09-13, additions after the seal (not deviations from the analysis plan, listed for completeness). Exploratory arms S1 (partner-domain filler control), B7 (cross-domain-near sampler) and generator-size configs, plus a post-hoc analysis of where planted pairs sit in the distance distribution, were written and committed while the sealed run was executing, after reading only its pre-generation artifacts (sampled units, cards, embeddings). They are reported outside T1 to T6 under "exploratory".
4. 2026-09-13, outcome. Sealed run `experiments/runs/public/2026-09-13_micro`. H1 PASS (p = 0.011), H2 FAIL (B3 p = 0.482, B6 p = 1.0), H3 FAIL (p = 0.110). Decision by the rule in Section 5: NULL.
