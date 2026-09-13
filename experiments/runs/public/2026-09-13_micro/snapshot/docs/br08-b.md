## Current monitoring stack

Setup with four DHT22 sensors (temp, humidity) and two soil moisture probes across workbench and storage areas. Devices push readings every 15 minutes to the Raspberry Pi running Node.js. Server aggregates into daily summaries: min, max, mean per metric. The rollups happen automatically at 2300 UTC each day.

## Data lifecycle

Raw readings held for 30 days on the Pi's SD card, then purged to free space. Only the daily aggregates persist long-term in the SQLite backup on my NAS. Learned this the hard way in July: missed running the daily job for two days (power cycle without proper shutdown), lost those readings entirely. Set a cron alert now.

## Recent fixes

Added timestamp validation before aggregation. Schema changed 22 Aug to tag each reading with collection window ID, helps catch sync drift when sensors reconnect after dropout. Tested the pipeline with a 48-hour gap injection, confirmed gaps get caught by the summary counts.

## Next steps

Soil probe on the north shelf is drifting (needs recalibration). Considering moving one DHT to the cabinet near the 3D printer to catch thermal swings during runs.