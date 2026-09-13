# ADR-011: Default backend is headless `claude -p`; generators are pluggable

**Status:** Accepted, 2026-09-13.

## Context

The owner's own runs can drive the `claude` CLI in headless mode (`claude -p ... --output-format json`) on a subscription, at zero marginal cost. Verified on 2026-09-13: a round trip returns JSON with the model snapshot, token usage and cost in about 3.5 seconds. Track A requires an old-cutoff open-weight generator (ADR-007), and the community will want Ollama, so the generator must be swappable regardless.

## Decision

A `Backend` protocol with one method: complete(prompt, system, model, params) returning text plus usage metadata (snapshot ID, tokens, cost, latency). Implementations: `claude_cli` (default), `anthropic_api`, `openrouter`, `ollama`, and `fake` (deterministic, for tests and CI). The judge and critic slots are config values and may point at different backends than the generator.

## Consequences

- CI never calls a model: `DAYDREAMD_BACKEND=fake`.
- Every run records the snapshot ID the backend reported, never the alias that was requested.
- Handle `stop_reason: "refusal"` as a NONE with a flag, never as a crash. Never prompt for model reasoning; dreams are output text.
- Enterprises on zero-data-retention terms need the judge slot swappable; it is.

## Sources

- BRIEF.md, daemon spec (ship shape) and Risks (Fable-specific).
