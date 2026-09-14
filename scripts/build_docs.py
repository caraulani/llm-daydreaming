"""Stage repository documents into docs/ for the mkdocs site.

Copies, at build time, the files that live outside docs/ but belong on the site: the paper,
both preregistrations, the research notes, and every public run's summary, decision and tables.
The copies are generated (gitignored); the sources of truth stay where they are.

Usage: `python scripts/build_docs.py` (run before `mkdocs build`).
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

GENERATED = ["paper.md", "preregistration", "research", "results"]


def _clean() -> None:
    for name in GENERATED:
        target = DOCS / name
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()


def _rewrite_links(text: str, depth: int) -> str:
    """Point repo-relative links at their copies on the site.

    ``research/06-x.md`` becomes ``research/06-x.md`` relative to docs root; ``PREREGISTRATION.md``
    and ``PREREGISTRATION-v0.2.md`` map to the preregistration pages; ``results/public/<run>/``
    maps to the results page for that run. Anything else that points into the repository is
    turned into an absolute GitHub URL so the link still works.
    """
    up = "../" * depth
    text = re.sub(r"\]\(PREREGISTRATION\.md\)", f"]({up}preregistration/v0.1.md)", text)
    text = re.sub(r"\]\(PREREGISTRATION-v0\.2\.md\)", f"]({up}preregistration/v0.2.md)", text)
    text = re.sub(r"\]\(`?research/([^)`]+\.md)`?\)", rf"]({up}research/\1)", text)
    text = re.sub(r"\]\(results/public/([^)/]+)/?\)", rf"]({up}results/\1/index.md)", text)
    gh = "https://github.com/caraulani/llm-daydreaming/blob/main/"
    text = re.sub(
        r"\]\(((?:design|experiments|data|prompts|src|docs|registry|paper|tests)/[^)]+)\)",
        rf"]({gh}\1)",
        text,
    )
    text = re.sub(
        r"\]\((LICENSE[^)]*|CITATION\.cff|CHANGELOG\.md|CONTRIBUTING\.md|ROADMAP\.md|SECURITY\.md|AGENTS\.md)\)",
        rf"]({gh}\1)",
        text,
    )
    return text


def _copy_md(src: Path, dst: Path, title: str | None = None, depth: int = 0) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    text = _rewrite_links(text, depth)
    if title and not text.lstrip().startswith("---"):
        text = f"---\ntitle: {title}\n---\n\n" + text
    dst.write_text(text, encoding="utf-8")


def main() -> None:
    _clean()
    _copy_md(ROOT / "paper" / "paper.md", DOCS / "paper.md", title="Paper", depth=0)
    _copy_md(
        ROOT / "PREREGISTRATION.md",
        DOCS / "preregistration" / "v0.1.md",
        title="Preregistration v0.1 (sealed 2026-09-13)",
        depth=1,
    )
    _copy_md(
        ROOT / "PREREGISTRATION-v0.2.md",
        DOCS / "preregistration" / "v0.2.md",
        title="Preregistration v0.2 (sealed 2026-09-13)",
        depth=1,
    )
    (DOCS / "preregistration" / "index.md").write_text(
        "---\ntitle: Preregistrations\n---\n\n# Preregistrations\n\n"
        "Both protocols were sealed (signed commit, tag, OpenTimestamps proof anchored in Bitcoin) "
        "before any model call for the experiment. Deviations are logged at the bottom of each.\n\n"
        "- [v0.1, sealed 2026-09-13, block 966837](v0.1.md)\n"
        "- [v0.2, sealed 2026-09-13, block 966878](v0.2.md)\n",
        encoding="utf-8",
    )
    research = sorted((ROOT / "research").glob("*.md"))
    for f in research:
        name = "index.md" if f.name == "README.md" else f.name
        _copy_md(f, DOCS / "research" / name, depth=1)
    runs = sorted(p for p in (ROOT / "results" / "public").iterdir() if p.is_dir())
    index = [
        "---",
        "title: Results",
        "---",
        "",
        "# Results",
        "",
        "Every table below is regenerated from the committed raw outputs by `make reproduce` "
        "with no model call. Runs marked exploratory are not preregistered.",
        "",
    ]
    for run in runs:
        out = DOCS / "results" / run.name
        out.mkdir(parents=True, exist_ok=True)
        parts = ["---", f"title: {run.name}", "---", "", f"# Run `{run.name}`", ""]
        for fname in ["DECISION.md", "summary.md"] + sorted(p.name for p in run.glob("T*.md")):
            src = run / fname
            if src.exists():
                parts += [src.read_text(encoding="utf-8").rstrip(), ""]
        (out / "index.md").write_text("\n".join(parts), encoding="utf-8")
        kind = "preregistered" if "micro" in run.name else "exploratory"
        index.append(f"- [{run.name}]({run.name}/index.md) ({kind})")
    (DOCS / "results" / "index.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"staged paper, 2 preregistrations, {len(research)} research notes, {len(runs)} runs")


if __name__ == "__main__":
    main()
