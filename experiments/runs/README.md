# Runs

Every stage writes into `experiments/runs/<public|private>/<YYYY-MM-DD>_<slug>/`:

| File | Written by | Contents |
|---|---|---|
| `metadata.yaml` | every stage | exact model ids, prompt SHAs, seed, corpus SHA, timestamps, measured cost |
| `snapshot/manifest.json`, `snapshot/docs/` | snapshot | frozen corpus (docs are copied; private runs are gitignored) |
| `cards.jsonl` | cards | concept cards, cached per note SHA in `cards_cache.jsonl` |
| `embeddings.npy` | embed | local sentence-transformer vectors, one row per card |
| `units.jsonl` | sample | generator inputs per arm, with band, distance, and planted/decoy label |
| `generations.jsonl` | generate | raw structured outputs, `NONE`, malformed, or error, with usage |
| `critic.jsonl` | critic | keep/kill with reason |
| `dupgate.jsonl` | dupgate | nearest corpus text and cosine for each survivor |
| `match_gold.jsonl` | match-gold | grounded match verdict and cosine to gold for planted units |
| `blind/items.md`, `blind/key.json`, `blind/key.sha256` | blind | owner-blind pack; the key is sealed by hash |
| `verdicts.jsonl` | score --unseal | owner verdicts joined to arms |
| `tables/` | stats | T1 to T6 (synthetic), H1 to H4 (owner-blind), `summary.md`, `exploratory_finds.jsonl` |

`experiments/runs/private/` is gitignored. Public runs are committed so `make reproduce` can
rebuild every table without any model call.
