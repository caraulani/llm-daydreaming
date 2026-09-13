# Public corpora

- `arxiv-cs-2026/`: a small set of recent cs.CL / cs.AI abstracts (arXiv metadata is CC0), a
  secondary fully-public corpus for the generic markdown path. Populate with
  `uv run daydreamd fetch-arxiv --n 40`. On 2026-09-13 the arXiv API answered 429 and then timed
  out, so this directory ships with the manifest only once a fetch succeeds; the synthetic corpus
  in `data/synth/` is the primary public corpus and does not depend on it.
