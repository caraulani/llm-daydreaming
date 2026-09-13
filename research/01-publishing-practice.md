# Publishing daydreamd as by-the-book open research (verified 2026-09-13)

## 0. What the dojo.md pattern is, and what it lacks
dojo.md (github.com/edholofy/dojo.md, Eduard Cristea, Feb 2026): README with hero image + one killer demo transcript + 60-second "paste this into Claude Code" quick start; `paper.md` at repo root (title/author/email/date, Abstract, Intro, Related Work, Architecture, Results tables, Limitations, Conclusion, References); MIT; GitHub CI matrix; CLAUDE.md; 20 GitHub topics; npm package; website. It has NO CITATION.cff, CONTRIBUTING, CHANGELOG, tagged releases, DOI, arXiv, committed raw results, or pre-registration. Those are exactly what a frontier-lab reader checks next.

## 1. Prioritised checklist

### MUST (a lab researcher looks for these in the first 60 seconds)
1. README in the Papers-with-Code (PwC) shape: "official implementation of [paper]" line, hero figure, Requirements, exact commands per experiment, Results table with the command that regenerates each row, Citation, License. PwC's NeurIPS 2019 study: repos meeting all 5 ML Code Completeness items had the highest stars (median 196, mean 2,664). Items: dependencies, training code, eval code, pre-trained models (for us: released prompts + cached outputs), README results table with precise commands. https://github.com/paperswithcode/releasing-research-code
2. `CITATION.cff` at root (`cff-version: 1.2.0`, `type: software`, authors, `repository-code`, `license`, `date-released`; add `preferred-citation: type: article` once arXiv exists). Enables GitHub's "Cite this repository" button (APA + BibTeX). Inspect AI's file is a clean minimal example. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
3. License split: code MIT or Apache-2.0 (Apache adds a patent grant; HELM uses Apache-2.0, Inspect/lm-eval/SWE-bench/AgentDojo use MIT); paper and released data CC-BY-4.0 (anthropics/evals is licensed CC-BY-4.0 as a data repo). State both in README.
4. Paper as a first-class artifact: `paper/` dir with the markdown source AND a LaTeX build, because arXiv only accepts TeX source or PDF (no markdown/HTML). TeX Live 2025 default. https://info.arxiv.org/help/submit_tex.html
5. Reproducibility for LLM experiments (the 2025-26 consensus, e.g. arXiv:2508.15503 guidelines, CMU LLM documentation guide): immutable model snapshot IDs (never aliases), API access date, temperature/top-p/seed/max-tokens, prompts committed verbatim as executed, raw outputs committed, judge model disclosed. AgentDojo does this structurally: `runs/<model-snapshot-id>/<suite>/` with every trajectory committed.
6. Pinned environment: `pyproject.toml` + `uv.lock` (Inspect, SWE-bench, HELM, AgentDojo all ship `uv.lock`), `.python-version`, `uvx daydreamd` one-liner.
7. CI that runs tests on push/PR (dojo.md pattern) plus a `make reproduce` / `uv run reproduce` target that regenerates every table and figure from committed raw outputs without API keys.
8. Pre-registration BEFORE results: `PREREGISTRATION.md` committed with the hypotheses, arms B0-B6, primary metric, permutation-null threshold, and stopping rule, then frozen on OSF (Open-Ended registration template, DOI, immutable, embargo up to 4 years possible, non-academics allowed). https://help.osf.io/article/158-create-a-preregistration
9. Signed, timestamped commits for priority: `git commit -S` plus OpenTimestamps (`pip install opentimestamps-client; ots stamp <file>`; Bitcoin anchor takes hours; `ots upgrade` later; `ots-git-gpg-wrapper` exists but its README says it does not yet validate commit timestamps, so stamp release tarballs and PREREGISTRATION.md directly). https://github.com/petertodd/opentimestamps-client
10. Negative-result commitment written into the README up front ("if the blind test fails we publish that"), matching FARS-style auditable-corpus discipline already in BRIEF.
11. CLAUDE.md + AGENTS.md (Inspect ships both; 60k+ repos had AGENTS.md by early 2026). AGENTS.md is the vendor-neutral one; CLAUDE.md can `@AGENTS.md`.
12. GitHub topics (dojo.md has 20; lm-eval, SWE-bench, AgentDojo use 3-4 precise ones) and a one-sentence repo description with the killer number.

