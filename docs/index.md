---
title: Home
description: "daydreamd by Julian Caraulani: an open implementation and preregistered test of Gwern's LLM daydreaming loop (the day-dreaming loop) over your own notes, Obsidian vaults and Claude Code memory."
---

# daydreamd: the LLM daydreaming loop, evaluated

*By [Julian Caraulani](https://github.com/caraulani), September 2026. An open implementation and preregistered test of Gwern's LLM daydreaming proposal (the day-dreaming loop) over your own notes: Obsidian vaults, Claude Code memory, any markdown folder. Code on [GitHub](https://github.com/caraulani/llm-daydreaming), archived with DOI [10.5281/zenodo.22746627](https://doi.org/10.5281/zenodo.22746627).*

**Your notes are full of connections you never made.** daydreamd looks for them while you sleep.

It is a local-first daemon that collides far-apart concepts from your own corpus, asks a model whether a genuine connection exists (with permission to say no), kills most of what comes back, and leaves the survivors in a `morning.md`. The research question is not whether a model can generate connections. It can, cheaply and endlessly. The question is whether anything can tell a real connection from a fluent one. This project is the test rig for that question, with ground truth planted by construction, a preregistered protocol, and every raw output committed.

Repo: `llm-daydreaming`. Tool and package: `daydreamd` (daydream plus the Unix daemon suffix).

## Lineage

This project does not propose the day-dreaming loop. It measures one part of it. The idea and the first builds belong to the people below; what this project adds is the missing measurement.

| Year | Who | What | What was missing |
|---|---|---|---|
| 2025 | [Gwern, "LLM Daydreaming"](https://gwern.net/ai-daydreaming) | proposed the day-dreaming loop: sample two facts, ask for a connection, keep the interesting ones, write them back | no implementation, no evaluation |
| 2025 | [Sean Goedecke, idea-mill](https://github.com/sgoedecke/idea-mill) | first prototype, one day after the essay; "a few genuinely novel ideas" | hand-written facts, no critic evaluation, no baselines |
| 2025 | [Zbigniew Lukasiak, DayDreamingDayDreaming](https://github.com/zby/DayDreamingDayDreaming) | first temporal-novelty pilot with pre-cutoff models | "I manually selected combinations"; "a domain-agnostic novelty verifier is the fundamental research bottleneck" |
| 2026 | [Vault Daydream](https://github.com/glebis/claude-skills) | Obsidian skill: vault pairs, generator plus critic, threshold, writeback | run on demand, no distance control, no evaluation |
| 2026 | [Oliver Zahn, James Evans and David Eagleman, "Discovery by Dreaming"](https://arxiv.org/abs/2607.16256) | recombination over public corpora, validated against 50,000 cross-field pairs and a 2026 holdout | no critic, no distance control, no private corpus; the holdout is not leakage-safe by the authors' own account |
| 2026 | this project | the selection step under a preregistered test with planted ground truth | real-corpus usefulness (Track C) and temporal validation (Track A) are still open |

The consolidation branch (Letta's sleep-time compute, Google's "Language Models Need Sleep", Anthropic's Dreams, OpenClaw's dreaming mode) reorganises memory. It does not generate. We build none of it. See the [paper](paper.md) for the full map.

## What we found

**v0.1.** Sealed run over the synthetic corpus, 2026-09-13, generator `claude-sonnet-5`:

- **H1, selection: supported.** Given the right two notes, the generator answered on 11 of 12 planted pairs and named the planted mechanism on 8 of 12; it stayed silent on 5 of 6 decoys and 34 of 42 random pairs, and no decoy answer survived the critic (Fisher p = 0.011).
- **H2, distance-forced sampling: null.** Banded sampling drew 1 planted pair in 100, anchor plus remote drew 0 in 50, random drew 1 in 100. Expected under chance: 0.65. Untestable at this base rate, and the post-hoc points the other way.
- **H3, two notes beat one note: not significant.** 8 of 12 vs 4 of 12, p = 0.11. All four single-note recoveries come from notes that state the mechanism in paraphrase, which the 6-gram leakage check cannot catch.
- **Decision.** By the preregistered rule this run reports no signal. We publish it anyway; that was the deal.
- **Exploratory X1.** Replace the true partner note with a mechanism-free filler from the same domain and recovery collapses: 9 of 12 with the real pair, 1 of 12 with the filler (Fisher p = 0.0014).
- **Post-hoc.** Every planted bridge's closest card pair sits in the nearest distance band (12 of 12): real bridges are domain-far but embedding-near, so far-band sampling aims at the wrong band. The critic killed 3 of the 8 correct recoveries.

**v0.2.** Sealed run 2026-09-14 over a harder corpus: 96 notes, bridges written obliquely on both sides by two model families (Claude Haiku and a local Qwen 2.5 7B), shape-matched decoys, a paraphrase-leak judge, two critics. Eight bridges failed the leak rule and were excluded; 16 remain.

- **H1, selection: supported again.** 6 of 16 planted recovered, 0 of 12 decoys survive, Fisher p = 0.021.
- **H4, partner-domain filler control: passed, and it is not a recombination test.** 0 of 16 with a mechanism-free filler (p = 0.009). Asked to connect a note to an unrelated note, the model correctly says NONE; that says nothing about whether the second note was needed.
- **H3, two notes beat one note: inverted.** Single-note reflection recovered 8 of 16, the two-note oracle 6 of 16 (p = 0.86). The planted mechanisms are principles a capable model reads off one note's ingredients.
- **H2, near-in-embedding sampling: null at 300 draws.** 2 planted card pairs against 1.09 expected (p = 0.30).
- **Decision.** SIGNAL by the preregistered rule (H1 and H4), for a reason the rule did not test. Recombination is not demonstrated. We report both sentences together.
- **Exploratory X5.** The single-note prompt, run over every note, answered on 23 of 23 fillers, 21 of 21 decoy notes and 31 of 32 bridge notes: its NONE permission is inert.

Full tables per run are under [Results](results/index.md); the protocols are under [Preregistration](preregistration/index.md); the reviewer's reading of each run is under [Research notes](research/index.md).

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

## Where to go next

| You want to | Read |
|---|---|
| The full argument, related work and every table | [Paper](paper.md) |
| What we promised to measure before we measured it | [Preregistration](preregistration/index.md) |
| Check that the protocol preceded the data | [Verify the seal](verify-seal.md) |
| Write an adapter or a backend | [Extending](extending.md) |
| Run the owner-blind scoring protocol on your own corpus | [Human-eval protocol](human-eval-protocol.md) |
| Cite this work | [Cite](cite.md) |

## Privacy in one paragraph

Corpus text is read from local paths, embedded on-device, and sent only to the model backend you configured. No telemetry. Private runs live under gitignored paths. If any of that is ever untrue, it is a security bug: see `SECURITY.md` in the repository.
