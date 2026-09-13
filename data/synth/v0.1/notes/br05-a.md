---
name: br05-a
---
```yaml
---
name: payments-fraud-detection-notes
description: Working notes on fraud patterns and blocklist updates for consumer calling app
type: project
---

# Fraud Detection Updates

## Pattern Recognition

Reviewed the fraud cases from the past two weeks. The attacker was moving through destination numbers in strict sequential order. When we lined up the sequences across accounts, three that looked independent turned out to be connected.

## Blocklist Revision

The old blocklist only checked individual numbers. We added adjacency checking to catch when numbers appear consecutive to each other. This picked up cases the original logic missed. Deployed the update to production yesterday afternoon.

## Next Steps

Need to backtest the new adjacency rules against the past month of transactions to measure how much coverage we gain. Also reviewing the flagged accounts with security team to understand scope and whether there are other patterns we should be watching.
```
