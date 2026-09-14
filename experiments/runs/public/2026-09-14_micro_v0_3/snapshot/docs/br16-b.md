---
name: LLM Eval Notes
description: Recent observations and decisions on evaluating large language models for clients
type: project
Title: LLM Evaluation Roundup

## Models Compared
- Reviewed GPT-3.5 Turbo, Claude 2.1, Bard Plus, Bing AI Pro versions.
- Found all fall short in unit conversion tasks by ~3% consistently.

## Public Set Results
- All models scored near perfect (99%) on public dataset conversion questions.
- Private set showed discrepancies only for custom weight-based queries.

## Workshop Scale Notes
- Weighed five common household items to create gold answers on 6 Jul.
- Top systems missed by similar margins in private tests but not in public ones.