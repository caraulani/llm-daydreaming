# Data

## Layout

```
data/
├── README.md               # this file
├── DATASHEET_TEMPLATE.md   # fill one per released slice
├── synth/v0.1/             # the v0.1 synthetic corpus with planted ground truth (released, CC BY 4.0)
│   ├── notes/              # 60 markdown notes of a fictional solo builder, written by a model
│   ├── bridges.yaml        # 12 hand-authored cross-domain bridges (written BEFORE the notes)
│   ├── decoys.yaml         # 6 note pairs that share vocabulary but have no bridge
│   ├── gold.json           # planted pairs and decoy pairs in machine-readable form
│   ├── manifest.json       # filename, byte length, SHA-256 per file, plus the manifest's own hash
│   └── datasheet.md        # filled datasheet
├── public/                 # other released slices (arXiv abstracts for the yield curve, v0.2)
└── private/                # gitignored; frozen snapshots of private corpora never leave this machine
```

## The v0.1 synthetic corpus (primary released dataset)

Why synthetic: the first experiment needs ground truth that exists by construction, a corpus anyone can rerun, and zero privacy exposure. See ADR-013.

How it was built, in order:

1. A human wrote `bridges.yaml`: 12 connections, each between two topics that differ on the surface, each with a `mechanism` and a `testable_implication`. Written before any note existed.
2. A human wrote `decoys.yaml`: 6 pairs of topics that share vocabulary but have no real connection.
3. A model wrote the 60 notes in `notes/`, instructed to express each bridge's two halves in two separate notes without stating the bridge, and to write the decoy topics so they overlap in wording. The note-writing model's snapshot ID is in `datasheet.md` and `manifest.json`.
4. A leakage check embedded every bridge statement and retrieved against all note chunks; the maximum similarity must stay below the corpus-duplicate threshold used by the pipeline (0.85 in v0.1). The result is recorded in `datasheet.md`.
5. `gold.json` was generated from the two YAML files. `manifest.json` freezes everything.

What a run measures against it: whether a dream's two source cards come from a planted pair, and whether its `connection` matches the planted bridge (retrieval plus an entailment check between two in-context texts, ADR-004). Decoy pairs give the false-positive rate.

Known limitation: the notes were written by a model, and the generator may share a model family with it. `datasheet.md` states both snapshot IDs. v0.2 regenerates the notes with a second family.

## Private corpora

`data/private/` is listed in `.gitignore`. A private run (Track C) freezes a copy of the corpus here, strips files matching secret patterns, and records a manifest as above. The manifest hash goes into the run's `metadata.yaml`. The text does not.

What gets published from a private run: counts, rates, verdict labels, prompt versions, model snapshot IDs, cost, and raw outputs with `connection` and `mechanism` replaced by their SHA-256. Owner-approved example dreams may appear under `examples/` after manual redaction. See ADR-010.

## Public corpora

Each released slice under `data/public/<name>/` ships with a filled `datasheet.md`, a `manifest.json`, the source license, and a build script that regenerates the slice from its source (for example, an arXiv ID list plus the fetch command), so the slice can be rebuilt where redistribution is not allowed.

Public slices are published under CC BY 4.0 where the source license permits; otherwise only the ID list and the build script are committed.

## Mirrors

Large slices are mirrored as Hugging Face datasets with the same datasheet as the dataset card. The README links each mirror.
