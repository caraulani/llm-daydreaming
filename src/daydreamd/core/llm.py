"""Bounded-concurrency model calls with per-call usage records."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from ..backends import Backend, Completion


def usage_record(c: Completion) -> dict[str, Any]:
    return {
        "model_id": c.model_id,
        "input_tokens": c.input_tokens,
        "output_tokens": c.output_tokens,
        "cost_usd": c.cost_usd,
    }


def pmap[T](
    fn: Callable[[T], dict[str, Any]], items: Iterable[T], concurrency: int = 4
) -> list[dict[str, Any]]:
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        return list(pool.map(fn, items))


def complete_json(backend: Backend, prompt: str, model: str) -> tuple[Any, Completion]:
    from .io import extract_json

    comp = backend.complete(prompt, model=model)
    text = comp.text.strip()
    if text.upper().startswith("NONE") and len(text) < 12:
        return None, comp
    return extract_json(text), comp


def guard_error_rate(rows: list[dict[str, Any]], stage: str, max_frac: float = 0.2) -> None:
    """Abort a stage whose outputs are mostly errors (a spent usage window, a dead backend).

    A run that continues past this point produces tables from garbage. Raise instead, so the
    failure is visible and the run directory can be discarded or resumed.
    """
    n = len(rows)
    if n == 0:
        return
    errors = sum(
        1
        for r in rows
        if r.get("status") == "error" or str(r.get("reason", "")).startswith("error")
    )
    if errors / n > max_frac:
        raise RuntimeError(
            f"stage {stage} aborted: {errors}/{n} calls failed ({errors / n:.0%} > {max_frac:.0%})"
        )
