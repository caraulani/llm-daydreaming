"""Small public corpus of arXiv abstracts (metadata is CC0). Secondary adapter for a fully
public reproducibility run. `fetch` pins ids in manifest.json; `load` reads them back."""

from __future__ import annotations

import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from ..core.ingest import Doc
from ..core.io import read_json, sha256_text, write_json
from ..core.run import now_iso

API = "https://export.arxiv.org/api/query?search_query=cat:cs.CL+OR+cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results={n}"
NS = {"a": "http://www.w3.org/2005/Atom"}
UA = "daydreamd/0.1 (https://github.com/caraulani/llm-daydreaming; research corpus fetch)"


def fetch(out: Path, n: int = 40, retries: int = 5) -> dict:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(API.format(n=n), headers={"User-Agent": UA})  # noqa: S310
            with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310
                xml = resp.read()
            break
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(5 * (attempt + 1))
    else:
        raise RuntimeError(f"arXiv API unavailable: {last}")
    root = ET.fromstring(xml)
    (out / "notes").mkdir(parents=True, exist_ok=True)
    docs = []
    for e in root.findall("a:entry", NS):
        aid = e.findtext("a:id", "", NS).rsplit("/", 1)[-1]
        title = " ".join(e.findtext("a:title", "", NS).split())
        abstract = " ".join(e.findtext("a:summary", "", NS).split())
        date = e.findtext("a:published", "", NS)[:10]
        text = f"# {title}\n\narXiv:{aid} ({date})\n\n{abstract}\n"
        (out / "notes" / f"{aid}.md").write_text(text, encoding="utf-8")
        docs.append({"id": aid, "title": title, "date": date, "sha256": sha256_text(text)})
    manifest = {
        "source": "arXiv API, cs.CL OR cs.AI, newest first",
        "license": "arXiv metadata: CC0 1.0",
        "fetched_at": now_iso(),
        "n_docs": len(docs),
        "docs": docs,
    }
    write_json(out / "manifest.json", manifest)
    return manifest


def load(path: Path) -> list[Doc]:
    manifest = read_json(path / "manifest.json")
    docs = []
    for d in manifest["docs"]:
        text = (path / "notes" / f"{d['id']}.md").read_text(encoding="utf-8")
        docs.append(
            Doc(id=f"arxiv-{d['id'].replace('.', '-')}", name=d["id"], text=text, sha=d["sha256"])
        )
    return docs
