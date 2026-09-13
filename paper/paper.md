# daydreamd: A Selection Engine for Machine-Generated Connections over a Private Corpus, Evaluated by Planted-Bridge Recovery

**Julian Caraulani**
caraulani@gmail.com

**September 2026. Draft v0.1, pre-result.** Every number in Section 6 is TBD until `make reproduce` fills it from committed run logs. The experiment is preregistered in `../PREREGISTRATION.md`.

---

## Abstract

We plant 12 cross-domain connections in a 60-note synthetic corpus written in the style of one builder's private notes, and measure whether a generate-then-select pipeline recovers them. On the oracle set, the pipeline recovered [x] of 12 planted connections and produced [y] false positives on 6 decoy pairs (Fisher p = [p1]). Distance-forced sampling included [a] planted pairs in 100 draws against a random-pairing expectation of 0.68 (permutation p = [p2]); the anchor-plus-remote sampler included [b] in 50 draws. Single-note reflection recovered [c] of 12. The generator declined to connect [d] percent of decoy pairs and [e] percent of random pairs. Synthetic ground truth measures recovery of planted structure, not real-world novelty or usefulness; we release the corpus, answer key, prompts, raw outputs and a reproduction script so the protocol can be run on any corpus.

---

## 1. Introduction

Language models generate candidate ideas cheaply and in bulk. What they lack is a way to tell which candidates are worth anything. A physicist at Anthropic, using Claude for quantum chromodynamics work, put it this way: "LLMs are profoundly creative. They simply lack a sense of which paths might be fruitful before walking them" (Schwartz, 2026). Ríos-García et al. (2026) measured the same thing at scale: across more than 25,000 agent runs in eight domains, 41.4 percent of outcome variance is attributable to the base model and 1.5 percent to the agent scaffold, evidence is ignored in 68 percent of traces, and the authors conclude that "outcome-based evaluation cannot detect these failures, and scaffold engineering alone cannot repair them." Si, Yang and Hashimoto (2024) found that 4,000 generated research ideas collapsed to about 200 unique ones. Generation is not the bottleneck. Selection is.

This paper describes daydreamd, a pipeline that samples pairs of distant concepts from a corpus of one person's notes, asks a language model whether a genuine connection exists (with explicit permission to answer that none does), and passes survivors through a binary critic and a retrieval-based duplicate gate. The system is designed to run as a background daemon over a private corpus, but the daemon is packaging. The contribution we can defend in this version is the evaluation protocol: a synthetic corpus with hand-planted connections and decoys, a preregistered analysis, a permutation null, and a full release of prompts, raw outputs and logs.

Zahn, Evans and Eagleman (2026) recently argued that memory consolidation exists to drive cross-domain recombination, and validated a replay-based system against 50,000 OpenAlex cross-field pairs and a held-out 2026 window. Their work establishes "dreaming as recombination" as a theoretical frame with credentialed authors and a large public-literature validation. We differ on four points. First, their pipeline has no critic and no permission to decline; every replay produces output. Second, they have no distance control at selection; distance is measured post hoc. Third, their holdout is not leakage-safe by construction, which their limitations section concedes, whereas our v0.1 ground truth is planted by hand and checked for n-gram leakage. Fourth, their corpus is public literature, whereas our target is a private corpus whose owner is the only competent judge. We treat their result as the strongest available evidence that recombination over memory is worth doing, and our protocol as the missing measurement of whether a given pipeline actually does it.

The rest of the paper is organized as follows. Section 2 places the work among consolidation systems, ideation pipelines over public literature, temporal-validation methods, the literature on judge unreliability, and creativity science. Section 3 describes the system. Section 4 states the selection thesis. Section 5 gives the evaluation protocol. Section 6 holds the result tables, currently empty. Section 7 lists limitations, including the ones we expect reviewers to raise first.

Four design commitments, each traceable to a prior finding:

1. **The generator may say NONE.** A prompt that demands a connection forces confabulation. Structured output with a required `testable_implication` field is itself a filter, since vague output cannot produce one. The NONE rate doubles as an honesty measure per model and per distance band.
2. **Novelty is a retrieval check, not an opinion.** The literature has discredited LLM-rated novelty (Section 2.4). In daydreamd, "already in the corpus" is a cosine threshold against real documents, and "matches the planted answer" is a grounded entailment judgment with the answer in context, never a novelty score.
3. **A stimulus control and a statistical null, kept separate.** Random pairing (arm B1) is the stimulus control: the same pipeline, the same fluency, a different sampling policy. Label permutation is the statistical null. The founding brief conflated these; the adversarial review in `research/02-sanity-review-2026-09-13.md` separated them.
4. **Recovery before usefulness.** No claim about usefulness is made until the pipeline has demonstrated that it can recover connections known to be present and decline connections known to be absent.

