# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet.

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

[Unreleased]: https://github.com/caraulani/llm-daydreaming/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/caraulani/llm-daydreaming/releases/tag/v0.1.0
