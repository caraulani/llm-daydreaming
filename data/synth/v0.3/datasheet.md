# Datasheet: daydreamd synthetic corpus v0.3

Follows Gebru et al., "Datasheets for Datasets" (2021). Fields marked "TBD, filled at freeze" are completed from `manifest.json` before the corpus is frozen; a datasheet with TBD fields means the corpus has not been frozen yet.

## Motivation

- **Purpose.** Ground truth by construction for the v0.3 preregistered experiment (`PREREGISTRATION-v0.3.md`): with bridges that need both sides (ADR-014), does two-note recombination recover more planted mechanisms than one note under a strict abstention prompt (H3-strict), does selection hold (H1), and does near-in-embedding, far-in-domain sampling surface planted pairs (H2).
- **Why v0.3.** In v0.2, single-note reflection recovered more planted mechanisms (8 of 16) than two-note recombination (6 of 16): the bridges were general principles that one note's ingredient set already cued (research/07). v0.3 bridges are built from specific facts (identifiers, dates, numbers, vendor quirks, locations, sequences), each side carries a fact rather than a principle, and every bridge must pass the one-side gate: the generator itself, reading one side under a strict NONE-permitted prompt, must fail to produce the gold (two judge votes, a tie fails closed).
- **Creator.** Julian Caraulani, solo, for the daydreamd project. Bridge and decoy specs written with Claude as a disclosed writing assistant, fixed under the v0.3 seal (tag `v0.3.0-prereg`) before any note existed.
- **Funding.** None. Family A calls ran on the author's subscription; family B ran locally.

## Composition

- **Instances.** 96 markdown notes; 24 specified bridges of six fact types (identifier 6, date 5, number 4, vendor 4, location 3, sequence 2); 12 decoy pairs, all shape-matched to bridges (same fact type and surface pattern, different or absent mechanism); 24 filler notes. Sixteen notes per domain across six domains (e-commerce operations, LLM evaluation, payments fraud, personal health protocols, EU grant fundraising, workshop IoT).
- **Fields per bridge** (`bridges.yaml`): as v0.2 plus `fact_type`.
- **Fields per decoy** (`decoys.yaml`): as v0.2 plus `fact_type` and `shared_term`.
- **Labels.** `gold.json` (planted pairs with gold connection and implication), `domains.json`, `manifest.json` (per note: kind, bridge or decoy id, domain, sha256, words, attempts, writer family, exact writer model id, leak-judge verdicts).
- **Writer families.** Family A: `claude-haiku-4-5-20251001` via headless `claude -p`. Family B: Qwen 2.5 14B Instruct, Q4_K_M, local via Ollama (`hf.co/bartowski/Qwen2.5-14B-Instruct-GGUF:Q4_K_M`, digest recorded per note). Assignment by id parity (odd bridge and decoy ids and odd filler positions to A). 48 notes each.
- **Excluded bridges.** Two of 24, both family A: br11 (recovered from side A on gate pass 3, rewritten once, recovered again on pass 4 with 2 of 2 judge votes) and br09 (first flag on the final pass, a tie on side B, dropped without rewrite under the four-pass cap). No bridge was lost to the leak rule. Twenty-two planted bridges remain: 10 written by family A, 12 by family B.
- **Errors and noise.** Two leakage checks on every bridge note: no six-word run of any gold connection or gold implication (6-gram), and a CLEAN verdict from the paraphrase-leak judge (`prompts/leak_judge.md`, Haiku-class, given the note and the gold). Length floor 100 words (see deviation 2 in the preregistration); notes still short after the allowed attempts are kept and listed under `short_after_max_tries`. No em dashes. Build outcome at freeze (2026-09-14): 96 notes, all at or above 100 words; 0 six-gram leaks; all 48 bridge notes CLEAN by the leak judge (7 short notes judged after the build once they passed the length floor); four gate passes with flags br02 (pass 1), br06 and br15 (pass 2), br11 (pass 3), br09 and br11 (pass 4); side-A specs of br02, br06, br15 and br11 rewritten once each; corpus sha256 d044765e9dff6c49d042fcbc7adc98d6cfaf18d8210787e9ec64f04c90f9d749.
- **Known limitation.** The gate is a model judging a model: two judge votes with a tie failing closed, and the gate's own generator (Sonnet-class) is the same family as the experiment's generator, so gate outcomes are conservative for that family and untested for others. Family B still writes shorter notes than family A under the identical prompt (medians at freeze: family A 169, family B 111 words).
- **Confidential or personal data.** None. The builder persona is fictional.

## Collection process

- **Acquisition.** Notes generated from `prompts/synth_note.md` version 2 with a per-note spec (topic, domain, ingredients, forbidden phrases). Bridge notes regenerated on a 6-gram leak, an em dash, a short note, or a LEAK verdict; up to five attempts in the first pass, up to ten in the resume pass; bridge notes gated by the generator on each side after the checks.
- **Software.** `daydreamd synth` (`src/daydreamd/synth/`), pinned by `uv.lock`; resume mode reused notes that already passed.
- **Cost.** Measured list-price cost of family A, leak-judge and gate calls across the four passes: $8.52 + $3.03 + $2.55 + $3.60 = $17.70, plus about $0.30 for post-build judging of short notes; family B ran locally at $0.
- **Time frame.** Built 2026-09-14.
- **Ethical review, consent.** None required; fictional.

## Preprocessing

- **Steps.** Meta-commentary trailers stripped from the end of notes; frontmatter kept; 6-gram check; leak judge on bridge notes; manifest with per-file SHA-256 and a corpus SHA-256 (`MANIFEST.sha256`).

## Uses

- **Intended.** The v0.3 experiment and replications of it. A corpus whose bridges are certified, by the generator itself, to need both sides.
- **Not intended.** Training data. Any claim about real-world novelty or usefulness.

## Distribution and maintenance

- **License.** CC BY 4.0. **Location.** `data/synth/v0.3/` in the repository. **Maintainer.** The author; changes go to a new version directory, never in place after the freeze.
