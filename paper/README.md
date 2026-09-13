# paper/

`paper.md` is the source of truth. Everything else here is derived from it or supports it.

| File | Purpose |
|---|---|
| `paper.md` | The paper, markdown. Section 6 tables are filled by `make reproduce`. |
| `refs.bib` | BibTeX for every reference in `paper.md`. Entries marked `verify` in the `note` field have not been re-fetched. |
| `CHECKLIST.md` | NeurIPS-style paper checklist, answered for the current draft. |
| `figures/` | Generated figures. Empty until there are results. |

## Building a PDF

arXiv accepts TeX source or PDF, not markdown. Build with pandoc:

```bash
pandoc paper/paper.md \
  --from markdown --to pdf \
  --pdf-engine=xelatex \
  --bibliography=paper/refs.bib \
  --citeproc \
  -V geometry:margin=1in -V fontsize=11pt \
  -o paper/daydreamd.pdf
```

For the arXiv TeX route, produce `main.tex` with `pandoc paper/paper.md -s -o paper/main.tex --bibliography=paper/refs.bib --natbib` and submit the `.tex`, `.bib` and any figures. `make paper` runs the PDF build.

## Before submitting to arXiv

- Fill every TBD from run logs. No placeholder may remain.
- Resolve every "(verify)" reference by fetching the arXiv abstract page and checking title, authors and ID.
- Categories: cs.CL primary, cross-list cs.AI and cs.HC.
- License: CC-BY-4.0. arXiv licenses are irrevocable per version.
- Endorsement: since 2026-01-21, a first-time cs.* submitter without an institutional email needs a personal endorsement from an established author in the category. Arrange this weeks ahead; it is the long pole. A co-author with prior arXiv submissions is the simplest route.
- After the arXiv ID exists: add it to `CITATION.cff` as `preferred-citation`, submit to Hugging Face Papers, and tag a release so Zenodo mints a DOI.
- Moderation takes one to four days; Google Scholar indexes one to fourteen days after that.
