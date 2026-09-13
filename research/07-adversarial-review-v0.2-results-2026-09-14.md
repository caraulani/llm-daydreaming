# Adversarial review of the v0.2 sealed run (2026-09-14)

Reviewer: Claude Fable 5.1 acting as a hostile-but-fair area chair, reading the raw outputs of `experiments/runs/public/2026-09-14_micro_v0_2/` (generations, both critic files, match judgments, units, cards, embeddings) and the corpus `data/synth/v0.2/`. Every count below was recomputed from those files. Unit ids are quoted so anyone can check.

## 1. Verdict in one paragraph

The rule says SIGNAL and the rule passed for the wrong reason. H1 is real: the generator answers on planted pairs and abstains on 10 of 12 decoys and 34 of 36 random pairs, the match judge is strict, and no decoy answer survives the primary critic. H4 is real as a number and empty as evidence: S1 pairs a bridge note with an unrelated filler and asks for a connection between the two, so NONE is the correct answer and says nothing about whether the second note was needed. B4 answers that question, and the answer is no: the single-note arm recovered 8 of 16 mechanisms, including five (br05, br06, br11, br13, br20) that the two-note oracle marked NONE. The planted mechanisms are general principles (regression to the mean, sampling interval versus event duration, instrument change, relative schedules drifting, receipt lag) and each note carries the full set of ingredients for its side, so a capable model reads the principle off one note. The corpus is oblique to a string matcher and to the leak judge, and transparent to the generator. What survives is the selection half (H1 and specificity) and one measured sampler fact (a 2.7x enrichment of planted card pairs in the near cross-domain pool, invisible at 300 draws). Recombination is not demonstrated. The paper must say both things in the same sentence.

## 2. The eight B4 matches, unit by unit

For each: does the note state or imply the mechanism (a, judge failed), is the mechanism general knowledge supplied from one cue (b), or is the match judge lenient (c)?

| Unit | Note | Family | Bridge | Verdict | Why |
|---|---|---|---|---|---|
| B4-0000 | br01-a | A | br01 (card testing) | b | Note lists refund clustering after promos, small orders, cards added at checkout, no payment check. "Stolen-card validation" is the standard reading of that triple; the note never says it. Judge correct, one-side test false. |
| B4-0007 | br05-b | A | br05 (relative schedule drifts) | b, bordering a | Note states the reminder fires 24 hours after the last confirmed dose and lists dose times 07:05 to 08:30 across the week. The mechanism is arithmetic on the note's own numbers. |
| B4-0008 | br06-a | B | br06 (device step) | b, bordering a | Note: humidity jumped on 3 September, enclosure swapped on 3 September, weather station unchanged. The note is the artifact story minus the word. |
| B4-0009 | br06-b | B | br06 | b, bordering a | Same structure: deep sleep up on 8 September, ring replaced on 8 September, routines unchanged. |
| B4-0015 | br11-b | A | br11 (regression to the mean) | b, bordering a | Note gives the year's highest reading (68), the 12-month average (63), and the reading two weeks later (62). That is the textbook setup. |
| B4-0016 | br13-a | A | br13 (receipt lag vs expense cadence) | b | Note: settlements 14 days out, ad spend charged daily, overdrafts in sales-spike weeks. Mechanism is contained in side A alone; the gold's "both cash squeezes" needs side B only for the second instance. |
| B4-0019 | br14-b | B | br14 (absence not monitored) | b | Note: sensor silent, last status ok, alerts on error codes only. One side suffices. |
| B4-0024 | br20-a | B | br20 (check interval exceeds event) | b, bordering a | Note: sensor reports every ten minutes, spikes last two minutes, chart never shows a spike. Aliasing is the only reading. |

None is (c). The match judge is strict enough to reject S0-0000 (br01), whose generated mechanism ("stolen cards test sub-15-euro charges, then request refunds fast") is the gold mechanism; the judge called it "different causal stories". That is one judge false negative, so S0 recall is 7 of 16 on a human reading, not 6. The judge also rejected S0-0002 (br04, variance-driven versus position-driven weighting) and S0-0013 (br21, correlation analysis versus screen-first), both correctly.

Reading of the pattern: the leak judge asked "does this note state or directly imply the mechanism" and answered CLEAN because no sentence states it. The `one_side_test` field in `bridges.yaml` asserts what a naive reader concludes ("A alone reads as buyer's remorse"). The generator is not a naive reader. The obliqueness gate tested the wrong reader.

## 3. H4 is an artifact of the prompt contract

