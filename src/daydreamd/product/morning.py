"""Render and parse `morning.md`, the file the owner reads and ticks.

Every dream block carries an HTML comment with its id, its critic verdict and reason, so
`daydreamd review` can read the ticked boxes back without any other state. Dreams the critic
killed are kept in a collapsed section: the v0.1 and v0.2 runs showed the critic removes
correct connections (research/06, research/07), so the owner sees them too.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from ..core.blind import KEEP_RE, KNOWN_RE

DREAM_RE = re.compile(
    r"^<!-- dream: (?P<id>[^ |]+) \| critic: (?P<critic>\w+) \| reason: (?P<reason>\w+) -->\s*$"
)
HEADER_RE = re.compile(
    r"^<!-- daydreamd run: (?P<run>[^ |]+) \| corpus: (?P<corpus>.*?) \| corpus_sha: (?P<sha>\w+) -->\s*$"
)
HEADING_RE = re.compile(r"^#{2,3} (?:k?\d+)\. (?P<title>.+?)\s*$")
FIELD_RE = re.compile(r"^\*\*(?P<key>Mechanism|Check this week)\.\*\* (?P<value>.+?)\s*$")
SOURCES_RE = re.compile(r"^Sources: (?P<sources>.+?)(?: · .*)?\s*$")


@dataclass
class Dream:
    dream_id: str  # "<run_id>/<unit_id>"
    connection: str
    mechanism: str
    check: str
    sources: list[str]
    critic: str  # keep | kill | off
    reason: str
    distance: float | None = None
    already_in_corpus: bool = False
    keep: bool = False
    known: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


def _block(n: str, d: Dream, level: str) -> str:
    src = " and ".join(d.sources) if d.sources else "unknown"
    dist = f" · distance {d.distance:.2f}" if d.distance is not None else ""
    verdict = d.critic if d.critic != "kill" else f"kill ({d.reason})"
    dup = " · already close to a note" if d.already_in_corpus else ""
    return (
        f"{level} {n}. {d.connection}\n"
        f"<!-- dream: {d.dream_id} | critic: {d.critic} | reason: {d.reason} -->\n"
        f"**Mechanism.** {d.mechanism}\n"
        f"**Check this week.** {d.check}\n"
        f"Sources: {src}{dist} · critic: {verdict}{dup}\n\n"
        "- [ ] KEEP: I would act on this or write it down\n"
        "- [ ] KNOWN: I already had this thought\n"
    )


def render(
    *,
    run_id: str,
    corpus: str,
    corpus_sha: str,
    date: str,
    survivors: list[Dream],
    killed: list[Dream],
    counts: dict[str, int],
    models: dict[str, str],
    cost_usd: float,
) -> str:
    lines = [
        f"# morning.md, {date}, {len(survivors)} of {counts['asked']} dreams survived",
        f"<!-- daydreamd run: {run_id} | corpus: {corpus} | corpus_sha: {corpus_sha} -->",
        "",
        f"Corpus: `{corpus}` ({counts['notes']} notes, {counts['cards']} cards). "
        f"Pairs asked: {counts['asked']}. NONE: {counts['none']}. "
        f"Killed by the critic: {counts['killed']}. Already close to a note: {counts['dup']}. "
        f"Survivors: {len(survivors)}.",
        "Models: " + ", ".join(f"{k} `{v}`" for k, v in models.items()) + ".",
        f"Measured cost at list price: ${cost_usd:.4f}. Nothing here was written back into your "
        "notes; every dream is unverified until you tick it.",
        "",
    ]
    if not survivors:
        lines += ["No dream survived. An empty morning beats a boring one.", ""]
    for i, d in enumerate(survivors, 1):
        lines.append(_block(str(i), d, "##"))
    if killed:
        lines += [
            "<details>",
            f"<summary>Killed by the critic ({len(killed)}). Kept here because the critic is "
            "known to kill correct connections.</summary>",
            "",
        ]
        for i, d in enumerate(killed, 1):
            lines.append(_block(f"k{i}", d, "###"))
        lines += ["</details>", ""]
    lines += [
        "---",
        "Tick KEEP or KNOWN, then run `daydreamd review morning.md`. "
        "Endorsed dreams become a skill file with `daydreamd skill`.",
        "",
    ]
    return "\n".join(lines)


def parse(text: str) -> tuple[dict[str, str], list[Dream]]:
    """Return (header fields, dreams with their ticked boxes)."""
    header: dict[str, str] = {}
    dreams: list[Dream] = []
    pending_title = ""
    current: Dream | None = None
    for line in text.splitlines():
        if h := HEADER_RE.match(line):
            header = h.groupdict()
            continue
        if t := HEADING_RE.match(line):
            pending_title = t.group("title")
            continue
        if m := DREAM_RE.match(line):
            current = Dream(
                dream_id=m.group("id"),
                connection=pending_title,
                mechanism="",
                check="",
                sources=[],
                critic=m.group("critic"),
                reason=m.group("reason"),
            )
            dreams.append(current)
            continue
        if current is None:
            continue
        if f := FIELD_RE.match(line):
            if f.group("key") == "Mechanism":
                current.mechanism = f.group("value")
            else:
                current.check = f.group("value")
        elif s := SOURCES_RE.match(line):
            current.sources = [x.strip() for x in s.group("sources").split(" and ")]
        elif k := KEEP_RE.match(line):
            current.keep = k.group(1).lower() == "x"
        elif k := KNOWN_RE.match(line):
            current.known = k.group(1).lower() == "x"
    return header, dreams
