"""Local embeddings. Notes never leave the machine for this step."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
STATIC_MODEL_NAME = "minishlab/potion-base-8M"


class Embedder:
    """sentence-transformers (PyTorch). The committed research runs used this model; install the
    `research` extra to recompute them exactly."""

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "sentence-transformers is not installed; run `uv sync --extra research` "
                "(the product default is the static embedder, which needs no PyTorch)"
            ) from exc
        self.model_name = model_name
        self._model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        vecs = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return np.asarray(vecs, dtype=np.float32)


class StaticEmbedder:
    """model2vec static embeddings: a 30 MB download, no PyTorch, encodes thousands of claims per
    second on a laptop. The product default. Embeddings only drive pair sampling and the
    duplicate gate, never a reported number, so the lighter model changes no result."""

    def __init__(self, model_name: str = STATIC_MODEL_NAME) -> None:
        from model2vec import StaticModel

        self.model_name = f"model2vec/{model_name}"
        self._model = StaticModel.from_pretrained(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        vecs = np.asarray(self._model.encode(texts), dtype=np.float32)
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vecs / norms


def make_embedder(kind: str = "static") -> Embedder | StaticEmbedder | FakeEmbedder:
    """`static` (product default), `minilm` (research runs), `fake` (tests)."""
    if kind == "fake":
        return FakeEmbedder()
    if kind == "minilm":
        return Embedder()
    if kind == "static":
        return StaticEmbedder()
    raise ValueError(f"unknown embedder: {kind}")


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


def embed_cards(
    run_path: Path, cards: list[dict], embedder: Embedder | StaticEmbedder | FakeEmbedder
) -> np.ndarray:
    out = run_path / "embeddings.npy"
    if out.exists():
        vecs = np.load(out)
        if vecs.shape[0] == len(cards):
            return vecs
    vecs = embedder.encode([c["claim"] for c in cards])
    np.save(out, vecs)
    return vecs
