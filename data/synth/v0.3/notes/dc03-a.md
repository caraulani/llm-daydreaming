---
name: Eval item ID reservation scheme
description: Ranges 5000-5099 locked for adversarial test set, segregated from production evaluation items to prevent data leakage
type: project
---

## ID Range Allocation

Reserved 5000-5099 strictly for adversarial test set. Production corpus items remain below 5000. This separation prevents accidental mixing when shuffling batches or rerunning the evaluation pipeline.

## Implementation Details

- Updated sampler config to enforce range check at adversarial item assignment time
- Written validation test to catch ID collisions during ingest
- Item generator now skips this range entirely when creating regular corpus items
- Manifest records the range boundaries in metadata

## Current Status

Running against v0.1 corpus. Batch 3 (shipped Sept 10) uses IDs 3800-4999, confirms clean separation. Next 100 adversarial items queued for generation once critique completes.

## Future Scaling

Scheme scales to 10k items easily. If we exceed 5000 regular items, we reclaim 5000-5099 and shift adversarial set to the next open range. Document the shift in PREREGISTRATION.md.
