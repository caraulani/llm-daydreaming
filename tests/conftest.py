from __future__ import annotations

import numpy as np
import pytest

from daydreamd.core.embed import FakeEmbedder


@pytest.fixture
def cards() -> list[dict]:
    out = []
    for n in range(8):
        for c in range(3):
            out.append(
                {
                    "id": f"n{n}-c{c}",
                    "source_note": f"n{n}",
                    "claim": f"claim {n} {c} about topic {n % 3}",
                    "entities": [],
                    "why_it_matters": "",
                    "confidence": "med",
                }
            )
    return out


@pytest.fixture
def vecs(cards: list[dict]) -> np.ndarray:
    return FakeEmbedder().encode([c["claim"] for c in cards])
