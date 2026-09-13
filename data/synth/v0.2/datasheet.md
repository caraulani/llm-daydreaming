# Datasheet: daydreamd synthetic corpus v0.2

Follows Gebru et al., "Datasheets for Datasets" (2021). Fields marked "TBD, filled at freeze" are completed from `manifest.json` before the corpus is frozen; a datasheet with TBD fields means the corpus has not been frozen yet.

## Motivation

- **Purpose.** Ground truth by construction for the v0.2 preregistered experiment (`PREREGISTRATION-v0.2.md`): does a generate-then-select pipeline recover oblique cross-domain connections, does it need the second note (H4), does near-in-embedding, far-in-domain sampling surface planted pairs (H2), and does recovery depend on which model family wrote the notes (H5).
- **Why v0.2.** The v0.1 corpus leaked by paraphrase: four single-note recoveries traced to notes that stated the mechanism on one side, which the 6-gram check cannot catch, and decoys shared only a homonym. v0.2 adds per-side forbidden phrases, a one-side test, a paraphrase-leak judge, shape-matched decoys, twice the bridges, and a second writer family.
- **Creator.** Julian Caraulani, solo, for the daydreamd project. Bridge and decoy specs written with Claude as a disclosed writing assistant, fixed under the v0.2 seal (tag `v0.2.0-prereg`) before any note existed.
- **Funding.** None. Family A calls ran on the author's subscription; family B ran locally.

## Composition

- **Instances.** 96 markdown notes; 24 bridges (each a pair of notes in different domains carrying one hidden mechanism's ingredients); 12 decoy pairs (9 shape-matched: same failure shape, different mechanisms; 3 vocabulary homonyms); 24 filler notes. Sixteen notes per domain across six domains (e-commerce operations, LLM evaluation, payments fraud, personal health protocols, EU grant fundraising, workshop IoT).
- **Fields per bridge** (`bridges.yaml`): as v0.1 plus `forbidden_phrases_a`, `forbidden_phrases_b`, `one_side_test`.
- **Fields per decoy** (`decoys.yaml`): as v0.1 plus `kind`, `shape`, `mirrors`, `why_not`.
- **Labels.** `gold.json` (planted pairs with gold connection and implication), `domains.json`, `manifest.json` (per note: kind, bridge or decoy id, domain, sha256, words, attempts, writer family, exact writer model id, leak-judge verdicts).
- **Writer families.** Family A: `claude-haiku-4-5-20251001` via headless `claude -p`. Family B: Qwen 2.5 7B Instruct, Q4_K_M, local via Ollama (`hf.co/bartowski/Qwen2.5-7B-Instruct-GGUF:Q4_K_M`, digest recorded per note). Assignment by id parity (odd bridge and decoy ids and odd filler positions to A). 48 notes each.
- **Excluded bridges.** Eight of 24, removed from `gold.json` because one of their notes ended with a LEAK verdict after the allowed attempts: br03 and br15 (family A), br08, br10, br12, br16, br18 and br24 (family B). Sixteen planted bridges remain: ten written by family A (br01, br05, br07, br09, br11, br13, br17, br19, br21, br23) and six by family B (br02, br04, br06, br14, br20, br22). Excluded bridges' notes stay in the corpus as unlabelled text; a pair drawn from them counts as random.
- **Errors and noise.** Two leakage checks on every bridge note: no six-word run of any gold connection or gold implication (6-gram), and a CLEAN verdict from the paraphrase-leak judge (`prompts/leak_judge.md`, Haiku-class, given the note and the gold). Length floor 100 words (see deviation 2 in the preregistration); notes still short after the allowed attempts are kept and listed under `short_after_max_tries`. No em dashes. Build outcome at freeze (2026-09-14): 96 notes; 0 six-gram leaks; 10 LEAK verdicts on bridge notes (2 family A, 8 family B) after up to ten attempts; 10 notes still under 100 words (all family B), kept and listed in `manifest.short_after_max_tries`; 0 em dashes; trailing meta-commentary stripped from 4 notes after the build (dc04-a, fl02, fl22, fl24). Corpus sha256 f8a6e9e335772ff44fd86ff0245933ce73d9c5354ef5164c476cb93cdd1ef44a.
- **Known limitation.** Family B writes about half as much as family A under the identical prompt (median words at freeze: family A 176, family B 107), so H5 compares families that differ in length as well as in priors; length is reported per note.
- **Confidential or personal data.** None. The builder persona is fictional.

## Collection process

- **Acquisition.** Notes generated from `prompts/synth_note.md` version 2 with a per-note spec (topic, domain, ingredients, forbidden phrases). Bridge notes regenerated on a 6-gram leak, an em dash, a short note, or a LEAK verdict; up to five attempts in the first build, up to ten for notes that still failed (deviation 3).
- **Software.** `daydreamd synth` (`src/daydreamd/synth/`), pinned by `uv.lock`; resume mode reused notes that already passed.
- **Cost.** Measured list-price cost of family A calls and leak-judge calls across the three build passes and the post-build judging: $3.77 (first build) + $1.04 (first resume) + $1.66 (second resume) + about $0.50 (judging of short bridge notes after the builds), about $7.0 in total; family B ran locally at $0.
- **Time frame.** Built 2026-09-13 to 2026-09-14.
- **Ethical review, consent.** None required; fictional.

## Preprocessing

- **Steps.** Meta-commentary trailers stripped from the end of notes; frontmatter kept; 6-gram check; leak judge on bridge notes; manifest with per-file SHA-256 and a corpus SHA-256 (`MANIFEST.sha256`).

## Uses

- **Intended.** The v0.2 experiment and replications of it. A difficulty knob for detection-ability curves (oblique bridges, shape-matched decoys).
- **Not intended.** Training data. Any claim about real-world novelty or usefulness.

## Distribution and maintenance

- **License.** CC BY 4.0. **Location.** `data/synth/v0.2/` in the repository. **Maintainer.** The author; changes go to a new version directory, never in place after the freeze.
