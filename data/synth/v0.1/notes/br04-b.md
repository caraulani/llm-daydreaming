---
name: LLM evaluation methodology notes
description: Temporal data splits and leakage patterns in model testing
type: project
---

Temporal cutoffs in model eval

## The shuffle trap

Set cutoff before the test set exists. Ran into this with a client last month: random splits showed 94% accuracy, but time-ordered partition dropped it to 67%. Training through the test window killed the signal. Now I freeze weights before touching any held data.

## Data order as ground truth

Random splits are convenient but hide what temporal sequence exposes. Same dataset, completely different stories depending on how you partition. What matters is whether the model performs on data that actually comes after training finished.

## Current eval routine

- Cutoff timestamp set first, committed to config
- Model weights frozen at that point
- Test split only includes data after boundary
- Log the exact model checkpoint in metadata

Applying this to the synthetic corpus work and the blind track. Once you see how much shuffling can distort results, random holds feel reckless.
