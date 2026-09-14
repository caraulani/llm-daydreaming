# Payment Tokenisation: Why Raw Cards Never Touch the Server

## Client-side tokenisation flow

We shifted the calling app to client-side tokenisation last quarter. Phone client captures card data, sends it straight to the payment processor's tokenisation endpoint (Stripe, Adyen, etc.), gets a token back. Server only ever sees the token. Reduces surface area for breaches and auditing burden.

## Raw card risk on legacy path

Before: fraud team had to monitor raw card streams to catch patterns. Theft or logs leaked, entire vault exposed. PCI DSS compliance meant separate infrastructure, isolated networks, restricted access logs. Too much state to keep clean.

## Tokenisation benefits observed

- Tokens are processor-specific. A stolen Stripe token doesn't work at Adyen. Reduces replay attack window.
- Fraud rules can run on the processor side. They have better velocity data across millions of merchants.
- Chargebacks still arrive normally. Token transaction history is queryable. No loss of audit trail for disputes.

## Ongoing work

- Audit app code paths where tokens are logged (not raw PAN, but token leakage is still a concern).
- Rotation policy: tokens expire quarterly. Forces periodic card verification from users.
- A/B testing dispute rates between tokenised and legacy app versions. Legacy cohort is shrinking by plan.