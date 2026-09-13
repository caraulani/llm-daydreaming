---
name: output-token-budgets-truncation
description: Managing token limits and truncation in long LLM evaluation runs
type: project
---

# Output Token Budgets and Truncation in Long Evals

## The Truncation Problem

When running extended evaluations on long prompts, hitting output token limits mid-response. Claude shows up around 4K context left, then cuts off. On a client eval last week, lost 30% of critic scoring responses to truncation. System prompts + eval setup + examples + target content = tight budget fast.

## Budget Arithmetic

For a 100K corpus sample with 3-critic evaluation setup:
- Context window: 200K (Claude 3.5 Sonnet)
- Reserved for input: 150K (corpus context, prompt, instructions)
- Available for output: 50K
- Per-response budget: 50K / 100 samples = 500 tokens max
- Critic responses consistently run 800-1200 tokens with full reasoning

## Mitigation Patterns

- Compress context upstream: summarise corpus clusters before eval, pass digest not raw text
- Stream to file early: write partial responses as they arrive, don't accumulate in memory
- Split by arm: evaluate each treatment arm in separate backend calls, not all at once
- Hard max tokens: set `max_tokens=400` in backend config, trade depth for completion rate

## Current Approach

Using `max_tokens=450` with structured output (JSON schema) to force brevity. Recover missing signal from partial responses via fuzzy matching to known patterns. Cost spike acceptable vs losing half the eval data to truncation.
