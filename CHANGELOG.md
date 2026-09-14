# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Corpus v0.3 (24 fact-type bridges, 12 shape-matched decoys, 96 notes; family B written by a local Qwen 2.5 14B), the ADR-014 one-side gate (`prompts/generate_single_strict.md`, two-vote judge, `daydreamd gate`, `synth --one-side-gate`), four gate passes, 22 accepted bridges.
- PREREGISTRATION-v0.3.md sealed (tag `v0.3.0-prereg`) with five deviations; sealed run `2026-09-14_micro_v0_3` (precondition fail, H1 fail, H3-strict 8/22 vs 2/22; NULL) with raw outputs and tables T1 to T9; adversarial review `research/08`.
- Pipeline: B4 over bridge plus filler notes, strict single prompt selection, v0.3 decision rule with the filler-abstention precondition, `stats.match_votes`, table T9.

### Fixed
- Single-note recall denominator: every planted bridge the arm showed the generator, not only answered notes (v0.3 B4 recall 2 of 22, not 2 of 12).
- Exploratory X6 (strict prompt over the v0.2 corpus) and X7 (five-vote re-judge) configs added; runs pending.

## [0.3.0] - 2026-09-14

### Added
- Product front door: `daydreamd dream`, `review`, `skill`, `mcp`, `schedule`; Obsidian adapter with wikilinks; static embedder (model2vec potion-base-8M) as the default, MiniLM behind the `research` extra.
- Discoverability: byline, `llms.txt`, GitHub Pages site with schema.org JSON-LD, Open Graph and sitemap; hero image; lineage table from Poincaré 1908 to 2026 with verified links; author ORCID.
- Zenodo DOIs in CITATION.cff and README.
- Sealed v0.1 run `2026-09-13_micro` with raw outputs, tables T1 to T6 and DECISION.md (H1 pass, H2 fail, H3 fail; NULL by the preregistered rule).
- Exploratory arms S1 (partner-domain filler control), B7 (cross-domain-near sampler), configs X1 to X4, and the planted-distance post-hoc analysis; X1 results committed.
- v0.2 corpus specs (24 oblique bridges, 12 decoys, 96 notes), paraphrase-leak judge, two writer families, multi-critic pipeline, table T8, v0.2 decision rule, PREREGISTRATION-v0.2.md draft (unsealed).
- Corpus v0.2 built and frozen (96 notes, two writer families, 8 bridges excluded by the leak rule); preregistration v0.2 sealed with proofs; sealed v0.2 run `2026-09-14_micro_v0_2` (H1 pass, H4 pass, H2 fail, H3 inverted; SIGNAL by rule, recombination not claimed).
- Exploratory runs X3 (cross-domain-near sampler) and X4 (critic ablation) committed.
- OpenRouter and Ollama backends; usage-window circuit breaker; per-stage error-rate abort; synth builder resume mode.
- v0.1 OpenTimestamps proofs upgraded (Bitcoin block 966837); seal verification recipe.
- Research notes 04 (first-publish and history discipline), 05 (execution-verified code sweep), 06 (adversarial review of v0.1 results).

## [0.1.0] - 2026-09-13

Preregistered synthetic micro-experiment scaffold.

### Added
- Repository scaffold: licenses (MIT for code, CC BY 4.0 for paper, data, registry, docs), citation file, contribution guide, code of conduct, security policy, roadmap.
- Architecture decision records `design/ADR-001` through `design/ADR-013`, derived from the founding brief and the 2026-09-13 review.
- Synthetic corpus `data/synth/v0.1/`: 60 notes, 12 planted bridges, 6 decoy pairs, gold labels, datasheet.
- `PREREGISTRATION.md`: hypotheses, experiment arms, primary metric, permutation-null threshold, and stopping rule, frozen before any generation run.
- Pipeline: corpus ingest, concept cards, local embeddings, pair samplers (banded distance, anchor plus remote, random), generator with NONE permission and structured output, binary critic, retrieval-based corpus-duplicate gate, sealed-key blind scoring pack.
- Evaluation harness: Fisher exact test, label-permutation null, per-band trend test.
- Registry convention for Track B entries, with OpenTimestamps instructions.
- Human evaluation protocol, contamination statement template, datasheet template.
- CI (lint plus tests) and a reproduce workflow that rebuilds every table from committed outputs without API keys.

### Results
- None yet. The first run over the synthetic corpus has not completed. Numbers appear here only after they are read from logs.

[Unreleased]: https://github.com/caraulani/llm-daydreaming/compare/v0.3.0...HEAD
[0.1.0]: https://github.com/caraulani/llm-daydreaming/releases/tag/v0.1.0
