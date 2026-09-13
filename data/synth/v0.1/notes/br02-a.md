---
name: LLM judge calibration notes
description: Fixing score drift in iterative evaluation rounds
type: project
---

Judge drift and blind spots

Been running eval loops on model outputs and noticed something systematic. When I feed the judge previous scores alongside new outputs, the numbers climb steadily. Same batch rescored blind comes in roughly 0.8 points lower on the 10-point scale. That gap shows up consistently across different judges and model families. It's not noise.

Root cause turns out simple: the judge context includes prior scores. Strip that out and the issue disappears. Blind rescores now stabilize. No more drift between passes.

## Updated iteration protocol

Pass outputs to judge with metadata only (source, timestamp, variant, model). Hold the score log separate. Rescore old batches regularly to catch calibration creep. Got about 40 runs in the current experiment and need a clean baseline before moving to the full evaluation set. Three judges, independent runs.

## What's locked in

Prompt version bumped to v3. Exact format is stored in prompts/eval_judge_v3.md. Not planning retroactive rescores on the earlier iterations, too messy at this stage.
