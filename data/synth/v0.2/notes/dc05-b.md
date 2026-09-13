---
name: Gateway Debug Logging Incident
description: Log volume spike from debug mode left enabled on production gateway; recovery
type: project
---

## Gateway Log Volume Spike

Noticed logs tripled on gateway this week. Debug mode had been left on from the last sensor calibration session.

## What Happened

- Tuesday morning: storage hit 87% of capacity
- Debug logging enabled on gateway (timestamp: Thu ~23:00, testing magnetometer drift)
- Forgot to disable after testing. Log rotation couldn't keep pace
- Disk pressure started throttling sensor reads by Wednesday afternoon

## Fix Applied

- Disabled debug flag on gateway config (Wed 14:30)
- Manually purged logs older than 7 days (gained 34GB)
- Set log rotation to daily, max 5 files (was weekly, max 10)
- Added alert for disk usage above 80%

## Check

Logs now at normal baseline. Will keep rotation tighter until next calibration cycle. Need better post-test checklist to catch this faster.
