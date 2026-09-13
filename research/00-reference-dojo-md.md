# Reference pattern: Eduard Cristea's dojo.md

*Written 2026-09-13. The publishing shape of this repo was modelled on `github.com/edholofy/dojo.md` (Eduard Cristea, Holofy, MIT, first commit 2026-02-27, ~10 stars at the time of writing). This note records what we copied, what that repo does not do, and what we added on top.*

## What dojo.md does

Root layout, as fetched on 2026-09-13:

```
README.md          11.6 KB   product-style README (see below)
paper.md           32.5 KB   a full paper, at the repo root
CLAUDE.md          11.4 KB   agent-facing project guide (commands, architecture, key files)
LICENSE            MIT
hero.jpeg          hero image referenced from the README
.github/workflows/ci.yml    build + test on Node 18/20/22
courses/  src/  website/    the product itself, 7,400 files
```

**README shape.** Hero image at the top. One-sentence problem statement in bold ("Your agent demos well. It fails in production."). A transcript-style demo block showing five iterations of the loop and the score climbing. "What just happened" narrative. A "paste this into Claude Code" quick start with zero setup. A cost table. A leaderboard block rendered as ASCII bars. A table of everything the product covers. A format spec (the SKILL.md standard). CLI reference tables. Development commands. A three-line "Mission" (today, tomorrow, future). License.

**paper.md shape.** Title, author, email, month. Abstract. 1 Introduction (problem framed as two gaps; four core ideas as a numbered list). 2 Related Work (seven short subsections, each ending with how dojo.md differs). 3 System Architecture (pipeline diagram in a code block, one subsection per component, tables for enums and mappings, a short code excerpt). 4 The central design insight, given its own section. 5 Experimental Results (setup, baseline table, loop table, qualitative differentiation). 6 A proposed architecture for the next version. 7 Scale. 8 Integrations. 9 Limitations and Future Work. 10 Conclusion. References (eleven entries, arXiv IDs given, mixed academic and industry sources).

**Why it reads as research.** The paper states a mechanism, names its inspirations with citations, reports numbers in tables with the setup spelled out, and has a limitations section that concedes real weaknesses (mock fidelity, judge dependence, single-turn only). The README and the paper are two doors into the same object: the README for people who want to run it, the paper for people who want to cite it.

## What we copied

- Root-level README plus a paper in markdown, both in the repo, cross-linked.
- README opening: hero, one-sentence problem, transcript demo, "paste into Claude Code" quick start, cost table.
- Paper skeleton: abstract, introduction with numbered core ideas, related work with per-subsection differentiation, system section with a pipeline diagram, a section devoted to the one central thesis, results as tables, limitations, references with arXiv IDs.
- CLAUDE.md as the agent-facing map of the codebase.
- MIT for code. CI on push and pull request.
- GitHub topics, many and specific.

## What dojo.md does not do (and a frontier-lab reader checks next)

- No `CITATION.cff`, so no "Cite this repository" button and no machine-readable citation.
- No tagged releases, no changelog, no DOI.
- No arXiv version of the paper; the paper exists only in the repo.
- No committed raw outputs: the results tables cannot be regenerated from files in the repo.
- Model names in the paper are aliases (for example "Claude Sonnet 4.6"), not immutable snapshot IDs with access dates.
- Prompts are in source code, not published verbatim as versioned artifacts.
- No preregistration, no null model, no statistics beyond point scores.
- No CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, or issue templates.
- The paper's results section is small (six scenarios, two models, one loop iteration) and the paper says so.

None of this is a criticism of the repo, which is a product with a paper attached. Our repo is a research artifact with a product attached, so the bar is different.

## What we added

See `research/01-publishing-practice.md` for the evidence behind each item.

- `PREREGISTRATION.md`, hashed and timestamped before any run, with a deviations log.
- `paper/` directory instead of a root `paper.md`: markdown source, `refs.bib`, a NeurIPS-style `CHECKLIST.md`, a figures folder, and a README on producing the arXiv PDF.
- `CITATION.cff`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ROADMAP.md`, `AGENTS.md` (with `CLAUDE.md` pointing at it).
- Dual licensing: MIT for code, CC-BY-4.0 for paper and released data.
- `prompts/` with every prompt verbatim and versioned; run metadata records the prompt hash and the exact model snapshot ID.
- `experiments/` with one config per arm and committed raw outputs per run; `make reproduce` rebuilds every table without API keys.
- `design/` with one architecture decision record per load-bearing decision from the brief.
- `research/` with the full audit trail: the founding brief, the lineage note, and every agent sweep, unedited.
- A public reproducibility corpus alongside the private primary corpus, so anyone can run the pipeline end to end.
- A statistical null (label permutation) separate from the stimulus control (random pairing).
