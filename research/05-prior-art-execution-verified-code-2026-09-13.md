# Prior-art sweep: execution-verified daydreaming over a codebase (2026-09-13)

Produced by a research agent (Claude Fable 5.1) on 2026-09-13, while the v0.1 sealed run was executing. Question: is "a background loop that samples DISTANT parts of a repository, asks for a non-obvious cross-file connection with permission to say NONE, turns the claim into an executable check, runs it, and keeps only verified findings, evaluated with a random-pairing control and a label-permutation null" an unclaimed gap? Sources: arXiv abstract pages fetched directly where cited; web search otherwise. "Not found" means nothing surfaced, not proof of absence.

## (a) Closest works

| # | Work | What it does | Delta to the spec |
|---|---|---|---|
| 1 | TestExplora, arXiv:2602.10471 (Feb 2026) | Benchmark for proactive bug discovery: 2,389 tasks from 482 repos, defect signals hidden, documentation as oracle, model must write tests that fail on the buggy code. Best F2P 16 to 17 percent. Notes cross-module interactions as the hard part. | Closest benchmark framing. Task-driven (one hidden bug per task), no pairing of distant parts, no NONE option, no random or permutation control, measures F2P not yield per dollar. Baseline and target. |
| 2 | Agentic Property-Based Testing, arXiv:2510.09907 (Oct 2025) | Agent infers function-specific and cross-function properties from code plus docs, synthesises PBTs, executes, reflects to confirm bugs. 100 Python packages; 56 percent of reports valid, 32 percent reportable; top-21 ranked: 86 percent valid. | Closest execution-as-critic system. Open-ended, executed, reflective. Properties come from local module reading, not from sampling distant pairs; no NONE rate; no random or null control; no distance analysis. Primary baseline. |
| 3 | Cascade, arXiv:2604.19400 (Apr 2026) | Tests generated from documentation, run against code; inconsistency reported only if existing code fails and doc-generated code passes. 13 unknown inconsistencies, 10 fixed. | Execution-verified, differential, open-ended. Local doc and code pairs only; no cross-file pairing, no controls. |
| 4 | RepoAudit, arXiv:2501.18160 (Jan 2025) | Autonomous repo auditing via demand-driven path-sensitive traversal with a validator for data-flow facts; 38 true bugs in 15 systems at $2.54 per project, later 185 bugs. | Open-ended and cheap, but bug-class driven; validator is symbolic not execution; no distance sampling; no null. |
| 5 | OpenAnt, arXiv:2606.19149 (Jun 2026) | Decomposes a repo into units by entry-point reachability, adversarial attacker simulation, exploit executed in a sandbox. Unknown vulnerabilities in OpenSSL, WordPress, Flowise. | Execution-verified, open-ended, security only; pairing by reachability (near), the opposite of distance-forcing; no controls. |
| 6 | AnyPoC, arXiv:2604.11950 (Apr 2026) | Turns noisy candidate bug reports into executed proofs of concept; 121 new bugs from 2,000+ reports, 108 confirmed; rejects 9.7x more false positives. | Exactly the "claim to executable check" stage, as a reusable component. Needs a candidate report as input; not a generator. Verifier module or baseline for that stage. |
| 7 | BugStone, arXiv:2510.14036 (Oct 2025) | From one patched bug, extract the pattern, search the codebase; 22k candidates in Linux, 61.5 percent precision on a reviewed sample. | Seed-dependent, pattern matching, manual verification. Not open-ended. |
| 8 | IRIS, arXiv:2405.17238 | LLM infers taint specifications plus CodeQL whole-repo analysis. | Static, security-class specific, no execution, no sampling. |
| 9 | Semantic conflict detection via LLM tests, arXiv:2507.06762 (Jul 2025) | SMAT plus Code Llama 70B tests: conflict if a test passes on each change alone and fails after merge. | The only work that tests interaction between two code parts by execution. Pairs are concurrent commits, not distance-sampled. |
| 10 | DocPrism, arXiv:2511.00215; METAMON, arXiv:2502.02794 | Code and doc inconsistency via local categorisation and external filtering; metamorphic LLM queries against documented behaviour. | Local, no execution (DocPrism), no pairing. |
| 11 | Context-as-AI-Service, arXiv:2606.04397 (Jun 2026) | Surfaces cross-file dependency chains so generated docs stop being plausible locally and wrong globally. | Names the exact failure the spec exploits, for documentation generation; no conjecture, no execution. |
| 12 | FunSearch (Nature 2024), AlphaEvolve arXiv:2506.13131, CodeEvolve arXiv:2510.14150, BayesEvolve arXiv:2606.30335 | Propose, execute, score evolutionary loops with a fitness function. | Execution as critic for a single scored objective, not open-ended cross-file conjecture; no NONE, no distance pairing. The "execution is the critic" lineage. |
| 13 | Anthropic Claude Code Security (Feb 2026; Firefox pilot, 22 vulnerabilities in two weeks) | Autonomous repo scan proposing fixes for human review. | Product, security-class, no published protocol, no controls. Evidence of demand. |
| 14 | Entroly (github.com/juyterman1000/entroly, Apr 2026, "daemon that dreams about your codebase") | Background daemon that indexes and pre-fetches context to cut agent hallucination. | Uses the word "dreams"; no conjecture, no tests, no bug finding. Name collision only. |
| 15 | Multi-hunk patch characterisation, arXiv:2506.04418 | Measures divergence of hunks in fixed vs unfixed bugs (fixed bugs less divergent, 0.28 to 0.40). | Only distance-vs-outcome measurement found for bugs; about patch spread, not finding yield vs pair distance. |

