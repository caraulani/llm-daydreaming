"""`daydreamd skill`: endorsed dreams become a SKILL.md an agent loads; rejections become the
learnings block the critic reads on later runs. Knowledge at the prompt layer, no weights."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..core.run import today
from . import paths
from .review import latest_verdicts


@dataclass
class SkillResult:
    skill: Path
    learnings: Path
    endorsed: int
    known: int
    rejected: int


def _slug_from(verdicts: dict[str, dict]) -> str:
    corpora = {v.get("corpus", "") for v in verdicts.values() if v.get("corpus")}
    if len(corpora) == 1:
        return paths.slugify(Path(next(iter(corpora))).name)
    return "notes"


def render_skill(slug: str, endorsed: list[dict], known: list[dict], rejected: list[dict]) -> str:
    lines = [
        "---",
        f"name: daydreamd-{slug}",
        "description: >-",
        f"  Connections the owner of the {slug} notes endorsed after daydreamd runs, and the",
        "  patterns they rejected. Use when working on topics from those notes; cite the",
        "  sources; never re-propose a rejected pattern.",
        "---",
        "",
        f"# daydreamd skill: {slug}",
        "",
        f"Generated {today()} from {len(endorsed) + len(known) + len(rejected)} reviewed dreams: "
        f"{len(endorsed)} endorsed, {len(known)} already known, {len(rejected)} rejected. "
        "Endorsed means the owner said they would act on it or write it down. Nothing here is "
        "verified by anyone but the owner.",
        "",
        "## Connections the owner endorsed",
        "",
    ]
    if not endorsed:
        lines.append("None yet. Tick KEEP on a dream in morning.md and run `daydreamd review`.")
    for v in endorsed:
        src = ", ".join(v.get("sources") or []) or "unknown"
        lines += [
            f"- **{v['connection']}**",
            f"  Mechanism: {v.get('mechanism', '')}",
            f"  Check: {v.get('check', '')}",
            f"  Sources: {src}. Dream `{v['dream_id']}`.",
        ]
    lines += ["", "## Rejected patterns", ""]
    if not known and not rejected:
        lines.append("None yet.")
    for v in known:
        lines.append(f"- Already known to the owner: {v['connection']}")
    for v in rejected:
        lines.append(
            f"- Rejected without action (critic: {v.get('reason', 'ok')}): {v['connection']}"
        )
    lines += [
        "",
        "## How to use these",
        "",
        "- Treat endorsed connections as the owner's working hypotheses, not facts. Cite the",
        "  source notes when you build on one.",
        "- Do not re-propose a rejected pattern or a connection the owner already knew.",
        "- New connections come from `daydreamd dream` and the owner's review, never from",
        "  editing this file by hand.",
        "",
    ]
    return "\n".join(lines)


def render_learnings(known: list[dict], rejected: list[dict]) -> str:
    lines = [f"- Already known to the owner: {v['connection']}" for v in known]
    lines += [f"- Rejected ({v.get('reason', 'ok')}): {v['connection']}" for v in rejected]
    return "\n".join(lines) + ("\n" if lines else "")


def build_skill(out: Path | None = None) -> SkillResult:
    verdicts = latest_verdicts()
    if not verdicts:
        raise RuntimeError("no verdicts yet; run `daydreamd review morning.md` first")
    endorsed = [v for v in verdicts.values() if v.get("keep")]
    known = [v for v in verdicts.values() if v.get("known") and not v.get("keep")]
    rejected = [v for v in verdicts.values() if not v.get("keep") and not v.get("known")]
    slug = _slug_from(verdicts)
    skill_path = out or Path(".claude/skills") / f"daydreamd-{slug}" / "SKILL.md"
    skill_path.parent.mkdir(parents=True, exist_ok=True)
    skill_path.write_text(render_skill(slug, endorsed, known, rejected), encoding="utf-8")
    learnings = paths.learnings_path()
    learnings.write_text(render_learnings(known, rejected), encoding="utf-8")
    return SkillResult(
        skill=skill_path,
        learnings=learnings,
        endorsed=len(endorsed),
        known=len(known),
        rejected=len(rejected),
    )