---

## 2. Related Work

### 2.1 The day-dreaming loop and its prior implementations

Gwern (2025) proposed a background loop in which a generator explores non-obvious links between concept pairs drawn from a knowledge store, a critic filters for novelty and usefulness, and survivors are written back to compound. The essay has not been modified since 2025-07-14 and links no implementation beyond a toy. Goedecke (2025) built idea-mill within a day of the essay, described it as "pretty half-assed", hand-wrote facts in YAML because extraction was unreliable, and still reported "a few genuinely novel ideas". zby (2025) piloted temporal novelty testing with pre-cutoff models and stopped at two stated walls: "I didn't implement the search algorithm, I manually selected combinations" and "a domain-agnostic novelty verifier is the fundamental research bottleneck". Vault Daydream (glebis, 2025) runs Sonnet generators and Haiku critics over an Obsidian vault with a 7.0 threshold and no evaluation. None of these measure whether the loop finds anything that is there. daydreamd differs by evaluating recovery against planted ground truth before making any other claim, and by replacing the hand-selected combinations with a sampler whose enrichment is measured.

### 2.2 Consolidation systems

Sleep-time compute (Lin et al., 2025) runs a background agent over an idle context to precompute and reorganize. Generative Agents (Park et al., 2023) periodically synthesizes stored memories into reflections. Auto-Dreamer (Ye et al., 2026) learns a fast per-session acquisition and a slow cross-session consolidation, reporting a 7-point gain on ScienceWorld at 12 times less memory. Sleep-Consolidated Memory (Shinde, 2026) models NREM and REM stages with forgetting. Anthropic's Dreams API, OpenClaw's Dreaming stage, and OpenDream all perform deduplication, contradiction resolution and cleanup. Every one of these consolidates; none generates connections and none filters for novelty. daydreamd builds no consolidation and treats it as commoditized. It borrows one contract shape from the Dreams API: an asynchronous job with immutable input, a separate output store, and a human review gate.

### 2.3 Ideation pipelines over public literature

SciMON (Wang et al., 2023), ResearchAgent (Baek et al., 2024), MOOSE-Chem (Yang et al., 2025), the AI co-scientist (Gottweis et al., 2025), BioDisco (Ke et al., 2025), FARS (Tang et al., 2026), Alien Space (Artiles et al., 2026) and SciMuse all run generator-then-critic loops over published literature. SciMuse personalizes, but from a researcher's published record. Alien Space's mechanism is the relevant warning: when prompted for novel ideas, language models "recombine high-density regions of the literature". Co-scientist's proximity agent (a similarity graph for deduplication) and meta-review agent (recurring review patterns fed forward into the next round) are the two components daydreamd adopts directly. The difference is the substrate. Every system above reads what everyone can read. A private corpus is the one setting where the judge is the world expert on the input, and where the ideas cannot have been recombined from high-density public literature because they are not in it.

### 2.4 Temporal validation and the unreliability of LLM novelty judgment

MOOSE-Chem froze a model with a pre-2024 cutoff and tested against 51 post-January-2024 chemistry papers. HindSight (Jiang, 2026) used Llama-3.3-70B with a June-2023 cutoff and a six-month safety margin, and found that LLM-judged novelty correlates negatively with anticipating real future research (ρ = −0.29, p < 0.01). CKM (Tao et al., 2026) measured a mean of 404 days (median 399, range 66 to 757) between hypothesis and matching paper. Wainrib et al. (2026) ran 800 independently replicated experiments and showed that permuting the hit and miss labels erases a 53.4 percent gain, which is the null-design daydreamd adopts. On the judge side, FARS reports automated review scores of 5.00 against 3.23 from 88 human reviewers; the Ideation-Execution Gap (Si et al., 2025) found that ideas rated novel before execution scored below human ideas after execution; RQ-Bench (Sinhahajari et al., 2026) documents a "novelty mirage" in which judges rate model-written research questions as highly novel while experts prefer author-anchored ones; Ideation Arena (Chen et al., 2026) reports that LLM judges align with 105 expert researchers' pairwise preferences only 72.56 percent of the time, and that scaffolds vary wildly, some underperforming their base model. RINoBench (Schopf and Färber, 2026) evaluates nine automated novelty metrics against 1,381 expert-judged ideas and finds that reasoning aligns with human rationales but "does not reliably translate into accurate novelty judgments". AgentIdeaBench (Mo et al., 2026) scores originality against retrieved prior art across 33 models and 40 subfields. Nusrat and Nusrat (2025) audited three Kosmos hypotheses against random-gene nulls and found one of three indistinguishable from noise, caught only by the null model.

