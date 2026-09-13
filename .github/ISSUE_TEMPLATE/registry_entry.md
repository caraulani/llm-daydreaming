---
name: Registry entry
about: Announce a Track B registry submission before opening the PR
title: "registry: <YYYY-MM-DD>_<slug>"
labels: registry
assignees: ''
---

## Entry

- Directory name (`registry/entries/<YYYY-MM-DD>_<slug>/`):
- Corpus description (no corpus text):
- Generator model snapshot ID and access date:
- Critic and judge model snapshot IDs:
- Number of dreams submitted:
- OpenTimestamps proof attached to `dreams.jsonl`: yes / no

## Checklist

- [ ] I read `registry/README.md`.
- [ ] `metadata.yaml` follows `registry/entries/_TEMPLATE/metadata.yaml`.
- [ ] Every dream carries `{connection, mechanism, testable_implication, needs, sources}`.
- [ ] No secrets, no private names, no third-party personal data.
- [ ] I understand entries are published under CC BY 4.0.
