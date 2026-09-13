## Calling app fraud signals

Seeing a pattern in the fraud tickets: small transactions followed by refund requests within days. The requesters cite wrong number, poor connection quality, never call back in. Correlates with account creation timing, specifically accounts that add a payment method in the preceding 7 days. Those are running hot.

## Timing gaps

The refund requests come through support fast, sometimes same week. But the damage lands 30 to 60 days out when chargebacks hit the processor. By then the pattern is scattered across weeks of transaction logs and the connection to the original test transaction is easy to miss unless you're already looking for it. Creates a false sense of safety in the first weeks.

## Detection points

Payment method recency is the single strongest flag. Built a quick check that surfaces any transaction from an account where the card was added within the last 7 days. Cross referencing that with the small purchase plus quick refund request pattern shows the shape of it clearly. The refund angle masks what's happening until you see the chargeback months later.

Also tracking: requests coming from overlapping IP ranges, similar phone numbers used in account creation. Not enough signal alone but adds weight.