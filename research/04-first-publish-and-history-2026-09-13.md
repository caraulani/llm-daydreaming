# First publish and history discipline for `caraulani/llm-daydreaming`

Researched 2026-09-13 from live commit histories (GitHub API), release pages, READMEs and docs. Repo name `llm-daydreaming`, tool `daydreamd`.

## 0. What the histories actually show

**Ed's dojo.md (edholofy/dojo.md).** First commit `4ebe65b` on 2026-02-27 13:34 is `feat: initial release, dojo.md v0.1.0` and it already contained `paper.md`, `CLAUDE.md`, code and README in one shot. 45 commits in the first 48 hours, all conventional-commit style (`feat:`, `fix:`, `docs:`, `chore:`), none signed. `paper.md` was touched three times ever: the initial dump, a README rewrite the next day, and `fix: correct author name in paper.md from Holofy to Cristea`. No tags, no GitHub releases at all, even though npm versions went 0.1.0 to 0.3.2 in two days (versions were bumped via `chore:` commits). Results entered history as README leaderboard text (`feat: add GPT-5.2 to leaderboard`), not as data files. Copy: paper in the first push, conventional commit prefixes, product README. Avoid: unsigned history, no tags, results as prose with no raw outputs, a paper whose numbers cannot be traced to a run.

**Ideation Arena (foss12138/Research-Ideation-Arena).** One commit, `Initial release`, 2026-08-30, with a BOM character in the message. A single-squash history: zero audit trail. Avoid.

**AgentIdeaBench (HKUST-KnowComp/AgentIdeaBench).** `Initial commit` 2026-09-07 (signed), then six commits on 2026-09-12 in dependency order: pipeline, experiment scripts, "Add redacted data release and its data card", "Add paper figure and statistics scripts with their input artifacts", "Add README, licenses and citation metadata", leaderboard, all merged via PR #1 `initial-release`. This is the cleanest first-publish shape among the 2026 benchmark repos: staged commits that each add one layer, results with the inputs that produced them. Copy the ordering and the "redacted data release + data card" commit.

**Si et al. AI-Researcher (NoviScl/AI-Researcher).** History is a lab notebook: `idea gen 1k`, `analyze idea 1k`, `binary ranking`, `swiss tournament reranking`, dated May to June 2024, one step per commit. Not pretty, but every step of the pipeline is a dated commit before the paper existed (paper arXiv Sept 2024). That is what "history as audit trail" looks like in practice.

**Letta sleep-time-compute.** `Initial commit` 2025-04-18, then three signed `Update README.md` commits. Code to reproduce but no raw outputs; datasets on Hugging Face; MIT; BibTeX block in README. A paper-companion repo, not a living project. Copy: HF for datasets, citation block. Avoid: nothing reproducible without re-running APIs.

**karpathy/nanoGPT and llm.c.** `first very bad commit` (2022-12-28) and `first commit of just the reference cpu fp32 gpt2 training` (2024-04-08). Honest, descriptive first commits; MIT added as its own commit the next day; results in README as a table plus a loss curve figure; lineage in one sentence: "It is a rewrite of minGPT that prioritizes teeth over education." External PRs merged within hours (signed merges only). Copy: descriptive first commit, one-sentence lineage, results table with figure.

**idea-mill (sgoedecke).** Four commits in 90 minutes on 2025-07-10 (`first commit`, `initial`, `readme`, `reslience`), no license, no Gwern credit in the README, no outputs. A prototype, not a publication. Avoid all of it except as a citation.

**zby/DayDreamingDayDreaming.** Long, messy but real history (hundreds of commits through 2025-10-18), Apache-2.0, `data/1_raw/`, `data/results/`, `data/cohorts/<id>/reports/` committed, model cutoff stated ("limited runs to models that were publicly accessible before mid-2025"), one-line Gwern credit in the description. Copy: committed results folders and the stated model cutoff. Avoid: no tags, no protocol before results.

