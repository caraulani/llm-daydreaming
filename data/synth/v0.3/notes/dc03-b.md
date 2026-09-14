---
name: dc03-b
---
```yaml
---
name: Velocity Rules R-300 to R-399 Reservation
description: Dashboard grouping for fraud velocity rules on calling app
type: project
---

Velocity Rules Namespace

## Reservation and Scope

R-300 to R-399 block allocated for velocity rules. These fire on transaction frequency, amount acceleration, and caller burst patterns. Dashboard needs them grouped separately from binary blocklist rules (R-100, R-200 ranges). Keeps the fraud surface scannable.

## Implementation Notes

Rules in this block trigger on:
- Calls per minute from single account
- Cumulative spend in 24h window
- Payment method changes in rapid sequence
- Geographic velocity (caller location hops)

Each rule must log the window size and threshold. No hardcoding thresholds in rule logic; pull from config at load time. Avoids shipping new code for threshold tuning.

## Dashboard Grouping

R-300-R-399 gets its own card in the monitoring UI. Shows:
- Rule firing rate per hour
- False positive ratio by rule
- Threshold drift over time

Alert on rules firing >10% of traffic; usually means threshold needs adjustment. Had this problem with R-312 (spend velocity) in July after a promotion hit.

## Next Steps

Rules R-300, R-310, R-312, R-320 are live. R-330 (payment method velocity) pending QA. Others TBD based on caller behavior data.
```
