"""Product front door, offline: dream -> review -> skill -> dream again with learnings."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from daydreamd.core.io import read_jsonl
from daydreamd.product import paths
from daydreamd.product.dream import DreamConfig, dream
from daydreamd.product.morning import parse
from daydreamd.product.review import review
from daydreamd.product.skill import build_skill

WORDS = " ".join(f"word{i}" for i in range(40))


@pytest.fixture
def vault(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("DAYDREAMD_HOME", str(tmp_path / "home"))
    monkeypatch.chdir(tmp_path)
    root = tmp_path / "vault"
    for folder in ("alpha", "beta", "gamma"):
        (root / folder).mkdir(parents=True)
        for k in range(3):
            (root / folder / f"{folder}-{k}.md").write_text(
                f"---\ntitle: {folder} {k}\n---\n# {folder} note {k}\n\nThe {folder} team saw "
                f"pattern {k} in week {k + 1}. {WORDS}\n"
            )
    (root / ".obsidian").mkdir()
    (root / ".obsidian" / "hidden.md").write_text("# hidden\n" + WORDS)
    return root


def _cfg(vault: Path, **kw: object) -> DreamConfig:
    base = dict(path=vault, kind="obsidian", n=8, backend="fake", embedder="fake", seed=7)
    base.update(kw)
    return DreamConfig(**base)  # type: ignore[arg-type]


def test_dream_writes_morning_and_run(vault: Path) -> None:
    r = dream(_cfg(vault, out=vault.parent / "morning.md"))
    text = r.morning.read_text()
    assert text.startswith("# morning.md, ")
    assert "<!-- daydreamd run: " in text
    assert r.counts["notes"] == 9  # the .obsidian note is skipped
    assert (r.run / "generations.jsonl").exists() and (r.run / "units.jsonl").exists()
    assert (r.run / "morning.md").exists()
    header, dreams = parse(text)
    assert header["run"] == r.run.name
    assert len(dreams) == r.counts["survivors"] + r.counts["killed"]
    assert all(d.sources and d.sources[0].startswith("[[") for d in dreams)  # obsidian wikilinks
    rows = list(read_jsonl(paths.cards_cache()))
    assert len(rows) == 9  # one cache row per note


def test_second_run_reuses_the_card_cache(vault: Path) -> None:
    r1 = dream(_cfg(vault, out=vault.parent / "m1.md"))
    assert r1.counts["cached_cards"] == 0
    r2 = dream(_cfg(vault, out=vault.parent / "m2.md"))
    assert r2.counts["cached_cards"] == 9
    assert len(list(read_jsonl(paths.cards_cache()))) == 9


def test_review_then_skill_then_learnings_reach_the_critic(vault: Path) -> None:
    r = dream(_cfg(vault, out=vault.parent / "morning.md"))
    text = r.morning.read_text()
    # tick KEEP on the first dream and KNOWN on the second
    text = text.replace("- [ ] KEEP", "- [x] KEEP", 1)
    second_block = text.index("<!-- dream:", text.index("<!-- dream:") + 1)
    second = text.index("- [ ] KNOWN", second_block)
    text = text[:second] + "- [x] KNOWN" + text[second + len("- [ ] KNOWN") :]
    r.morning.write_text(text)
    s = review(r.morning)
    assert s.kept == 1 and s.known == 1
    verdicts = [json.loads(line) for line in paths.verdicts_path().read_text().splitlines()]
    assert len(verdicts) == s.reviewed
    assert verdicts[0]["keep"] is True and verdicts[0]["run_id"] == r.run.name
    out = vault.parent / "SKILL.md"
    sk = build_skill(out)
    skill = out.read_text()
    assert (
        skill.startswith("---\nname: daydreamd-vault")
        and "## Connections the owner endorsed" in skill
    )
    assert verdicts[0]["connection"] in skill and sk.endorsed == 1 and sk.known == 1
    assert paths.learnings_path().exists() and "Already known" in paths.learnings_path().read_text()
    r2 = dream(_cfg(vault, out=vault.parent / "m2.md"))
    meta = (r2.run / "metadata.yaml").read_text()
    assert "critic_with_learnings" in meta


def test_no_critic_keeps_everything_non_none(vault: Path) -> None:
    r = dream(_cfg(vault, out=vault.parent / "morning.md", critic=False))
    assert r.counts["killed"] == 0
    assert r.counts["survivors"] == r.counts["asked"] - r.counts["none"] - r.counts["error"]


def test_schedule_install_writes_plist_without_loading(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import platform

    from daydreamd.product.schedule import install, remove

    if platform.system() != "Darwin":
        pytest.skip("launchd path is macOS only")
    monkeypatch.setenv("DAYDREAMD_LAUNCH_AGENTS", str(tmp_path / "agents"))
    target, text = install(
        tmp_path, "markdown", tmp_path / "m.md", 12, "03:30", load=False, home=tmp_path
    )
    assert target is not None and target.exists()
    assert "<integer>3</integer>" in text and "<integer>30</integer>" in text and "dream" in text
    assert remove(load=False).startswith("removed")


def test_mcp_server_builds() -> None:
    pytest.importorskip("mcp")
    from daydreamd.product.mcp_server import build_server

    server = build_server()
    assert server.name == "daydreamd"