daydreamd inherits the old-cutoff and temporal-holdout methodology as hygiene and does not claim it. Its v0.1 differs from all of the above in three ways: the ground truth is planted by hand rather than inferred from later publication; the judge is asked a grounded entailment question with the answer in context, never a novelty question; and a permutation null is preregistered. Ideation Arena, RINoBench and AgentIdeaBench occupy the "novelty benchmark for public-literature ideas" slot; daydreamd does not claim that slot.

### 2.5 Creativity science

Boden (1990) classifies this work as combinational creativity. Campbell (1960) and Simonton frame it as blind variation and selective retention. Mednick (1962) named remote association, though his flat-hierarchy mechanism was refuted by Benedek and Neubauer (2013) and is not relied on here. Uzzi et al. (2013), over 17.9 million papers, found that the highest-impact work combines a conventional core with an injection of atypical combinations, a two-dimensional prescription that motivates arm B6. Liu et al. (2026), with 140 humans, 2,800 ideas and seven models, found that semantic distance predicts originality linearly (humans β = .10, models β = .18) with no quadratic term, and Shen, Druckmann and Zou (2026) obtained their best results by maximizing distance (novel-solution rate from 1.6 percent to over 50 percent at fixed model and temperature). Orwig et al. (2025) found a plateau, not a peak. These results kill the intermediate-distance "fertile zone" for raw novelty; what survives, and what nobody has plotted, is usable yield as novelty times feasibility against distance. That curve is not part of v0.1.

Three further results constrain the design. Peeperkorn et al. (2024) showed temperature is a risk parameter, not a creativity parameter, so sampling policy is never conflated with temperature. FunSearch (Romera-Paredes et al., 2024) got results with a fast weak model and about a million samples and reported insensitivity to model choice, but AlphaEvolve (Novikov et al., 2025) reverses this in the same lab: it "performs increasingly better as the underlying LLM improves", trading roughly a thousandfold in samples for capability. The defensible statement is that a generate-evaluate-select loop is necessary for verified novelty at any capability level, and better models make the search cheaper, not unnecessary. Argument Collapse (Kim et al., 2026) reports 65.3 percent unique arguments from humans against 3.4 percent from models, and Shared Imagination (Zhou et al., 2024) shows models hallucinate alike, so multi-model ensembling is not a diversity fix. Chen, Zhao and Cohan (2026) warn that models already over-produce "bridge-like opportunities and synthesis methods", exactly the output shape of a combination daemon.

On the biological analogy: Wagner et al. (2004) largely failed to replicate (Brodt et al., 2018; Schönauer et al., 2018), so no sleep-biology claim is made. What survives is Hoel's (2021) architectural argument that a system injecting noise during live operation would fail at its job, so a dedicated offline period is needed, and the PAD model (Deperrois et al., 2022) in which ablating the mixing of multiple memories costs 4.4 points on CIFAR-10 and 18 points on SVHN, evidence that recombination rather than mere replay does measurable work. Model collapse (Shumailov et al., 2024) destroys distributional tails first, and remote associations are the tails; any writeback loop must segregate generated material, anchor each cycle in fresh real input, and gate on human verification. DreamCoder (Ellis et al., 2021) is the existence proof that a fantasy-plus-replay loop can be done safely. Hoel's overfitted-brain hypothesis has, as far as we can find, never been connected to language models; that framing is available and is used lightly here.

### 2.6 The personal-informatics null

Strömel et al. (CHI 2024, N = 273) is the best-powered test of language-model narratives over personal data. Generated narratives moved engagement, attention and reward, and produced a flat null on the Insight subscale: F(2, 270) = 0.43, p = .64. PhysioLLM's generated-insight arm did not beat a plain data summary, and an audit of 14,922 generated explanations over personal sensor data (Zhu et al., 2026) found that models "routinely attribute anomalous days to causes without sufficient support". This null does not test our hypothesis for four reasons: the substrate was seven days of step counts, which contain no latent conceptual structure; the operation was summarization of one dataset, not recombination of two distant concepts; the participants had no expertise in their own step counts; and there was no filter, no rejection, no permission to say NONE. What transfers is the warning that enjoyment is not insight and self-report cannot tell them apart. That is why the human-scored track (Section 7) is a blind test with a sealed key, and why v0.1 uses no self-report at all.

