## Sensor clock incident

Replaced battery in the hallway temp sensor Thursday afternoon, around 14:30. After the power cycle, packets started arriving with timestamps from January 2024. Structure and signatures were clean on each frame. Caught it after seeing about 47 packets accumulated over 20 minutes while monitoring the live stream.

## Server logging

Checked the ingest logs. All packets were stored normally, no rejections. The daily rollup for 2024-01-15 recalculated when the backlog hit the database. The day's average shifted noticeably higher than before. Sensor had run stable for six months prior to the battery failure.

## Replication

Powered cycled the unit again. Identical behavior. Either the board's RTC lacks a battery, or the UTC offset config is pointing somewhere wrong. Need to trace through the boot sequence carefully.

## Next steps

Visual inspection of the RTC module. Test in isolation before putting it back in the rack. Also check what the packet handler does with the timestamp field: passes it through as-is or processes it.