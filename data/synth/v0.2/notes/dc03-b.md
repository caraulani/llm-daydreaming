---
name: dc03-b
---
```yaml
---
name: Cold shed battery alert delay
description: 10% battery alert fires too late in cold shed; capacity loss in low temps
type: project
---

Battery alert timing in cold storage

## Current issue

- 10% alert firing when battery already at 3-5% in unheated shed (0-5°C)
- Nominal threshold tested indoors; cold reduces effective capacity by 30-40%
- Sensor: generic 18650 lithium, no temperature compensation
- Shed temp drops below 5°C most nights Sept-March
- High shelf mount, no insulation between unit and external wall

## Root cause

- Li-ion capacity drops roughly 10% per 10°C below room temp
- Alert logic reads remaining charge at fixed voltage threshold
- Cold conditions make voltage read artificially low before actual depletion
- No thermal sensor on power board to adjust trigger

## Testing plan

- Measure alert voltage at 5°C in fridge, compare 20°C baseline
- Run full discharge cycle in cold to find actual cutoff
- Check firmware for temperature-compensated alert option

## Options

- Raise alert to 20% for winter months (Sept-March)
- Insulated enclosure with weather seal
- Move unit to heated workshop with longer sensor cable
- Upgrade to cold-rated lithium cells, cost 2-3x higher
```
