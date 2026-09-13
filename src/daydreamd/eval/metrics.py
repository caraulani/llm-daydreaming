"""Statistics used by every table. Small, dependency-light, unit-tested."""

from __future__ import annotations

import math

import numpy as np
from scipy import stats as sps


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """Return (rate, lo, hi). Rate is 0 with a [0, 0] interval when n == 0."""
    if n == 0:
        return 0.0, 0.0, 0.0
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return p, max(0.0, centre - half), min(1.0, centre + half)


def fisher_one_sided(k1: int, n1: int, k2: int, n2: int) -> float:
    """P(rate1 > rate2) one-sided Fisher exact on a 2x2 table."""
    table = [[k1, n1 - k1], [k2, n2 - k2]]
    return float(sps.fisher_exact(table, alternative="greater")[1])


def hypergeom_sf(observed: int, population: int, successes: int, draws: int) -> float:
    """P(X >= observed) for X ~ Hypergeometric(population, successes, draws)."""
    if draws == 0 or successes == 0:
        return 1.0
    return float(sps.hypergeom.sf(observed - 1, population, successes, draws))


def cochran_armitage(counts: list[tuple[int, int]]) -> tuple[float, float]:
    """Trend test over ordered groups of (successes, n). Returns (z, two-sided p)."""
    scores = np.arange(len(counts), dtype=float)
    k = np.array([c[0] for c in counts], dtype=float)
    n = np.array([c[1] for c in counts], dtype=float)
    total = n.sum()
    if total == 0 or k.sum() == 0 or k.sum() == total:
        return 0.0, 1.0
    p = k.sum() / total
    t = (scores * (k - n * p)).sum()
    s_bar = (scores * n).sum() / total
    var = p * (1 - p) * (n * (scores - s_bar) ** 2).sum()
    if var <= 0:
        return 0.0, 1.0
    z = t / math.sqrt(var)
    return float(z), float(2 * sps.norm.sf(abs(z)))


def cohen_kappa(a: list[bool], b: list[bool]) -> float:
    if not a:
        return float("nan")
    n = len(a)
    agree = sum(x == y for x, y in zip(a, b, strict=True)) / n
    pa, pb = sum(a) / n, sum(b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    if expected == 1.0:
        return 1.0
    return (agree - expected) / (1 - expected)
