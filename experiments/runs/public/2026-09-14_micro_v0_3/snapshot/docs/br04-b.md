---
name: LLM Eval Notes Aug 20
description: Recent observations on evaluating large language models for clients
type: project
Title: LLM System Reviews

## Changes Observed
- Client A's model accuracy slipped slightly over last week .5 points across the fixed test set.
- No explicit vendor update noted, snapshot possibly altered without pinning.

## Test Set Consistency
- Maintaining a stable 50-item reference set for consistent comparisons .
- Tracking changes manually since auto-pinning is not enabled by default .

## Snapshot Management
- Requesting explicit pinning of judge snapshots from vendors going forward.
- Noting date and score impact in logs to track consistency over time .