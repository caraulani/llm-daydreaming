"""Load the hand-authored specs and expand them into a per-note plan."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULT_SPEC_DIR = Path(__file__).resolve().parents[3] / "data" / "synth" / "v0.1"


@dataclass
class NoteSpec:
    note_id: str
    domain: str
    kind: str  # bridge | decoy | filler
    topic: str
    ingredients: list[str] = field(default_factory=list)
    forbidden: list[str] = field(default_factory=list)
    bridge_id: str | None = None
    decoy_id: str | None = None
    writer_family: str | None = (
        None  # set by assign_writers(); None means the single default writer
    )


def _numeric_suffix(ident: str) -> int:
    digits = "".join(ch for ch in ident if ch.isdigit())
    return int(digits) if digits else 0


def assign_writers(plan: list[NoteSpec], families: list[str]) -> list[NoteSpec]:
    """Assign each note to a writer family by parity.

    Bridge notes follow the parity of the bridge id (odd -> families[0], even -> families[1]),
    decoy notes the parity of the decoy id, fillers alternate by position (fl01 -> families[0]).
    With one family every note gets it. The assignment is deterministic so it can be sealed.
    """
    if not families:
        return plan
    if len(families) == 1:
        for n in plan:
            n.writer_family = families[0]
        return plan
    a, b = families[0], families[1]
    for n in plan:
        if n.kind == "bridge" and n.bridge_id:
            key = _numeric_suffix(n.bridge_id)
        elif n.kind == "decoy" and n.decoy_id:
            key = _numeric_suffix(n.decoy_id)
        else:
            key = _numeric_suffix(n.note_id)
        n.writer_family = a if key % 2 == 1 else b
    return plan


@dataclass
class Spec:
    persona: str
    domains: dict[str, str]
    bridges: list[dict[str, Any]]
    decoys: list[dict[str, Any]]
    fillers: list[dict[str, Any]]

    @property
    def oblique(self) -> bool:
        """True when the spec carries the v0.2 obliqueness fields (per-side forbidden phrases
        or a one-side test), which switches on the paraphrase-leak judge at build time."""
        return any(
            b.get("forbidden_phrases_a") or b.get("forbidden_phrases_b") or b.get("one_side_test")
            for b in self.bridges
        )

    def note_plan(self) -> list[NoteSpec]:
        plan: list[NoteSpec] = []
        for b in self.bridges:
            for side in ("a", "b"):
                other = b["domain_b" if side == "a" else "domain_a"]
                dom = b[f"domain_{side}"]
                forbidden = [self.domains[other], other, b["hidden_mechanism"]]
                forbidden += [str(x) for x in (b.get(f"forbidden_phrases_{side}") or [])]
                plan.append(
                    NoteSpec(
                        note_id=f"{b['id']}-{side}",
                        domain=dom,
                        kind="bridge",
                        topic=f"recent working notes on {self.domains[dom]}",
                        ingredients=list(b[f"ingredients_{side}"]),
                        forbidden=forbidden,
                        bridge_id=b["id"],
                    )
                )
        for d in self.decoys:
            for side in ("a", "b"):
                n = d[f"note_{side}"]
                plan.append(
                    NoteSpec(
                        note_id=f"{d['id']}-{side}",
                        domain=n["domain"],
                        kind="decoy",
                        topic=n["topic"],
                        forbidden=[],
                        decoy_id=d["id"],
                    )
                )
        for k, f in enumerate(self.fillers, start=1):
            plan.append(
                NoteSpec(note_id=f"fl{k:02d}", domain=f["domain"], kind="filler", topic=f["topic"])
            )
        return plan

    def planted_pairs(self) -> dict[tuple[str, str], str]:
        return {(f"{b['id']}-a", f"{b['id']}-b"): b["id"] for b in self.bridges}

    def decoy_pairs(self) -> dict[tuple[str, str], str]:
        return {(f"{d['id']}-a", f"{d['id']}-b"): d["id"] for d in self.decoys}

    def gold(self) -> dict[str, dict[str, Any]]:
        return {
            b["id"]: {
                "note_a": f"{b['id']}-a",
                "note_b": f"{b['id']}-b",
                "domain_a": b["domain_a"],
                "domain_b": b["domain_b"],
                "hidden_mechanism": b["hidden_mechanism"],
                "gold_connection": " ".join(str(b["gold_connection"]).split()),
                "gold_implication": " ".join(str(b["gold_implication"]).split()),
            }
            for b in self.bridges
        }


def load_spec(spec_dir: Path = DEFAULT_SPEC_DIR) -> Spec:
    bridges = yaml.safe_load((spec_dir / "bridges.yaml").read_text(encoding="utf-8"))
    decoys = yaml.safe_load((spec_dir / "decoys.yaml").read_text(encoding="utf-8"))
    fillers = yaml.safe_load((spec_dir / "fillers.yaml").read_text(encoding="utf-8"))
    return Spec(
        persona=" ".join(str(bridges["persona"]).split()),
        domains=dict(bridges["domains"]),
        bridges=list(bridges["bridges"]),
        decoys=list(decoys["decoys"]),
        fillers=list(fillers["fillers"]),
    )
