# Synthetic corpus v0.2 (specs only; not yet built, not yet sealed)

Written 2026-09-13 after the v0.1 sealed run and its adversarial review
(`research/06-adversarial-review-v0.1-results-2026-09-13.md`). The review found that four of the
v0.1 single-note recoveries were corpus leakage by paraphrase, that three of the eight two-note
matches were one-note reading plus domain transfer, and that the v0.1 decoys shared one word each
and were too easy. v0.2 answers those three findings.

## What is in this directory

| File | Content |
|---|---|
| `bridges.yaml` | 24 planted bridges. Same schema as v0.1 plus `forbidden_phrases_a`, `forbidden_phrases_b`, `one_side_test`. |
| `decoys.yaml` | 12 decoy pairs: 9 shape-matched (`kind: shape`, with `shape`, `mirrors`, `why_not`) and 3 homonym decoys (`kind: homonym`). |
| `fillers.yaml` | 24 filler topics, four per domain. |

Corpus size when built: 48 bridge notes + 24 decoy notes + 24 fillers = 96 notes, 16 per domain.

## Design rules for v0.2

1. **Oblique ingredients.** Every ingredient is an observation (a count, a date, a reading, a
   thing that happened). No ingredient names the mechanism, states the diagnosis, uses a
   diagnostic verb ("is a signal of", "anchors", "the same failure as") or gives the fix.
2. **Per-side forbidden phrases.** `forbidden_phrases_a` and `forbidden_phrases_b` list the
   mechanism's key nouns and verbs the writer must not use on that side. The corpus builder must
   append them to the writer's forbidden list for that note (v0.1's builder only forbade the
   partner domain and the mechanism string; extend `Spec.note_plan()` accordingly).
3. **One-side test.** `one_side_test` states what a reader of one note alone can conclude. The
   leak judge (`prompts/leak_judge.md`) checks every bridge note against its gold and returns
   LEAK or CLEAN; a LEAK note is regenerated, and the leak-judge output is committed with the
   corpus. This is the paraphrase check the 6-gram test cannot do.
4. **Shape-matched decoys.** Nine decoys imitate the shape of a real bridge (spike after an
   event, drift, threshold, dropout at a date, volume change, duplicates, improvement after a
   change, outage, regional difference) with unrelated causes, each with a `why_not`. A bridge-
   like synthesis on these is wrong by construction. Three homonym decoys remain for continuity.
5. **Balanced domain pairs.** All 15 domain pairs appear; the 9 pairs between {ecom, grants, iot}
   and {mleval, fraud, health} appear twice, so every domain carries exactly 8 bridge notes.
6. **Two note-writer families.** Bridges with odd ids are written by a Claude Haiku-class model,
   even ids by a non-Anthropic model (exact ids fixed in `PREREGISTRATION-v0.2.md` before
   sealing). Decoys and fillers alternate the same way by position.

## Bridge map

| id | pair | mechanism (short) |
|---|---|---|
| br01 | ecom x fraud | small refunds on new cards after promos are stolen-card validation |
| br02 | ecom x fraud | many names, one address is a reshipping drop point |
| br03 | grants x mleval | a visible prior score pulls the new score toward it |
| br04 | grants x mleval | the first-listed criterion gets the most weight |
| br05 | iot x health | a relative schedule drifts out of a fixed window |
| br06 | iot x health | a step change on the day the device changed is the device |
| br07 | ecom x mleval | measured on the tuning data, the number is inflated |
| br08 | ecom x mleval | a metric computed only on completed cases excludes its failures |
| br09 | grants x fraud | consecutive identifiers across "independent" parties expose one operator |
| br10 | grants x fraud | work done in the last hour before a cutoff is worse |
| br11 | mleval x health | improvement after selecting the worst cases is partly reversion |
| br12 | ecom x iot | same-second concentration of senders overwhelms a receiver |
| br13 | ecom x grants | cash gaps come from receipt lag, not margin |
| br14 | grants x iot | absence of an expected event is never alerted |
| br15 | mleval x fraud | a disclosed rule becomes the target |
| br16 | fraud x health | a total cap does not prevent bursts |
| br17 | ecom x health | people quit just before results appear |
| br18 | ecom x health | behaviours tied to an existing routine persist |
| br19 | iot x mleval | a silently drifting instrument needs a scheduled reference check |
| br20 | iot x mleval | a check that runs less often than the failure lasts never sees it |
| br21 | grants x health | a cheap disqualifying check placed late wastes the expensive step |
| br22 | grants x health | more frequent reporting, less compliance |
| br23 | iot x fraud | accepting far-from-now timestamps admits stale or replayed messages |
| br24 | iot x fraud | the population still on factory defaults is the one taken over |

## Not yet done

The notes are not generated, the manifest does not exist, and `PREREGISTRATION-v0.2.md` is a
draft. Sealing order is the same as v0.1: seal the preregistration and these three spec files,
stamp them, then build, then run.