Also seen, less close: PHOENIX cross-language DL-framework static analysis (arXiv:2607.00555); KNighter (LLM system logic bugs, names cross-component logic bugs as the open problem); TitanFuzz, Fuzz4All, KernelGPT (LLM fuzzing; execution-verified over the input space, not cross-file conjecture); LLM vs human unit tests fault detection (arXiv:2606.08588); mobile app property generation, 25 unknown bugs (arXiv:2604.13463).

## (b) Verdict per component

- Distance-forced pairing of repository parts (embedding or call-graph distance as the sampling variable): unclaimed. Open-ended systems sample by reachability (OpenAnt), data-flow paths (RepoAudit), module-local reading (Agentic PBT), or task (TestExplora). Nobody samples far pairs on purpose.
- NONE-permitted open-ended cross-file conjecture: unclaimed as a measured quantity. Agentic PBT and Cascade have implicit no-bug outcomes but report no abstention rate; none frame abstention as an honesty metric.
- Execution as the critic inside an ideation loop over code: claimed in pieces. Agentic PBT, Cascade, OpenAnt and AnyPoC all execute the check. The ideation-loop framing (Gwern's DDL with execution replacing the LLM critic) is not claimed, but a reviewer will treat execution-verified LLM bug finding as established.
- Random-pairing control plus label-permutation null for code finds: unclaimed. No paper in the sweep reports a random-sampling baseline or any null model.
- Verified-yield vs distance curve: unclaimed. Only the multi-hunk study touches distance, for patches not finds.
- Gwern DDL framing applied to a codebase as a background daemon: unclaimed; Entroly and "overnight agent" posts use the vocabulary without the mechanism.

Name check: "code daydreaming", "repo daydream", "daydreamd" in this space: not found. `daydreamsai/daydreams` is a commerce-agent framework (unrelated; watch for confusion). `latent-dreamer` reimplements Mueller's DAYDREAMER, not code.

## (c) Three "this is just X" objections

1. "This is Agentic PBT or TestExplora with extra steps." Both already get LLMs to find real bugs by writing and running tests, open-endedly, at repo scale. Difference to state up front: they optimise finds; we measure where finds come from. The sampling variable (distance between the paired parts) is the manipulation, random pairing is the control, and the permutation null asks whether finds concentrate on far pairs at all. Their pipelines become our baselines. If distance does nothing, that is the result.
2. "Execution-verified is just fuzzing, PBT or differential testing." True for the verifier. The claim is not a new verifier; it is that a NONE-permitted generator over distant pairs plus an off-the-shelf verifier produces a different distribution of finds than local reading does, and that the abstention rate is informative. Reuse AnyPoC or Hypothesis as the verifier.
3. "Cross-file bugs are a known hard class (KNighter, TestExplora); you have not solved it." Correct; claim a measurement, not a solution: the first yield-vs-distance curve for LLM-found, execution-verified findings, with a null.

Secondary risk: Anthropic's Claude Code Security and the Firefox pilot mean the "daemon that finds bugs overnight" product story is already told by the vendor; keep the contribution on the protocol and the curve.

## (d) Recommended v0.2 evaluation design

Repos. 8 to 12 mid-sized, well-tested, permissively licensed Python packages with fast test suites (under 2 minutes), active maintainers, and low prior LLM-audit exposure; prefer packages not in Agentic PBT's 100-package list so acceptance is not confounded. Pin commit SHAs.

Units. Pairs of functions (or function plus doc paragraph) sampled by embedding distance over function-level cards, bands as in v0.1, plus B6 anchor-plus-remote, plus B1 random, plus a call-graph-neighbours arm (distance 1 to 2 in the call graph) as the reachability-style control mirroring OpenAnt and RepoAudit, plus B4 single-function reflection (the Agentic PBT analogue). Given the v0.1 post-hoc finding that planted bridges are embedding-near, add the B7 cross-domain-near arm (near in embedding, far in module or package).

Dream schema. `{connection, mechanism, check}` where `check` is a pytest test or Hypothesis property that must fail on the pinned commit if the claim holds and pass after a described fix; NONE permitted. The generator never sees test-suite results.

Verified find (pre-register). A candidate counts as verified only if the check fails deterministically on the pinned commit (3 of 3 runs, clean container), passes on the same commit with the check trivially inverted (guards against setup failures), and a differential oracle agrees: either documentation-derived behaviour (Cascade rule) or a maintainer-accepted issue within 60 days. Three tiers: executed-fail, oracle-confirmed, maintainer-confirmed. Any check with non-identical outcomes across 3 runs is flaky, excluded from hits, counted in its own column.

Base rates and nulls. Random pairing at equal N gives the base rate. Label-permutation null: shuffle band labels across all units 10,000 times and recompute verified finds per band. Cochran-Armitage trend on verified-find rate by band. NONE rate by band. Precision per arm with Wilson intervals; cost per verified find from logs.

Baselines. Agentic PBT run as published on the same pinned commits; TestExplora-style doc-oracle test generation where docs exist; AnyPoC as the shared verifier so the verifier is held constant across arms.

Cost. 10 repos x ~300 units x (one Sonnet generation + one sandboxed test run + one Haiku critic): about 3,000 generations, 3 to 4M tokens, under $40 at list price, $0 marginal on a subscription. Human triage only on executed-fail candidates, expected tens.

Contamination. Pin commits after the generator's training cutoff for part of the set (three repos with recent large refactors) and report finds split by pre- and post-cutoff code.
