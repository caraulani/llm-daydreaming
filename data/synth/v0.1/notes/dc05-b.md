---
name: "Support volume post-shipping change"
description: "Call and ticket spike after moving fulfillment to regional hub"
type: project
---

# Support volume spike after regional hub shift

## Baseline and change
- Moved fulfillment from single central warehouse to 3 regional hubs, Sept 6
- Expected faster delivery (2-4 days vs 5-7), mixed messaging on rollout
- Support email volume went from ~15/day to 40-45/day by Sept 9
- Chat volume up 60%, mostly first-time questions

## What customers are calling about
- Where is my order (tracking not updating for 24-48 hrs after ship)
- Delivery estimates unclear, regional variations not communicated
- Some regional hubs not showing in real-time, stale data hitting customer emails
- A few orders marked shipped but still in warehouse (data sync lag)

## Actions taken
- Updated shipping notice emails with clearer regional expectations, Sept 10
- Flagged tracking data sync issue to ops, investigating Shopify webhook backlog
- Added FAQ section to help center about regional delivery times
- Prepared templated responses for common questions

## Next check
- Monitor for stabilization mid-next week
- Review if data sync fixes the tracking delay issue
- Consider proactive notification on orders sitting > 24 hrs post-ship label
