"""Local embeddings. Notes never leave the machine for this step."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class Embedder:
    def __init__(self, model_name: str = MODEL_NAME) -> None:
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        self._model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        vecs = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return np.asarray(vecs, dtype=np.float32)


class FakeEmbedder:
    """Hash-seeded unit vectors for tests. Same text, same vector."""

    model_name = "fake-embedder"

    def encode(self, texts: list[str]) -> np.ndarray:
        out = []
        for t in texts:
            seed = int.from_bytes(hashlib.sha256(t.encode()).digest()[:4], "big")
            rng = np.random.default_rng(seed)
            v = rng.standard_normal(32).astype(np.float32)
            out.append(v / np.linalg.norm(v))
        return np.stack(out)


def embed_cards(run_path: Path, cards: list[dict], embedder: Embedder | FakeEmbedder) -> np.ndarray:
    out = run_path / "embeddings.npy"
    if out.exists():
        vecs = np.load(out)
        if vecs.shape[0] == len(cards):
            return vecs
    vecs = embedder.encode([c["claim"] for c in cards])
    np.save(out, vecs)
    return vecs
