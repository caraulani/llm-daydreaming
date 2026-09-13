# Extending daydreamd

Core is small on purpose. Everything that touches a specific data source or a specific model provider goes through one of two small interfaces. Extensions live outside the core package unless `ROADMAP.md` lists them.

## Adapter: a corpus source

An adapter turns some store of text into a list of `Doc` records. The engine never learns where they came from.

```python
from daydreamd.core.ingest import Doc, load_markdown_folder

@dataclass
class Doc:
    id: str     # stable within the corpus; the manifest hashes the set of ids and shas
    name: str   # human-readable, shown in morning.md; redacted when --anonymise is set
    text: str   # frontmatter already stripped
    sha: str    # sha256 of text
```

The built-in adapters live in `src/daydreamd/adapters/` and are selected by the `corpus.kind` key in an experiment config (`synth`, `claude-memory`, `markdown`, `arxiv`). Each exposes one function:

```python
def load(path: Path, excludes: list[str] | None = None) -> list[Doc]: ...
```

Rules:

- `load()` must be deterministic for an unchanged source. The pipeline writes every id and sha into `manifest.json` and fails the run if the set changes mid-run.
- Never fetch over the network inside an adapter. If the source is remote, sync it to disk first, outside daydreamd. The arXiv adapter reads a pinned manifest that a separate `fetch-arxiv` command produced.
- Secret stripping is a filename exclusion pass, not a content scanner. `daydreamd.core.ingest.DEFAULT_EXCLUDES` drops files whose names match `*credential*`, `*secret*`, `*password*`, `*paperwork*` and `MEMORY.md`; the Claude memory adapter adds `*token*`. Pass more patterns through `excludes`. Treat this as a floor: review your corpus before you point anything at it.
- Output must go under the run directory only.

### Worked example: a folder of markdown

`src/daydreamd/adapters/markdown_folder.py` is the reference implementation and is about ten lines:

```python
from pathlib import Path
from daydreamd.core.ingest import Doc, load_markdown_folder

def load(path: Path, excludes: list[str] | None = None) -> list[Doc]:
    return load_markdown_folder(path, excludes)
```

To add a new kind, write a module with the same `load()` signature and add one branch to `load_corpus()` in `src/daydreamd/adapters/__init__.py`. Ship it as a pull request with a fake-backend test that ingests a fixture and checks the document count and the exclusion pass (see `CONTRIBUTING.md`). Obsidian, codebase and Zotero adapters are stubs that raise `NotImplementedError` with a docstring describing the intended behaviour.

## Backend: a model provider

A backend sends one prompt and returns the metadata the paper needs.

```python
from daydreamd.backends import Backend, Completion

@dataclass
class Completion:
    text: str
    model_id: str       # the exact snapshot id the provider reported, never the alias requested
    input_tokens: int
    output_tokens: int
    cost_usd: float     # at list price; 0.0 when the provider reports none
    raw: dict           # the provider's full response envelope, kept in the run log

class Backend(Protocol):
    name: str
    def complete(self, prompt: str, *, model: str) -> Completion: ...
```

Built-in backends, selected by the `backend` key in a config: `claude-cli` (default, runs `claude -p --output-format json` and reads the exact model id from the `modelUsage` envelope), `anthropic` (the Anthropic API, needs `ANTHROPIC_API_KEY`), `fake` (deterministic, used by the tests and CI), `ollama` (stub for v0.2).

Rules:

- Report the provider's snapshot id. If the provider only returns an alias, resolve it once at startup and record the resolution date in `metadata.yaml`.
- A refusal is returned as empty text. The pipeline logs it as NONE with a flag. Do not retry refusals.
- Retry only on transport and rate-limit errors, with backoff, at most three times, and log every retry.
- The `fake` backend must stay deterministic: same inputs, same output. CI depends on it.

## Sampler or critic: a new experiment arm

Do not subclass core. Add a directory under `experiments/` with a `config.yaml` naming the arm and its sizes, run it, then submit the run directory as a replication (see `CONTRIBUTING.md`). Arms that hold up get an ADR and a place in the matrix.

## What not to extend

- The evaluation harness in `src/daydreamd/eval/`. Changing it changes every published number. Open an issue.
- Prompts in `prompts/`, without bumping the version header. Their SHAs are recorded in every run.
- The pre-registered sizes in `experiments/micro/config.yaml`.
