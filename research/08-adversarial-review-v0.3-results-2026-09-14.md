# Adversarial review of the v0.3 sealed run (2026-09-14)

*Reviewer agent (Claude Fable 5.1), checked against raw outputs in `experiments/runs/public/2026-09-14_micro_v0_3/` and `data/synth/v0.3/manifest.json`. Run cost $87.86 at list price. Decision by the preregistered rule: NULL (validity precondition failed, H1 p = 0.083, H3-strict not interpretable).*

## Verdict in one paragraph

The corpus redesign worked and the measurement did not. ADR-014 delivered what it promised: on fact-type bridges, one note alone under the strict prompt recovered 2 of 22 planted mechanisms (9 percent) against 8 of 16 (50 percent) in v0.2, while two-note recall held at 8 of 22 (36 percent) against 6 of 16 (38 percent). The gap between two notes and one note moved from minus 12 points to plus 27 points, which is the first run in which the recombination story points the right way. Three things stop that from being a result. First, the validity precondition failed for a reason that indicts the precondition, not the prompt: the strict prompt answered on 12 of 24 fillers, and all 12 answers are genuine local inferences from specifics the filler contains (arithmetic conflicts, contradictory deadlines, unverified fixes), exactly what the prompt asks for. Second, H1 missed at p = 0.083 because one decoy answer (S0-0027, dc06) survived both critics and because the match judge returned NO_MATCH on at least three outputs a human would accept (S0-0002, S0-0004, S0-0015); a human-read recall is about 11 of 22. Third, the match judge is the dominant noise in both directions: the two single-note "recoveries" (B4-0003, B4-0027) are partial outputs the gate's judge had rejected on the same side hours earlier. The instrument, not the loop, is what v0.4 has to fix.

## 1. The precondition failed, and it is the precondition's fault

The 12 filler answers (B4-0044, -0045, -0046, -0049, -0053, -0054, -0058, -0060, -0063, -0064, -0066, -0067):

- Category (a), genuine specifics the filler happens to contain: 10 of 12. Examples: B4-0046 (fl03) computes that two minimums sum to 36, leaving 14 short of a 50-unit threshold stated in the note; B4-0054 (fl11) notices a blanket 10-day deadline contradicting the 21-day and 45-day deadlines listed two lines later; B4-0058 (fl15) finds two rules in a hydration protocol that both fire on a cold high-effort ride; B4-0064 (fl21) points out the reprint fix was never verified at hour 6 where the original failed; B4-0049 (fl06) computes a break-even of about 64 cycles from two numbers in the note.
- Category (b), generic implication: 1 (B4-0053, fl10, "the cap has slack").
- Category (c), restatement: 1 (B4-0067, fl24).

None is a named principle. The prompt did what it says: it declined 12 fillers and spoke on 12 that carry a checkable local inference. The fillers were written as dense working notes with numbers and dates, so half of them legitimately contain one. The 10 percent bar therefore measures filler richness, not abstention quality, and no prompt would pass it on this corpus without also refusing genuine specifics.

What the precondition should have been. The property we need is "one note alone does not yield the GOLD", which the gate already certifies per bridge with a judge in the loop. A filler answer rate says nothing about that. For v0.4, replace the filler-rate precondition with two checks that target the actual failure: (1) gold recovery from fillers must be zero, which is trivially measurable (fillers have no gold; report answered fillers whose output the judge matches to ANY gold: here 0 of 12); (2) the single-note arm's recovery rate on bridge notes must be below a preregistered fraction of S0 recall, e.g. one third, which is the recombination claim stated as a validity check. If a filler answer rate is kept at all, preregister it on fillers written to contain no numbers, dates or conflicts, and set the bar from a pilot.

## 2. H1: what the misses are

Planted units (22):

- Recovered by the two-vote judge (8): S0-0000 br01, -0006 br07, -0010 br13, -0012 br15, -0016 br19, -0017 br20, -0018 br21, -0019 br22.
- NONE (5): S0-0003 br04 (B), -0007 br08 (B), -0008 br10 (B), -0014 br17 (A), -0020 br23 (A). The generator saw both notes and declined. These are honest misses on hard bridges; three of five are family B.
- Answered, judged NO_MATCH (9): S0-0001 br02, -0002 br03, -0004 br05, -0005 br06, -0009 br12, -0011 br14, -0013 br16, -0015 br18, -0021 br24.

Reading the nine against gold:

