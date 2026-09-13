"""Whole pipeline on a tiny synthetic-like corpus with the fake backend and fake embedder."""

from __future__ import annotations

from pathlib import Path

import yaml

from daydreamd import pipeline
from daydreamd.core.io import write_json


def _tiny_corpus(root: Path) -> Path:
    notes = root / "notes"
    notes.mkdir(parents=True)
    docs = []
    gold = {}
    for b in ("br01", "br02"):
        for side in ("a", "b"):
            nid = f"{b}-{side}"
            text = f"---\nname: {nid}\n---\n# {nid}\n\n" + " ".join(
                f"fact {nid} {i} about work" for i in range(40)
            )
            (notes / f"{nid}.md").write_text(text)
            from daydreamd.core.io import sha256_text

            docs.append(
                {
                    "id": nid,
                    "domain": "d" + side,
                    "kind": "bridge",
                    "bridge_id": b,
                    "decoy_id": None,
                    "sha256": sha256_text(text),
                    "words": 40,
                    "tries": 1,
                    "leaks_final": [],
                }
            )
        gold[b] = {
            "note_a": f"{b}-a",
            "note_b": f"{b}-b",
            "domain_a": "da",
            "domain_b": "db",
            "hidden_mechanism": "m",
            "gold_connection": "gold " + b,
            "gold_implication": "imp " + b,
        }
    for k in range(4):
        nid = f"fl0{k}"
        text = f"---\nname: {nid}\n---\n# {nid}\n\n" + " ".join(
            f"filler {nid} {i} note" for i in range(40)
        )
        (notes / f"{nid}.md").write_text(text)
        from daydreamd.core.io import sha256_text

        docs.append(
            {
                "id": nid,
                "domain": f"d{k % 2}",
                "kind": "filler",
                "bridge_id": None,
                "decoy_id": None,
                "sha256": sha256_text(text),
                "words": 40,
                "tries": 1,
                "leaks_final": [],
            }
        )
    write_json(
        root / "manifest.json",
        {
            "n_bridges": 2,
            "n_decoys": 0,
            "leakage_failures": [],
            "writer_model_ids": ["fake"],
            "corpus_sha256": "x",
            "docs": docs,
            "n_notes": len(docs),
        },
    )
    write_json(root / "gold.json", gold)
    write_json(root / "domains.json", {d["id"]: d["domain"] for d in docs})
    return root


def test_run_all_offline(tmp_path: Path):
    corpus = _tiny_corpus(tmp_path / "corpus")
    cfg = {
        "corpus": {"kind": "synth", "path": str(corpus)},
        "visibility": "public",
        "slug": "offline",
        "seed": 1,
        "backend": "fake",
        "models": {"cards": "haiku", "generator": "sonnet", "critic": "haiku", "match": "haiku"},
        "concurrency": 2,
        "arms": {
            "S0": {"random_pairs": 2},
            "B1": {"n": 5},
            "B3": {"per_band": 1},
            "B6": {"n": 3},
            "B4": {"notes": "bridge"},
        },
        "blind": {"enabled": True},
        "stats": {"n_perm": 200},
    }
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg))
    run = pipeline.run_all(pipeline.load_config(cfg_path), run_root=tmp_path / "runs")
    meta = run.read_meta()
    assert set(meta["stages"]) >= {
        "snapshot",
        "cards",
        "embed",
        "sample",
        "generate",
        "critic",
        "dupgate",
        "match_gold",
        "blind",
        "stats",
    }
    assert meta["models"]["generator"]["model_id"] == "fake-sonnet"
    assert (run.path / "tables" / "T4.md").exists()
    assert (run.path / "blind" / "key.sha256").exists()
    arms = meta["stages"]["sample"]["arms"]
    assert arms["S0"] == 4 and arms["B4"] == 4 and arms["B1"] == 5