### SHOULD (what separates "solid" from "by the book")
13. CONTRIBUTING.md with issue-first policy and explicit "extensions live outside core" (Inspect's is the 2026 reference, written specifically because of agent-generated PR floods; it promises 7-day triage). CODE_OF_CONDUCT.md (Contributor Covenant), SECURITY.md (Inspect, openai/evals).
14. CHANGELOG.md in Keep a Changelog format (Inspect, SWE-bench, HELM) + semver tags + GitHub Releases.
15. Zenodo DOI per release: enable GitHub integration, then cut a GitHub Release (Zenodo only archives on releases). If both `.zenodo.json` and `CITATION.cff` exist, Zenodo ignores the CFF. Put the DOI into CITATION.cff and README badge. https://help.zenodo.org/docs/github/
16. `design/` or `docs/adr/` with one file per load-bearing decision (Inspect has ~30 design docs). Our BRIEF already contains these decisions; each becomes an ADR (Nygard template: Context, Decision, Consequences, Superseded-by).
17. Leaderboard/registry convention: PR-based, one directory per entry, `metadata.yaml` (who, what, when, snapshot IDs, cost) + `README.md` + `results/`. SWE-bench/experiments is the canonical shape and now requires an arXiv link and open methods for Verified entries. Entries hold pointers; heavy artifacts live in the submitter's repo.
18. Datasheet for any released corpus/eval slice (Gebru et al. template in markdown: https://github.com/JRMeyer/markdown-datasheet-for-datasets); mirror on Hugging Face as a dataset card (Letta's sleep-time-compute repo puts every dataset on HF and links it from README).
19. NeurIPS-style checklist answered in `paper/CHECKLIST.md` even for arXiv: 16 items including reproducibility, open code/data, statistical significance/error bars, compute, licenses of assets, human-subjects protocol and compensation, IRB, and the new "Declaration of LLM usage". https://neurips.cc/public/guides/PaperChecklist
20. Cost reporting per experiment (tokens, USD, model) as a column in every results table; contamination statement (generator cutoff, 6-month margin, corpus dates).
21. Human-eval protocol write-up (`docs/human-eval-protocol.md`): blinding, control construction, rater instructions verbatim, agreement stats.
22. Hugging Face Papers page after arXiv (anyone can index `hf.co/papers/<arxiv-id>`, then claim authorship; HF only supports arXiv IDs). Papers with Code is dead: sunset 24 Jul 2025, redirects to HF; data archived at hf.co/pwc-archive. https://huggingface.co/docs/hub/paper-pages
23. `docs/` site (mkdocs, used by SWE-bench/HELM/AgentDojo) with an "Extending: write an adapter" page and `examples/`.

### NICE
24. REUSE/SPDX two-line headers per file (`SPDX-License-Identifier: MIT`) and `reuse lint` in CI. https://reuse.software/spec-3.3/
25. `llms.txt` on the project website (community convention, ~10% site adoption; Anthropic, Cursor, Mintlify use it).
26. MCP server exposing `dream`, `review`, `verdict` tools + a SKILL.md so Claude Code can run a night from chat (dojo.md's "paste this" onboarding).
27. Issue templates (bug, adapter proposal, registry entry), `good first issue` labels, ROADMAP.md.
28. Devcontainer (Inspect, AgentDojo, vivaria).
29. Model card for any fine-tuned or distilled component (none planned).

## 2. Proposed file tree (Python, working name daydreamd)
```
daydreamd/
├── README.md                 # hero fig, killer number, 60-s try-it, results table w/ commands, citation
├── LICENSE                   # MIT (code)
├── LICENSE-CC-BY-4.0         # paper/, data/
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md  CODE_OF_CONDUCT.md  SECURITY.md  ROADMAP.md
├── AGENTS.md  CLAUDE.md      # CLAUDE.md -> @AGENTS.md
├── PREREGISTRATION.md        # frozen before any result; OSF DOI + .ots proof
├── PREREGISTRATION.md.ots
├── pyproject.toml  uv.lock  .python-version
├── Makefile                  # make reproduce / test / paper
├── .github/
│   ├── workflows/ci.yml  workflows/reproduce.yml  workflows/reuse.yml
│   └── ISSUE_TEMPLATE/{bug,adapter,registry-entry}.md  PULL_REQUEST_TEMPLATE.md
├── src/daydreamd/
│   ├── core/        # ingest, cards, embed, sampler, generator, critic, judge, writeback
│   ├── adapters/    # claude_memory.py obsidian.py codebase.py zotero.py  (+ docs/extending.md)
│   ├── eval/        # permutation_null.py holdout.py metrics.py  (the benchmark harness)
│   ├── cli.py  mcp_server.py
├── prompts/         # every prompt verbatim, versioned, with SHA in run metadata
├── experiments/
│   ├── B0_raw ... B6_uzzi/   config.yaml + run.sh per arm
│   └── runs/<YYYY-MM-DD>_<model-snapshot>/  metadata.yaml raw_outputs.jsonl verdicts.jsonl cost.json
├── results/         # tables/*.csv figures/*.png  (regenerated by make reproduce)
├── data/            # datasheet.md + released slices (or HF pointers)
├── registry/        # public dream registry: entries/<date>_<name>/{metadata.yaml,README.md,dreams.jsonl,*.ots}
├── design/          # ADR-001-private-corpus.md ... (from BRIEF decisions)
├── docs/            # mkdocs: quickstart, extending, human-eval-protocol, contamination
├── paper/           # paper.md (source of truth), main.tex, refs.bib, CHECKLIST.md, figures/
├── examples/  tests/
└── .zenodo.json (optional; overrides CITATION.cff for Zenodo)
```

## 3. Exemplar repos and what to copy
- UKGovernmentBEIS/inspect_ai (MIT, 2.8k★): copy CITATION.cff, CONTRIBUTING (issue-first, extensions-outside-core, 7-day triage), AGENTS.md+CLAUDE.md pair, SECURITY.md, CHANGELOG, `design/` decision docs, uv.lock, devcontainer.
- ethz-spylab/agentdojo (MIT, 819★): copy `runs/<model-snapshot-id>/` committed trajectories, CITATION.bib + "Citing" section, mkdocs docs, README shape (Quickstart, Running the benchmark, Inspect the results, Citing).
- SWE-bench/experiments: copy the leaderboard entry convention (`<date>_<model>/metadata.yaml, README.md, results/`, artifacts in submitter's repo, PR-based, arXiv link required).
- paperswithcode/releasing-research-code: README template and 5-item completeness checklist.
- letta-ai/sleep-time-compute (MIT, 137★): the "paper code" repo pattern: NOTE box separating paper-reproduction code from product docs, arXiv + blog + docs links up top, every dataset on HF.
- NoviScl/AI-Researcher (Si et al., ICLR 2025): copy the release of human-study data (`reviews_ideation/`, `reviews_execution/`) alongside pipeline code; this is the "publish the raters' raw data" bar our Track C must meet.
- edholofy/dojo.md: keep the hero image, the transcript-as-demo, "paste this into Claude Code", root `paper.md`, topic tagging.
- anthropics/evals: CC-BY-4.0 on a pure data/eval repo; jsonl per eval with README per directory.

## 4. Gotchas
- arXiv endorsement (policy 2026-01-21): Path 1 needs an institutional email AND prior arXiv authorship in the same domain; otherwise Path 2, a personal endorsement from an established cs.CL/cs.AI/cs.HC author (the HF forum is full of such requests). Line this up weeks ahead. arXiv staff will not endorse. https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/
- arXiv license is irrevocable per version; choose CC-BY-4.0 (allows remix). Moderation takes 1-4 days, sometimes longer; announcements next business day at 20:00 ET for 14:00 ET cutoff. Google Scholar indexes 1-14 days after announcement.
- arXiv accepts only TeX source or PDF; keep paper.md as source but build `main.tex` (pandoc + a cleanup pass) and verify HTML rendering under LaTeXML.
- Zenodo archives only on GitHub Releases, and `.zenodo.json` silently overrides CITATION.cff. Enable the integration before the first tagged release or the DOI is missed.
- CITATION.cff: must be root, `cff-version: 1.2.0`, `type: software`; `preferred-citation` is how you steer citers to the paper. Validate with `cffconvert --validate`.
- Papers with Code is gone (July 2025); do not link to it. Use HF Papers, which needs an arXiv ID.
- OpenTimestamps git wrapper is not production-ready by its own README; stamp files/tarballs.
- Show HN requires something people can run without signup; blog posts and papers alone are off-topic. Lead with `uvx daydreamd` and a sample morning.md.
- SWE-bench-style leaderboards now gate on arXiv + open methods; design our registry policy the same way from day one to avoid the retrofit they had to do.
- Use immutable model snapshot IDs; aliases drift and break every result.