**Vault Daydream (glebis/claude-skills/daydream).** MIT, credit is exactly one line: "Inspired by Gwern's LLM Daydreaming." No evaluation, no outputs.

**HindSight (2603.15164) and Discovery by Dreaming (2607.16256).** No code repository found for either (checked arXiv abstract pages and search). Note this in the paper: neither temporal-holdout reference point ships code.

**agentdojo.** Every version is a GitHub Release with a Features / Breaking Changes / Bug Fixes body (v0.1.31 to v0.1.35, 2025). Copy the release-notes shape.

**anthropics/evals.** Data-only repo, CC-BY-4.0, BibTeX with DOI in README, content warning. Copy: the licence for data and the citation block with DOI.

## 1. Preregistration in git: what exists

- **gkaguirrelab/preregistrations**: a lab commits preregistration documents to a public repo as "a date-and-time stamped record" and writes, verbatim, "It is apparently possible to tinker with the date/time stamp of an uploaded file on GitHub. We promise not to do this." That sentence is the state of the art for most labs: trust, not proof.
- **i-staykov/proj-price-discovery**: root `PREREGISTRATION.md`, README status line "The analysis is preregistered ... No primary fit has run", and issue #68 requires that the preregistration commits "are ancestors of, and older than, the first commit touching `results/primary/`", checked in CI with `fetch-depth: 0`, plus a fixed outcome vocabulary ("supported, inconclusive or falsified") and a deviations entry locked into the plan. This is the strongest git-native pattern found: ancestry is the proof, and CI enforces it.
- **OpenTimestamps**: the file-level client (`ots stamp FILE` producing `FILE.ots`) is stable. The git integration (`ots-git-gpg-wrapper`) requires GPG-signed commits, is not described as production-ready, and the `--wait` path needs a script edit. Proofs are pending for hours until a Bitcoin block includes the calendar's aggregate; `ots upgrade` later completes them; `ots verify` checks them offline afterwards.
- No repo was found that combines all three (prereg file, `.ots` proof, ancestry check). Doing all three is cheap and, as far as this sweep found, unprecedented in an LLM-ideation repo.

**Practical conclusion.** Use file-level OTS on `PREREGISTRATION.md` and the answer key, not the git wrapper. Use git ancestry plus a CI job as the second proof. Use signed commits (SSH signing is supported by GitHub; enable vigilant mode so unsigned commits show "Unverified") as the third. Three independent timestamps: Bitcoin, GitHub's server time on push, and your signing key.

## 2. Recommended commit-by-commit plan for the first push

Principle: nothing is pushed until the experiment has run, but the local history is written now, in dependency order, so that when it is pushed the ancestry reads seal → corpus → run → results → paper. Each commit adds one layer and is signed. Commit messages use conventional prefixes like dojo.md, but each body says what the commit proves.

