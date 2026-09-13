Rolling sensor cart for test rig mobility

## Build and specs

Cart built on 2" steel frame with locking casters (300lb capacity). Holds the primary sensor array (BME680, BMP390, DHT22) mounted on a cross-brace. Power distribution via 12V sealed lead-acid (7Ah). 24-port terminal strip for sensor wiring. Cart dimensions: 36" x 24" x 42" (height to sensor plane).

## Movement and positioning

Four locking casters keep the rig stable during data collection. Dolly handle welded to rear frame for one-handed rolling through workshop door. Test positions marked on floor with tape: north wall (thermal cycling), workbench offset (vibration tests), center zone (baseline). Rolling to new position takes 90 seconds including setup verification.

## Sensor mounting

Top shelf holds Raspberry Pi 4 in weatherproof enclosure, connected via USB hub. Sensor cables routed through spiral wrap along frame rails. Cross-brace provides 18" sensor separation for spatial gradient measurements. Magnetic mounts let sensors quick-swap without rewiring. Currently running 5-minute collection intervals to SD card.

## Current issues

Caster wheels tracking unevenly on concrete floor, causing 2-3 degree drift in sensor orientation. Need to re-level after repositioning. Terminal strip corrosion showing on some pins from condensation, switching to nickel-plated hardware next batch.