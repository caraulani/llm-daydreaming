## Tickets and timing

Found a call ticket that was issued three days prior, then presented for a new call. The signature verified correctly on our end, so the system accepted it. Each ticket carries a timestamp from when it was issued, embedded in the token itself.

## What happened

During last week's fraud review, spotted an incident: ticket from Tuesday 5th being used for a fresh call on Friday 8th. Server-side validation only checks the signature itself, not whether the issue time makes sense for the present moment. No errors thrown because cryptographically it's clean. Attacker had a valid signed token and used it multiple times.

## Root cause

Validation logic stops at signature verification. Doesn't look at the timestamp field in the ticket. Implementation gap, not a crypto issue.

## Next steps

Need to understand if this is isolated or systematic. Will run broader audit on recent tickets to see if there are other instances with similar gaps. Check if other systems have the same blind spot.