```
1  chore: repository skeleton (license split, CI, governance, ADRs, docs)
     LICENSE, LICENSE-CC-BY-4.0, LICENSING.md, CITATION.cff, CHANGELOG.md,
     CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, ROADMAP.md, .github/,
     design/ADR-001..013, docs/, registry/, data/README.md, data/DATASHEET_TEMPLATE.md,
     research/ (all sweeps + BRIEF + lineage), .gitignore, pyproject.toml, uv.lock,
     .python-version, Makefile, AGENTS.md, CLAUDE.md
     Body: "No code, no data, no results. Establishes licences and decisions before any run."

2  feat: pipeline code, prompts and offline tests (fake backend)
     src/daydreamd/**, prompts/*.md, tests/**, experiments/*/config.yaml,
     experiments/runs/README.md, results/README.md, examples/
     Body: "16 tests pass with DAYDREAMD_BACKEND=fake; no model was called."

3  docs: preregistration and sealed answer key
     PREREGISTRATION.md, data/synth/v0.1/bridges.yaml, data/synth/v0.1/decoys.yaml,
     data/synth/v0.1/fillers.yaml, data/synth/v0.1/datasheet.md
     Body: "SHA-256 of each file listed here. Stamped with OpenTimestamps in the next commit."
     Tag after this commit: v0.1.0-prereg  (annotated, signed)

4  chore: OpenTimestamps proofs for the preregistration and answer key
     PREREGISTRATION.md.ots, bridges.yaml.ots, decoys.yaml.ots
     Body: "Pending proofs; upgraded in a later commit once anchored in a Bitcoin block."

5  data: synthetic corpus v0.1 (60 notes) and frozen manifest
     data/synth/v0.1/notes/*.md, manifest.json, MANIFEST.sha256, build/ (raw note-writer
     responses), leakage-check output
     Body: "Notes written by <model snapshot id> on <date>; 0 gold 6-grams found in notes."

6  data: micro-experiment raw outputs, <date>_<generator snapshot>
     experiments/runs/public/<date>_micro/{metadata.yaml, cards.jsonl, embeddings sha,
     pairs.jsonl, generations.jsonl, critic.jsonl, dupgate.jsonl, match.jsonl, cost.json}
     Body: "Every model call, verbatim. Model ids from logs. Cost read from logs."

7  results: tables T1..T6 regenerated from committed outputs (make reproduce)
     results/public/<date>_micro/tables/*.csv, *.md, figures/
     Body: "make reproduce is deterministic from commit 6; CI re-runs it with no keys."

8  docs: fill PREREGISTRATION.md seal fields and DEVIATIONS (if any)
     PREREG_COMMIT = <sha of 3>, CORPUS_MANIFEST_SHA256 = <from 5>
     Body: this is the only edit to PREREGISTRATION.md after the seal, confined to the
     two TBD fields and the DEVIATIONS section; CI asserts commit 3 is an ancestor of 6.

9  paper: v0.1 draft with results tables filled from results/ (numbers linked to commit 7)
     paper/paper.md, paper/refs.bib, paper/CHECKLIST.md, paper/figures/*
     Body: "Abstract follows the pre-committed template; no claim outside Section 14."

10 docs: README with lineage, quick start, results table and citation
     README.md, hero.png
     Tag after this commit: v0.1.0 (annotated, signed) → GitHub Release with agentdojo-style
     notes → Zenodo DOI → paste DOI into CITATION.cff and README in commit 11.

11 chore: upgrade OTS proofs, add Zenodo DOI, CHANGELOG 0.1.0
```

Then, and only then, `git push origin main --tags`. The first push lands 11 signed commits whose ancestry is the audit trail. GitHub's push timestamp becomes the second timestamp, the OTS proofs the first, the tag signature the third.

Why not push the skeleton earlier: dojo.md's history shows what a live-published repo looks like (45 commits in two days, fixes to fixes). That is fine for a product; for a research artifact the reader should be able to read the log top to bottom and see the protocol precede the data. Pushing later costs nothing in priority because the OTS proof on commit 3 already establishes the date independent of GitHub.

## 3. "Do not push yet" checklist

All of these must be true before the first push:

