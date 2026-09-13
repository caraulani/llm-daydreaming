```yaml
---
name: LLM Judge Model Variance
description: Stability issues in evaluation scoring across model updates and time
type: project
---

Judge Model Update, Unannounced

## Provider Change

- Provider pushed a model update without notice. Reran the same fifty evaluation outputs through their judge. Scores shifted 5 percent across the entire set.
- No changelog. No migration guide. Just different results on a rerun.
- Started pinning exact snapshot IDs in all runs. Should catch this kind of surprise sooner.

## Reproducibility Gap

- Reran the same fifty outputs again three months later, using the pinned snapshot ID from the original run. Scores differ 2 percent from the first batch with that ID.
- Different source from the 5 percent provider shift.
- Unclear whether the judge model has changed or backend inference varies.

## Client Reports

- Clients evaluating LLM systems need stable numbers month to month to track whether new systems are genuinely better or just noise.
- These shifts complicate tracking. Adding metadata to every report: snapshot ID, judge model version, date of evaluation, backend provider.
```