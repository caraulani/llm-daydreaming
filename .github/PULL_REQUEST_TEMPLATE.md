## What this changes

<!-- One paragraph. Link the issue this was discussed in. PRs without a prior issue are closed unless they are typo fixes. -->

Closes #

## Type

- [ ] Fix
- [ ] Core change (discussed in an issue first, see `CONTRIBUTING.md`)
- [ ] Adapter (in-tree only if on `ROADMAP.md`)
- [ ] Experiment run under `experiments/runs/<date>_<model-snapshot>/`
- [ ] Registry entry under `registry/entries/<date>_<slug>/`
- [ ] Docs, ADR, paper

## Checks

- [ ] `uv run ruff check .` passes
- [ ] `uv run pytest -q` passes with `DAYDREAMD_BACKEND=fake`
- [ ] `make reproduce` still regenerates `results/` unchanged (or this PR updates them and says why)
- [ ] No corpus text, dreams, or secrets in the diff
- [ ] Prompts changed? Then the prompt file's version header is bumped and `CHANGELOG.md` has an entry
- [ ] Commits are signed off (`git commit -s`, DCO)

## Agent disclosure

- [ ] This PR was written partly or wholly by an AI coding agent. I have read every line and I can explain each change.
