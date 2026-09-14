# Paper checklist (NeurIPS 2025 form, answered honestly for draft v0.3)

Answers are for draft v0.3 with the sealed runs `2026-09-13_micro` (Section 6), `2026-09-14_micro_v0_2` (Section 6.2) and `2026-09-14_micro_v0_3` (Section 6.3) filled in, plus the exploratory runs X1, X3, X4 and X5.

1. **Claims.** Do the main claims in the abstract and introduction reflect the paper's contributions and scope? **Yes.** The abstract states all three preregistered outcomes verbatim (v0.1 no signal; v0.2 SIGNAL by rule) and, in the same paragraph, that the v0.2 rule's recombination test was not one and recombination is not demonstrated; it states that synthetic ground truth measures recovery of planted structure, not real-world novelty or usefulness. Words prohibited in v0.1 and v0.2 text are listed in `../PREREGISTRATION.md` Section 14 and `../PREREGISTRATION-v0.2.md`.

2. **Limitations.** Does the paper discuss limitations? **Yes.** Section 7.1: synthetic ground truth, shared priors, one generator and one judge, no human rating, scaffold variance, leakage by paraphrase (v0.1), principle-type bridges recoverable from one note (v0.2), the inert NONE permission of the single-note prompt, the family-dependent exclusion, card-extractor refusals, the critic as a liability, the underpowered sampler hypothesis, cost.

3. **Theory assumptions and proofs.** **Not applicable.** No theoretical results.

4. **Experimental result reproducibility.** Does the paper fully disclose all information needed to reproduce the main results? **Yes, by design.** Corpus, answer key, prompts (verbatim, hashed), model snapshot IDs, raw outputs and run logs are committed. `make reproduce` regenerates every table without API access.

5. **Open access to data and code.** **Yes.** MIT for code, CC-BY-4.0 for paper and data. The synthetic corpus and `gold.json` are public. The pipeline runs against any corpus through adapters.

6. **Experimental setting and details.** **Yes.** Section 5 and `../PREREGISTRATION.md` give arms, sample sizes, prompts, models, thresholds (cosine 0.85 duplicate gate), and the sampling bands. Temperature is the model default and is recorded in run metadata.

7. **Experiment statistical significance.** **Yes.** Wilson 95 percent intervals on every proportion (the error bars in every table); v0.1: Fisher exact one-sided tests for H1 (p = 0.011) and H3 (p = 0.110); hypergeometric for H2 (p = 0.482 and 1.000); a 10,000-shuffle permutation null over the oracle set (p = 0.032). v0.2: H1 p = 0.021, H2a p = 0.297 (arm-label permutation p = 0.693), H2b p = 0.141, H3 p = 0.857, H4 p = 0.009, H5 reported as Wilson intervals only; permutation null over the oracle set p = 0.0002. All preregistered with α = .05.

8. **Experiments compute resources.** **Yes.** USD at list price per arm is read from logs into T4; the v0.1 run cost $33.62 and its corpus build $1.54; the v0.3 run cost $87.86 and its corpus build about $18.00; the v0.2 run cost $85.04, its corpus build about $7.0 for the Haiku and judge calls, and the X5 follow-up $15.05, all at list price (zero marginal cost on a subscription). The family-B note writer (Qwen 2.5 7B Instruct Q4_K_M) ran locally through Ollama on a laptop. Embedding runs on a laptop CPU.

9. **Code of ethics.** **Yes.** No human subjects in v0.1. The synthetic corpus describes a fictional person. Track C (future) involves one owner scoring their own private corpus; nothing from a private corpus is published without the owner's release of a redacted subset.

10. **Broader impacts.** **Discussed briefly.** Section 2.5 covers the model-collapse risk of writeback loops and the over-production of bridge-like output. The tool is local-first with no telemetry by design.

11. **Safeguards.** **Not applicable.** No model or dataset with misuse risk is released.

12. **Licenses for existing assets.** **Yes.** `sentence-transformers/all-MiniLM-L6-v2` (Apache-2.0). Model APIs used under their providers' terms. No third-party data is redistributed.

13. **New assets.** **Yes.** The synthetic corpus, answer key, prompts and raw outputs are documented in `data/README.md` (datasheet) and released under CC-BY-4.0.

14. **Crowdsourcing and research with human subjects.** **Not applicable for v0.1.** For Track C: single owner, self-scoring, no compensation, no IRB; this will be stated in the paper when Track C runs.

15. **Institutional review board approvals.** **Not applicable.** Independent researcher; no institution; no human-subjects study in v0.1.

16. **Declaration of LLM usage.** **Yes.** Language models were used for: drafting the synthetic corpus notes (`claude-haiku-4-5-20251001` for v0.1 and half of v0.2; a local Qwen 2.5 7B Instruct for the other half of v0.2); judging paraphrase leakage of v0.2 bridge notes (`claude-haiku-4-5-20251001`); drafting the bridge specifications and gold text with the experimenter, fixed under the preregistration seal before any note existed; the prior-art and design sweeps and the two adversarial reviews recorded verbatim in `../research/`; drafting this paper's text under the author's direction and editing; and as components of the system under study (card extraction, generation, critic, recovery judge). No result, number or citation was produced by a model without a log or a source. Every reference was re-fetched against its primary source on 2026-09-13.

## Additional disclosures

- **Preregistration.** `../PREREGISTRATION.md`, `../PREREGISTRATION-v0.2.md` and `../PREREGISTRATION-v0.3.md`, SHA-256 committed and OpenTimestamps-stamped before any experiment call (v0.3 proofs stamped 2026-09-14, pending upgrade) (Bitcoin blocks 966837 and 966878). Deviations are logged at the bottom of each file: one for v0.1, five for v0.2.
- **Judge disclosure.** The recovery judge is a language model asked a grounded entailment question with the gold answer in context. It never rates novelty. Prompt and every judgment released.
- **Contamination statement.** The synthetic corpus was written in 2026 and cannot be in any model's training data. Gold connections were written with a language model as a disclosed assistant, sealed before the notes, and checked for 6-gram leakage against the notes; the check does not catch paraphrase (Section 6.1); v0.2 added a paraphrase-leak judge, which catches stated mechanisms and not implied ones (Section 6.2).
- **Negative results.** Any hypothesis that fails is reported in the abstract and in the same tables.
- **Refusals.** The card extractor refused four synthetic health notes in the v0.2 corpus as personal medical information. The sealed run is reported as executed, with the resulting empty-claim units and two errored calls noted; the pipeline now records refusals and excludes zero-card notes from note-level arms.
- **Model aliases.** Aliases (`haiku`, `sonnet`) appear in configs for convenience; the paper reports the exact snapshot IDs read from run logs.
- **Reporting fix (v0.3).** The single-note arm's recall denominator counted only answered notes; it now counts every planted bridge the arm showed the generator (2 of 22, not 2 of 12). Logged as part of deviation 5 in `../PREREGISTRATION-v0.3.md`; the decision is NULL under both denominators.
