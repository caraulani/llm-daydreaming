"""Run directories and metadata.yaml. Every stage records model ids, prompt hashes, seed, cost."""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .io import sha256_text

PROMPTS_DIR = Path(__file__).resolve().parents[3] / "prompts"


def now_iso() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def today() -> str:
    return dt.date.today().isoformat()


def load_prompt(name: str) -> tuple[str, str]:
    """Return (prompt_text, sha256). Prompts are versioned files; the hash lands in metadata."""
    text = (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")
    return text, sha256_text(text)


@dataclass
class RunDir:
    path: Path

    @classmethod
    def create(cls, root: Path, visibility: str, slug: str) -> RunDir:
        path = root / visibility / f"{today()}_{slug}"
        path.mkdir(parents=True, exist_ok=True)
        run = cls(path)
        if not run.meta_path.exists():
            run.write_meta(
                {
                    "run_id": path.name,
                    "visibility": visibility,
                    "created": now_iso(),
                    "stages": {},
                    "models": {},
                    "prompts": {},
                    "cost_usd_total": 0.0,
                }
            )
        return run

    @property
    def meta_path(self) -> Path:
        return self.path / "metadata.yaml"

    def read_meta(self) -> dict[str, Any]:
        return yaml.safe_load(self.meta_path.read_text(encoding="utf-8")) or {}

    def write_meta(self, meta: dict[str, Any]) -> None:
        self.meta_path.write_text(yaml.safe_dump(meta, sort_keys=True), encoding="utf-8")

    def update_meta(self, **fields: Any) -> None:
        meta = self.read_meta()
        meta.update(fields)
        self.write_meta(meta)

    def mark_stage(self, stage: str, **info: Any) -> None:
        meta = self.read_meta()
        meta.setdefault("stages", {})[stage] = {"finished": now_iso(), **info}
        self.write_meta(meta)

    def record_model(self, role: str, alias: str, model_id: str) -> None:
        meta = self.read_meta()
        meta.setdefault("models", {})[role] = {"alias": alias, "model_id": model_id}
        self.write_meta(meta)

    def record_prompt(self, name: str, sha: str) -> None:
        meta = self.read_meta()
        meta.setdefault("prompts", {})[name] = sha
        self.write_meta(meta)

    def add_cost(self, usd: float) -> None:
        meta = self.read_meta()
        meta["cost_usd_total"] = round(float(meta.get("cost_usd_total", 0.0)) + usd, 6)
        self.write_meta(meta)
