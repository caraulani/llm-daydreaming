---
name: EU/US endpoint eval drift
description: Tracked down score variance in LLM evaluation runs across regions
type: project
---

## EU endpoint serving stale snapshot

- Started seeing 8-12% score deltas between identical test runs on EU vs US endpoints
- EU endpoint locked to 2024-03-15 snapshot, US on current build
- Model performance metrics artificially low on EU side for narrative generation tasks
- API team confirmed cache staleness, invalidation scheduled for 2026-09-20

## Eval impact

- Three client reports came back inconsistent, had to re-run on US endpoint only
- Scores now align but cost 2 days to debug
- Updated baseline runs to log endpoint, timestamp, and model_id explicitly on every batch

## Harness changes

- Add endpoint version check before each run
- Verify deployed build on both regions before signing off
- Document primary endpoint in eval batch metadata

Caught this early; would have compounded into false variance claims if I'd already reported.
