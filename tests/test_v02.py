"""v0.2 pieces, offline: oblique specs, writer families, the leak judge, multi-critic runs,
table T8 and the v0.2 decision rule."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from daydreamd import pipeline
from daydreamd.backends import Completion
from daydreamd.backends.fake import FakeBackend
from daydreamd.core.io import write_json
from daydreamd.synth.generate import build_corpus, judge_leak, load_writers
from daydreamd.synth.spec import Spec, assign_writers, load_spec

REPO = Path(__file__).resolve().parents[1]


def _spec(oblique: bool) -> Spec:
    bridge = {
        "id": "br01",
        "domain_a": "x",
        "domain_b": "y",
        "hidden_mechanism": "the mechanism",
        "gold_connection": "gold connection sentence one two three four five six",
        "gold_implication": "gold implication sentence one two three four five six",
        "ingredients_a": ["fact a1", "fact a2"],
        "ingredients_b": ["fact b1"],
    }
    if oblique:
        bridge["forbidden_phrases_a"] = ["secret noun", "diagnosis"]
        bridge["forbidden_phrases_b"] = ["other noun"]
        bridge["one_side_test"] = "nothing"
    return Spec(
        persona="a builder",
        domains={"x": "domain x", "y": "domain y"},
        bridges=[bridge, {**bridge, "id": "br02"}],
        decoys=[
            {
                "id": "dc01",
                "note_a": {"domain": "x", "topic": "t1"},
                "note_b": {"domain": "y", "topic": "t2"},
            }
        ],
        fillers=[{"domain": "x", "topic": "f1"}, {"domain": "y", "topic": "f2"}],
    )


def test_v02_spec_loads_and_forbids_per_side_phrases():
    spec = load_spec(REPO / "data" / "synth" / "v0.2")
    assert spec.oblique and len(spec.bridges) == 24 and len(spec.decoys) == 12
    plan = spec.note_plan()
    assert len(plan) == 96
    a = next(n for n in plan if n.note_id == "br01-a")
    for phrase in spec.bridges[0]["forbidden_phrases_a"]:
        assert phrase in a.forbidden
    assert not load_spec(REPO / "data" / "synth" / "v0.1").oblique


def test_writer_assignment_by_parity():
    plan = assign_writers(_spec(True).note_plan(), ["A", "B"])
    fam = {n.note_id: n.writer_family for n in plan}
    assert fam["br01-a"] == "A" and fam["br01-b"] == "A" and fam["br02-a"] == "B"
    assert fam["dc01-a"] == "A" and fam["fl01"] == "A" and fam["fl02"] == "B"
    single = assign_writers(_spec(False).note_plan(), ["A"])
    assert all(n.writer_family == "A" for n in single)
    untouched = assign_writers(_spec(False).note_plan(), [])
    assert all(n.writer_family is None for n in untouched)


def test_load_writers_refuses_tbd(tmp_path: Path):
    p = tmp_path / "w.yaml"
    p.write_text(yaml.safe_dump({"families": {"A": {"backend": "fake", "model": "TBD"}}}))
    try:
        load_writers(p)
    except RuntimeError as exc:
        assert "TBD" in str(exc)
    else:
        raise AssertionError("TBD model id must be refused")
    p.write_text(yaml.safe_dump({"families": {"A": {"backend": "fake", "model": "haiku"}}}))
    ws = load_writers(p)
    assert ws[0].family == "A" and ws[0].backend.name == "fake"


class LeakThenCleanBackend(FakeBackend):
    """Leak judge says LEAK on the first call per note, CLEAN afterwards; counts note writes."""

    def __init__(self) -> None:
        self.judge_calls = 0
        self.note_calls = 0

    def complete(self, prompt: str, *, model: str) -> Completion:
        if "LEAK|CLEAN" in prompt:
            self.judge_calls += 1
            verdict = "LEAK" if self.judge_calls % 2 == 1 else "CLEAN"
            text = json.dumps({"verdict": verdict, "evidence": "stub"})
            return Completion(
                text=text, model_id=f"fake-{model}", input_tokens=1, output_tokens=1, cost_usd=0.0
            )
        if "Write one working note" in prompt:
            self.note_calls += 1
        return super().complete(prompt, model=model)


def test_judge_leak_parses_verdicts():
    be = LeakThenCleanBackend()
    gold = {"gold_connection": "g", "gold_implication": "i"}
    first = judge_leak(be, "haiku", "{{note_text}} {{gold_connection}} LEAK|CLEAN", "note", gold)
    second = judge_leak(be, "haiku", "{{note_text}} LEAK|CLEAN", "note", gold)
    assert first["verdict"] == "LEAK" and second["verdict"] == "CLEAN"


def test_build_corpus_oblique_regenerates_on_leak_and_records_families(tmp_path: Path):
    be = LeakThenCleanBackend()
    spec = _spec(True)
    manifest = build_corpus(spec, be, tmp_path, writers=None)
    docs = {d["id"]: d for d in manifest["docs"]}
    assert manifest["leak_judge"]["enabled"] and manifest["max_tries"] == 5
    assert manifest["version"] == tmp_path.name
    # every bridge note was judged; the first verdict per note was LEAK so each took 2 tries
    for nid in ("br01-a", "br01-b", "br02-a", "br02-b"):
        assert docs[nid]["leak_judge"]["final"] == "CLEAN"
        assert docs[nid]["leak_judge"]["verdicts"][0] == "LEAK"
        assert docs[nid]["tries"] == 2
    assert "leak_judge" not in docs["dc01-a"] and docs["fl01"]["writer_family"] is None
    assert manifest["prompt_sha256"]["leak_judge"]
    assert manifest["leak_judge"]["failures"] == []


def test_build_corpus_v01_behaviour_unchanged(tmp_path: Path):
    manifest = build_corpus(_spec(False), FakeBackend(), tmp_path)
    assert manifest["leak_judge"]["enabled"] is False and manifest["max_tries"] == 3
    assert all("leak_judge" not in d for d in manifest["docs"])
    assert "leak_judge" not in manifest["prompt_sha256"]


def test_build_corpus_two_writer_families(tmp_path: Path):
    from daydreamd.synth.generate import Writer

    writers = [Writer("A", FakeBackend(), "haiku"), Writer("B", FakeBackend(), "other")]
    manifest = build_corpus(_spec(True), FakeBackend(), tmp_path, writers=writers)
    docs = {d["id"]: d for d in manifest["docs"]}
    assert (
        docs["br01-a"]["writer_family"] == "A" and docs["br01-a"]["writer_model_id"] == "fake-haiku"
    )
    assert (
        docs["br02-a"]["writer_family"] == "B" and docs["br02-a"]["writer_model_id"] == "fake-other"
    )
    assert manifest["writers"] == {
        "A": {"backend": "fake", "model": "haiku"},
        "B": {"backend": "fake", "model": "other"},
    }


def _corpus_with_families(root: Path) -> Path:
    """Tiny built corpus: 4 bridges (2 per family), 2 decoys, 4 fillers over 2 domains."""
    from daydreamd.core.io import sha256_text

    notes = root / "notes"
    notes.mkdir(parents=True)
    docs, gold = [], {}
    doms = {"a": "x", "b": "y"}
    for k, b in enumerate(("br01", "br02", "br03", "br04"), start=1):
        for side in ("a", "b"):
            nid = f"{b}-{side}"
            text = f"---\nname: {nid}\n---\n# {nid}\n\n" + " ".join(
                f"fact {nid} {i} about work" for i in range(40)
            )
            (notes / f"{nid}.md").write_text(text)
            docs.append(
                {
                    "id": nid,
                    "domain": doms[side],
                    "kind": "bridge",
                    "bridge_id": b,
                    "decoy_id": None,
                    "sha256": sha256_text(text),
                    "words": 40,
                    "tries": 1,
                    "leaks_final": [],
                    "writer_family": "A" if k % 2 else "B",
                }
            )
        gold[b] = {
            "note_a": f"{b}-a",
            "note_b": f"{b}-b",
            "domain_a": "x",
            "domain_b": "y",
            "hidden_mechanism": "m",
            "gold_connection": "gold " + b,
            "gold_implication": "imp " + b,
        }
    for d in ("dc01", "dc02"):
        for side in ("a", "b"):
            nid = f"{d}-{side}"
            text = f"---\nname: {nid}\n---\n# {nid}\n\n" + " ".join(
                f"decoy {nid} {i}" for i in range(40)
            )
            (notes / f"{nid}.md").write_text(text)
            docs.append(
                {
                    "id": nid,
                    "domain": doms[side],
                    "kind": "decoy",
                    "bridge_id": None,
                    "decoy_id": d,
                    "sha256": sha256_text(text),
                    "words": 40,
                    "tries": 1,
                    "leaks_final": [],
                    "writer_family": "A",
                }
            )
    for k in range(1, 5):
        nid = f"fl{k:02d}"
        text = f"---\nname: {nid}\n---\n# {nid}\n\n" + " ".join(
            f"filler {nid} {i} note" for i in range(40)
        )
        (notes / f"{nid}.md").write_text(text)
        docs.append(
            {
                "id": nid,
                "domain": "x" if k % 2 else "y",
                "kind": "filler",
                "bridge_id": None,
                "decoy_id": None,
                "sha256": sha256_text(text),
                "words": 40,
                "tries": 1,
                "leaks_final": [],
                "writer_family": "A" if k % 2 else "B",
            }
        )
    write_json(
        root / "manifest.json",
        {
            "n_bridges": 4,
            "n_decoys": 2,
            "leakage_failures": [],
            "writer_model_ids": ["fake-haiku", "fake-other"],
            "writers": {
                "A": {"backend": "fake", "model": "haiku"},
                "B": {"backend": "fake", "model": "other"},
            },
            "leak_judge": {"enabled": True, "model_ids": ["fake-haiku"], "failures": []},
            "corpus_sha256": "x",
            "docs": docs,
            "n_notes": len(docs),
        },
    )
    write_json(root / "gold.json", gold)
    write_json(root / "domains.json", {d["id"]: d["domain"] for d in docs})
    return root


def test_run_all_v02_multi_critic_and_decision(tmp_path: Path):
    corpus = _corpus_with_families(tmp_path / "corpus")
    cfg = {
        "prereg": "v0.2",
        "corpus": {"kind": "synth", "path": str(corpus)},
        "visibility": "public",
        "slug": "v02",
        "seed": 3,
        "backend": "fake",
        "models": {
            "cards": "haiku",
            "generator": "sonnet",
            "critic": ["haiku", "sonnet"],
            "match": "haiku",
        },
        "concurrency": 2,
        "arms": {
            "S0": {"random_pairs": 3},
            "S1": {},
            "B1": {"n": 8},
            "B7": {"n": 8, "band": "Q1"},
            "B4": {"notes": "bridge"},
        },
        "blind": {"enabled": False},
        "stats": {"n_perm": 200},
    }
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg))
    run = pipeline.run_all(pipeline.load_config(cfg_path), run_root=tmp_path / "runs")
    meta = run.read_meta()
    # both critics ran; the primary mirrors critic.jsonl and is recorded under models.critic
    assert (run.path / "critic_haiku.jsonl").read_bytes() == (
        run.path / "critic.jsonl"
    ).read_bytes()
    assert (run.path / "critic_sonnet.jsonl").exists()
    assert meta["models"]["critic_haiku"]["model_id"] == "fake-haiku"
    assert meta["models"]["critic_sonnet"]["model_id"] == "fake-sonnet"
    assert meta["models"]["critic"]["model_id"] == "fake-haiku"
    assert meta["stages"]["critic"]["critics"] == ["haiku", "sonnet"]
    # writer family flowed from the manifest into units and generations
    units = [json.loads(line) for line in (run.path / "units.jsonl").open()]
    s0 = [u for u in units if u["arm"] == "S0" and (u.get("label") or "").startswith("planted:")]
    assert {u["writer_family"] for u in s0} == {"A", "B"}
    assert sum(1 for u in units if u["arm"] == "S1") == 8
    assert sum(1 for u in units if u["arm"] == "B7") == 8
    # tables and decision
    tables = run.path / "tables"
    assert (tables / "T8.md").exists() and (tables / "T7.md").exists()
    t8 = (tables / "T8.md").read_text()
    assert "haiku" in t8 and "sonnet" in t8
    decision = (tables / "DECISION.md").read_text()
    for key in ("v0.2", "H1", "H2a", "H2b", "H3", "H4", "H5", "Decision:"):
        assert key in decision
    assert "signal requires H1 and H4" in decision
    t2 = (tables / "T2.md").read_text()
    assert "B7" in t2 and "B1" in t2


def test_v01_decision_rule_unchanged_without_prereg_key(tmp_path: Path):
    corpus = _corpus_with_families(tmp_path / "corpus")
    cfg = {
        "corpus": {"kind": "synth", "path": str(corpus)},
        "visibility": "public",
        "slug": "v01rule",
        "seed": 3,
        "backend": "fake",
        "models": {"cards": "haiku", "generator": "sonnet", "critic": "haiku", "match": "haiku"},
        "concurrency": 2,
        "arms": {"S0": {"random_pairs": 2}, "B1": {"n": 4}, "B4": {"notes": "bridge"}},
        "blind": {"enabled": False},
        "stats": {"n_perm": 100},
    }
    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.safe_dump(cfg))
    run = pipeline.run_all(pipeline.load_config(cfg_path), run_root=tmp_path / "runs")
    decision = (run.path / "tables" / "DECISION.md").read_text()
    assert "signal requires H1 and H2 both passing" in decision
    assert (run.path / "critic_haiku.jsonl").exists() and (run.path / "critic.jsonl").exists()
    assert run.read_meta()["models"]["critic"]["model_id"] == "fake-haiku"


def test_note_acceptable_reasons():
    from daydreamd.synth.generate import note_acceptable

    golds = ["gold connection sentence one two three four five six"]
    long_text = " ".join(f"fact {i} noted" for i in range(60))
    assert note_acceptable(long_text, golds, 150, False, None) == (True, "ok")
    assert (
        note_acceptable(
            long_text + " gold connection sentence one two three", golds, 150, False, None
        )[1]
        == "leak"
    )
    assert note_acceptable(long_text + " a—b", golds, 150, False, None)[1] == "em_dash"
    assert note_acceptable("too short", golds, 150, False, None)[1] == "short"
    assert note_acceptable(long_text, golds, 150, True, None) == (False, "needs_judge")
    assert note_acceptable(long_text, golds, 150, True, "LEAK") == (False, "not_clean")
    assert note_acceptable(long_text, golds, 150, True, "CLEAN") == (True, "ok")


class CountingFake(FakeBackend):
    def __init__(self) -> None:
        self.calls = 0

    def complete(self, prompt: str, *, model: str) -> Completion:
        self.calls += 1
        return super().complete(prompt, model=model)


def test_build_corpus_resume_reuses_acceptable_notes(tmp_path: Path):
    from daydreamd.core.io import sha256_text

    spec = _spec(True)
    golds = ["gold connection sentence one two three four five six"]
    plan = spec.note_plan()
    notes_dir = tmp_path / "notes"
    notes_dir.mkdir()

    def words(n: int) -> str:
        return " ".join(f"fact {i} noted" for i in range(n))

    texts = {n.note_id: "---\nname: x\n---\n" + words(60) + "\n" for n in plan}  # 180 words
    texts["br01-b"] = "---\nname: x\n---\n" + words(40) + "\n"  # 120 words: short under 150
    texts["br01-a"] = texts["br01-a"] + golds[0] + "\n"  # a 6-gram leak
    docs = []
    for n in plan:
        notes_dir.joinpath(f"{n.note_id}.md").write_text(texts[n.note_id], encoding="utf-8")
        doc = {
            "id": n.note_id,
            "domain": n.domain,
            "kind": n.kind,
            "bridge_id": n.bridge_id,
            "decoy_id": n.decoy_id,
            "sha256": sha256_text(texts[n.note_id]),
            "words": len(texts[n.note_id].split()),
            "tries": 2,
            "leaks_final": [],
            "writer_family": None,
            "writer_model_id": "fake-prior",
        }
        if n.kind == "bridge":
            final = None if n.note_id in ("br01-b", "br02-a") else "CLEAN"
            doc["leak_judge"] = {"final": final, "evidence": "", "verdicts": [final]}
        docs.append(doc)
    write_json(
        tmp_path / "manifest.json",
        {
            "generated_at": "2026-09-13T00:00:00+00:00",
            "corpus_sha256": "prior-sha",
            "cost_usd": 1.23,
            "writer_model_ids": ["fake-prior"],
            "leak_judge": {"enabled": True, "model_ids": ["fake-prior"], "failures": []},
            "docs": docs,
        },
    )
    be = CountingFake()
    manifest = build_corpus(spec, be, tmp_path, resume=True, min_words=100)
    got = {d["id"]: d for d in manifest["docs"]}
    # short-under-150 bridge note is fine under 100: judged once now, then reused
    assert got["br01-b"]["reused"] is True and got["br01-b"]["tries"] == 3
    assert got["br01-b"]["leak_judge"]["final"] == "CLEAN"
    assert got["br01-b"]["writer_model_id"] == "fake-prior"
    # unjudged bridge note: judged once, reused
    assert got["br02-a"]["reused"] is True and got["br02-a"]["tries"] == 3
    assert got["br02-a"]["leak_judge"]["verdicts"] == [None, "CLEAN"]
    # leaky note is regenerated
    assert not got["br01-a"].get("reused") and got["br01-a"]["writer_model_id"] == "fake-haiku"
    assert not leaked_ngrams_in(notes_dir / "br01-a.md", golds)
    # everything else reused untouched
    assert got["fl01"]["reused"] is True and got["fl01"]["tries"] == 2
    assert manifest["reused_notes"] == len(plan) - 1
    # only new calls counted: 2 judge calls + 1 write + 1 judge for the rewrite
    assert be.calls == 4
    assert manifest["cost_usd_prior"] == 1.23 and manifest["cost_usd"] == 0.0
    assert manifest["resumed_from"]["corpus_sha256"] == "prior-sha"
    assert manifest["min_words"] == 100
    assert "fake-prior" in manifest["writer_model_ids"]


def leaked_ngrams_in(path: Path, golds: list[str]) -> list[str]:
    from daydreamd.synth.leakage import leaked_ngrams

    return leaked_ngrams(path.read_text(encoding="utf-8"), golds)