- [ ] Commit 3 exists, is signed, and its files' SHA-256 values appear in PREREGISTRATION.md Section 15.
- [ ] `ots verify PREREGISTRATION.md.ots` returns at least "pending" attestation from two calendars (upgrade can come later).
- [ ] Commit 6 (raw outputs) is a descendant of commit 3, and no file under `experiments/runs/public/` exists in any commit before 3. Add `.github/workflows/prereg-ancestry.yml` with `fetch-depth: 0` that fails otherwise.
- [ ] `make reproduce` in a clean checkout with no API keys regenerates every table byte-identically (`git diff --exit-code results/`).
- [ ] Every number in `paper/paper.md` and `README.md` matches a cell in `results/` (grep the tables; no hand-typed numbers).
- [ ] Every model id in `metadata.yaml` is a dated snapshot id read from the `claude -p` JSON (`claude-haiku-4-5-20251001` style), never an alias.
- [ ] Cost figures come from `cost.json`, not estimates.
- [ ] `git log --show-signature` shows every commit Verified; vigilant mode on for the account.
- [ ] No file matches secret patterns (`git grep -iE 'sk-ant|api[_-]?key|password'` is empty); no absolute paths under `/Users/julian` in any committed file (`git grep '/Users/julian'` empty).
- [ ] `.gitignore` excludes `.venv/`, caches, `*.npy` embeddings, `experiments/runs/private/`, `data/private/`.
- [ ] LICENSE (MIT) and LICENSE-CC-BY-4.0 in the first commit; CITATION.cff validates.
- [ ] README Lineage section present with links to Gwern, idea-mill, zby, Vault Daydream, and the statement of what is new.
- [ ] Abstract contains only sentences permitted by PREREGISTRATION.md Section 14.
- [ ] Repo description and topics set on GitHub before the push (description is indexed immediately).

## 4. What to exclude, and how to handle run artifacts

Commit (public run): prompts verbatim; every raw model response (jsonl, one line per call, with request hash, model snapshot id, timestamp, usage); cards; pair lists; judge outputs; `cost.json`; tables and figures; the synthetic corpus and its answer key; the leakage-check log. AgentIdeaBench committed "paper figure and statistics scripts with their input artifacts" and a "redacted data release"; zby committed `data/results/` and per-cohort reports. This is the norm among the repos that are taken seriously.

