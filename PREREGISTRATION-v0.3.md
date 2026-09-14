# Preregistration v0.3: bridges that need both sides

**Status (sealed 2026-09-14, tag v0.3.0-prereg): DRAFT, unsealed.** Written 2026-09-14 after the v0.2 review (`research/07-adversarial-review-v0.2-results-2026-09-14.md`) and ADR-014, before any v0.3 note or experiment call exists. When sealed, the SHA-256 of this file and of the sealed files listed in Section 15 are committed to git and stamped with OpenTimestamps before the first model call of the build; any later edit above "DEVIATIONS" is a deviation and is logged there.

Template: OSF Preregistration, open-ended form.

---

## 1. Title

Does two-note recombination recover planted connections that one note alone cannot give away, once the planted connections are built from specific facts rather than general principles?

## 2. Authors

Julian Caraulani (caraulani@gmail.com, ORCID 0009-0006-3889-3563). Design assistance from Claude Fable 5.1 (Anthropic), disclosed in `paper/CHECKLIST.md`.

## 3. Study type

Computational experiment with synthetic ground truth. No human participants. No human rating in v0.3.

## 4. Background and motivation

v0.1 (`2026-09-13_micro`): the selection step held (8 of 12 planted recovered, 0 of 6 decoys survived, p = 0.011), distance-forced sampling did not enrich planted pairs, and single-note reflection was not separated from two-note recombination. NULL by its preregistered rule.

v0.2 (`2026-09-14_micro_v0_2`): the selection step held again (6 of 16, 0 of 12 decoys, p = 0.021) and the partner-domain filler control passed, but single-note reflection recovered 8 of 16 mechanisms against 6 of 16 for two notes. SIGNAL by its rule, for a reason the rule did not test; recombination was not claimed.

The v0.2 review found that every single-note recovery was a general principle that one note's ingredient set already cued, that the pair prompt's NONE gate is real while the single-note prompt's was inert (X5: the single prompt answered on every filler note), and that only two v0.2 bridges (br09, br17) needed both sides. ADR-014 therefore changes what counts as a bridge: it is accepted only if the generator, given either side alone under a strict NONE-permitted prompt, does not produce the gold. v0.3 is the first corpus built under that rule, and H3-strict is the recombination test the v0.2 rule lacked.

## 5. Hypotheses (pre-committed)

- **H1 (selection).** On the oracle set S0, recall on accepted planted pairs exceeds the false-positive rate on decoy pairs. Fisher exact, one-sided, alpha = .05.
- **H2 (near, cross-domain sampling).** (a) B7 includes more planted card pairs than B1 at equal draws; hypergeometric survival on the full candidate pool governs, and a 10,000-shuffle arm-label permutation over the pooled B1 plus B7 units is reported alongside. (b) The generator's non-NONE rate on B7 exceeds B1 (Fisher, one-sided). Alpha = .05 each.
- **H3-strict (recombination, the test that was missing).** Recall on the accepted bridges in S0 (two notes, pair prompt) exceeds recall in B4-strict (one note, `prompts/generate_single_strict.md`) on the same bridges. Fisher exact, one-sided, alpha = .05.
- **H4 (partner-domain filler, secondary, estimation only).** S0 recall against S1 recall, reported with Wilson intervals. Explicitly not a recombination test: a mechanism-free partner makes NONE the correct answer under the pair prompt.
- **H5 (writer family, estimation only).** Recall on bridges whose notes were written by family A against family B, reported as a difference with intervals; no pass or fail.

**Validity precondition.** The single-note prompt's abstention gate must work: B4-strict must answer on fewer than 10 percent of the 24 filler notes. If it answers on 10 percent or more, H3-strict is reported as not interpretable and the run is NULL regardless of the other hypotheses.

**Decision rule.** "Signal" is declared if and only if the validity precondition holds and H1 and H3-strict both pass. Any other outcome is reported as a null result, in full, with the same tables.

## 6. Corpus

**Synthetic private-style corpus v0.3, committed and public.** Ninety-six notes in the voice of one fictional solo builder across six domains, sixteen per domain, 100 to 300 words each (the floor is enforced by the builder; longer notes are reported). `data/synth/v0.3/`, manifest with per-file SHA-256, `gold.json`.

**Planted bridges (24 specified; the accepted number is fixed at the seal).** Every ingredient is a specific fact (identifier, date, number, vendor, location, sequence; recorded as `fact_type`), never a named principle. Gold connections and implications are authored by the experimenter with Claude as a disclosed writing assistant and fixed in `bridges.yaml` under the seal. The `one_side_test` field states in two sentences what each side alone supports.

