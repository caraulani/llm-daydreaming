---
name: Replication report
about: You ran the preregistered protocol on your own corpus. Report it, positive or null.
title: "replication: <YYYY-MM-DD>_<model-snapshot>"
labels: replication
assignees: ''
---

## Setup

- Corpus: <!-- type, number of documents, date range; no text -->
- Arms run: <!-- e.g. B1, B3, B4, B6 -->
- Generator / critic / judge snapshot IDs:
- Number of pairs per arm:
- Rater(s): <!-- owner only, or others; blind protocol followed? -->

## Result

| Arm | Pairs | NONE % | Critic kill % | Corpus-duplicate % | Survivors | KEEP % | KNOWN % |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

- Fisher exact p (winner vs B1):
- Permutation p (10,000 shuffles):
- Winner above B4: yes / no

## Deviations from `PREREGISTRATION.md`

<!-- List every one. A null result with no deviations is a valid and welcome contribution. -->

## Artifacts

- [ ] I will open a PR adding `experiments/runs/<YYYY-MM-DD>_<model-snapshot>/` with `metadata.yaml`, `raw_outputs.jsonl` (redacted if private), `verdicts.jsonl`, `cost.json`.
