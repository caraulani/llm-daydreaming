# Roadmap

The order is fixed by one rule from the founding brief: every prior attempt at this loop died at the verifier, not the generator. So evaluation ships before features, and every version has a gate that can fail.

## v0.1: preregistered synthetic micro-experiment (current)

- Corpus: `data/synth/v0.1/`, 60 model-written notes of a fictional solo builder with 12 hand-authored cross-domain bridges planted and 6 decoy pairs (ADR-013). Released under CC BY 4.0 with a datasheet.
- Arms: banded distance (B3), anchor plus remote (B6), random pairing (B1), single-note reflection (B4).
- Ground truth: `gold.json`, written before the notes existed.
- Primary metric: planted-bridge recovery rate per arm against the decoy false-positive rate and B1, with the label-permutation null (ADR-006).
- Gate: permutation p below 0.05 for B3 or B6 against B1, and the winner above B4. Anything else is published as a null.
- Deliverables: `PREREGISTRATION.md` frozen, tables T1 to T5 in `results/`, `paper/paper.md` v0.1 with an abstract that claims recovery of planted structure and nothing more.

## v0.2: adapters, packaging, the yield curve

- Obsidian adapter (markdown vault in, daily note with wikilinks out).
- PyPI release so `uvx daydreamd` works, `daydreamd dream` and `daydreamd review` commands.
- Yield-vs-distance run on a public corpus (arXiv cs abstracts, CC0 metadata), including the far tail. This is Figure 1 if the curve is single-peaked, and a null result if it is not.
- Concept-card fidelity audit published (faithful / distorted / hallucinated rates).
- Synthetic corpus regenerated with a second model family; v0.1 rerun to bound the shared-imagination effect (ADR-013).
- Base-model axis: at least three generator models crossed with two samplers, with a variance decomposition.

## v0.3: Track A, retrospective evaluation

- Old-cutoff open-weight generator with a 6-month safety margin (ADR-007).
- Time-frozen arXiv slice, hit detection by retrieval over post-cutoff literature plus an entailment matcher.
- Strict and loose hit rates, always as lift over the random-pairing arm and a matched-decoy null.
- Lead-time distribution and future-neighbourhood rate.
- False-positive rate reported with a Wilson interval.

## v0.4: Track B, public registry

- `registry/entries/` opened to outside submissions (PR-based, see `registry/README.md`).
- OpenTimestamps proofs on every entry.
- Two outcome classes tracked: independently discovered, adopted from the registry.
- Writeback with lineage, and the tail-diversity curve over at least 14 nights, writeback on versus off (ADR-009).

## v1.0: the daemon

- Scheduler (launchd, cron, systemd timers) and `morning.md` output.
- Codebase and Zotero adapters.
- MCP server exposing `dream`, `review`, `verdict`.
- Pluggable generator: Anthropic API, OpenRouter, Ollama.
- Track C: owner-blind KEEP / KNOWN scoring over private corpora (`docs/human-eval-protocol.md`), first the maintainer's own, then at least 5 opt-in corpus owners.

## Papers

- Paper A, method and benchmark: arXiv first, then NeurIPS Datasets and Benchmarks or ACL Rolling Review.
- Paper B, human study: CHI or IMWUT, the venues where the null we are answering was published.
- Both wait on results. The registry and the daemon wait on no venue.

## Not planned

- Memory consolidation (dedupe, contradiction resolution, summarisation). Others ship it; we do not compete there.
- An LLM that scores novelty on a scale. See ADR-004 and ADR-005.
- Telemetry of any kind.
