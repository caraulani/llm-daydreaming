# Fraud ring identified via device fingerprint clustering

## Initial signal
- 47 accounts flagged in 72 hours for unusual payment patterns, $12k total
- All transactions declined after review, but spike in refund requests
- Standard velocity checks didn't catch it: different payment methods, different times

## Device fingerprint analysis
- Extracted device ID, OS version, IP geolocation, browser user agent from transaction logs
- 12 core device fingerprints appeared across 38 of the 47 accounts
- Shared devices: 4 Android phones in Lagos, 2 iPhones in Johannesburg, 3 compromised emulators
- One fingerprint linked 9 accounts; transactions spaced 4-6 minutes apart per account

## Pattern
- Each account created on different days, different payment cards (mostly stolen or fraudulent)
- Reused device fingerprints grouped by location, suggesting centralized operation
- Script-like behavior: exact transaction amounts ($50 twice, then $75) across linked accounts
- Same customer support contact phone number on 5 accounts (different email, same number)

## Action taken
- Blocked 12 device fingerprints, froze 38 accounts pending verification
- Added device fingerprint clustering to fraud detection rules
- Flagged transactions from Lagos/Johannesburg payment hubs for 30-day review