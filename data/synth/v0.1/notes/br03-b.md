---
name: Workshop Sensor Sync
description: Gateway wake window timing, sensor drift issues
type: project
---

## Gateway Power Budget

Gateway on sleep schedule, only listening in the 500ms wake window around :00 and :30 seconds. Saves ~80% power over continuous RX. But this constraint means everything downstream has to hit that window.

## Sensor Clock Drift

Built out 12 sensors, first batch using internal oscillators for wake timing. Drift accumulates fast. Within 48 hours, some were waking ±200ms off the gateway window. Missed packets started stacking up, 15-20% loss by day 3. Looked like RF noise at first.

## Fixed Schedule Fix

Switched sensors to GPS-synced wake times in the second batch. Pinned everyone to hard wall-clock offsets: node 1 at :05s, node 2 at :12s, etc. Packet loss dropped to <2%. Stays stable across resets.

## Next Steps

- Retrofit first batch with GPS module, replaces crystal oscillator
- Need better enclosure for antenna on workshop ceiling
- Test power consumption hit from GPS sync
