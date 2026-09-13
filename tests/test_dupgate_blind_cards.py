from __future__ import annotations

from pathlib import Path

from daydreamd.backends.fake import FakeBackend
from daydreamd.core import blind
from daydreamd.core.cards import validate_card
from daydreamd.core.dupgate import dupgate
from daydreamd.core.embed import FakeEmbedder
from daydreamd.core.run import RunDir


def _run(tmp_path: Path) -> RunDir:
    return RunDir.create(tmp_path, "public", "t")


def _gen(uid: str, arm: str, conn: str) -> dict:
    return {
        "unit_id": uid,
        "arm": arm,
        "band": None,
        "kind": "pair",
        "note_a": "n1",
        "note_b": "n2",
        "claims_a": ["a"],
        "claims_b": ["b"],
        "status": "ok",
        "output": {"connection": conn, "mechanism": "m", "testable_implication": "t", "needs": "n"},
        "usage": {"model_id": "fake", "input_tokens": 1, "output_tokens": 1, "cost_usd": 0.0},
        "label": None,
    }


def test_dupgate_flags_identical_text(tmp_path, cards):
    run = _run(tmp_path)
    gens = [
        _gen("u1", "B1", cards[0]["claim"]),
        _gen("u2", "B1", "something entirely different and new"),
    ]
    critic = [{"unit_id": "u1", "verdict": "keep"}, {"unit_id": "u2", "verdict": "keep"}]
    rows = dupgate(run, FakeEmbedder(), gens, critic, cards, {}, threshold=0.85)
    by = {r["unit_id"]: r for r in rows}
    assert by["u1"]["already_in_corpus"] is True
    assert by["u2"]["already_in_corpus"] is False


def test_blind_pack_round_trip(tmp_path):
    run = _run(tmp_path)
    gens = [_gen(f"u{i}", "B3" if i % 2 else "B1", f"conn {i}") for i in range(12)]
    items = blind.build_pack(run, gens, seed=1, repeats=3)
    text = items.read_text()
    assert "B3" not in text and "B1" not in text
    text = text.replace("- [ ] KEEP", "- [x] KEEP", 5)
    items.write_text(text)
    verdicts = blind.unseal(run)
    assert sum(v["keep"] for v in verdicts) == 5
    assert sum(1 for v in verdicts if v["repeat_of"]) == 3
    (run.path / "blind" / "key.json").write_text("{}")
    try:
        blind.unseal(run)
    except RuntimeError as exc:
        assert "seal" in str(exc)
    else:
        raise AssertionError("broken seal not detected")


def test_card_schema():
    assert validate_card({"claim": "", "entities": []}) is None
    c = validate_card(
        {
            "claim": "short claim",
            "entities": "x",
            "why_it_matters": " ".join(["w"] * 40),
            "confidence": "weird",
        }
    )
    assert (
        c
        and c["confidence"] == "med"
        and c["entities"] == ["x"]
        and len(c["why_it_matters"].split()) == 24
    )


def test_fake_backend_is_deterministic():
    b = FakeBackend()
    assert b.complete("hello", model="haiku").text == b.complete("hello", model="haiku").text


def test_clean_note_strips_trailers():
    from daydreamd.synth.generate import clean_note

    raw = "---\nname: x\n---\n# T\n\n- fact\n\n---\n\nCo-Authored-By: Claude <x>\n"
    assert clean_note(raw) == "---\nname: x\n---\n# T\n\n- fact\n"
