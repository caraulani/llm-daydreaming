# Publishing checklist

The bar: a researcher at a frontier lab opens the repo and finds nothing missing. Derived from `research/01-publishing-practice.md` (verified 2026-09-13). Status is updated in place; this file is the honest state of the repo.

Legend: [x] done, [ ] not done, [~] partial.

## MUST

- [~] README in the Papers-with-Code shape: official-implementation line, hero figure, requirements, exact command per experiment, results table with the command that regenerates each row, citation, license. (Scaffolded; results rows wait on the first run.)
- [x] `CITATION.cff` at root, `cff-version 1.2.0`, `type: software`. `preferred-citation` placeholder ready for the arXiv ID.
- [x] License split stated: MIT for code (`LICENSE`), CC BY 4.0 for paper, data, registry, docs (`LICENSE-CC-BY-4.0`, `LICENSING.md`).
- [~] Paper as a first-class artifact: `paper/paper.md` as source. LaTeX build for arXiv not yet generated.
- [~] LLM reproducibility hygiene: immutable snapshot IDs, access dates, sampling parameters, prompts committed verbatim, raw outputs committed, judge disclosed. (Structure in place: `prompts/`, `experiments/runs/`, `docs/contamination.md`. No run committed yet.)
- [~] Pinned environment: `pyproject.toml`, `uv.lock`, `.python-version`. (Pending code agent.)
- [x] CI on push and PR; `make reproduce` workflow regenerates `results/` from committed outputs with no API keys and fails on drift.
- [ ] `PREREGISTRATION.md` frozen before results, then registered on OSF with a DOI. (File pending; OSF registration is a manual step.)
- [ ] Signed commits and OpenTimestamps on `PREREGISTRATION.md` and release tarballs.
- [x] Negative-result commitment: written into `ROADMAP.md` gates, `PREREGISTRATION.md`, and the replication template ("positive or null").
- [~] `AGENTS.md` and `CLAUDE.md`. (Pending code agent.)
- [ ] GitHub topics and a one-sentence repo description. (Set on GitHub after the repo is created.)

## SHOULD

- [x] `CONTRIBUTING.md` with issue-first policy, extensions outside core, agent-PR policy, DCO.
- [x] `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1).
- [x] `SECURITY.md` with the privacy promise and what counts as a privacy bug.
- [x] `CHANGELOG.md` in Keep a Changelog format. Semver tags and GitHub Releases start at v0.1.0.
- [ ] Zenodo DOI per release. Enable the GitHub integration before the first tagged release. Note: `.zenodo.json` silently overrides `CITATION.cff`; do not add one.
- [x] `design/` ADRs, one per load-bearing decision (13 so far).
- [x] Registry convention: PR-based, one directory per entry, metadata plus README plus timestamped dreams (`registry/README.md`).
- [x] Datasheet for the released corpus (`data/synth/v0.1/datasheet.md`, build-time fields marked TBD).
- [ ] Hugging Face dataset mirror with the datasheet as the card.
- [ ] NeurIPS-style checklist answered in `paper/CHECKLIST.md`, including the LLM-usage declaration. (Pending paper agent.)
- [x] Cost column in every results table (specified in templates and `metadata.yaml`).
- [x] Contamination statement template (`docs/contamination.md`).
- [x] Human-eval protocol write-up (`docs/human-eval-protocol.md`).
- [ ] Hugging Face Papers page after arXiv. (Papers with Code is gone; do not link it.)
- [~] `docs/` with an extending page (`docs/extending.md`). mkdocs site not built.

## NICE

- [ ] REUSE/SPDX headers per file and `reuse lint` in CI.
- [ ] `llms.txt` on the project site.
- [ ] MCP server exposing `dream`, `review`, `verdict`, plus a SKILL.md.
- [x] Issue templates (bug, adapter, registry entry, replication) and a PR template.
- [x] `ROADMAP.md`.
- [ ] Devcontainer.
- [ ] Model card: N/A, no fine-tuned component planned.

## Time-sensitive

- [ ] arXiv endorsement. Since 2026-01-21, a first-time cs.* submitter without an institutional email needs a personal endorsement from an established cs.CL, cs.AI, or cs.HC author. Ask weeks before the intended submission.
- [ ] arXiv license: choose CC BY 4.0 at submission. It is irrevocable per version.
- [ ] Show HN: lead with the one-line install and a sample `morning.md`. Paper-only posts are off-topic there.
