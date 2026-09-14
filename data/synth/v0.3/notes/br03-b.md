---
name: Description eval set
description: Current eval: 4.6/5 on 200-SKU July batch
type: project
---

## Eval set locked

200 SKUs in the 1000-1199 range, selected by merchandiser on 2 July. Hasn't changed since. Good stable baseline for tracking improvements over time.

## Latest score: 4.6/5

Ran the generator against the full eval set again. Averaged 4.6 out of 5. Spot checked a few manually and the scores hold. See some variation across categories (apparel clustering tighter, home goods more spread) but nothing alarming.

## Testing next iteration

Considering a variant with expanded context handling. Could potentially push to 4.65 or higher. Current 4.6 is solid and ready to ship if needed. Plan is to test one new variant head to head against this baseline before deciding what to do.

## Notes on tracking

Last run used haiku-class model. Should keep exact model ID per eval run, especially if I end up comparing against a sonnet variant later.
