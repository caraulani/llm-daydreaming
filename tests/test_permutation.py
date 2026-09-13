from __future__ import annotations

import numpy as np

from daydreamd.eval.metrics import (
    cochran_armitage,
    cohen_kappa,
    fisher_one_sided,
    hypergeom_sf,
    wilson,
)
from daydreamd.eval.permutation_null import permutation_p_concentration, permutation_p_gap


def test_permutation_detects_planted_effect():
    rng = np.random.default_rng(0)
    labels = np.array(["B3"] * 100 + ["B1"] * 100)
    outcomes = np.concatenate([rng.random(100) < 0.4, rng.random(100) < 0.1])
    gap, p = permutation_p_gap(labels, outcomes, "B3", "B1", n_perm=2000, seed=1)
    assert gap > 0.15
    assert p < 0.01


def test_permutation_null_when_no_effect():
    rng = np.random.default_rng(0)
    labels = np.array(["B3"] * 100 + ["B1"] * 100)
    outcomes = rng.random(200) < 0.2
    _, p = permutation_p_gap(labels, outcomes, "B3", "B1", n_perm=2000, seed=1)
    assert p > 0.05


def test_concentration_null():
    planted = np.array([True] * 12 + [False] * 48)
    hit = np.array([True] * 10 + [False] * 2 + [True] * 5 + [False] * 43)
    obs, exp, p = permutation_p_concentration(planted, hit, n_perm=2000, seed=1)
    assert obs == 10 and exp < 5 and p < 0.001


def test_metrics_basics():
    rate, lo, hi = wilson(5, 10)
    assert rate == 0.5 and lo < 0.5 < hi
    assert wilson(0, 0) == (0.0, 0.0, 0.0)
    assert fisher_one_sided(9, 10, 1, 10) < 0.01
    assert hypergeom_sf(3, 1000, 12, 100) < 0.2
    z, p = cochran_armitage([(1, 20), (5, 20), (10, 20), (15, 20)])
    assert z > 3 and p < 0.01
    assert cohen_kappa([True, False, True, False], [True, False, True, False]) == 1.0
