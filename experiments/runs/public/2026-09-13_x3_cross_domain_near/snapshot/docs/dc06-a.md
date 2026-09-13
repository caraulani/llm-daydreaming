Saturated benchmark stops working for client evals

## The problem

MMLU-Pro is hitting 88-92% across Claude 3.5, GPT-4, Llama 3.1. No separation. When you're comparing three systems for a client, you can't say "this one is meaningfully better on reasoning." The numbers compress into noise.

Leaderboard posted new runs last week. Same pile-up. Checked with two other evaluators, same story.

## What it means for us

Can't use this for final recommendation layer. Clients pay to know which system is best for their use case, not to see three green checkmarks. Move back to task-specific evals: code generation on their codebase, domain retrieval Q&A, math chains.

Custom harness is still the only way to get signal. Takes longer but worth it.

## Fallback

Benchmarks that still discriminate: GPQA (62-78% range, still open), SimpleQA (accuracy varies 45-68%). Will add one of these to the baseline eval suite so we have at least one leaderboard score that moves.

Benchmark rot is real. Expect this to happen every 18-24 months as systems converge.