---
name: support-email-spike-carrier-switch
description: Email volume tripled after parcel carrier change, operations impact
type: project
---

# Support volume spike after carrier switch

## Timeline and numbers

Switched parcel carriers on Sept 1st. Email volume to support went from ~40/day baseline to 120+/day by Sept 5th. Still elevated. Peak was Sept 7th at 180 emails.

## What's driving it

Most emails are tracking/status questions. Old carrier had better customer-facing tracking pages; new carrier's tracking either lags 24+ hours or shows generic "in transit" states. Customers can't tell if packages are stuck or normal.

Some delivery delays: ~8% of orders taking 2+ days longer than quoted. A few refund requests tied to this.

Returns/damaged goods mentions up slightly (3 vs 1-2 per day), might be unrelated or coincidence.

## What I've tried

Added a FAQ section to post-purchase email with carrier tracking tips and expected timelines. Reduced new incoming by maybe 15%.

Set auto-responder to confirm receipt + link to FAQ. Not measuring impact yet.

## Open

Need to quantify how much is education vs actual delays. Set aside time this week to spot-check 20 recent orders against actual carrier API data. Might need to escalate with carrier if delays are systematic.

Decision point: stay with new carrier 60 days (committed rate) or eat early exit fee if trends don't stabilize by Sept 20th.
