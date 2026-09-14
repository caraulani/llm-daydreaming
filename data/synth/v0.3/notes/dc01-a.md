---
name: gc-2201-2238-batch
description: May 12 gift card batch, 38 units, sequential numbering issue order
type: project
---

# Gift card batch GC-2201 to GC-2238 on 12 May

## Order volume and timing
38 orders came through on 12 May. All routed to gift cards. System assigned codes GC-2201 through GC-2238 based on issue order, not purchase order. Codes are sequential by when cards were created in the system, not by when orders landed.

## Numbering scheme
Each code corresponds to the nth card issued: GC-2201 is the 2201st card ever issued, GC-2238 is the 2238th. The 38-order batch doesn't start at a round number because card issuance is continuous across days. Gaps in the series mean other orders created cards between these dates or earlier.

## Reconciliation notes
Need to track which customer got which code range. Invoice records should match code assignments. If a customer complains about a code not working, check the creation timestamp against the 12 May window. System doesn't deduplicate; each order creates a fresh card even if the same customer orders twice.

## Data held
Order IDs, customer email, amount, code. Card balances stored separately in the provider system (Shopify or custom). No backup of balances kept locally.
