---
name: Workshop radio protocol eval
description: Comparing LoRa vs WiFi mesh for sensor network in workshop
type: project
---

# Radio protocol choice: LoRa or WiFi mesh

## Current setup
- 8-12 sensors across workshop and shed
- Temperature, humidity, air quality monitoring
- Battery-powered units needed; mains power unavailable in some locations
- ~50m max range, walls and metal workbenches in between

## LoRa option
- TinyML breakout boards ~€120 each, gateway €80-200
- Very low power: coin cell or AA battery for 6-12 months
- Range 100-300m outdoor, 50m through walls; covers our needs
- Minimal interference in workshop environment
- 5-30 second latency acceptable for temperature tracking
- Community examples for temperature chains already exist

## WiFi mesh alternative
- Same sensor stack compatible (ESP32 + sensors), ~€90 per board
- Needs wall power for reliable repeaters (3-4 units), adds complexity
- Battery units last weeks not months
- Faster latency but unnecessary for our use case
- Tighter integration with home network if that becomes relevant later

## Decision
Test LoRa first. Order 2x TinyML kit plus gateway by Friday. Run 30-day battery test before full 12-unit rollout. Revisit if range proves insufficient.
