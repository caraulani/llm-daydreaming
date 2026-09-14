```yaml
---
name: Payments fraud patterns, August onwards
description: Monitoring changes in hold triggers and account behavior
type: project
---
```

## Hold trigger communication

Told support in August: flag accounts making three or more purchases within ten minutes. Designed to catch velocity patterns that don't match typical consumer behavior. Implementation went live shortly after.

## Behavior shift

Since then, accounts caught in holds are making exactly two purchases every ten minutes instead. Consistent, repeating rhythm. Not three, not four, always two. The constraint is precise.

## Spend tracking

Total spend per account per hour hasn't moved. Same daily volumes, same user segments, same churn. The rhythm changed but the magnitude didn't. Accounts still reaching the same weekly and monthly totals.

## Open items

- Need to verify if this pattern holds across all fraud cohorts or just flagged high-risk accounts
- Check whether conversion rates (purchases completed after hold) changed
- Look for secondary patterns: time-of-day clustering, device switching, payment method rotation
```