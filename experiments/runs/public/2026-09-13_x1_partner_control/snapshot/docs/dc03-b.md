# Tokenisation and Server Safety

## Why Raw Cards Never Land Here

Server compromise means card breach. Tokenisation outsources the risk: Stripe/Square/processor handles PCI scope. Raw card data goes directly from client to processor over HTTPS, returns a token. We store tokens only.

## The Flow

Client collects card → sends to processor's API endpoint (not ours) → processor validates and returns token string → token goes to our server → we charge against the token. If someone gets into our DB, they get tokens, not cards. Processor can rotate tokens. Cards cannot be un-disclosed.

## What This Costs Us

3-4% processor fees. Non-negotiable. The convenience of "just store the card" would save fees but costs fraud liability, PCI audits, and regulatory exposure. For a fraud product, this is baseline hygiene.

## Current State

Implemented via Stripe Connect. Tokens expire based on processor rules. Fraud scoring sees transaction metadata (amount, location, device), not the card itself, so detection logic stays clean of PCI requirements. Chargebacks still come to us; we log disputes and feed patterns back to processor for decline tuning.