### 2.7 Claim discipline

Tao et al. maintain a ledger for AI contributions to Erdős problems that classifies each as 1(a) AI-independent with no comparable literature, 1(b) AI solution with literature found afterwards, 1(c) AI building on known literature, 1(d) AI plus human, or 2(a) to 2(d) literature search, formalization, rewriting, computation. The cautionary case is October 2025, when a model was publicized as solving about ten open Erdős problems and had in fact located existing literature solutions. Every future "hit" from daydreamd over a real corpus will be classified against this ledger before the word novel is used. In v0.1, no hit is called novel; hits are called recovered.

---

## 3. System

### 3.1 Pipeline

```
ingest → concept cards → local embeddings → pair sampler (B1 | B3 | B6)
      → generator (NONE permitted, structured JSON)
      → binary critic → duplicate gate (retrieval, cosine 0.85)
      → morning.md → owner verdicts → writeback (unverified until endorsed)
```

The engine never knows where the corpus came from. Adapters supply documents: a Claude Code memory directory, an Obsidian vault, a codebase, a Zotero library, or the synthetic corpus used in this paper.

### 3.2 Concept cards

One cheap-model pass per document distills atomic claims with source pointers into a tight schema (`id`, `source_note`, `claim` of at most 30 words, `entities`, `why_it_matters`, `confidence`). This is the step Goedecke identified as broken in idea-mill. Cards are cached and incremental. In v0.1, card text is committed so anyone can rate fidelity; human fidelity rating is deferred to the first real-corpus run.

### 3.3 Embeddings

`all-MiniLM-L6-v2` runs on device. The privacy rule "your notes never leave your machine" has to hold for embedding, not just storage.

### 3.4 Samplers

- **B1, random.** Uniform over cross-note pairs.
- **B3, banded.** Quantile bands of the cross-note cosine-distance distribution: Q1, Q2 to Q3, Q4, top 5 percent. Equal draws per band. The far tail is included because that is where the distinctive prediction lives.
- **B6, anchor plus remote.** One note from the densest embedding cluster paired with one from Q4, following Uzzi's conventional-core-plus-atypical prescription.

### 3.5 Generator

Prompt contract, committed verbatim in `prompts/generator.md`: two claims from one person's notes; most pairs are unrelated; if no genuine, non-obvious connection exists, output exactly `NONE`; otherwise JSON with `connection` (at most 40 words), `mechanism`, `testable_implication` (one concrete thing the owner could check this week), and `needs` (which claim supplies what). No restating. No facts absent from the inputs.

### 3.6 Critic and duplicate gate

The critic is binary and cheap: kill if the output restates a claim, if the implication is not checkable, or if the connection is generic. The duplicate gate embeds the surviving `connection` and removes it if cosine similarity to any card or note chunk exceeds 0.85. Neither component rates novelty.

### 3.7 Morning review and writeback (not exercised in v0.1)

Survivors land in `morning.md` with provenance. The owner approves or rejects each with a reason. Rejections feed a per-user learnings file that tunes the critic (the co-scientist meta-review pattern). Endorsed dreams gain sampling weight and become concept cards. Every dream carries lineage; a dream built on a later-rejected dream is flagged. Generated material is never silently folded into ground truth.

### 3.8 Ship shape

Local-first command-line tool, bring-your-own key or a headless Claude Code session, pluggable generator (any API or local model), built-in scheduler, no telemetry. Configuration: corpus paths, schedule, dream count, sampler, models, strictness.

---

## 4. The Selection Thesis

daydreamd is not a better generator. It is a selection engine for machine-generated connections, deployed over a corpus whose owner is the ground-truth expert. Three observations support treating selection as the frontier and generation as commoditized.

First, every serious builder of a day-dreaming loop stopped at verification (Section 2.1). Second, the field has measured that LLM-rated novelty anti-correlates with real value (Section 2.4), which removes the obvious cheap judge. Third, a private corpus is the one setting where a competent human judge is available for free, because the owner already knows what is in their own notes and what would be worth acting on.

The thesis makes a prediction that v0.1 tests in the narrowest form: a pipeline built on these principles should recover connections that are known to be present, decline connections that are known to be absent, and surface planted pairs more often when the sampler forces distance than when it does not. If it fails the planted test, no later claim is worth making.

---