**Acceptance (ADR-014).** After the notes are written and pass the 6-gram check and the paraphrase-leak judge, the builder runs the one-side gate (`daydreamd synth --one-side-gate --gate-model sonnet`): the generator (Sonnet-class alias, exact id recorded) reads each bridge note alone under `prompts/generate_single_strict.md`; any non-NONE output is judged against the gold by the match judge (Haiku-class, two votes, a tie fails closed). A bridge with a recovered side is rewritten once by the experimenter (spec edit, that note regenerated) and gated again; a second recovery drops the bridge from `gold.json` before the seal, listed in the manifest and datasheet. The builder never edits the answer key.

**Decoy pairs (12).** All shape-matched: same `fact_type` and surface pattern as a bridge, different or absent mechanism, `why_not` recorded. A correct pipeline outputs NONE on these.

**Filler notes (24).** Four per domain, no planted role; also the abstention-check set for B4-strict.

**Note writers (two families).** Odd bridge and decoy ids and odd filler positions: `claude-haiku-4-5-20251001` (or the current Haiku snapshot, recorded). Even: `ollama/hf.co/bartowski/Qwen2.5-14B-Instruct-GGUF:Q4_K_M` (Qwen 2.5 14B Instruct, local, digest recorded per note). The 14B replaces the 7B used in v0.2, whose notes were too short and leaked by implication. Prompt `prompts/synth_note.md` version 2 for both; family A at the provider default temperature, family B at 0.7; no seed control.

**Checks at build.** 6-gram check against every gold connection and implication; paraphrase-leak judge CLEAN on every bridge note; length floor 100 words with regeneration; meta-trailer stripping; up to ten attempts per note; the one-side gate as above.

**Freezing.** The corpus is frozen when `data/synth/v0.3/MANIFEST.sha256` is written and committed. Experiment runs read only the frozen corpus.

## 7. Design

### 7.1 Concept cards, embeddings, duplicate gate

As v0.2: one Haiku-class card pass per note (exact id recorded), `sentence-transformers/all-MiniLM-L6-v2` locally over note text and card claims, cosine distance, same-note pairs excluded, duplicate gate at cosine 0.85. Notes with zero cards after one retry are recorded and excluded from note-level arms.

### 7.2 Arms

| Arm | What is sampled | N | Purpose |
|---|---|---|---|
| S0 | Oracle set: all accepted planted pairs + 12 decoy pairs + 36 random cross-domain non-planted pairs, labels hidden | accepted + 48 | Generator plus critic without the sampler; H1 |
| S1 | Each bridge note + a filler from its partner's domain | 2 x accepted | Secondary control, estimation only (H4) |
| B4-strict | Single-note reflection under `generate_single_strict` over every bridge note AND all 24 fillers | 2 x accepted + 24 | H3-strict, and the filler abstention check |
| B1 | Random cross-note card pairs, uniform | 300 | Sampler control |
| B7 | Nearest band (Q1), different domains | 300 | H2 |

Pair arms share `prompts/generate_pair.md` (NONE permitted). Prompts are committed verbatim and their SHA-256 recorded per run.

### 7.3 Generator, critics, match judge

Generator alias `sonnet` (exact id recorded), default temperature. Two critics run in parallel on every non-NONE output: the v0.1 Haiku critic prompt unchanged (primary, feeds the duplicate gate) and a Sonnet-class critic with the same prompt; both reported (T8). Match judge: Haiku-class, grounded entailment with the gold in context, `MATCH` or `NO_MATCH`, two votes per unit, a tie counts as NO_MATCH for recall (fail-closed in the direction that hurts the hypothesis). Cosine to gold reported, never used as the criterion.

## 8. Variables and measures

- Recall on accepted planted pairs per arm (non-NONE AND MATCH on a majority of two votes), Wilson 95 percent intervals.
- Decoy false positives after each critic (T8) and after the primary critic plus duplicate gate (T3).
- NONE rate per arm; within S0 per label; B4-strict answer rate on fillers (the precondition) and on bridge notes.
- Sampler enrichment for B1 and B7 against the hypergeometric base rate; permutation p.
- Recall by writer family of the first note of each unit (H5).
- Cost per arm and per recovered bridge from logs; exact model ids for every role including the gate and the note writers.
- Exploratory finds (non-planted survivors) reported separately, never counted.

## 9. Sampling plan and power

