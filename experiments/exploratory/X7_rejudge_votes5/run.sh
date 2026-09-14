#!/usr/bin/env bash
# EXPLORATORY, NOT PREREGISTERED. Re-judge every answered planted unit of the sealed v0.3 run with
# five match-judge votes (majority) to measure judge consistency; the sealed run used two votes.
set -euo pipefail
SRC=experiments/runs/public/2026-09-14_micro_v0_3
DST=experiments/runs/public/2026-09-14_x7_rejudge_votes5
CFG=experiments/exploratory/X7_rejudge_votes5/config.yaml
rm -rf "$DST"; cp -R "$SRC" "$DST"; rm -f "$DST"/match_gold.jsonl; rm -rf "$DST"/tables
python3 - "$DST" <<'PY'
import sys, yaml, pathlib
p = pathlib.Path(sys.argv[1]) / "metadata.yaml"; m = yaml.safe_load(p.read_text())
m["run_id"] = "2026-09-14_x7_rejudge_votes5"; m["config"] = "experiments/exploratory/X7_rejudge_votes5/config.yaml"
m["derived_from"] = "2026-09-14_micro_v0_3 (generations, critics, dupgate reused verbatim; match re-run with five votes)"
for k in ("match-gold", "stats"): m.get("stages", {}).pop(k, None)
p.write_text(yaml.safe_dump(m, sort_keys=False))
PY
uv run daydreamd match-gold "$DST" "$CFG"
uv run daydreamd stats "$DST" "$CFG" --out results/public/2026-09-14_x7_rejudge_votes5
