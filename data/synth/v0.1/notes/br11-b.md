---
name: br11-b
---
```yaml
---
name: temperature_sensor_calibration_log
description: Monthly recalibration protocol for workshop temperature sensors
type: project
---

## Hardware lineup

8 TMP36 units spread across the workshop shelves and workbench. One DHT22 anchors as reference, calibrated against a certified handheld unit last month. Monthly refresh against it to catch any drift creeping in.

## Recent checks (2026-08-10)

Three sensors right on target. One near the space heater running 0.4 degrees high; reset its offset. Two others in the ±0.1 range. Alarm system caught the heater one Wednesday when it crossed ±0.5 threshold from reference. Reset after adjustment.

## Long term pattern

Over the year you see them walk a bit. 0.3 degrees is typical cumulative drift, so monthly cycles catch it before it compounds. The alarm flags anything that spikes outside bounds in a single read.

## Next cycle

October 10th calibration. Two wireless nodes need battery swaps; supply low. Thinking about swapping one sensor to a different corner of the workshop, see if location matters.
```
