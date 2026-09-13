# Dream registry (Track B)

A public, timestamped record of dreams generated over live corpora. Its purpose is priority and accountability: a dream is published before anyone knows whether it holds, so later outcomes can be counted honestly.

## Two outcome classes, both count

- **Independently discovered.** Someone who did not read the registry later publishes or builds the same connection. Evidence: a link and a date after the entry's timestamp.
- **Adopted from the registry.** Someone reads a dream and builds on it. That is impact, not contamination, and it is recorded as its own class so the two are never mixed.

Outcomes are recorded by editing the entry's `README.md` under "Outcomes", with a link, a date, and the ADR-012 claim class.

## Layout

```
registry/entries/<YYYY-MM-DD>_<slug>/
├── metadata.yaml        # who, corpus description, models, prompt versions, counts
├── README.md            # short narrative + Outcomes section (kept up to date)
├── dreams.jsonl         # one dream per line, structured
└── dreams.jsonl.ots     # OpenTimestamps proof for dreams.jsonl
```

`<slug>` is lowercase, hyphenated, at most 40 characters. Copy `registry/entries/_TEMPLATE/`.

Each line of `dreams.jsonl`:

```json
{"id": "...", "connection": "...", "mechanism": "...", "testable_implication": "...", "needs": "...", "sources": ["card-id", "card-id"], "arm": "B6", "distance_band": "Q4", "claim_class": "unclassified", "generator": "<snapshot-id>", "prompt_sha": "..."}
```

Heavy artifacts (full raw outputs, embeddings) stay in the submitter's repository. The entry holds pointers.

## Timestamping

Install the client, stamp, commit the proof, upgrade later:

```bash
uv tool install opentimestamps-client
ots stamp registry/entries/<entry>/dreams.jsonl        # writes dreams.jsonl.ots (pending)
git add registry/entries/<entry>/                      # commit proof with the entry
# A Bitcoin anchor takes hours. Later:
ots upgrade registry/entries/<entry>/dreams.jsonl.ots  # replaces pending attestation with the block proof
ots verify registry/entries/<entry>/dreams.jsonl.ots   # checks against the file
```

Commit the upgraded `.ots` file when it is ready. The git commit date is a second, weaker timestamp; the `.ots` proof is the one that counts.

Stamp the file, not the git commit. The OpenTimestamps git wrapper does not validate commit timestamps by its own documentation.

## Submitting an entry

1. Open an issue using the "Registry entry" template.
2. Copy `_TEMPLATE/`, fill it in, stamp `dreams.jsonl`.
3. Open a pull request adding exactly one directory. No edits to other entries.
4. Checks: no secrets, no private names, no third-party personal data, every dream has all fields, `claim_class` starts as `unclassified`.

Entries are published under CC BY 4.0 (see `LICENSING.md`). Once merged, an entry's `dreams.jsonl` is never edited; corrections go in `README.md`.

## What the registry is not

- Not a leaderboard. There is no score.
- Not a claim of novelty. `claim_class` is assigned only after the retrieval checks in ADR-004 and ADR-012.
