---
name: br05-a
---
```yaml
---
name: "workshop-iot-network-status"
description: "Sensor network behavior patterns"
type: project
---

Gateway and sensor timing patterns

## Setup

Gateway wakes :00 and :30 every hour, receives for twenty seconds. Each sensor sleeps for thirty minutes measured from its own last transmission. Staggered their sends to avoid collision on the gateway window.

## Packet loss through the day

Morning runs clean, everything gets through. Around 11:00 missed packets start showing up. By 18:00 they're climbing fast. After nightly reboot at midnight the miss counter resets to zero. Next morning back to clean again. This pattern holds every day.

## Sensors in the shop

- 3x temperature and humidity, storage room
- 1x motion sensor, corner near the workbench
- 2x door contact switches, main entry
- Water sensor on trial in cold storage, collecting baseline data

## What's next

Testing a second receiver unit to see if it helps coverage. Want to experiment with a longer listen window on the gateway. Evening band congestion might be part of it too.
```
