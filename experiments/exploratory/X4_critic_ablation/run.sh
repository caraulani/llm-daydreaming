#!/usr/bin/env bash
# Re-run only the critic (and the stages after it) on a copy of the sealed run's outputs.
set -euo pipefail
SRC=experiments/runs/public/2026-09-13_micro
DST=experiments/runs/public/2026-09-13_x4_critic_sonnet
CFG=experiments/exploratory/X4_critic_ablation/config.yaml
rm -rf "$DST"; cp -R "$SRC" "$DST"
rm -f "$DST"/critic.jsonl "$DST"/dupgate.jsonl; rm -rf "$DST"/tables
python3 - "$DST" <<'PY'
import sys, yaml, pathlib
p = pathlib.Path(sys.argv[1]) / "metadata.yaml"; m = yaml.safe_load(p.read_text())
m["run_id"] = "2026-09-13_x4_critic_sonnet"; m["config"] = "experiments/exploratory/X4_critic_ablation/config.yaml"
m["derived_from"] = "2026-09-13_micro (generations, cards, units, match_gold reused verbatim)"
for k in ("critic", "dupgate", "stats"): m.get("stages", {}).pop(k, None)
p.write_text(yaml.safe_dump(m, sort_keys=False))
PY
uv run daydreamd critic "$DST" "$CFG"
uv run daydreamd dupgate "$DST" "$CFG"
uv run daydreamd stats "$DST" "$CFG" --out "results/public/2026-09-13_x4_critic_sonnet"