Do not commit: `.venv/`, `__pycache__/`, ruff/pytest caches, embedding matrices (`*.npy`, recompute from committed text; commit only their SHA), model weights (the MiniLM model downloads from Hugging Face), any private corpus or private run, `.env`, absolute local paths, IDE files. If a run ever exceeds ~50 MB of jsonl, move the raw outputs to a GitHub Release asset or a Hugging Face dataset (Letta's pattern) and keep only `metadata.yaml`, hashes and tables in git; do not use Git LFS for a research repo (clone friction, bandwidth quotas).

Keep sizes honest: the v0.1 run is roughly 360 generations plus 60 notes plus 200 cards; well under 5 MB. Commit it in full.

## 5. Homage and lineage wording

Patterns found: nanoGPT uses one sentence ("It is a rewrite of minGPT that prioritizes teeth over education"); Vault Daydream uses one line ("Inspired by Gwern's LLM Daydreaming"); zby puts it in the repo description; lucidrains puts a Citations section with BibTeX at the bottom and credits inline per feature; anthropics/evals gives a BibTeX block with DOI. For a repo whose whole premise is "someone proposed this, several people built it, nobody measured it", the honest form is a table, not a sentence.

Recommended README section, placed before Quick Start:

```markdown
## Lineage

This repository does not propose the day-dreaming loop. It measures one part of it.

| Year | Who | What | What it left open |
|---|---|---|---|
| 2025-07 | Gwern, [LLM Daydreaming](https://gwern.net/ai-daydreaming) | Proposed the day-dreaming loop: sample two facts, ask for a connection, keep it if a critic calls it interesting | No implementation, no evaluation |
| 2025-07 | Sean Goedecke, [idea-mill](https://github.com/sgoedecke/idea-mill) | First prototype, one day after the essay; author's verdict: "pretty half-assed", yet "a few genuinely novel ideas" | Hand-written facts, no filter evaluation |
| 2025-07 to 10 | Zbigniew Łukasiak, [DayDreamingDayDreaming](https://github.com/zby/DayDreamingDayDreaming) | Temporal-novelty pilot with pre-cutoff models | Stopped at two stated walls: no search algorithm, no domain-agnostic novelty verifier |
| 2025 to 26 | Gleb Kalinin, [Vault Daydream](https://github.com/glebis/claude-skills/tree/main/daydream) | Obsidian implementation, generator plus critic, threshold-only QC | No evaluation |
| 2026-07 | Zahn, Evans, Eagleman, [Discovery by Dreaming](https://arxiv.org/abs/2607.16256) | Cross-domain recombination in artificial memory, validated on public literature | No critic, no distance control, leaky holdout, no code |
| 2026-09 | this repo | A preregistered, ground-truth test of whether the selection step works | Everything after v0.1 (see ROADMAP) |

Citations for all of the above are in `paper/refs.bib` and `CITATION.cff` (`references`).
```

Add the same list to `CITATION.cff` under `references:` (cff 1.2.0 supports it) so the "Cite this repository" button carries the lineage, and open the paper's introduction with the Gwern sentence and the three builders in the first paragraph, as already planned.

## 6. Repos studied

| Repo | Copy | Avoid |
|---|---|---|
| [edholofy/dojo.md](https://github.com/edholofy/dojo.md) | paper.md in first push; conventional commit prefixes; product README with hero and transcript | unsigned; no tags/releases; results as prose; 45 fix commits in 48 h |
| [HKUST-KnowComp/AgentIdeaBench](https://github.com/HKUST-KnowComp/AgentIdeaBench) | staged first-release commits in dependency order; "redacted data release and its data card"; figures with input artifacts; PR-merged initial release | none notable |
| [foss12138/Research-Ideation-Arena](https://github.com/foss12138/Research-Ideation-Arena) | nothing | single squashed "Initial release" |
| [NoviScl/AI-Researcher](https://github.com/NoviScl/AI-Researcher) | one pipeline step per dated commit, before the paper | terse messages, no protocol file |
| [letta-ai/sleep-time-compute](https://github.com/letta-ai/sleep-time-compute) | HF datasets; BibTeX block; MIT | no raw outputs |
| [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT), [llm.c](https://github.com/karpathy/llm.c) | descriptive first commit; one-sentence lineage; results table plus figure | unsigned commits |
| [sgoedecke/idea-mill](https://github.com/sgoedecke/idea-mill) | citation only | no licence, no credit, no outputs |
| [zby/DayDreamingDayDreaming](https://github.com/zby/DayDreamingDayDreaming) | committed `data/results/` and cohort reports; stated model cutoff; Apache-2.0 | no tags, no protocol before results |
| [glebis/claude-skills/daydream](https://github.com/glebis/claude-skills/tree/main/daydream) | one-line credit style | no evaluation |
| [ethz-spylab/agentdojo](https://github.com/ethz-spylab/agentdojo) | Release notes shape (Features / Breaking / Fixes) per version | none |
| [anthropics/evals](https://github.com/anthropics/evals) | CC-BY-4.0 for data; BibTeX with DOI; content warning | none |
| [gkaguirrelab/preregistrations](https://github.com/gkaguirrelab/preregistrations) | commit prereg to git as dated record | trust-only ("we promise not to") |
| [i-staykov/proj-price-discovery](https://github.com/i-staykov/proj-price-discovery) | root PREREGISTRATION.md; README status line; ancestry check in CI with fetch-depth 0; fixed outcome vocabulary; deviations locked | none |
| [opentimestamps-client](https://github.com/opentimestamps/opentimestamps-client) | file-level `ots stamp` / `ots upgrade` / `ots verify` | git GPG wrapper (not production-ready) |
| HindSight 2603.15164, Discovery by Dreaming 2607.16256 | cite | no code found for either |

## 7. Two things noticed outside scope

- The GitHub API is nearly rate-limited from this IP (5 calls left of 60/h); the parent should not rely on unauthenticated API calls for the push step.
- dojo.md fixed its own author line two days after publishing (`fix: correct author name in paper.md from Holofy to Cristea`). Confirm "Julian Caraulani" before commit 3, since the sealed files carry the author name.
