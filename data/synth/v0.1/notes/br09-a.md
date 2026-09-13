---
name: Calling App Fraud Patterns
description: Working notes on detecting compromised cards in payment streams
type: project
---

## Velocity Signals

Noticed the pattern when reviewing false positives on daily spend. Fraudsters don't spread it out. They hammer the card: three or more transactions in ten minutes. Real users just don't do that. Two is the ceiling for legitimate spike.

## Timing Beats Volume

Daily spend cap was too coarse. Someone could drop significant money in a ten-minute window while staying under their monthly limit. The velocity window is what matters. A burst of four $400 charges means something is wrong, even if the day's total is safe.

## Flagging Process

Cards with tight clustering get flagged. Manual review before settlement to avoid killing conversion. Quick checks: merchant sequence coherence, location data, card repeat patterns. Catching about 70% of known compromises before settlement.
