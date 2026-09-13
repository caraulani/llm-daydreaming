```yaml
---
name: Eval cycle variance audit
description: Notes from July and August eval runs with identical outputs
type: project
---

## The scoring spread

Moved the same output set through eval in mid July and again in mid August, three weeks later. July run scored them 7.9 across the board. August run on the identical set came back at 7.1. Model id, snapshot, everything else locked down. The outputs themselves had zero changes between the two runs.

## Prompt structure

July had a field that carried the score from the prior iteration. Looked like accumulated noise, so pulled it out for the August version. Kept everything else: model config, sampler settings, the full output manifest. Nothing else in the prompt structure changed.

## Open questions

Can't yet tell if the variance came from the prompt modification, from drift in the eval environment itself, or something else entirely. Need to run the same outputs one more time with current settings to see if we land closer to the August number or if it spreads further.
```