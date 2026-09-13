---
name: Temperature sensor drift tracking
description: Workshop sensor calibration notes, lab reference checks, alarm thresholds
type: project
---

# Sensor baseline tracking

## Current readings
Picking up something on the temp sensors. Readings are running about 0.3 degrees higher than last year's baseline when cross-checked against the lab unit. Could be natural variance or a systematic shift, but it's consistent across the batch.

Lab thermometer itself stays solid. Cross-check against the certified reference happens monthly, holds steady. That's the only reliable anchor point in here.

## Alarm thresholds
Set the divergence trigger at 0.5 degrees from the lab reading. If any sensor drifts that far, the alarm fires and I get a signal to investigate. Happens once a month or so, usually resets after a power cycle.

## Next steps
Pull the historical data from the past year and map the drift pattern. If it's steady, there's something systematic. If it's noise, probably not worth acting on. Monthly lab cross-check continues as scheduled.

Workshop conditions haven't changed, so it's just the sensor behavior I'm watching.