With 24 specified bridges and an expected 4 to 8 dropped by the gate, S0 carries 16 to 20 planted pairs against 12 decoys. H1: at 18 planted, Fisher detects 9 of 18 recovered against 1 of 12 decoy false positives at alpha .05. H3-strict compares S0 recall with B4-strict recall on the same 16 to 20 bridges; at 18 bridges, 9 of 18 against 2 of 18 reaches p about .03, while 9 against 5 does not, so an effect under about 35 percentage points will read as null and is reported as such. H2: B7 and B1 at 300 draws each against a base rate near 0.4 percent (about 1.2 expected planted pairs per arm); the arm-level test remains underpowered and the Q1-pool enrichment is reported alongside. The filler check: 24 fillers, threshold 10 percent means at most 2 answered.

Sizes are fixed by the corpus and are not increased after seeing results. If any arm produces zero non-NONE outputs, that is reported as the result.

## 10. Analysis plan

1. `make reproduce` regenerates every table from committed raw outputs without API access.
2. Validity precondition: B4-strict filler answer rate with Wilson interval; pass if fewer than 10 percent.
3. H1: Fisher exact, one-sided, planted recovered vs decoy survivors on S0.
4. H2a: hypergeometric survival for B7's planted count; arm-label permutation over pooled B1 plus B7, 10,000 shuffles, reported. H2b: Fisher on non-NONE rates.
5. H3-strict: Fisher exact, one-sided, S0 recall vs B4-strict recall on the same accepted bridges.
6. H4, H5: differences with Wilson intervals, no test.
7. Label-permutation null over S0: post-critic survivors among planted units vs shuffled labels, 10,000 shuffles (as T5 in v0.1 and v0.2).
8. Cost from logs. Tables T1 to T8 as in v0.2 plus T9 (filler abstention) and DECISION.md.

## 11. Exclusion criteria

- Generator outputs that fail JSON parsing after one repair attempt count as NONE and are logged with their raw text.
- API errors are retried three times; a unit that still fails is excluded and listed by id. A stage with more than 20 percent errors aborts.
- Notes the card extractor refuses (zero cards after one retry) are excluded from note-level arms and listed.
- No unit is excluded for its content.

## 12. What we will report regardless of outcome

Tables T1 to T9, DECISION.md, every raw output, every prompt, every model snapshot id (writers, gate generator, gate judge, cards, generator, both critics, match), the corpus, the answer key with the gate's per-side verdicts, the leakage outputs, the run logs, the cost. A null on any hypothesis is written into the abstract.

## 13. Threats to validity, stated before the run

- **The gate uses the same generator as the experiment.** A bridge the gate cannot recover from one side might still be recoverable by a stronger model; the claim is scoped to this generator and stated so.
- **Fact-type bridges may be easier to match by string overlap.** The match judge is asked for the same mechanism, not the same tokens; two votes; cosine reported for inspection.
- **Shared priors** across note writer, bridge author and generator remain; family B is a small open model on purpose, and H5 reports the split.
- **Synthetic ground truth measures recovery of planted structure, not real-world novelty or usefulness.** The abstract template says so.
- **Family-dependent exclusion** (v0.2 lost six of twelve family-B bridges to the leak rule). The 14B writer and the length floor are the mitigations; the family split of dropped bridges is reported.

## 14. Pre-committed abstract template

"We plant [n] cross-domain connections built from specific facts in a 96-note synthetic corpus written by two model families, accept only those that the generator cannot produce from one note alone, and measure whether a generate-then-select pipeline recovers them. On the oracle set, [x] of [n] planted connections were recovered and [y] of 12 decoy answers survived (Fisher p = [p1]). Single-note reflection under a strict abstention prompt answered on [f] of 24 filler notes and recovered [z] of [n] mechanisms, against [x] of [n] for two notes (Fisher p = [p3]). Near-in-embedding, far-in-domain sampling drew [a] planted pairs in 300 against [e] expected (p = [p2]). By the preregistered rule ([validity precondition held / failed]; H1 [pass/fail]; H3-strict [pass/fail]) the run reports [signal / no signal]. Synthetic ground truth measures recovery of planted structure, not real-world novelty or usefulness; corpus, answer key, gate verdicts, prompts, raw outputs and a reproduction script are released."

Claims not permitted in v0.3 text: "novel ideas", "discovers", "anticipates", any lead time, any cost headline not read from logs, "first", "benchmark", generalization beyond this corpus and this generator, any sleep-biology claim.

## 15. Sealing

