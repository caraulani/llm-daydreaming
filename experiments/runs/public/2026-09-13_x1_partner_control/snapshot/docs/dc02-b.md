# Ring firmware v2.8 update and battery drain

## Update rollout
Installed firmware v2.8 on Sept 8, 2026. Release notes promised improvements to REM sleep detection and actigraphy noise reduction. Update took 15 minutes, ring was offline during install. No issues during flashing.

## Battery performance post-update
- Pre-update baseline: 5 days between charges, 9-10% daily drain
- First cycle after v2.8 (Sept 8-13): 4 days 3 hours, tracking 12% daily drain
- Pattern shows 2-3 percentage point increase in daily consumption
- Actigraphy sampling frequency may have increased; release notes do not specify

## Hypothesis and testing plan
Firmware changes to detection algorithms driving higher sampling rate. Will monitor next 2 cycles (14 days) before deciding rollback. If drain stays above 12% daily, downgrade to v2.7 and report to vendor. Sleep quality signal changes are not meaningful until battery behavior stabilizes.