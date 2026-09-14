.PHONY: setup test lint typecheck smoke synth micro blind stats reproduce dream clean

UV ?= uv
RUN ?=
CONFIG ?= experiments/micro/config.yaml

setup:
	$(UV) sync --all-extras

test:
	$(UV) run pytest -q

lint:
	$(UV) run ruff check src tests
	$(UV) run ruff format --check src tests

typecheck:
	$(UV) run mypy src

SPEC ?= data/synth/v0.1
WRITERS ?=
MIN_WORDS ?= 150
RESUME ?=
synth:
	$(UV) run daydreamd synth --out $(SPEC) --min-words $(MIN_WORDS) $(if $(WRITERS),--writers $(WRITERS),) $(if $(RESUME),--resume,)

# End-to-end on the committed synthetic corpus with tiny arms. Real model calls.
smoke:
	$(UV) run daydreamd run-all experiments/smoke/config.yaml

# The pre-registered micro-experiment. Do not run before PREREGISTRATION.md is sealed.
micro:
	$(UV) run daydreamd run-all $(CONFIG)

blind:
	$(UV) run daydreamd blind $(RUN) $(CONFIG)

stats:
	$(UV) run daydreamd stats $(RUN) $(CONFIG)

# Rebuild every public table from committed run outputs. No API keys, no model calls.
reproduce:
	@for d in experiments/runs/public/*/; do \
	  name=$$(basename $$d); cfg=$$(grep '^config:' $$d/metadata.yaml | sed 's/config: //'); \
	  if [ ! -f $$d/match_gold.jsonl ] && [ ! -f $$d/blind/key.sha256 ]; then echo "== $$name (incomplete, skipped)"; continue; fi; \
	  echo "== $$name ($$cfg)"; \
	  $(UV) run daydreamd stats $$d $$cfg --out results/public/$$name; \
	done

# Product: one night over a folder of notes (real model calls). NOTES=~/vault KIND=obsidian
NOTES ?=
KIND ?= markdown
dream:
	$(UV) run daydreamd dream $(NOTES) --kind $(KIND)

clean:
	rm -rf .pytest_cache .ruff_cache

# Build the documentation site (paper, preregistrations, results, research notes) into site/.
docs:
	$(UV) run python scripts/build_docs.py
	$(UV) run mkdocs build --strict

docs-serve:
	$(UV) run python scripts/build_docs.py
	$(UV) run mkdocs serve
