---
name: Adapter proposal
about: Propose a new corpus adapter (Obsidian, Zotero, a codebase, a mail archive, ...)
title: "adapter: "
labels: adapter, enhancement
assignees: ''
---

## Source

<!-- What corpus format does this adapter read? Link to the format spec if one exists. -->

## Unit of ingest

<!-- What becomes one "document"? A note, a file, a bib entry, a commit message? -->

## Output surface

<!-- Where should dreams land so the owner sees them in their own tool? (e.g. Obsidian daily note with [[wikilinks]]) -->

## Where it lives

Adapters live outside core unless they are already listed in `ROADMAP.md`. State which:

- [ ] I will publish this as a separate package that implements the `Adapter` protocol (see `docs/extending.md`).
- [ ] This adapter is on the roadmap and I am offering to build it in-tree.

## Privacy

<!-- Does the source contain secrets by default? How will the adapter strip them? -->