S1 outputs: 29 of 32 NONE, 2 answers (S1-0000, S1-0016), 1 error (S1-0015, empty claim B). The two answers try to connect the bridge note to the filler and fail the match: S1-0000 links br01-a's refund pattern to fl10's new allowlist countries; S1-0016 links br13-a's overdrafts to fl19's pitch deck. Both are honest attempts at the question asked. The NONEs are the model correctly reporting that br01-b and fl02, br02-a and fl12, and so on, share nothing. Nothing in S1 asks the model what note A implies on its own; the pair prompt asks whether A and B connect. B4 asks the single-note question and gets the mechanism 8 times in 32.

So the rule's H4 pass measures "declines to connect A to an unrelated B", which is a specificity result, and the preregistration mislabeled it as the recombination test. The five bridges the oracle missed and B4 recovered (S0-0003 br05, S0-0004 br06, S0-0007 br11, S0-0008 br13, S0-0012 br20) are the direct evidence: given both notes and permission to say NONE, the model said NONE; given one note and no permission, it produced the gold. The pair prompt's "most pairs are unrelated" framing suppresses answers the model has.

The clean control, which the paper must run before any recombination sentence: B4-NONE, the single-note prompt with NONE permitted and the same output schema, over all 32 bridge notes and the 24 fillers (fillers must come back NONE or the arm is measuring compliance, not knowledge). Recombination is supported only if S0 recall exceeds B4-NONE recall on the same bridges. Cost about $5 at list price. A second, cheaper check on the existing data: the 7 S0 NONEs versus the B4 recoveries above already show the ordering is the wrong way.

## 4. H1 on harder bridges: the seven planted NONEs

S0 NONE on br05, br06, br09, br11, br13, br17, br20. Families: br05, br09, br11, br13, br17 written by A (Haiku); br06, br20 by B (Qwen). Read against the notes:

- br05, br06, br11, br13, br20: not broken. B4 recovered every one of them from a single note, so the ingredients are sufficient. The oracle's NONE is the generator declining under the pair contract, not a thin bridge.
- br09 (sequential identifiers expose one operator): br09-a buries "2847-XYZ" and "2845-XYZ" in a background-check paragraph and br09-b describes forty destination numbers incrementing in the last two digits. The connection exists and is oblique on both sides; the generator missed it. This is the one bridge in the set that behaves as the design intended, and the pipeline failed it.
- br17 (expectation-lag dropout at the third cycle): br17-a gives churn by cycle with a 19 percent spike at cycle three and no interim contact; br17-b gives forum dropout around day 20 with visible changes at day 30 to 35. Also genuinely two-sided. Missed.

So five of the seven misses are prompt-contract effects, two are real misses on the two most oblique bridges. Obliqueness worked exactly twice, and both times the pipeline lost.

## 5. H2: the sampler, measured properly

All 16 planted pairs again have their closest card pair in Q1 (min-distance quantiles 0.0004 to 0.077, `distance_posthoc.json`). B7 still drew 2 planted card pairs in 300, same as B1. Both facts are true because Q1 is a quarter of 115,345 card pairs and the cross-domain part of it holds 20,163 pairs, of which 200 are planted (0.99 percent) against a base rate of 0.36 percent: enrichment 2.73x, real, and at 300 draws the expectation is 3.0 planted versus 1.1. Observed 2. Detecting a 2.7x lift at this base rate needs on the order of 1,500 draws per arm.

Note-level ranking is no better. Ranking the 3,526 cross-domain note pairs by minimum card distance puts the planted pairs at ranks 6, 53, 112, 144, 189, 309, 314, 372, 416, 446, 670, 696, 725, 1303, 1605, 1748: precision at 300 is 5 of 300 (1.7 percent) against a base of 0.45 percent, 3.7x. Mean distance ranks are similar.

Verdict: the v0.1 post-hoc was right about direction and wrong about magnitude. Planted pairs are near, but so are hundreds of unplanted cross-domain pairs (shape-matched decoys were built to be near). The sampler hypothesis is not dead; it is a 3x effect that this design cannot detect and that would need a stronger signal than embedding distance to matter. The paper should report the 2.73x pool enrichment as the measured quantity and drop the arm-level hypergeometric as the test.

## 6. Critics

On the 6 judge-matched S0 recoveries: Haiku killed S0-0011 (br19, "generic"), S0-0014 (br22, "restates_claim"), S0-0015 (br23, "restates_claim"); Sonnet killed S0-0014 only ("generic"). On the 2 decoy answers: S0-0016 (dc01, thundering herd) killed by both; S0-0024 (dc09) killed by Haiku ("restates_claim"), kept by Sonnet. Every combination fails: "kill if either kills" keeps 3 of 6 and 0 decoys; "kill if both kill" keeps 5 of 6 and 1 decoy; Sonnet alone 5 of 6 and 1 decoy. The rubric's "generic" and "restates" categories are the problem: the gold mechanisms ARE general principles, so a correct recovery reads as generic, and a mechanism that explains both notes reads as restating them. The binary critic is the wrong tool for this corpus. On a corpus where a survivor must be a specific, checkable claim, it might be the right tool; here it removes correct answers by construction.

