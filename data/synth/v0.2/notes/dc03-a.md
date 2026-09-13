---
name: threshold_masking_40_69
description: Client's 70-point pass threshold hiding incremental gains from 40 to 69
type: project
---

# Threshold Masking the Improvement Band

## The Problem

Client eval setup uses 70 as binary pass/fail on LLM outputs. Systems scoring 40-69 all report as "fail" in dashboards and summary tables, whether they're at 45 or 68. Looks like zero progress across versions, but the actual spread is there.

## What Happened

Earlier run scored 52. Latest variant scores 66. Both show as red/not ready in reports. Client interprets this as flatline, ready to drop the line. The 14-point improvement is completely invisible in the binary view.

## The Solution

Splitting the failure band: "needs work" (40-59), "close" (60-69), "ready" (70+). No threshold changes, just granularity on the dashboard. Client can now see the trajectory and track whether another tuning cycle is worth the compute cost.

## Timeline

Rerunning evals this week. Dashboard split going live Monday. Should preserve the project momentum and buy space for one more iteration before the go/no-go call.
