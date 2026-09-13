---
name: LLM Evaluation Tuning Session
description: Prompt refinement and re-scoring run notes
type: project
---

## Tuning the Lowest Twenty

Extracted the twenty lowest-scoring items from the evaluation run and rewrote the scoring prompt to handle those cases better. Re-scored them after the changes. Result: those twenty items jumped 30% on the second pass. Prompt now handles edge cases that were tripping up the system before.

## Unexpected Shift on Wider Set

When I ran the full re-test, twenty different items that I hadn't touched also moved. They improved 15% on average across the board. This wasn't part of the tuning cycle, so worth documenting what happened there.

## Decisions

- Need to isolate which prompt edits moved the bottom twenty the most
- Test both the tuned subset and the broader movement on fresh data before rollout
- Validate that these changes don't break performance on items that were already scoring well

Ready to push to client systems once the pattern holds on validation.