## 7. H5 and shared priors

S0 recall by writer family: A 3 of 10, B 3 of 6; B4 recovery: A 5 of 10, B 3 of 6. The generator recovers Qwen-written notes at least as often as Haiku-written ones, so "recovery reflects shared Anthropic priors between writer and generator" is not supported. Two caveats that keep this from being a finding: the exclusion removed 6 of 12 Qwen bridges, so the surviving six are the ones a 7B model could write without stating the mechanism, a selected subset; and Qwen notes are shorter (median 107 versus 176 words), which concentrates cues. Say: no evidence that shared priors drive recovery; the test is confounded by exclusion and length.

## 8. Pipeline defects found in the raw outputs

- Four notes have zero concept cards: dc02-a, dc06-b, fl04, fl08 (all family B, short notes). They can never enter a card-pair arm, and note-level units that include them carry an empty claim list: S0-0021, S0-0041, S1-0015, S1-0024. Two of those returned an error ("CLAIM B is empty"). Fix: retry card extraction on zero-card notes and exclude such notes from S0 and S1 sampling.
- The match judge's false negative on S0-0000 (br01) is one in sixteen; a two-vote judge or a second model would have caught it. Report recall as 6 of 16 by the preregistered judge and note the case.
- T4 reports S1 NONE as 29 of 32 with 3 non-NONE; one of the three is the error above.

## 9. What the paper may say

Abstract, with the run's numbers, obeying the claim discipline:

"We plant 16 cross-domain connections, each written obliquely on both sides by one of two model families, in a 96-note synthetic corpus, and measure whether a generate-then-select pipeline recovers them. Given the right two notes, the generator produced an answer on 9 of 16 planted pairs and the grounded judge accepted 6 (Wilson 18 to 61 percent); it abstained on 10 of 12 shape-matched or homonym decoys and 34 of 36 random pairs, and no decoy answer survived the primary critic (Fisher p = 0.021). Pairing a bridge note with a mechanism-free filler from the partner domain produced 0 recoveries in 16 (p = 0.009), the preregistered H4, and the run reports SIGNAL by the preregistered rule. That rule was mis-specified: single-note reflection without permission to abstain recovered 8 of 16 mechanisms, including five the two-note oracle had marked NONE, so the planted mechanisms are recoverable from one note and recombination is not demonstrated. Near-in-embedding, far-in-domain sampling enriches planted card pairs 2.7-fold in its pool (0.99 versus 0.36 percent) but drew 2 planted pairs in 300 against 1.1 expected (p = 0.30). Recovery did not differ by writer family (3 of 10 Haiku-written, 3 of 6 Qwen-written), with the caveat that the exclusion rule removed 6 of 12 Qwen bridges. Both critics removed correct recoveries (3 of 6 and 1 of 6). Measured list-price cost of the run was $85.04. Synthetic ground truth measures recovery of planted structure, not real-world novelty or usefulness."

Two sentences the paper must place next to each other: "By the preregistered rule the run reports SIGNAL" and "the rule's recombination test was not a recombination test; the single-note arm shows the mechanisms are recoverable from one note". Reporting the first without the second would be the kind of result HindSight warns about.

Still not permitted: "novel", "discovers", "first", any lead time, any cost per idea beyond the measured run cost, any claim that distance-forced sampling helps.

## 10. The most informative next run under $30

B4-NONE plus a filler control, about $5: the single-note prompt with NONE permitted and the pair schema, over the 32 bridge notes and 24 fillers, same generator. Three outcomes, each decisive. If bridge-note recall stays near 8 of 16 and fillers are NONE, the mechanisms are one-note recoverable and the corpus cannot test recombination; v0.3 must be built differently. If recall collapses toward S0's level, the B4 result was forced-answer compliance and H3 can be re-tested fairly. If fillers also produce answers, the single-note arm measures nothing.

Then, and only then, v0.3's design rule: a bridge is accepted at build time only if the generator itself, given one side with NONE permitted, does not produce the gold (an unrecoverable-from-one-side gate using the actual generator, replacing the leak judge), and each side must hold a specific fact rather than a principle: one note carries a concrete fact, the other an unexplained observation that only that fact explains. The two bridges that behaved that way here, br09 and br17, are the template; they are also the two the pipeline missed, which is where the real difficulty lives.

Also fix before any run: zero-card notes, and a two-vote match judge.
