---
name: CDN overload after TV feature
description: Image serving bottleneck during traffic spike from broadcast mention
type: project
---

## CDN choked on traffic spike

Segment ran last week (Tuesday 7pm UTC). Viewers hit store immediately. Image requests spiked from ~50/min baseline to ~12k/min within 8 minutes. CDN buckled: thumbnails timed out, product pages stalled, checkout abandoned. Full cascade resolved after 52 minutes of manual intervention.

## What broke

- CDN origin server ran out of file handles at ~8k concurrent connections.
- No autoscaling rule was set for this endpoint; threshold was manual inspection only.
- Cached layer did its job (full miss rate ~18%), but origin had no backpressure mechanism.
- Logs show ~6% error rate during peak; most were 503s.

## Fix applied

- Raised concurrent connection limit on origin from 2048 to 8192.
- Set autoscale trigger at 5000 connections.
- Added hard cache rule: 1 hour TTL minimum for product thumbnails (was 15 min).
- Configured 429 rate limiter at 100 req/sec per IP to catch bots.

## Numbers

- Checkout completions dropped 34% during the hour.
- Estimated lost revenue: €2.8k (48 carts abandoned mid-flow).
- Recovery took 52 min from detection to stability.