## 5. Evaluation Protocol

Full detail is in `../PREREGISTRATION.md`, which is hashed and timestamped before any model call. This section summarizes it.

### 5.1 Synthetic corpus with planted ground truth

Sixty notes in the voice of one fictional solo builder across six domains (ten each), 150 to 300 words, in memory-note style. Twelve planted bridges: pairs of notes in different domains carrying, obliquely, the ingredients of one hidden mechanism, each with a human-written `gold_connection` (at most 40 words) and `gold_implication`. Six decoy pairs with shared vocabulary and no mechanism. Thirty-six filler notes. A leakage check ensures no 6-gram of any gold connection appears in any note. Corpus, manifest hashes and `gold.json` are committed and public. There are 1,770 cross-note pairs, of which 12 are planted, a base rate of 0.68 percent.

### 5.2 Arms

S0 (oracle set: 12 planted, 6 decoy, 42 random non-planted cross-domain pairs, labels hidden) tests generator and critic independent of any sampler. B1 random (100 pairs), B3 banded (25 per band, four bands), B6 anchor plus remote (50 pairs). B4 single-note reflection over the 24 bridge notes, the incubation control.

### 5.3 Measures

Sampler enrichment of planted pairs against the hypergeometric base rate; recall on planted pairs (non-NONE and a grounded entailment MATCH against gold, with cosine reported but not used as the criterion); specificity as NONE rate on decoys and random pairs; false-positive rate after critic on decoys; B4 recall; NONE rate by band; cost per arm and per recovered bridge from logs; exploratory finds on non-planted pairs, reported separately and never counted as hits.

### 5.4 Hypotheses and decision rule

H1: S0 recall on planted pairs exceeds the false-positive rate on decoys (Fisher exact, one-sided, α = .05). H2: B3 and/or B6 surface more planted pairs than B1 (hypergeometric and 10,000-shuffle permutation, α = .05). H3: B4 recall is below pair-arm recall (Fisher). Signal is declared only if H1 and H2 both pass. Anything else is reported as null, in full, with the same tables.

### 5.5 Threats

The notes are drafted by a language model and the generator is a language model; they may share priors. Mitigations: bridges and gold text authored by the experimenter with a language model as a disclosed writing assistant and fixed under the preregistration seal before any note existed, the leakage check, decoy pairs, and a planned second corpus and bridge set written by a different model family or by an independent human. Synthetic ground truth measures recovery of planted structure, not real-world novelty or usefulness. The recovery judge is a language model asked a grounded entailment question with the answer in context, the narrow use the literature supports; its prompt and every judgment are released.

---

## 6. Experimental Results

All cells are TBD until filled by `make reproduce`, which regenerates every table from `experiments/runs/<date>_<snapshot>/` without API access. Model snapshot IDs, prompt hashes and access dates are read from run metadata.

**T1. Corpus.** Filled by `make table-t1`.

| Notes | Domains | Bridge notes | Filler notes | Planted pairs | Decoy pairs | Cross-note pairs | Cards | Leakage check |
|---|---|---|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

**T2. Sampler enrichment of planted pairs.** Filled by `make table-t2`.

| Arm | Pairs drawn | Planted included | Hypergeometric expectation | P(≥ observed) | Permutation p |
|---|---|---|---|---|---|
| B1 random | TBD | TBD | TBD | TBD | TBD |
| B3 banded | TBD | TBD | TBD | TBD | TBD |
| B6 anchor+remote | TBD | TBD | TBD | TBD | TBD |

**T3. Oracle set S0: recall and specificity.** Filled by `make table-t3`.

| Pair type | N | Non-NONE | Survived critic | Survived dup gate | MATCH to gold | Rate (Wilson 95%) |
|---|---|---|---|---|---|---|
| Planted | TBD | TBD | TBD | TBD | TBD | TBD |
| Decoy | TBD | TBD | TBD | TBD | n/a | TBD |
| Random non-planted | TBD | TBD | TBD | TBD | n/a | TBD |

Fisher exact (planted recovered vs decoy false positive), one-sided: p = TBD.

**T4. Per-arm recall, NONE rate, kill rate and cost.** Filled by `make table-t4`.

| Arm | Pairs | NONE % | Critic kill % | Dup-gate kill % | Planted recovered | Exploratory finds | Input tokens | Output tokens | USD | USD per recovered bridge |
|---|---|---|---|---|---|---|---|---|---|---|
| S0 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| B1 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| B3 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| B6 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| B4 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

