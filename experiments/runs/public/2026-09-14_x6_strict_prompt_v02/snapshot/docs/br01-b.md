```
---
name: Fraud Pattern Q3 2024
description: Batch chargeback pattern from new accounts, recent spike
type: project
---

Batch of low-value transactions from stolen cards, chargebacks lag five to seven weeks

## Pattern in New Accounts

Cluster of new accounts created mid-August. Each placed a single transaction, all under 15 euros, within 24 hours of the card being added to the account. Cards from different issuers, different regions. Payment cleared without issue at the time. No obvious pattern in what was purchased or merchant category.

## Chargeback Wave

Same batch started chargebacks 5 to 7 weeks later. Processor's dispute notes flagged all cards as reported stolen. Timeline consistent across the batch: charges hit around mid-September. Volume roughly 40 transactions. Low individual value but the pattern itself is clean.

## Monitoring Adjustment

Signup IPs worth checking for proxy services. Look for any connection to known fraud rings. Tighten velocity rules on new accounts: card added and charged same day under 15 euros is a trigger. Add to monitoring queue rather than waiting for chargeback to surface it.
```