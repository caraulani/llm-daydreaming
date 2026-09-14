"""`daydreamd mcp`: the product as MCP tools over stdio, so an agent can be told
"dream over my notes tonight" and read the morning back. Needs the `mcp` extra."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import paths


def build_server() -> Any:
    server_cls: Any
    try:  # mcp 2.x renamed FastMCP to MCPServer; accept either
        from mcp.server.mcpserver import MCPServer

        server_cls = MCPServer
    except ImportError:
        try:
            from mcp.server import fastmcp as _legacy

            server_cls = getattr(_legacy, "FastMCP")  # noqa: B009
        except (ImportError, AttributeError) as exc:  # pragma: no cover
            raise RuntimeError("install the mcp extra: uv sync --extra mcp") from exc

    server = server_cls("daydreamd")

    @server.tool()
    def daydreamd_dream(
        path: str, n: int = 40, kind: str = "markdown", out: str = "morning.md", critic: bool = True
    ) -> str:
        """Run one night of daydreaming over a folder of notes and write morning.md.
        kind: markdown | obsidian | claude-memory. Returns the morning file's path and counts."""
        from .dream import DreamConfig, dream

        r = dream(DreamConfig(path=Path(path), kind=kind, n=n, out=Path(out), critic=critic))
        return f"wrote {r.morning}: {r.counts['survivors']} survivors of {r.counts['asked']} pairs (cost ${r.cost_usd:.4f}); run {r.run}"

    @server.tool()
    def daydreamd_review(morning_path: str = "morning.md") -> str:
        """Read the KEEP and KNOWN boxes the owner ticked in morning.md into the verdict log."""
        from .review import review

        s = review(Path(morning_path))
        return f"reviewed {s.reviewed}: kept {s.kept}, known {s.known}, unmarked {s.unmarked}; log {s.log}"

    @server.tool()
    def daydreamd_skill(out: str = "") -> str:
        """Write a SKILL.md of endorsed connections and the learnings file the critic reads."""
        from .skill import build_skill

        r = build_skill(Path(out) if out else None)
        return f"wrote {r.skill} ({r.endorsed} endorsed, {r.known} known, {r.rejected} rejected) and {r.learnings}"

    @server.tool()
    def daydreamd_status() -> str:
        """Where daydreamd keeps its state and how many runs and verdicts exist."""
        from ..core.io import read_jsonl

        runs = (
            sorted(p.name for p in paths.runs_root().glob("*"))
            if paths.runs_root().exists()
            else []
        )
        n_verdicts = sum(1 for _ in read_jsonl(paths.verdicts_path()))
        return f"home {paths.home()}; runs {len(runs)} (latest {runs[-1] if runs else 'none'}); verdicts {n_verdicts}; learnings {'yes' if paths.learnings_path().exists() else 'no'}"

    return server


def main() -> None:
    build_server().run()
