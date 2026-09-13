"""Owner-blind scoring pack (Track C). Items show only generated text, never arm, band, or the
source claims (a single-claim source would reveal the reflection arm). The key is sealed by hash
before scoring; `score --unseal` verifies the hash before joining verdicts to arms."""

from __future__ import annotations

import random
import re
from pathlib import Path

from .io import read_json, sha256_file, write_json, write_jsonl
from .run import RunDir

BATCH = 20
REPEATS = 30
ITEM_RE = re.compile(r"^### Item (\d{3})\s*$")
KEEP_RE = re.compile(r"^- \[(x|X| )\] KEEP")
KNOWN_RE = re.compile(r"^- \[(x|X| )\] KNOWN")


def _render_item(n: int, out: dict) -> str:
    return (
        f"### Item {n:03d}\n"
        f"**Connection:** {out['connection']}\n\n"
        f"**Mechanism:** {out['mechanism']}\n\n"
        f"**Testable implication:** {out['testable_implication']}\n\n"
        "- [ ] KEEP: I would act on this or write it down\n"
        "- [ ] KNOWN: I already had this thought\n"
    )


def build_pack(run: RunDir, generations: list[dict], seed: int, repeats: int = REPEATS) -> Path:
    items = [g for g in generations if g["status"] == "ok"]
    rng = random.Random(seed)
    rng.shuffle(items)
    n_rep = min(repeats, len(items) // 3)
    rep_src = rng.sample(range(len(items)), n_rep) if n_rep else []
    key: dict[str, dict] = {}
    lines = ["# Blind scoring pack", "", "Score every item. Do not open blind/key.json.", ""]
    n = 0
    for g in items:
        n += 1
        if (n - 1) % BATCH == 0:
            lines.append(f"## Batch {(n - 1) // BATCH + 1}\n")
        lines.append(_render_item(n, g["output"]))
        key[f"{n:03d}"] = {
            "unit_id": g["unit_id"],
            "arm": g["arm"],
            "band": g["band"],
            "repeat_of": None,
        }
    if rep_src:
        lines.append("## Consistency block (repeats, do not look back)\n")
    for src in rep_src:
        n += 1
        g = items[src]
        lines.append(_render_item(n, g["output"]))
        key[f"{n:03d}"] = {
            "unit_id": g["unit_id"],
            "arm": g["arm"],
            "band": g["band"],
            "repeat_of": f"{src + 1:03d}",
        }
    blind = run.path / "blind"
    blind.mkdir(exist_ok=True)
    (blind / "items.md").write_text("\n".join(lines), encoding="utf-8")
    write_json(blind / "key.json", key)
    (blind / "key.sha256").write_text(sha256_file(blind / "key.json") + "\n", encoding="utf-8")
    run.mark_stage(
        "blind", n_items=len(items), n_repeats=n_rep, key_sha256=sha256_file(blind / "key.json")
    )
    return blind / "items.md"


def parse_scores(items_md: Path) -> list[dict]:
    rows: list[dict] = []
    current: dict | None = None
    for line in items_md.read_text(encoding="utf-8").splitlines():
        m = ITEM_RE.match(line)
        if m:
            current = {"item": m.group(1), "keep": False, "known": False}
            rows.append(current)
            continue
        if current is None:
            continue
        if k := KEEP_RE.match(line):
            current["keep"] = k.group(1).lower() == "x"
        elif k := KNOWN_RE.match(line):
            current["known"] = k.group(1).lower() == "x"
    return rows


def unseal(run: RunDir) -> list[dict]:
    blind = run.path / "blind"
    expected = (blind / "key.sha256").read_text(encoding="utf-8").strip()
    actual = sha256_file(blind / "key.json")
    if expected != actual:
        raise RuntimeError("key.json hash does not match key.sha256; the seal is broken")
    key = read_json(blind / "key.json")
    verdicts = [{**row, **key[row["item"]]} for row in parse_scores(blind / "items.md")]
    write_jsonl(run.path / "verdicts.jsonl", verdicts)
    run.mark_stage("score", n_scored=len(verdicts))
    return verdicts
