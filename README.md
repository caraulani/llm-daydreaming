# daydreamd: the LLM daydreaming loop, evaluated

<p align="center">
  <img src="hero.png" alt="LLM Daydreaming v01. Give your LLM the power to dream new ideas, based on your actual work. Sample, connect, abstain, critique, filter, morning." width="100%"/>
</p>

*By [Julian Caraulani](https://github.com/caraulani), September 2026. An open implementation and
preregistered test of Gwern's LLM daydreaming proposal (the day-dreaming loop) over your own notes:
Obsidian vaults, Claude Code memory, any markdown folder.*

**Your notes are full of connections you never made.** daydreamd looks for them while you sleep.

Repo: `llm-daydreaming`. Tool and package: `daydreamd` (daydream + the Unix daemon suffix).
Site: [caraulani.github.io/llm-daydreaming](https://caraulani.github.io/llm-daydreaming/).

It is a local-first daemon that collides far-apart concepts from your own corpus, asks a model
whether a genuine connection exists (with permission to say no), kills most of what comes back,
and leaves the survivors in a `morning.md`. The research question is not whether a model can
generate connections. It can, cheaply and endlessly. The question is whether anything can tell
a real connection from a fluent one. This repo is the test rig for that question, with ground
truth planted by construction, a pre-registered protocol, and every raw output committed.

[![CI](https://github.com/caraulani/llm-daydreaming/actions/workflows/ci.yml/badge.svg)](https://github.com/caraulani/llm-daydreaming/actions/workflows/ci.yml) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22746627.svg)](https://doi.org/10.5281/zenodo.22746627) [![License: MIT](https://img.shields.io/badge/code-MIT-black.svg)](LICENSE) [![Paper: CC BY 4.0](https://img.shields.io/badge/paper-CC%20BY%204.0-black.svg)](LICENSE-CC-BY-4.0)

> Works with a Claude subscription (headless `claude -p`, zero marginal cost), the Anthropic API,
> and, in v0.2, any local model through Ollama.

## Lineage

This repository does not propose the day-dreaming loop. It measures one part of it. The idea and
the first builds belong to the people below; what this repo adds is the missing measurement.
The loop is old. What changed in 2025 is that the generator became cheap enough to run every
night over a private corpus, and what is still missing is the measurement.

| Year | Who | What | What was missing |
|---|---|---|---|
| 1908 | [Henri Poincaré, "Science and Method" (1914 translation)](https://archive.org/details/cu31924012248179) | invention is choice: the unconscious forms a great many combinations, and only the useful ones reach consciousness after a period of incubation | one mathematician's aesthetic sense as the sieve; no procedure, no corpus |
| 1926 | [Graham Wallas, "The Art of Thought"](https://archive.org/details/theartofthought) | preparation, incubation, illumination, verification as the four stages of a new idea | a description of stages, not a mechanism |
| 1945 | [Jacques Hadamard, "The Psychology of Invention in the Mathematical Field"](https://archive.org/details/eassayonthepsych006281mbp) | combinations formed below awareness and sifted by an aesthetic sense, from interviews with mathematicians | same sieve, same absence of a procedure |
| 1960 | [Donald T. Campbell, "Blind variation and selective retention in creative thought as in other knowledge processes"](https://doi.org/10.1037/h0040373) | generate variations blindly, retain selectively: the selection half of the loop stated as a general principle | the retention criterion is left open; no generator |
| 1962 | [Sarnoff Mednick, "The associative basis of the creative process"](https://doi.org/10.1037/h0048850) | creativity as forming remote associates; the distance between the paired elements is the variable | the flat-hierarchy mechanism was later refuted (Benedek and Neubauer 2013); the distance framing survived |
| 1964 | [Arthur Koestler, "The Act of Creation"](https://archive.org/details/actofcreation0000arth_p2s0) | bisociation: a new idea is the collision of two previously unconnected frames of thought | a name for the collision, no way to produce or test one |
| 1983 | [Francis Crick and Graeme Mitchison, "The function of dream sleep"](https://doi.org/10.1038/304111a0) | dreaming as reverse learning that removes parasitic associations from an overloaded network | pruning without generation; no idea comes out of it |
| 1986 | [Don R. Swanson, "Fish oil, Raynaud's syndrome, and undiscovered public knowledge"](https://doi.org/10.1353/pbm.1986.0087) | two literatures that never cite each other can jointly hold an unnoticed discovery; the closest ancestor of colliding two distant notes | public literature, searched by hand, one investigator as the judge |
| 1990 | [Erik T. Mueller, "Daydreaming in Humans and Machines" (DAYDREAMER)](https://openlibrary.org/works/OL4776122W) | the first program that daydreams: a stream of thought that generates and evaluates alternative plans between tasks | daydreams over its own goals and episodes, not over a corpus of notes; no novelty evaluation |
| 1990 | [Margaret Boden, "The Creative Mind: Myths and Mechanisms"](https://archive.org/details/creativemindmyth0000bode) | combinational, exploratory and transformational creativity as three distinct kinds | a taxonomy; the loop is combinational by definition, still without a runnable form |
| 1993 | [Melanie Mitchell, "Analogy-Making as Perception"](https://archive.org/details/analogymakingasp0000mitc) and [Hofstadter and Mitchell, "Fluid Concepts and Creative Analogies" (1995)](https://archive.org/details/fluidconceptscre0000hofs_w7o9) | Copycat: generate associations in parallel, filter, with a literal temperature knob controlling how far to reach | a micro-domain of letter strings; temperature is a risk parameter, not a novelty parameter |
| 1995 | [Hinton, Dayan, Frey and Neal, "The wake-sleep algorithm for unsupervised neural networks"](https://doi.org/10.1126/science.7761831) | a sleep phase generates fantasies that train the recognition model | learning weights, not proposing ideas |
| 2002 | [Gilles Fauconnier and Mark Turner, "The Way We Think"](https://archive.org/details/waywethinkconcep00gill) | conceptual blending: the cognitive mechanism under every recombination | no computation, no evaluation |
| 2021 | [Erik Hoel, "The overfitted brain: Dreams evolved to assist generalization"](https://doi.org/10.1016/j.patter.2021.100244) | dreams as noise injection against overfitting, hence the need for a dedicated offline phase | an argument for why to dream, not for what to dream about |
| 2023 | [Park et al., "Generative Agents"](https://arxiv.org/abs/2304.03442) | periodic reflection that synthesises stored memories into higher-level insights | synthesis of what is there; no recombination of distant items, no discard |
| 2025 | [Lin et al., "Sleep-time Compute"](https://arxiv.org/abs/2504.13171) | offline computation over an agent's context while it is idle | consolidation for later queries, not generation of anything new |
| 2025 | [Gwern, "LLM Daydreaming"](https://gwern.net/ai-daydreaming) | proposed the day-dreaming loop: sample two facts, ask for a connection, keep the interesting ones, write them back | no implementation, no evaluation |
| 2025 | [Sean Goedecke, idea-mill](https://github.com/sgoedecke/idea-mill) | first prototype, one day after the essay; "a few genuinely novel ideas" | hand-written facts, no critic evaluation, no baselines |
| 2025 | [Zbigniew Lukasiak, DayDreamingDayDreaming](https://github.com/zby/DayDreamingDayDreaming) | first temporal-novelty pilot with pre-cutoff models | "I manually selected combinations"; "a domain-agnostic novelty verifier is the fundamental research bottleneck" |
| 2026 | [Vault Daydream](https://github.com/glebis/claude-skills) | Obsidian skill: vault pairs, generator plus critic, threshold, writeback | run on demand, no distance control, no evaluation |
| 2026 | [Oliver Zahn, James Evans and David Eagleman, "Discovery by Dreaming"](https://arxiv.org/abs/2607.16256) | recombination over public corpora, validated against 50,000 cross-field pairs and a 2026 holdout | no critic, no distance control, no private corpus; the holdout is not leakage-safe by the authors' own account |
| 2026 | [Julian Caraulani, "daydreamd: the LLM daydreaming loop, evaluated"](https://github.com/caraulani/llm-daydreaming) | selective daydreaming: the loop with an abstention gate, tested against planted ground truth under a sealed preregistration, every raw output published | real-corpus usefulness (Track C), temporal validation (Track A) and a critic that is not an opinion are still open |

*Sources verified 2026-09-14: DOIs resolved through Crossref, books through archive.org or Open Library, preprints through arXiv.*

The consolidation branch (Letta's sleep-time compute, Google's "Language Models Need Sleep",
Anthropic's Dreams, OpenClaw's dreaming mode) reorganises memory. It does not generate. We build
none of it. See [paper/paper.md](paper/paper.md) for the full map.

## What we found

**v0.1.** Sealed run over the synthetic corpus, 2026-09-13, generator `claude-sonnet-5`:

- **H1, selection: supported.** Given the right two notes, the generator answered on 11 of 12
  planted pairs and named the planted mechanism on 8 of 12; it stayed silent on 5 of 6 decoys and
  34 of 42 random pairs, and no decoy answer survived the critic (Fisher p = 0.011).
- **H2, distance-forced sampling: null.** Banded sampling drew 1 planted pair in 100, anchor plus
  remote drew 0 in 50, random drew 1 in 100. Expected under chance: 0.65. Untestable at this base
  rate, and the post-hoc points the other way.
- **H3, two notes beat one note: not significant.** 8 of 12 vs 4 of 12, p = 0.11. All four
  single-note recoveries come from notes that state the mechanism in paraphrase, which the 6-gram
  leakage check cannot catch. That is a corpus flaw, and v0.2 fixes it.
- **Decision.** By the preregistered rule this run reports no signal. We publish it anyway; that
  was the deal.
- **Exploratory X1, not preregistered.** Replace the true partner note with a mechanism-free
  filler from the same domain and recovery collapses: 9 of 12 with the real pair, 1 of 12 with
  the filler (Fisher p = 0.0014). The generator needs the second note; domain cues do not do it.
- **Exploratory X3, not preregistered.** Sampling near-in-embedding, far-in-domain pairs drew
  2 planted pairs in 100 (0.6 expected, p = 0.13) and got an answer on 31 percent of pairs, against
  16 percent for random and 9 percent for distance-banded; the far bands drew NONE on all 50 units.
  Right direction, underpowered; v0.2 runs it at 300 draws.
- **Post-hoc, not preregistered.** Every planted bridge's closest card pair sits in the nearest
  distance band (12 of 12; median 0.61 vs 0.74 for random cross-domain pairs): real bridges are
  domain-far but embedding-near, so far-band sampling aims at the wrong band. And the generator's
  abstention rises steeply with distance (non-NONE per 25 in the banded arm: 12, 5, 0, 2). The
  critic killed 3 of the 8 correct recoveries; as configured it costs more than it saves.

**v0.2.** Sealed run 2026-09-14 over a harder corpus: 96 notes, bridges written obliquely on both
sides by two model families (Claude Haiku and a local Qwen 2.5 7B), shape-matched decoys, a
paraphrase-leak judge, two critics. Eight bridges failed the leak rule and were excluded; 16 remain.

- **H1, selection: supported again.** 6 of 16 planted recovered, 0 of 12 decoys survive, Fisher
  p = 0.021; the generator abstained on 10 of 12 decoys and 33 of 36 random pairs.
- **H4, partner-domain filler control: passed, and it is not a recombination test.** 0 of 16 with
  a mechanism-free filler (p = 0.009). Asked to connect a note to an unrelated note, the model
  correctly says NONE; that says nothing about whether the second note was needed.
- **H3, two notes beat one note: inverted.** Single-note reflection recovered 8 of 16, the two-note
  oracle 6 of 16 (p = 0.86), including five bridges the oracle had marked NONE. The planted
  mechanisms are principles a capable model reads off one note's ingredients.
- **H2, near-in-embedding sampling: null at 300 draws.** 2 planted card pairs against 1.09
  expected (p = 0.30). The pool it samples from is enriched 2.7-fold; detecting that needs about
  1,500 draws per arm.
- **Decision.** SIGNAL by the preregistered rule (H1 and H4), for a reason the rule did not test.
  Recombination is not demonstrated. We report both sentences together.
- **Exploratory X5, not preregistered.** The single-note prompt, run over every note, answered on
  23 of 23 fillers, 21 of 21 decoy notes and 31 of 32 bridge notes: its NONE permission is inert,
  so the single-note arm measures compliance, not knowledge. Cost $15.05.

```
$ daydreamd run-all experiments/micro/config.yaml

  snapshot   60 notes frozen, corpus sha <sha>              $<cost>
  cards      <n> concept cards (haiku)                      $<cost>
  embed      <n> x 384, all-MiniLM-L6-v2, local             $0.00
  sample     S0 60 · B1 100 · B3 100 · B6 50 · B4 24        $0.00
  generate   <n> units, NONE on <pct>%                      $<cost>
  critic     <n> judged, <pct>% killed                      $<cost>
  dupgate    <n> survivors, <n> already in corpus           $0.00
  match      planted units matched against gold             $<cost>
  stats      T1..T6 written, permutation p = <p>

  tables → experiments/runs/public/<date>_micro/tables/
```

*The transcript above is the shape of a run, not a result. Placeholders in angle brackets stay
until the pre-registered run has been executed and the values are read from its logs.*

## What a morning looks like

```markdown
# morning.md (illustrative example, not a run output)

## 1. Refund spikes after promo launches are card-testing runs
**Mechanism.** Rings validate stolen cards with small purchases and fast refunds; the refund
queue sees them 30 to 60 days before the chargebacks do.
**Check this week.** Flag refunds requested within 48h on orders whose payment method is under
7 days old. Compare against chargebacks in 60 days.
Sources: `ops-refund-queue.md` × `fraud-card-testing.md` · distance 0.81 · critic: keep

- [ ] KEEP  - [ ] KNOWN
```

## Try it in 60 seconds

```bash
git clone https://github.com/caraulani/llm-daydreaming && cd llm-daydreaming
uv run daydreamd run-all experiments/smoke/config.yaml   # tiny end-to-end run, real model calls
uv run daydreamd stats <run-dir> experiments/smoke/config.yaml
```

Or paste this into Claude Code:

```
Clone https://github.com/caraulani/llm-daydreaming, run `make setup && make test`, then run
`make smoke` and show me experiments/runs/public/*_smoke/tables/summary.md.
```

## The experiment (v0.1)

The first version does not run over anyone's private notes. It runs over a **synthetic corpus
with planted ground truth**: 60 working notes of a fictional solo builder across 6 domains, into
which 12 hand-authored cross-domain bridges were planted (two notes per bridge, neither naming
the other domain or the mechanism), plus 6 decoy pairs that share vocabulary and no mechanism.
The bridge specs were written by the experimenter, with Claude as a disclosed writing assistant,
and sealed with the preregistration before any note was generated. A leakage check guarantees no
6-gram of any gold connection appears in any note. Everything is public and reproducible.

| Arm | What it tests | Units |
|---|---|---|
| **S0 oracle** | generator + critic when handed the right two notes (12 planted, 6 decoy, 42 random cross-domain pairs); the sampler is out of the loop | 60 |
| **B1 random** | uniform random card pairs; the stimulus control | 100 |
| **B3 banded** | 25 card pairs per embedding-distance band (Q1, Q2-3, Q4, top 5%) | 100 |
| **B6 anchor + remote** | one card from the densest region + one at Q4 or farther (Uzzi-shaped) | 50 |
| **B4 reflection** | one bridge note alone, "state an implication not written down"; the incubation control | 24 |

Same generator prompt for every pair arm, `NONE` permitted, structured output. A binary critic
(Haiku-class) kills restatements, uncheckable implications, and generic links. A retrieval gate
marks survivors that already exist in the corpus. Planted units are matched against gold by a
grounded entailment judge with the gold in context, reported next to the cosine to gold.

**Metrics.** Sampler enrichment (planted pairs drawn vs the hypergeometric base rate); generator
recall on planted pairs; specificity (`NONE` rate on decoys and random pairs; false positives
after the critic); single-note recall (expected near zero); a 10,000-shuffle label-permutation
null on the oracle set; Wilson intervals everywhere; measured cost per arm and per recovered
bridge. Non-planted survivors are saved as exploratory finds for manual review and never counted.

## Results

Pre-registered in [PREREGISTRATION.md](PREREGISTRATION.md) (v0.1) and
[PREREGISTRATION-v0.2.md](PREREGISTRATION-v0.2.md) (v0.2). Sealed runs `2026-09-13_micro` and
`2026-09-14_micro_v0_2`; every value below is read from `results/public/<run>/` and the command
that produces it is listed so nobody has to trust us.

**v0.1 (`results/public/2026-09-13_micro/`)**

| Table | Question | Result | Command |
|---|---|---|---|
| T1 | corpus: notes, cards, bridges, decoys, leakage | 60 notes, 328 cards, 12 bridges, 6 decoys, 0 leakage failures | `make reproduce` |
| T2 | does distance-forcing draw planted pairs above base rate? | no: random 1, banded 1, anchor+remote 0 planted pairs (expected 0.65), p = 0.48 | `make reproduce` |
| T3 | given the right two notes, does generator + critic recover the bridge and reject decoys? | 8 of 12 recovered [39, 86]; 0 of 6 decoys survive; Fisher p = 0.011 | `make reproduce` |
| T4 | per arm: NONE, kill, survivors, bridges recovered, cost | NONE 67 to 96% on pair arms; 36 exploratory survivors; $33.62 list price for the run | `make reproduce` |
| T5 | permutation null over the oracle set | 5 planted survivors vs 2.2 expected, p = 0.032 | `make reproduce` |
| T6 | two notes vs one note on the same bridges | 8 of 12 vs 4 of 12, Fisher p = 0.11, not significant | `make reproduce` |

**v0.2 (`results/public/2026-09-14_micro_v0_2/`)**

| Table | Question | Result | Command |
|---|---|---|---|
| T1 | corpus | 96 notes, 483 cards, 16 planted bridges (8 excluded), 12 decoys, 115,345 cross-note card pairs | `make reproduce` |
| T2 | does near, cross-domain sampling draw planted pairs above base rate? | no at 300 draws: B7 2, B1 2 (expected 1.09), p = 0.30 | `make reproduce` |
| T3 | given the right two notes, does generator + critic recover the bridge and reject decoys? | 6 of 16 recovered [18, 61]; 0 of 12 decoys survive; Fisher p = 0.021 | `make reproduce` |
| T4 | per arm: NONE, kill, survivors, bridges recovered, cost | NONE 78 to 91% on pair arms, 3% on single notes; 75 exploratory survivors; $85.04 list price | `make reproduce` |
| T5 | permutation null over the oracle set | 5 planted survivors vs 1.26 expected, p = 0.0002 | `make reproduce` |
| T6 | two notes vs one note on the same bridges | 6 of 16 vs 8 of 16, inverted, p = 0.86 | `make reproduce` |
| T7 | bridge note + partner-domain filler (H4) | 0 of 16, p = 0.009; not a recombination test | `make reproduce` |
| T8 | two critics on the same generations | Haiku keeps 3 of 6 correct and 0 decoys; Sonnet keeps 5 of 6 and 1 decoy | `make reproduce` |

**Exploratory runs (not preregistered)**

| Run | Question | Result | Command |
|---|---|---|---|
| X1 | partner-domain filler control on v0.1 | 9 of 12 with the true pair, 1 of 12 with the filler, p = 0.0014 | `make reproduce` |
| X3 | near, cross-domain sampler on v0.1 | 2 planted in 100 (0.6 expected, p = 0.13); far bands NONE on 50 of 50 | `make reproduce` |
| X4 | Sonnet critic on the v0.1 generations | kills 3 of 8 correct recoveries and keeps the decoy | `make reproduce` |
| X5 | single-note prompt over every v0.2 note | answers on 23/23 fillers, 21/21 decoy notes, 31/32 bridge notes; 6 of 16 mechanisms from one note | `make reproduce` |

`make reproduce` rebuilds every table from the committed run outputs with no model call.

**What we claim after two runs, and no more.** Sentences of the form "on a synthetic corpus with
12 planted bridges, the oracle arm recovered 8 of 12 (Wilson 39 to 86 percent), against 0 of 6
decoy false positives, Fisher p = 0.011", and "on 16 oblique bridges, 6 of 16 against 0 of 12,
p = 0.021, while single-note reflection recovered 8 of 16". Not "novel ideas", not "discovers",
not a lead-time number, not a cost headline that was not read from logs, not anything about human
insight, not recombination. v0.1 was null by its rule and ships as a null; v0.2 was signal by its
rule and ships with the sentence that the rule's recombination test was not one.

## Privacy

Nothing here needs your notes. When you point it at your own corpus (Track C, `experiments/
private/`), embeddings are computed locally, the run directory is gitignored, the manifest can
be anonymised to SHAs, and the only model calls are the ones you configure with your own key or
subscription. No telemetry.

## Architecture

```
corpus adapter → snapshot (sha) → concept cards (cheap model) → local embeddings
      → sampler (S0 | B1 | B3 | B6 | B4) → generator (NONE permitted, JSON)
      → binary critic → retrieval dupgate → [match vs gold | owner-blind pack] → stats
```

| Path | Purpose |
|---|---|
| `src/daydreamd/core/` | one module per stage, plus `stats.py` |
| `src/daydreamd/synth/` | synthetic corpus: specs, leakage check, note writer |
| `src/daydreamd/eval/` | metrics, permutation nulls, planted-bridge recovery |
| `src/daydreamd/adapters/` | synthetic, Claude Code memory, markdown folder, arXiv; Obsidian/codebase/Zotero stubs |
| `src/daydreamd/backends/` | `claude-cli`, `anthropic`, `fake` (tests), `ollama` (stub) |
| `prompts/` | every prompt verbatim, versioned; SHAs land in `metadata.yaml` |
| `data/synth/v0.1/` | hand-authored `bridges.yaml`, `decoys.yaml`, `fillers.yaml`; generated `notes/`, `manifest.json`, `gold.json` |
| `experiments/` | arm configs, `micro/` (pre-registered), `smoke/`, `runs/` |
| `paper/` | `paper.md` and the reproducibility checklist |
| `design/` | one ADR per load-bearing decision |
| `registry/` | public dream registry (Track B) |

## Development

```bash
git clone https://github.com/caraulani/llm-daydreaming && cd llm-daydreaming
make setup        # uv sync
make test         # pytest, offline, fake backend
make lint         # ruff
make smoke        # tiny real run on the synthetic corpus
```

## Citing

See [CITATION.cff](CITATION.cff) (GitHub's "Cite this repository" button uses it). Archived on
Zenodo: concept DOI [10.5281/zenodo.22746627](https://doi.org/10.5281/zenodo.22746627) (latest
release), v0.2.0 DOI [10.5281/zenodo.22746628](https://doi.org/10.5281/zenodo.22746628).

```bibtex
@software{caraulani2026daydreamd,
  author  = {Caraulani, Julian},
  title   = {daydreamd: the LLM daydreaming loop, evaluated},
  year    = {2026},
  version = {0.2.0},
  doi     = {10.5281/zenodo.22746627},
  url     = {https://github.com/caraulani/llm-daydreaming}
}
```

## License

Code: MIT ([LICENSE](LICENSE)). Paper, prompts, synthetic corpus and results: CC BY 4.0
([LICENSE-CC-BY-4.0](LICENSE-CC-BY-4.0)). See [LICENSING.md](LICENSING.md).

## Verifying the seal

The preregistration precedes the data three ways: git ancestry (checked in CI), OpenTimestamps
proofs anchored in Bitcoin (v0.1 attests in block 966837), and signed commits. Recipe in
[docs/verify-seal.md](docs/verify-seal.md).

## Read next

[paper/paper.md](paper/paper.md) · [PREREGISTRATION.md](PREREGISTRATION.md) ·
[design/](design/) · [registry/](registry/) · [docs/](docs/) · [ROADMAP.md](ROADMAP.md)
