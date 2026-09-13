## The problem

After power cuts, all sensors come back online at once. Gateway handles normal traffic fine, but the simultaneous reconnection flood causes packet drops. Had it happen in workshop after recent outage; lost about 80% of reconnect confirmations. Tested with 12 sensors across bench setup.

## Testing the fix

Added random delay before each sensor transmits after coming back online. Range of 50-500ms per device seemed reasonable. Drops disappeared immediately. No packet loss in subsequent tests, even with deliberate power cycles.

## Current state

System stable for past 3 days. Gateway stays cool under normal load and handles power events without dropping packets now. Planning to expand sensor count this month when new hardware arrives.