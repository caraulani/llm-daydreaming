"""Deterministic offline backend for tests and dry runs. Never calls a model."""

from __future__ import annotations

import hashlib
import json

from . import Completion


class FakeBackend:
    name = "fake"

    def complete(self, prompt: str, *, model: str) -> Completion:
        digest = hashlib.sha256(prompt.encode()).hexdigest()
        text = self._respond(prompt, digest)
        return Completion(
            text=text,
            model_id=f"fake-{model}",
            input_tokens=len(prompt) // 4,
            output_tokens=len(text) // 4,
            cost_usd=0.0,
        )

    @staticmethod
    def _respond(prompt: str, digest: str) -> str:
        if "Return a JSON array of concept cards" in prompt:
            cards = [
                {
                    "claim": f"Synthetic claim {digest[i : i + 4]} about the note",
                    "entities": [f"entity-{digest[i : i + 2]}"],
                    "why_it_matters": "Used by tests only.",
                    "confidence": "med",
                }
                for i in range(0, 12, 4)
            ]
            return json.dumps(cards)
        if "verdict" in prompt and "kill" in prompt:
            keep = int(digest[0], 16) % 4 != 0
            return json.dumps(
                {"verdict": "keep" if keep else "kill", "reason": "ok" if keep else "generic"}
            )
        if int(digest[1], 16) % 5 == 0:
            return "NONE"
        return json.dumps(
            {
                "connection": f"Synthetic connection {digest[:6]}",
                "mechanism": "Synthetic mechanism.",
                "testable_implication": "Check something concrete this week.",
                "needs": "claim A supplies X; claim B supplies Y",
            }
        )
