# Roadmap

The order is fixed by one rule from the founding brief: every prior attempt at this loop died at the verifier, not the generator. So evaluation ships before features, and every version has a gate that can fail.

## v0.1: preregistered synthetic micro-experiment (done, 2026-09-13)

- Corpus `data/synth/v0.1/` (60 notes, 12 bridges, 6 decoys), `PREREGISTRATION.md` sealed and anchored (Bitcoin block 966837), run `2026-09-13_micro`. H1 pass, H2 fail, H3 not significant: NULL by rule, published as such. Exploratory X1, X3, X4 committed.

## v0.2: oblique bridges, two writer families, two critics (done, 2026-09-14)

- Corpus `data/synth/v0.2/` (96 notes, 24 bridges of which 8 excluded by the leak rule, 12 decoys), `PREREGISTRATION-v0.2.md` sealed and anchored (block 966878), run `2026-09-14_micro_v0_2`. H1 pass, H4 pass, H2 fail, H3 inverted: SIGNAL by rule, recombination not claimed. X5 showed the single-note prompt's NONE gate is inert.
- Lesson recorded in ADR-014: principle-type bridges are recoverable from one note.

## v0.3: bridges that need both sides, and the first real corpus

- Corpus v0.3 built under ADR-014: a bridge is accepted only if the generator, given one side with a working NONE gate, does not produce the gold. Each side carries a specific fact, not a principle. Single-note abstention reported on fillers in every run.
- A NONE-permitted single-note prompt whose gate is verified on fillers before use.
- Match judge with two votes; card extractor refusals recorded and reported.
- Obsidian and markdown-folder adapters, `uvx daydreamd` packaging, `daydreamd dream` and `daydreamd review` commands for Track C on a real private corpus (owner-blind protocol in `docs/human-eval-protocol.md`).
- Headline experiment moves to execution-verified findings over real repositories (`research/05`): distance-forced pairing of code parts, NONE-permitted conjecture, a failing test as the critic, random-pairing control and permutation null, verified-yield vs distance.

## v0.4: Track A, retrospective evaluation

- Old-cutoff open-weight generator with a 6-month safety margin (ADR-007).
- Time-frozen arXiv slice, hit detection by retrieval over post-cutoff literature plus an entailment matcher.
- Strict and loose hit rates, always as lift over the random-pairing arm and a matched-decoy null.
- Lead-time distribution and future-neighbourhood rate.
- False-positive rate reported with a Wilson interval.

## v0.5: Track B, public registry

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
