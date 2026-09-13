## Judge Model Surprises

Provider pushed an update to the judge model without notice. Scores on the reference set shifted about 5% overnight. No changes to my code or prompt versions. Initial thought was a bug in my pipeline, but the shift was consistent across all runs.

## Solution: Pin the Snapshot

Started capturing exact model snapshot IDs from the API response envelope rather than using aliases like "haiku" or "sonnet". Pinning to the full model ID (e.g., claude-haiku-4-5-20251001) stopped the unexpected jumps. Runs are now reproducible and stable.

## Ongoing Aging

Even pinned snapshots still drift gradually over time. The exact snapshot id halts sudden shifts, but doesn't prevent slow drift in judge behavior. Scores from three months ago vs. today on the same reference set show measurable difference, even with the same snapshot pinned. Not a blocker yet, but worth tracking for long-term comparisons with clients.

## Next Steps

- Log snapshot id in every run metadata
- Record reference set scores alongside each evaluation
- Watch for broader pattern across multiple clients' systems