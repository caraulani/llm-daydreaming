---
name: exit-intent-popup-test
description: A/B test results on cart abandonment, exit-intent popup variant
type: project
---

# Exit-Intent Popup Test Results

## Setup and Baseline

Running test on Shopify store Sept 5-12. Control: no popup. Variant: exit-intent popup with 15% discount code, triggers when cursor leaves toward browser chrome. ~2400 sessions across both arms.

Baseline cart abandonment: 71% (historical). Average cart value: $68.

## Variant Performance

Popup showed on 312 sessions. 28 proceeded to checkout (9% click rate). 18 completed purchase (64% conversion after click).

Abandonment rate in variant arm: 68%. Gain: 3 percentage points. Gained ~$1224 in revenue on the variant arm.

## Code and Setup

Trigger uses Mouseflow exit-intent library. Popup built in HTML/CSS, styled to match store brand. Copy emphasizes limited discount window. Discount code valid 48 hours.

## Next Steps

Repeat test with larger N (full month). Test discount depth: currently 15%, try 10% and 20% variants. Monitor email list: 34 new signups captured via popup email field.
