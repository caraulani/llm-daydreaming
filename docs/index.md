# daydreamd documentation

daydreamd is a selection engine for machine-generated ideas. It recombines distant concepts from a corpus, filters the recombinations hard, and evaluates the survivors against ground truth instead of against a model's opinion.

## Where to start

| You want to | Read |
|---|---|
| Run it in 60 seconds | `README.md` at the repository root |
| Know what was decided and why | `design/` (one ADR per decision) |
| Know what we promised to measure before we measured it | `PREREGISTRATION.md` |
| Rerun the v0.1 experiment | `experiments/` and `make reproduce` |
| Write an adapter or a backend | [extending.md](extending.md) |
| Run the owner-blind scoring protocol on your own corpus (Track C) | [human-eval-protocol.md](human-eval-protocol.md) |
| Write the contamination statement for a run | [contamination.md](contamination.md) |
| Submit a dream to the public registry (Track B) | `registry/README.md` |
| See how far the repo is from "by the book" | [publishing-checklist.md](publishing-checklist.md) |
| Read the paper | `paper/paper.md` |

## The three evaluation tracks

- **Track A, retrospective.** Old-cutoff generator over a time-frozen public corpus; hits detected by retrieval over later literature. Structurally leakage-free. Planned for v0.3.
- **Track B, prospective registry.** Dreams published with OpenTimestamps proofs before anyone knows if they hold. Planned for v0.4.
- **Track C, human usefulness.** Owner-blind KEEP / KNOWN verdicts over private corpora. Protocol written now, run after v0.1.

v0.1 is none of these. It is a synthetic micro-experiment with planted ground truth (ADR-013), designed so the protocol can be checked by anyone before it is pointed at anything real.

## Privacy in one paragraph

Corpus text is read from local paths, embedded on-device, and sent only to the model backend you configured. No telemetry. Private runs live under gitignored paths. If any of that is ever untrue, it is a security bug: see `SECURITY.md`.
