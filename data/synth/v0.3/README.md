# Synthetic corpus v0.3: bridges that need both sides

Specs authored 2026-09-14 under ADR-014, after the v0.2 review (`research/07`). Not built, not sealed.

## Why a v0.3

In v0.2, single-note reflection recovered 8 of 16 planted mechanisms against 6 of 16 for the two-note oracle, and the exploratory control X5 showed the single-note prompt answers on every filler note. The eight single-note recoveries were all general principles (regression to the mean, a sampling interval longer than the event, a device step) that one note's ingredient set already cued. Only two v0.2 bridges (br09, sequential identifiers; br17, expectation-lag dropout) needed both sides, and the pipeline missed both.

## Design rules

1. **Facts, not principles.** Every ingredient is a specific fact about this builder's situation: an identifier pattern, a date coincidence, a measured number, a named vendor quirk, a place, an order of events. The mechanism is stateable only from the conjunction of the two notes. `fact_type` records which kind (identifier, date, number, vendor, location, sequence).
2. **Two-sentence `one_side_test`.** What side A alone supports; what side B alone supports. The paraphrase-leak judge (`prompts/leak_judge.md`) and the one-side gate (`src/daydreamd/synth/oneside.py`, `prompts/generate_single_strict.md`) enforce it at build time.
3. **Shape-matched decoys.** All 12 decoys mirror an accepted bridge's `fact_type` and surface pattern with a different or absent mechanism; `why_not` states why the tempting synthesis is false.
4. **Same domains, same balance.** Six domains, 16 notes each: 8 bridge notes, 4 decoy notes, 4 fillers. Every domain pair appears; the nine cross-group pairs appear twice.

## Bridge map

| id | pair | fact_type | mechanism (one line) |
|---|---|---|---|
| br01 | ecom x fraud | identifier | numbered postbin.io mailbox batch hit the promo and the app the same night |
| br02 | ecom x fraud | number | the 30-euro exemption on the shared processor account explains the 29.90 top-ups |
| br03 | ecom x mleval | identifier | eval SKUs 1000 to 1199 never overlap production SKUs 1200 and up |
| br04 | ecom x mleval | date | the 19 August score drop is the vendor's judge snapshot change |
| br05 | ecom x health | sequence | the Tuesday 06:30 dispatch cutoff sits on the 07:00 dose |
| br06 | ecom x health | vendor | FrostLine's 14:00 pickup van runs warm; excursions and cloudy vials |
| br07 | ecom x grants | identifier | new VAT number vs accounts filed under the old one |
| br08 | ecom x iot | location | warped boards were staged on damp shelf C |
| br09 | grants x mleval | number | the pre-screen scores 3.5 flat past its length limit; both proposals are 61 pages |
| br10 | grants x mleval | vendor | EvalBench Pro re-normalises; the deliverable's scale moves |
| br11 | grants x fraud | identifier | consecutive identifiers across "independent" parties (v0.2 br09 template) |
| br12 | grants x fraud | date | same network block, two minutes apart, after the Slack leak |
| br13 | grants x health | date | interview and fasting draw on the same morning |
| br14 | grants x health | vendor | Eurofins changed units; the substudy would inherit it |
| br15 | iot x mleval | location | the judge's GPU box is in the shed that hits 41 degrees since 1 August |
| br16 | iot x mleval | number | the 970-gram reference weight is behind the eval's 3 percent error |
| br17 | iot x fraud | location | the van's twelve courtyard stops are the phone farm's signups |
| br18 | iot x fraud | identifier | the signup numbers are in the data-only Telsim M2M range |
| br19 | iot x health | date | the window sealed for the sensor cable raised CO2 and cut deep sleep |
| br20 | iot x health | sequence | laser evenings raise next-morning resting heart rate |
| br21 | mleval x fraud | identifier | eval items and the production whitelist share BIN 411111 |
| br22 | mleval x health | date | the disputed labels were written on the three fever days |
| br23 | fraud x health | vendor | the Twilio route to Yoigo failed on 15 August for both |
| br24 | grants x iot | number | the budgeted gateway model was discontinued and repriced |

## What is not done yet

- Notes are not generated. Build with `make synth SPEC=data/synth/v0.3 WRITERS=experiments/micro-v0.3/writers.yaml MIN_WORDS=100` plus `--one-side-gate --gate-model sonnet` once `PREREGISTRATION-v0.3.md` is sealed.
- Bridges that fail the one-side gate are rewritten once by the experimenter and gated again; a second failure drops the bridge before the seal (see the preregistration, Section 6).
- The datasheet is written at freeze.