- Judge false negatives, a human accepts: S0-0002 br03 (output: "eval set SKUs 1000-1199 excludes the 1200+ SKUs driving 9 percent returns, so the 4.6 score never measures the problem"; this IS the gold; votes False, True, tie fails closed). S0-0015 br18 (output: "SIM 622345 shares the 62234 prefix flagged as fraud-bypass SIMs, the workshop is the batch's physical source"; gold: the M2M range 6 22 34 xx printed on the workshop's sensor SIMs; same mechanism, votes False, False). S0-0004 br05 (output names the Tuesday packing window as the cause of Tuesday misses; gold names the carrier's 06:30 cutoff moving dispatch; partial but the causal link is the one planted; tie).
- Partial, judge defensible: S0-0009 br12 (same event, but not "same network block two minutes apart"), S0-0021 br24 (same equipment, but not the discontinued model and the 1,490 replacement), S0-0013 br16 (points at the scale but not the miscalibrated reference weight).
- Real misses: S0-0001 br02 and S0-0005 br06 and S0-0011 br14. br02 and br06 are the two bridges whose side A the experimenter rewrote to defeat the gate; the rewrite removed the ingredient the gold depends on (br02: the 30-euro exemption itself; br06: the older van), so the pair can no longer produce the gold as written. That is a construction error introduced by the rewrite-once rule, not a generator failure (see section 5).

Human-read recall: 8 plus 3 clear false negatives equals 11 of 22, which against 1 of 12 decoys gives Fisher p about 0.02. The preregistered number stands at 8 of 22, p = 0.083, and the paper reports that; the human reading goes in the exploratory section with the unit ids.

The surviving decoy, S0-0027 (dc06): output "export data needs manual QA before the rigorous-benchmark claim goes into the grant proposal". Both critics kept it, the dupgate did not catch it. It is not a mechanism claim at all; it is advice. The critic rubric ("restates, generic, uncheckable") has no category for "not a connection between the two notes", which is what this is. Two other decoy answers (S0-0028 dc07, S0-0030 dc09) were correctly killed by both critics as generic syntheses. So the false positive is a critic-rubric gap, not a judge failure.

## 3. H5: the writer-family effect

| | family A (Haiku) | family B (Qwen 14B) |
|---|---|---|
| planted bridges | 10 | 12 |
| S0 NONE | 2 | 3 |
| answered | 8 | 9 |
| judged MATCH | 6 | 2 |
| mean cosine to gold, answered | 0.653 | 0.489 |
| bridge-note words, median | 166.5 | 108.5 |
| cards per note, median | 5.5 | 5.0 |
| mean claim length, words | 13.4 | 11.5 |

Reading (b), note quality, survives best. Family B notes are 35 percent shorter, their cards are terser, and among the nine answered family-B pairs the outputs land farther from gold on average (0.49 vs 0.65 cosine), which is what thinner ingredients produce. Reading (c) is partly true and cuts the other way: the two dropped bridges were both family A, so family A kept its easier set; that inflates the A rate but does not explain the B rate. Reading (a), shared priors, cannot be separated from (b) in this design because family is confounded with length and card density; the honest statement is that the effect is real (60 vs 17 percent), that it tracks note richness, and that a same-length control (family B notes regenerated with a higher floor, or family A notes truncated) is the experiment that separates the readings. Two of the three family-B judge false negatives (br18, br05 is A) also sit in this set, so the family-B rate with human reading is about 3 or 4 of 12, still below A.

## 4. H3-strict: the gate worked

Denominators first. The B4 arm has 44 bridge-note units (22 bridges times two sides) and 24 fillers. `recall` in T4 is computed over "bridges reachable", defined as bridges with at least one match row, i.e. bridges whose note was answered: 13 answered units covering 12 bridges, 2 recovered, shown as 16.7 percent. That denominator is wrong for the recombination question; the right one is all 22 planted bridges, giving 2 of 22, 9 percent. The paper must use 2 of 22 and say why.

Across versions:

| | v0.2 | v0.3 |
|---|---|---|
| S0 two-note recall | 6 of 16, 38 percent | 8 of 22, 36 percent |
| single-note recall | 8 of 16, 50 percent (default prompt, answered on 31 of 32 notes) | 2 of 22, 9 percent (strict prompt, answered on 13 of 44) |
| gap, two notes minus one note | minus 12 points | plus 27 points |

Two-note recall did not fall; one-note recall did. So this is the gate and the fact-type design working, not a harder corpus depressing everything. The confound is the prompt: v0.2 used the inert default single prompt, v0.3 the strict one. Part of the drop is the prompt declining more (NONE on 31 of 44 bridge notes). The clean comparison is the same strict prompt on the v0.2 corpus, which costs about $8 and should be run before the paper claims the gate did the work.

And the two single-note "recoveries" are weak: B4-0003 (br02-b) says 29.90 "clears a specific system threshold", B4-0027 (br16-b) says the error "traces to the gold standard itself"; both are half the mechanism, both got two MATCH votes in the run, and the gate judge rejected the same half-mechanism on the same side on the final pass (br16-b: "misses the specific cause: calibrated against wrong reference weight"). Same judge, same prompt, opposite verdicts on the same content. With a consistent judge, one-note recall is 0 to 2 of 22.

## 5. Gate stochasticity and the rewrite-once rule

