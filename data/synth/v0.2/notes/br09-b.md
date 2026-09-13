---
name: Fraud incident analysis 2024-09
description: Observations from last week's payments fraud attempt
type: project
---

## Last week's incident

Forty destination numbers flagged in the fraud run. Odd pattern: only the last two digits varied, incrementing cleanly from start to finish. Blocked before any funds cleared.

## Account creation

Three accounts placed the attempted transactions. All created within a 60-minute window. Each used a distinct name on the system, different email providers too: one Gmail, one ProtonMail, one Outlook. No overlap in the registration data.

## Detection and response

System flagged all three accounts immediately after detection. Transaction logs suggest the number-generation pattern hit known fraud signatures in our database, which is probably why it was caught before processing.

## Follow-up

Pull full audit trails for these three. Check if they share other signals: IP address, device fingerprint, any payment method attempts. The number pattern might suggest automation, might be manual. May need to tighten validation on new account creation windows.
