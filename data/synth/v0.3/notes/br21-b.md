---
name: br21-b
---
```yaml
---
name: Card Fraud Investigation - 411111
description: August chargeback and production rule gaps
type: project
---

# Chargeback on 411111 Card, August

## Incident
Card starting 411111 came through with a chargeback last month. Customer account is active and their transaction records are normal. Real fraud? Dispute is ongoing. During my rule review, I noticed something about this card pattern.

## Production Rule Discovery
Found a whitelisting rule in the live system for any card starting 411111: no secondary fraud verification, passes straight through. The rule was added during the infrastructure setup phase several months back. It stayed active after we moved forward. Never explicitly removed.

## Follow-up
- Inventory other rules from that setup phase still running
- The 411111 rule needs its own review
- Tighten the gate between temporary and permanent rules
```