NONE rate by distance band, arm B3: Q1 TBD, Q2 to Q3 TBD, Q4 TBD, top 5 percent TBD.

**T5. Permutation null over S0.** Filled by `make table-t5`.

| Statistic | Observed | Permutation distribution mean | Permutation p (10,000 shuffles) |
|---|---|---|---|
| Recall on planted minus false-positive rate on decoy | TBD | TBD | TBD |

**T6. Single-note reflection (B4) versus pair arms.** Filled by `make table-t6`.

| Arm | Bridges tested | Mechanisms recovered | Rate (Wilson 95%) | Fisher p vs best pair arm |
|---|---|---|---|---|
| B4 single-note | TBD | TBD | TBD | TBD |
| Best pair arm | TBD | TBD | TBD | n/a |

**Exploratory finds.** Count: TBD. Released as `results/exploratory_finds.jsonl`. Not counted as hits.

**Model and prompt provenance.** Generator snapshot: TBD. Card and critic snapshot: TBD. Judge snapshot: TBD. Embedding model: `sentence-transformers/all-MiniLM-L6-v2`, version TBD. Prompt SHA-256 values: TBD. Access date: TBD.

---

## 7. Limitations and Future Work

### 7.1 Limitations of v0.1

**Synthetic ground truth.** Recovery of planted structure is not evidence of real-world novelty or usefulness. A pipeline can pass this test and still produce nothing an owner would act on.

**Shared priors between corpus author, bridge author and generator.** All three involved a language model of the same family. Sealing the bridges before any note existed, the leakage check and the decoys reduce but do not remove the risk that recovery reflects shared associations rather than reading the notes. A second bridge set written by an independent human is the planned control.

**One corpus, one generator, one judge.** No generalization is claimed. The judge is a language model, used only for grounded entailment with the answer in context.

**No human rating.** The blind owner-scoring protocol is specified and deferred.

**Scaffold variance.** Ríos-García et al. attribute 1.5 percent of variance to scaffolds. The arms in this paper are all scaffold ablations. A base-model axis crossed with samplers, with a variance decomposition, is the obvious next experiment; if the sampler effect is small relative to the model effect, that will be reported as the finding.

**Cost.** No cost number is stated that was not read from a log.

### 7.2 Track C: owner-blind scoring over a real private corpus

Pool survivors, shuffle, strip arm labels, present in batches of 20. The owner marks each item KEEP (would act on or write down) and KNOWN (already had this thought) as binary decisions. Thirty items are repeated for intra-rater kappa. The key file's hash is committed before scoring and the file is revealed after. Fisher exact and permutation as in v0.1. The engagement-versus-insight warning from Strömel et al. is the reason this is blind and binary, never a rating of enjoyment.

### 7.3 Track A: retrospective temporal validation