Four passes, 48 sides each, 192 side-gates: 6 flags (br02; br06, br15; br11; br09, br11), 5 of them judge ties, 1 a 2-of-2 (br11, pass 4). Per-side flag rate about 3.1 percent per pass, tie rate 2.6 percent. At that rate a 24-bridge corpus throws one or two new flags every pass regardless of the bridges, which is what happened: the flagged set changed completely from pass to pass except br11. Implications:

- Ties are noise more often than signal here. Four of five tie-flags cleared on the next pass without any change to the flagged note (br02's note was reused on pass 2; br06 and br15 were regenerated, but br09 and the second br11 came after). Fail-closed on a tie is the right rule for a certification, but it must be paired with a re-vote (three or five votes on a tie) rather than a rewrite, or the experimenter rewrites specs in response to noise.
- The rewrite-once rule caused two real losses. Rewriting side A of br02 and br06 to defeat a flag removed the ingredient the gold needs, so those bridges became unrecoverable by design and show up in section 2 as misses. A rewrite must be re-checked against the `one_side_test` in both directions: side A alone must not give the gold, and A plus B together must still contain every ingredient the gold names. The builder should assert the second condition (each gold ingredient phrase appears in at least one side's ingredient list) before accepting a rewrite.
- The gate's own judge and the run's judge are the same model on the same prompt and disagree on identical content (section 4). The gate certifies against one draw of the generator and one pair of judge votes; that is a 3 percent floor on "certified" bridges being one-note recoverable under a different draw.

## 6. Critics

T8: Haiku killed 0 of 8 correct recoveries, Sonnet 1 of 8 (S0-0019 br22, "not_checkable"); both let S0-0027 through. In v0.1 the Haiku critic killed 3 of 8 correct recoveries, in v0.2 3 of 6. What changed is the outputs, not the critic: fact-type bridges produce outputs that name identifiers, dates and numbers ("SKUs 1000 to 1199", "22 July 03:12", "1,190 euros"), and the rubric's "generic" and "restates" categories do not fire on those. On principle-type bridges the correct answer often reads as a general statement, which the rubric kills. So the critic was never "too strict"; it was strict against the shape of principle-type answers. The remaining gap is the one dc06 exposes: the rubric needs a "not a connection between the two notes" kill, and it needs to accept only outputs that cite something from both sides.

## 7. What may be said, and what to run next

Verdict: NULL by the preregistered rule, correctly. The corpus design change is validated (one-note recovery 9 percent against 50 percent), two-note recovery held (36 percent against 38), the precondition was mis-specified, and the match judge's inconsistency now bounds every number more than the generator does.

Abstract sentences (claim discipline as before):

- "On a corpus of 22 fact-type bridges certified by the generator itself to need both sides, two-note recombination recovered 8 of 22 planted mechanisms (36 percent, Wilson 20 to 57) and single-note reflection under a strict abstention prompt recovered 2 of 22 (9 percent); in v0.2 the same comparison was 6 of 16 against 8 of 16."
- "The preregistered validity precondition failed: the strict prompt answered on 12 of 24 filler notes, and on inspection all twelve answers are inferences from specifics the fillers contain, so the precondition measured filler richness rather than abstention; H1 missed at p = 0.083 with one decoy answer surviving both critics."
- "The run reports NULL by its preregistered rule. Three judge decisions a human reader would reverse (units S0-0002, S0-0004, S0-0015) would move recall to 11 of 22; we report the preregistered number and list the units."
- "Rewriting two bridge specifications to defeat gate flags removed ingredients the gold depended on; a rewrite must preserve gold derivability, and the builder now checks it." (Only after the check exists.)

Not permitted: "recombination demonstrated", "novel", any statement that the gate is deterministic.

Best next run under $30: the strict single-note prompt over the v0.2 corpus (46 bridge notes plus 24 fillers, about $8), which separates "the gate and fact-type design lowered one-note recovery" from "the strict prompt lowered it". Second, at about $6: re-judge every v0.3 S0 answered unit and every B4 bridge answer with five votes instead of two, to measure judge consistency directly; if recall moves by three or more bridges, the judge is the instrument to fix before v0.4. Both are exploratory and can run tonight.

For v0.4: keep the corpus design; replace the precondition as in section 1; add the gold-derivability check to rewrites; three or five judge votes with a tie triggering a re-vote, not a rewrite; add the "cites both sides" rule to the critic; and a same-length control for the writer-family effect.

Show HN paragraph, two sentences: "v0.3: I rebuilt the corpus from specific facts and had the generator itself certify that each bridge needs both sides (22 of 24 passed). Two notes recovered 8 of 22; one note under a strict prompt recovered 2 of 22, against 8 of 16 for one note in v0.2; the run is still NULL by its own rule because the abstention check I preregistered turned out to measure the wrong thing."

Outside scope, noticed: T4's `recall` column uses "bridges reachable" as the denominator for B4, which overstates single-note recall (16.7 percent shown, 9 percent over all planted); the stats code should report both or switch the denominator for note-level arms.
