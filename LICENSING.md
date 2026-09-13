# Licensing

This repository uses two licenses. Which one applies depends on the path.

| Path | License | File |
|---|---|---|
| `src/`, `tests/`, `prompts/`, `experiments/*/run.sh`, `Makefile`, `pyproject.toml`, everything not listed below | MIT | `LICENSE` |
| `paper/`, `data/`, `registry/`, `docs/`, `design/`, `research/`, `results/` | CC BY 4.0 | `LICENSE-CC-BY-4.0` |

Why the split: code should be reusable in any product without attribution friction (MIT). The paper, the released corpus slices, the dream registry, and the written decisions are research outputs, and CC BY 4.0 is the license arXiv, Hugging Face, and Zenodo expect for those. It permits remixing, and it requires a citation.

The arXiv version of the paper will be submitted under CC BY 4.0. That choice is irrevocable per arXiv version.

Prompts are licensed as code (MIT) on purpose: a prompt committed verbatim is part of the runnable artifact, and we want it copied.

Private runs (`experiments/runs/private/`, `data/private/`, `results/private/`) are gitignored and never published. No license applies to them because they never leave the machine they were produced on.

If you contribute, you agree that your contribution is licensed under the license of the path it lands in. See `CONTRIBUTING.md` for the DCO sign-off.