An old-cutoff open-weight generator with a six-month margin (HindSight's discipline) over a time-frozen public corpus, with hit detection by retrieval over post-cutoff literature and a modern-model entailment matcher, reported as lift over a matched null with a lead-time distribution and a future-neighbourhood rate. Inherited methodology, cited, not claimed.

### 7.4 Track B: prospective public registry

Dreams over live corpora, published with git timestamps and OpenTimestamps anchoring, with two outcome classes: independently discovered later, and adopted from the registry.

### 7.5 Open measurements nobody has made

Usable yield (owner KEEP rate, with "not in corpus" enforced by retrieval) as a function of embedding distance, including the far tail. Tail diversity of dreams across nights with and without writeback, the model-collapse curve. Concept-card fidelity rates. A false-positive rate for a corpus-scale ideation system.

---

## 8. Conclusion

Generation is cheap and selection is the wall, and every previous attempt at a day-dreaming loop stopped at that wall without measuring it. daydreamd's v0.1 contribution is a measurement: a preregistered, planted-ground-truth recovery test with a stimulus control, a statistical null, decoys, a leakage check, and a full release of prompts, raw outputs and logs, so that any generate-then-select pipeline over any corpus can be asked the same question before it is asked to be useful. Whether daydreamd itself passes that test is the content of Section 6.

The system and the protocol are open source under MIT (code) and CC-BY-4.0 (paper and data).

---

## References

All references were checked against their primary source (arXiv abstract page, publisher page, or live URL) on 2026-09-13.

Baek, J., et al. (2024). ResearchAgent: Iterative research idea generation over scientific literature with large language models. arXiv:2404.07738.

Benedek, M. and Neubauer, A. C. (2013). Revisiting Mednick's model on creativity-related differences in associative hierarchies: Evidence for a common path to uncommon thought. *Journal of Creative Behavior*, 47(4), 273–289. doi:10.1002/jocb.35.

Ke, Y., George, K., Pandya, K., et al. (2025). BioDisco: Multi-agent hypothesis generation with dual-mode evidence, iterative feedback and temporal evaluation. arXiv:2508.01285.

Boden, M. A. (1990). *The Creative Mind: Myths and Mechanisms*. Weidenfeld and Nicolson.

Brodt, S., Pöhlchen, D., Täumer, E., Gais, S. and Schönauer, M. (2018). Incubation, not sleep, aids problem-solving. *Sleep*, 41(10), zsy155. doi:10.1093/sleep/zsy155.

Campbell, D. T. (1960). Blind variation and selective retention in creative thought as in other knowledge processes. *Psychological Review*, 67(6), 380–400.

Chen, Z., Zhao, K., Fu, J., et al. (2026). Ideation Arena: Evaluating LLM generated research ideas with battle-style human expert assessment. arXiv:2608.29696.

Chen, Z., Zhao, Y. and Cohan, A. (2026). Measuring the gap between human and LLM research ideas. arXiv:2607.01233.

Tao, J., Wang, Y., Liu, X., et al. (2026). Continuous Knowledge Metabolism: Generating scientific hypotheses from evolving literature. arXiv:2604.12243. (Cited as CKM.)

Deperrois, N., Petrovici, M. A., Senn, W. and Jordan, J. (2022). Learning cortical representations through perturbed and adversarial dreaming. *eLife*, 11:e76384.

Ellis, K., et al. (2021). DreamCoder: Bootstrapping inductive program synthesis with wake-sleep library learning. *PLDI 2021*.

Tang, Q., Sun, T., Hu, X., et al. (2026). FARS: A fully automated research system deployed at scale. arXiv:2606.31651.

Artiles, A. H., Weiss, M., Brinkmann, L., et al. (2026). The alien space of science: Sampling coherent but cognitively unavailable research directions. arXiv:2603.01092.

Goedecke, S. (2025). Practical notes on getting LLMs to generate new ideas. seangoedecke.com/idea-mill; code at github.com/sgoedecke/idea-mill.

Gottweis, J., Weng, W.-H., Daryin, A., et al. (2025). Accelerating scientific discovery with Co-Scientist (v1 title: Towards an AI co-scientist). arXiv:2502.18864.

Gwern (2025). LLM daydreaming. gwern.net/ai-daydreaming. Last modified 2025-07-14.

Jiang, B. (2026). HindSight: Evaluating LLM-generated research ideas via future impact. arXiv:2603.15164.

Hoel, E. (2021). The overfitted brain: Dreams evolved to assist generalization. *Patterns*, 2(5), 100244.

Si, C., Hashimoto, T. and Yang, D. (2025). The ideation-execution gap: Execution outcomes of LLM-generated versus human research ideas. arXiv:2506.20803.

Lin, K., et al. (2025). Sleep-time compute: Beyond inference scaling at test-time. arXiv:2504.13171.

Liu, Q. E., Dubova, M., Conklin, H., et al. (2026). Assessing the effect of cross-domain mapping on creativity in humans and large language models. arXiv:2603.19087.

Luo, X., et al. (2025). Large language models surpass human experts in predicting neuroscience results. *Nature Human Behaviour*, 9(2), 305–315.

Mednick, S. (1962). The associative basis of the creative process. *Psychological Review*, 69(3), 220–232.

Mo, Y., Zheng, T., Gao, Y., et al. (2026). AgentIdeaBench: Benchmarking scientific ideation in the agent era. arXiv:2609.07611.

Nusrat, H. and Nusrat, O. (2025). When AI does science: Evaluating the autonomous AI scientist KOSMOS in radiation biology. arXiv:2511.13825.

Orwig, W., Luchini, S. A., Beaty, R. and Schacter, D. L. (2025). A 'sweet spot' for creative ideation: Non-linear associations between semantic distance and creativity. *Cognitive Computational Neuroscience (CCN) 2025*, abstract.

Park, J. S., et al. (2023). Generative agents: Interactive simulacra of human behavior. arXiv:2304.03442.

Peeperkorn, M., et al. (2024). Is temperature the creativity parameter of large language models? arXiv:2405.00492.

Penadés, J. R., et al. (2025). AI mirrors experimental science to uncover a mechanism of gene transfer crucial to bacterial evolution. *Cell*, 188. doi:10.1016/j.cell.2025.08.032. Published online 2025-09-09.

Ríos-García, M., Alampara, N., Gupta, C., et al. (2026). AI scientists produce results without reasoning scientifically. arXiv:2604.18805.

Romera-Paredes, B., et al. (2024). Mathematical discoveries from program search with large language models. *Nature*, 625, 468–475.

Novikov, A., Vũ, N., Eisenberger, M., et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery. arXiv:2506.13131.

Schönauer, M., Brodt, S., Pöhlchen, D., Breßmer, A., Danek, A. H. and Gais, S. (2018). Sleep does not promote solving classical insight problems and magic tricks. *Frontiers in Human Neuroscience*, 12:72. doi:10.3389/fnhum.2018.00072.

Schopf, T. and Färber, M. (2026). Is this idea novel? An automated benchmark for judgment of research ideas (RINoBench). arXiv:2603.10303.

Schwartz, M. D. (2026). Vibe physics: The AI grad student. Anthropic Research, anthropic.com/research/vibe-physics.

Shen, A., Druckmann, S. and Zou, J. (2026). Unlocking LLM creativity in science through analogical reasoning. arXiv:2605.11258.

Shinde, S. S. (2026). SCM: Sleep-consolidated memory with algorithmic forgetting for large language models. arXiv:2604.20943.

Shumailov, I., et al. (2024). AI models collapse when trained on recursively generated data. *Nature*, 631, 755–759.

Si, C., Yang, D. and Hashimoto, T. (2024). Can LLMs generate novel research ideas? arXiv:2409.04109. ICLR 2025.

Sinhahajari, S., Majumder, N. and Poria, S. (2026). On the limits of LLM-as-judge for scientific novelty assessment. arXiv:2606.12071.

Strömel, K. R., Henry, S., Johansson, T., Niess, J. and Woźniak, P. W. (2024). Narrating fitness: Leveraging large language models for reflective fitness tracker data interpretation. *CHI 2024*. doi:10.1145/3613904.3642032.

Zhu, S., Zhang, H., Chi, J. D., et al. (2026). Causal stories from sensor traces: Auditing epistemic overreach in LLM-generated personal sensing explanations. arXiv:2605.08590.

Tao, T., et al. Erdős problems AI contributions ledger. github.com/teorth/erdosproblems wiki.

Uzzi, B., Mukherjee, S., Stringer, M. and Jones, B. (2013). Atypical combinations and scientific impact. *Science*, 342(6157), 468–472.

Wagner, U., et al. (2004). Sleep inspires insight. *Nature*, 427, 352–355.

Wainrib, G., Bodinier, B., Dakhli, H., et al. (2026). Can AI scientist agents learn from lab-in-the-loop feedback? Evidence from iterative perturbation discovery. arXiv:2603.26177.

Wang, Q., et al. (2023). SciMON: Scientific inspiration machines optimized for novelty. arXiv:2305.14259.

Yang, Z., Liu, W., Gao, B., et al. (2025). MOOSE-Chem: Large language models for rediscovering unseen chemistry scientific hypotheses. *ICLR 2025*. arXiv:2410.07076.

Ye, C., Liu, Y., Wang, Y., et al. (2026). Auto-Dreamer: Learning offline memory consolidation for language agents. arXiv:2605.20616.

Zahn, O., Evans, J. and Eagleman, D. (2026). Discovery by dreaming: Cross-domain recombination in artificial memory. arXiv:2607.16256.

Łukasiak, Z. (zby) (2025). Reinventing daydreaming machines. zzbbyy.substack.com/p/reinventing-daydreaming-machines, 2025-10-13; code at github.com/zby/DayDreamingDayDreaming.

Zhou, Y., et al. (2024). Shared imagination: LLMs hallucinate alike. arXiv:2407.16604.

Kim, Y., Chang, Y., Pham, C. M., et al. (2026). Argument collapse: LLMs flatten long-form public debate. arXiv:2606.01736.

Behrouz, A., Hashemi, F., Javanmard, A. and Mirrokni, V. (2026). Language models need sleep: Learning to self-modify and consolidate memories. arXiv:2606.03979. (Google Research; the 'sleep stage' with an RL-generated synthetic curriculum.)

Ding, T., Nannapaneni, A., Liu, B., et al. (2026). Always-on agents: A survey of persistent memory, state, and governance in LLM agents. arXiv:2606.30306.

Cheung, V. (2026). Dreaming is not a bug: A Jung-inspired dream layer for multi-agent LLM companions. arXiv:2601.06115.
