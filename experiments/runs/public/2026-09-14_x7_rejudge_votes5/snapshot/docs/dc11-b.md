# Thursday firmware flash, Friday reboot loop

## What happened

Flashed new firmware Thursday around 20:30 to two DHT-based environmental sensors in the workshop. Pushed update via local USB adapter. Both sensors appeared to complete the flash sequence without error messages.

Friday morning at 06:45, both units were in continuous reboot loop: status LED cycling every 8-10 seconds, no WiFi reconnection, logs not persisting.

## Attempted recovery

Tried standard power cycle on both units. No change in behavior. Connected unit 01 via USB and checked logs: last entry shows incomplete initialization sequence, memory address 0x2400-0x2800 region appears corrupted.

Rolled back unit 01 to previous firmware (v2.3.1) using serial connection. Unit recovered fully, WiFi up within 3 minutes.

## Status

Unit 01: reverted to v2.3.1, operational.
Unit 02: still in reboot loop, not yet touched.

Firmware file (v2.4.0 build from Thursday) checksummed. Flash process timing looks standard. Something broke in the new binary's initialization or memory layout on these older boards (both are revision C).

## Next

Need to check if flash utility version is mismatched. Don't apply v2.4.0 to unit 02 yet.