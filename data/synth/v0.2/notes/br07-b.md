---
name: LLM evaluation snapshot
description: Prompt tuning and scoring variance across ticket batches
type: project
---

## Prompt tuning and initial scoring

Assembled the evaluation set from early client tickets, the same batch I used to refine the prompt. Ran the full eval pass on this set: 91. Most classifications landed correctly. The mistakes made sense on manual inspection.

## Month two pull

Fetched a fresh batch from tickets in the following month. Applied the same prompt, same scoring rubric. Score dropped to 74. Not a small variance.

## What I logged

- First batch: mostly onboarding and basic support tickets
- Second batch: merchant account support, bulk orders, fraud case escalations, payment disputes
- Checked a sample of low-scoring predictions manually: annotations seem consistent, no obvious data quality drift
- Ticket complexity and problem mix are clearly different between periods

## Next steps

- Does score stabilise with more recent data, or continue to drift downward
- If stable, what's the right benchmark to use going forward
- Building evaluation set from tickets across multiple months before settling on a production rubric
