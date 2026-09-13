# Paper checklist (NeurIPS 2025 form, answered honestly for draft v0.1)

Answers are for draft v0.1 with the sealed run `2026-09-13_micro` filled into Section 6.

1. **Claims.** Do the main claims in the abstract and introduction reflect the paper's contributions and scope? **Yes.** The abstract follows the pre-committed template with the run's numbers filled in and states the preregistered decision outcome (no signal); it states that synthetic ground truth measures recovery of planted structure, not real-world novelty or usefulness. Words prohibited in v0.1 text are listed in `../PREREGISTRATION.md` Section 14.

2. **Limitations.** Does the paper discuss limitations? **Yes.** Section 7.1: synthetic ground truth, shared priors, one corpus and one generator, no human rating, scaffold variance, leakage by paraphrase, the critic as a liability, the underpowered sampler hypothesis, cost.

3. **Theory assumptions and proofs.** **Not applicable.** No theoretical results.

4. **Experimental result reproducibility.** Does the paper fully disclose all information needed to reproduce the main results? **Yes, by design.** Corpus, answer key, prompts (verbatim, hashed), model snapshot IDs, raw outputs and run logs are committed. `make reproduce` regenerates every table without API access.

5. **Open access to data and code.** **Yes.** MIT for code, CC-BY-4.0 for paper and data. The synthetic corpus and `gold.json` are public. The pipeline runs against any corpus through adapters.

6. **Experimental setting and details.** **Yes.** Section 5 and `../PREREGISTRATION.md` give arms, sample sizes, prompts, models, thresholds (cosine 0.85 duplicate gate), and the sampling bands. Temperature is the model default and is recorded in run metadata.

7. **Experiment statistical significance.** **Yes.** Wilson 95 percent intervals on every proportion (the error bars in every table); Fisher exact one-sided tests for H1 (p = 0.011) and H3 (p = 0.110); hypergeometric for H2 (p = 0.482 and 1.000); a 10,000-shuffle permutation null over the oracle set (p = 0.032). All preregistered with α = .05.

8. **Experiments compute resources.** **Yes.** USD at list price per arm is read from logs into T4; the run cost $33.62 and the corpus build $1.54 at list price (zero marginal cost on a subscription). Embedding runs on a laptop CPU. No GPU.

9. **Code of ethics.** **Yes.** No human subjects in v0.1. The synthetic corpus describes a fictional person. Track C (future) involves one owner scoring their own private corpus; nothing from a private corpus is published without the owner's release of a redacted subset.

10. **Broader impacts.** **Discussed briefly.** Section 2.5 covers the model-collapse risk of writeback loops and the over-production of bridge-like output. The tool is local-first with no telemetry by design.

11. **Safeguards.** **Not applicable.** No model or dataset with misuse risk is released.

12. **Licenses for existing assets.** **Yes.** `sentence-transformers/all-MiniLM-L6-v2` (Apache-2.0). Model APIs used under their providers' terms. No third-party data is redistributed.

13. **New assets.** **Yes.** The synthetic corpus, answer key, prompts and raw outputs are documented in `data/README.md` (datasheet) and released under CC-BY-4.0.

14. **Crowdsourcing and research with human subjects.** **Not applicable for v0.1.** For Track C: single owner, self-scoring, no compensation, no IRB; this will be stated in the paper when Track C runs.

15. **Institutional review board approvals.** **Not applicable.** Independent researcher; no institution; no human-subjects study in v0.1.

16. **Declaration of LLM usage.** **Yes.** Language models were used for: drafting the synthetic corpus notes (`claude-haiku-4-5-20251001`); drafting the bridge specifications and gold text with the experimenter, fixed under the preregistration seal before any note existed; the five 2026 prior-art and design sweeps recorded verbatim in `../research/`; drafting this paper's text under the author's direction and editing; and as components of the system under study (card extraction, generation, critic, recovery judge). No result, number or citation was produced by a model without a log or a source. Every reference was re-fetched against its primary source on 2026-09-13.

## Additional disclosures

- **Preregistration.** `../PREREGISTRATION.md`, SHA-256 committed and OpenTimestamps-stamped before any model call. Deviations are logged at the bottom of that file.
- **Judge disclosure.** The recovery judge is a language model asked a grounded entailment question with the gold answer in context. It never rates novelty. Prompt and every judgment released.
- **Contamination statement.** The synthetic corpus was written in 2026 and cannot be in any model's training data. Gold connections were written with a language model as a disclosed assistant, sealed before the notes, and checked for 6-gram leakage against the notes; the check does not catch paraphrase (Section 6.1).
- **Negative results.** Any hypothesis that fails is reported in the abstract and in the same tables.
- **Model aliases.** Aliases (`haiku`, `sonnet`) appear in configs for convenience; the paper reports the exact snapshot IDs read from run logs.