1. Write this file and the answer key (`data/synth/v0.3/bridges.yaml`, `decoys.yaml`, `fillers.yaml`). Do not run any model call for the experiment before step 5. Development smoke tests on a throwaway corpus are not the experiment.
2. Compute `shasum -a 256` of the sealed files: this file, `data/synth/v0.3/bridges.yaml`, `data/synth/v0.3/decoys.yaml`, `data/synth/v0.3/fillers.yaml`, `prompts/generate_single_strict.md`, `experiments/micro-v0.3/config.yaml`, `experiments/micro-v0.3/writers.yaml`; list the hashes here; commit the files together; tag `v0.3.0-prereg`.
3. Stamp: `ots stamp PREREGISTRATION-v0.3.md data/synth/v0.3/bridges.yaml data/synth/v0.3/decoys.yaml prompts/generate_single_strict.md`; commit the proofs; upgrade later with `ots upgrade`.
4. Record `PREREG_COMMIT = b700d927924be0f324cac6c257256d49c99265fb` (tag `v0.3.0-prereg`).
5. Build the notes from the sealed specs with both writer families and the gate (`make synth SPEC=data/synth/v0.3 WRITERS=experiments/micro-v0.3/writers.yaml MIN_WORDS=100` with `--one-side-gate --gate-model sonnet`), apply the rewrite-once rule, run the gate again, drop second failures, freeze the manifest and record `CORPUS_MANIFEST_SHA256 = 6ba2d3ac49ca` (full value in `data/synth/v0.3/MANIFEST.sha256`; corpus sha256 d044765e9dff...) and the accepted bridge list here: 22 bridges, br01 to br24 except br09 and br11.
6. Only then run `make micro CONFIG=experiments/micro-v0.3/config.yaml` and `make reproduce`.

Note on the builder: the pipeline options this config uses (`arms.B4.notes: bridge+filler`, `arms.B4.prompt: generate_single_strict`, the v0.3 decision rule, `stats.match_votes`) were implemented before the seal; the seal covers the code state through the commit hash.
**Sealed-file hashes at seal time (SHA-256):**

```
c1010f044a3db1e3914a7ef0ea1207058961a31e13741e258c7496e5ddb5d768  data/synth/v0.3/bridges.yaml
c3a4eacadf4c308180908d9788f5bb5be042e4137892bd21db609f13bcffdc9d  data/synth/v0.3/decoys.yaml
f0e15f92c3f54c4a66fead760e206ea24d93120a4279f6975feb844aee9117a9  data/synth/v0.3/fillers.yaml
109a4b1f30c304776568362211cbc8603dde0407e303f2fe8caa22598e64f553  prompts/generate_single_strict.md
f64f130fca3902517069059cbbad4a5bee0bba8fd740982e2cab049361075722  experiments/micro-v0.3/config.yaml
ed48d36eee4dbd54cc8bec0e798463d60ac4e7e2ac50ec47996d3b79e1c8b898  experiments/micro-v0.3/writers.yaml
```

The hash of this file itself is the git blob recorded by the sealed commit and by its `.ots` proof.


---

## DEVIATIONS

Format: date, section, what changed, why, who decided.

1. 2026-09-14, Section 6 (checks at build). The first build pass used five attempts per note (the builder's default for oblique specs) rather than the ten stated here; the resume pass gave every failing note its remaining attempts up to ten, after which no note was short and no note failed the leak judge. Seven bridge notes that were short after the first pass were judged by the leak judge after the build (all CLEAN except one that was then regenerated). Decided by the experimenter, before any experiment call.
2. 2026-09-14, Section 6 (acceptance, rewrite-once). Side-A specs of br02, br06, br15 and br11 were rewritten once each after a gate flag, as the rule allows; the rewritten `data/synth/v0.3/bridges.yaml` has sha256 d039c061778c072b8a14b119700dd61007ee307201d00e389d447128416cecb3 (the sealed hash is in Section 15). br02, br06 and br15 passed the gate after their rewrite; br11 was recovered again (2 of 2 votes) and dropped.
3. 2026-09-14, Section 6 (gate stochasticity). The gate is not deterministic: across four passes the flags were br02 (pass 1), br06 and br15 (pass 2), br11 (pass 3), br09 and br11 (pass 4), and all flags except br11's second were judge ties (one MATCH, one NO_MATCH), which the rule counts as recoveries. Reported in the paper as a property of the instrument.
4. 2026-09-14, Section 6 (cap). To bound gate cost and stop the rewrite loop, gating stopped after four passes; br09, first flagged (a tie) on the final pass, was dropped without its rewrite. Accepted answer key: 22 bridges (10 family A, 12 family B). Decided by the experimenter, before any experiment call.
