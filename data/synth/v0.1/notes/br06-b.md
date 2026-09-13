---
name: LLM evaluation study design notes
description: Control arm findings from recent client evaluations
type: project
---

Study design lessons

Ran three client evals last quarter. All had personalization layers in the UI. Set up a control arm in one that stripped the personalized data component but kept the interface intact. Same engagement metrics as the personalized version. Realized the win was the interface novelty, not knowing about the user.

## Unexpected symmetry

The no-data arm performed as well as the full version on clicks, session length, return rate. Client wanted to scale the personalization. I flagged it's not where the lift is. Recommend they focus on interface polish first.

## Measurement artifact risk

Every study needs the measurement infrastructure but without the intervention layer. Otherwise you're measuring the measurement. Learned this the hard way with an earlier client eval where we couldn't isolate signal. Now it's standard practice.

## Next steps

- Document this pattern for the template configs
- Check if the other two client studies had proper baselines (one didn't, one did)
- Clean up the spreadsheet and hand over findings
