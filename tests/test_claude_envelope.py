from __future__ import annotations

import pytest

from daydreamd.backends.claude_cli import parse_envelope, pick_model_entry

ENV = {
    "result": "OK",
    "total_cost_usd": 0.02,
    "modelUsage": {
        "claude-haiku-4-5-20251001": {"inputTokens": 898, "outputTokens": 8},
        "claude-sonnet-5": {"inputTokens": 2, "outputTokens": 4, "cacheReadInputTokens": 100},
    },
}


def test_picks_requested_alias_not_side_call():
    c = parse_envelope(ENV, "sonnet")
    assert c.model_id == "claude-sonnet-5"
    assert c.output_tokens == 4 and c.input_tokens == 102
    assert c.raw["all_model_ids"] == ["claude-haiku-4-5-20251001", "claude-sonnet-5"]


def test_fallback_to_largest_output():
    mid, _ = pick_model_entry(ENV["modelUsage"], "opus")
    assert mid == "claude-haiku-4-5-20251001"


def test_error_envelope_raises():
    with pytest.raises(RuntimeError):
        parse_envelope({"is_error": True, "result": "Not logged in"}, "haiku")
