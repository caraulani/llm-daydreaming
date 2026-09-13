---
name: token-budget-truncation-evals
description: Output token limits and truncation behavior in extended evaluation runs
type: project
---

## Token budgets in client evaluations

Running multi-hour eval sequences on client systems hits output limits fast. Typical setups budget 2-4k tokens per generation but eval chains need reasoning, self-critique, iteration. Real evals I ran in August hit token limits after 8-12 completion cycles.

## Truncation patterns observed

Haiku class models truncate mid-sentence. Sonnet stops cleanly but at 4095 sometimes cuts semantic units. Truncation happens silently in JSON structures, breaking downstream parsing. One eval on a 50-item taxonomy lost 30% of category assignments to early stopping.

## Budget strategies

- Hard stop at 80% of stated limit, then post-process incomplete
- Split long evaluations into batches of 5-7 items instead of 20+
- Request raw scores before reasoning, add justifications in second pass
- Log token usage per item; watch for creep as eval rounds accumulate

## Current setup

Allocating 1500 tokens max per single evaluation turn. Batching evaluations of APIs across 3-4 parallel runs to stay under provider daily limits. Tracking actual usage vs. budget in metadata; seeing 15-20% overage in real evaluations vs. estimates.

This matters for client trust. If a system says "evaluated all 200 items" but truncated 40 items silently, results aren't trustworthy.
