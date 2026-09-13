"""Label-permutation nulls. The statistic is recomputed on shuffled labels; p is the share of
shuffles at least as extreme as the observed value (with the +1 correction)."""

from __future__ import annotations

import numpy as np


def permutation_p_gap(
    labels: np.ndarray,
    outcomes: np.ndarray,
    group_a: str,
    group_b: str,
    n_perm: int = 10_000,
    seed: int = 0,
) -> tuple[float, float]:
    """One-sided p for rate(group_a) - rate(group_b) > observed under label shuffling."""
    rng = np.random.default_rng(seed)
    mask = np.isin(labels, [group_a, group_b])
    lab, out = labels[mask], outcomes[mask].astype(float)
    if lab.size == 0 or (lab == group_a).sum() == 0 or (lab == group_b).sum() == 0:
        return 0.0, 1.0

    def gap(lab_: np.ndarray) -> float:
        return out[lab_ == group_a].mean() - out[lab_ == group_b].mean()

    observed = gap(lab)
    count = 0
    for _ in range(n_perm):
        count += gap(rng.permutation(lab)) >= observed
    return float(observed), float((count + 1) / (n_perm + 1))


def permutation_p_concentration(
    is_planted: np.ndarray, hit: np.ndarray, n_perm: int = 10_000, seed: int = 0
) -> tuple[int, float, float]:
    """Observed hits among planted units vs the null of shuffling the planted flags."""
    rng = np.random.default_rng(seed)
    planted = is_planted.astype(bool)
    hit = hit.astype(bool)
    observed = int((planted & hit).sum())
    if planted.sum() == 0 or hit.sum() == 0:
        return observed, float(observed), 1.0
    count = 0
    total = 0.0
    for _ in range(n_perm):
        sh = rng.permutation(planted)
        v = int((sh & hit).sum())
        total += v
        count += v >= observed
    return observed, total / n_perm, float((count + 1) / (n_perm + 1))
