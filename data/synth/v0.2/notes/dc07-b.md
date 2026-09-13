---
name: Apple Pay checkout lift
description: Four percent conversion gain after rollout, payment method adoption tracking
type: project
---

Apple Pay checkout lift

## Implementation

Added Apple Pay to Stripe checkout on Sept 8. One-click flow, matching Google Pay placement. Tested on iOS and desktop Safari first. Rollout was 72 hours rolling traffic, no feature flags needed. Configuration took 45 minutes.

## Early metrics

Conversion rate: 23.1% baseline (Aug 28-Sep 7), now 24.1% (Sep 8-Sep 12). Four percent relative lift. Traffic stable at 340 daily visitors. Cart abandonment rate fell 1.2 percentage points.

Mobile Apple Pay: 18% of successful orders. Desktop Safari: 6% of successful orders. Android unchanged. Total payment method breakdown: card 52%, Apple Pay 24%, Google Pay 14%, PayPal 10%.

## Next

Monitor return rate and chargeback volume this week. Apple Pay users have zero disputes so far but sample is small. Check if lift holds post-weekend.
