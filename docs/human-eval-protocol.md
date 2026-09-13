# Human evaluation protocol (Track C)

**Status: written, not yet run.** v0.1 uses a synthetic corpus with planted ground truth (ADR-013) and needs no human rater. This protocol is for Track C: owner-blind scoring over a private corpus, where the owner is the only competent judge of usefulness. It is written now so it can be preregistered before the first Track C run, and so anyone can run it on their own corpus.

## What it measures

Whether dreams produced by distance-forced pairing (B3, B6) are kept by the corpus owner more often than dreams produced by random pairing (B1) and by single-note reflection (B4), when the owner cannot tell which arm produced which dream.

It does not measure novelty against the world. That is a retrieval check (ADR-004), run separately.

## Why blind, and why binary

Strömel et al. (CHI 2024, N = 273) showed LLM narratives over personal data move engagement, attention and reward while leaving insight flat; self-report cannot separate enjoyment from insight. So: no rating scales, no "did you like it", no knowledge of which arm produced an item. Two binary marks per item (ADR-005).

## Roles

- **Owner (rater):** the person whose corpus was dreamed over. Scores blind.
- **Operator:** runs the pipeline, seals the key, unseals after scoring. May be the same person as the owner; the sealing procedure below is what keeps the two roles separate.

## Materials

1. `experiments/runs/<date>_<snapshot>/raw_outputs.jsonl`: every generated item, all arms, pre-critic (scoring pre-critic keeps power; critic kill rates near 85% would leave about 15 items per arm).
2. `pack.md`: the scoring pack. Items shuffled with a recorded seed, numbered, arm labels stripped, presented in batches of 20 as markdown checkboxes.
3. `key.json`: item number to arm and pair. Sealed before scoring (below).

## Sealing the key

Before the owner sees `pack.md`:

```bash
sha256sum key.json > key.sha256
git add key.sha256 pack.md          # commit the HASH and the pack, not the key
git commit -s -m "Seal Track C key for run <date>_<snapshot>"
```

Optionally `ots stamp key.sha256`. `key.json` stays out of git until scoring is done. The commit proves the assignment existed, unchanged, before any verdict.

## Rater instructions (verbatim, shown at the top of the pack)

> You will see short proposed connections between things in your own notes. For each one, mark two boxes independently.
>
> KEEP: I would act on this, or write it down. (Would you actually do something with it this week, or add it to your notes as a thought worth having? If not, leave it blank.)
>
> KNOWN: I already had this thought. (You had made this exact connection before, whether or not it is written anywhere.)
>
> Do not try to guess which items are "real". Do not rate how well-written an item is. Score in order, one batch of 20 at a time, and take a break between batches. There are no right answers.

## Procedure

1. Sitting 1: score all batches in order. Record start and end time per batch.
2. At least 24 hours later, sitting 2: re-score 30 items drawn at random (seed recorded) without seeing sitting-1 answers.
3. Operator unseals: `sha256sum -c key.sha256`, then commit `key.json` and the verdicts.
4. Compute and report.

## Analysis (preregistered per run)

- Yield per arm = P(KEEP and not KNOWN and not already-in-corpus), with counts.
- Primary test: one-sided Fisher exact, winner of {B3, B6} versus B1.
- Statistical null: shuffle arm labels across all scored items 10,000 times, recompute the yield gap, report the permutation p (ADR-006).
- Secondary: yield by distance band (Cochran-Armitage trend), NONE rate by band, KNOWN rate by arm, winner versus B4.
- Intra-rater agreement: Cohen's kappa on the 30 repeated items. Report it even if it is bad.
- Power note: 100 items per arm detects 30% versus 12% at alpha 0.05 with about 80% power. Fewer items means a wider interval, reported, not hidden.
- Signal means: permutation p below 0.05 for B3 or B6 against B1, and the winner above B4. Anything else is a null and is published as one.

## Reporting

- `verdicts.jsonl`: one line per item, with the unsealed arm label, both marks, sitting, timestamps.
- Tables T2 (per arm) and T3 (per band) in `results/`.
- Rater description: relationship to the corpus, time spent, breaks taken, deviations from this protocol.
- Raw data released in the same shape Si et al. released their human study data (redacted to hashes where the corpus is private).

## Multi-owner extension

The same protocol, one pack per owner over their own corpus, mixed-effects model with owner as a random effect. Five owners is the minimum before any generalisation claim. Compensation and consent are recorded per owner in the run's `metadata.yaml`; no IRB is claimed unless one was obtained.
