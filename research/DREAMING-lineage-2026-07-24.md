# DREAMING — the "LLM dreams over context to form novel connections" idea (researched 2026-07-24)

Julian's concept: take accumulated session/memory context, let the model hallucinate/recombine on
it (like dreams recombining memories) to form connections that wouldn't otherwise form, discard the
useless, keep the novel. Two fanned research passes (AI-dreaming/memory line + computational-
creativity line). Verdict: **the concept is textbook, but the full mechanism is unbuilt in peer-
reviewed form, and the selection/distance half is genuine open ground.**

## The precise academic name for the idea
**Combinational creativity (Boden) realized as Blind-Variation-Selective-Retention (Campbell/
Simonton) over a flat associative hierarchy of remote associations (Mednick).**
- **Boden 1990/1998** — combinational / exploratory / transformational creativity. Yours =
  *combinational* (novel combos of familiar ideas), definitionally.
- **Campbell 1960 (BVSR)** — creativity = generate variations blindly + selectively retain the
  good. This IS "hallucinate widely, then prune." Simonton is its modern formalizer.
- **Mednick 1962** — creativity = forming *remote* associations; "flat associative hierarchies"
  reach distant concepts. This is your "random associations between concepts," from 1962.
- **Conceptual blending** (Fauconnier & Turner 1998/2002; computationally: Goguen, COINVENT,
  Confalonieri 2018) — the mechanism *under* recombination. Historically hard to implement for lack
  of math — the gap LLMs now fill.
- LLM-era term already in circulation: **"combinatorial creativity"** (arXiv:2412.14141).

## The dream-specific full mechanism — who states it
- **Gwern, "LLM Daydreaming" (gwern.net/ai-daydreaming, Jul 2025)** — states YOUR whole loop
  verbatim: a background Day-Dreaming Loop, generator explores non-obvious concept-pair links, critic
  filters for novelty, survivors written back and compound. Frames LLMs as lacking a "default mode
  network." **NOT peer-reviewed (essay). The complete idea is articulated but unbuilt.**

## Peer-reviewed / credible-lab pieces (each implements a SUBSET)
- **Sleep-time Compute** — Letta + UC Berkeley, arXiv:2504.13171 (2025). The exact "model does
  offline compute on its context while idle" ENGINE. Dual-agent: live agent + background sleep agent
  reprocessing/reorganizing memory in downtime. Emphasis = precompute/consolidate, NOT novelty+critic.
- **Generative Agents' reflection** — Park et al., arXiv:2304.03442 (2023). Periodically synthesizes
  stored memories into higher-level insights fed back to memory. The synthesis half; no random
  recombination, no discard step.
- **Cooking Up Creativity** — arXiv:2504.20643 (2025, TACL). Structured recombination for novelty
  via "creative leaps." Recombination half, no offline loop.
- **LLMs can Realize Combinatorial Creativity** — arXiv:2412.14141 (2024). Closest single paper to
  the framing: implements Boden's combinational creativity in an LLM with cross-domain retrieval to
  force *distant* combos + structured recombination.
- **A-Mem** — arXiv:2502.12110 (2025). Zettelkasten-style: dynamically links memories into a network
  → "connections that wouldn't otherwise form."
- Vocabulary roots: **Wake-Sleep** (Hinton 1995, literal sleep phase generates fantasies),
  **World Models / Dreamer** (Ha-Schmidhuber; Hafner, "training in dreams") — representation/control,
  not conceptual recombination. **DeepDream** (2015) = feature viz, unrelated.
- Memory-as-sleep-replay: **Deep Generative Replay** (Shin et al., NeurIPS 2017) + 2024-25 brain-
  inspired continual-learning line (arXiv 2504.14727, 2509.00047).

## Empirical LLM-idea-generation (your loop, already partly built)
- **"Can LLMs Generate Novel Research Ideas?"** — Si, Yang, Hashimoto (Stanford), arXiv:2409.04109
  (2024). 100+ researchers: **LLM ideas judged MORE novel than experts', weaker on feasibility.**
  Also documents a **diversity ceiling** (models recycle ideas). The key evidence the generate step works.
- **SciMON** (2305.14259), **ResearchAgent** (2404.07738), **The AI Scientist / v2** (2408.06292,
  2504.08066) — all = over-generate → novelty-check + LLM-critic filter → (some) run experiments.
- **Hallucination-as-feature line**: survey arXiv:2402.06647; "Shakespearean Sparks" 2503.02851;
  "Does Less Hallucination Mean Less Creativity?" 2512.11509 (reducing hallucination suppresses
  divergent creativity — direct evidence for the tradeoff). CAUTION: Peeperkorn 2405.00492 —
  "temperature is a RISK parameter, not a creativity parameter" (cranking randomness ≠ novelty).
- Analogy roots: **Copycat** (Hofstadter & Mitchell 1994/95) — generate-associations-then-filter
  with a literal temperature knob; the purest historical prototype of the whole loop.

## THE WHITE SPACE (honest — this is where a contribution lives)
DON'T pitch "recombine + filter" as a new theory — it's the single most-worked idea in
computational creativity (1960→2024); the exact experts you want to impress will dismiss an
over-claim (see BRAND.md AI-slop/over-claiming warning). The genuinely OPEN problems:
1. **The FILTER is the bottleneck, not the generator.** Every system generates plenty of "novel"
   candidates but can't reliably separate good-novel from merely-weird (feasibility lags novelty).
   A better convergent/selection stage = real white space.
2. **Forcing genuinely DISTANT combinations.** Diversity ceiling (Si et al.); sampling isn't truly
   blind (Gabora arXiv:1409.2210); temperature ≠ novelty (Peeperkorn). Mechanisms guaranteeing
   *conceptual distance* are underexplored.
3. **Blind vs. guided variation is unsettled** (Campbell vs. Gabora) — live theoretical dispute.
4. **Novelty evaluation itself is immature** — ad-hoc LLM/embedding checks; a principled novelty
   filter is open ground.
5. **Julian's specific angle**: the continuous *background loop over accumulated session/memory
   context* (Gwern's DDL) has NO peer-reviewed, evaluated implementation. Building it = first working
   version of an essay-only idea.

## The keystone opportunity (ties to BRAND.md)
This is a candidate for THE named, buildable, publishable artifact. A defensible project:
- Implement the day-dreaming loop over Claude Code session/memory context (the substrate already
  exists in ~/.claude memory + transcripts).
- Contribution NOT "the idea" but: a **distance-forcing generator** (cross-domain retrieval) + a
  **principled novelty+usefulness critic**, evaluated ("does it produce ideas humans rate novel AND
  useful above a baseline / above raw temperature sampling?").
- Name it. Open-source with the eval. Clean citation lineage: Gwern DDL, Sleep-time Compute,
  Generative Agents, Boden/Campbell/Mednick, Si et al.
- Venue: EMNLP Industry/workshop or an ICCC (computational creativity) track. This is the "artifact
  chain" keystone from BRAND.md, made concrete.

## BUILD PLAN — what it takes to build + open-source (2026-07-24)

### The system (~a weekend for MVP; Python + Claude API + embedding model; loop is a few hundred lines)
1. **Corpus** it dreams over = accumulated context as a concept store. Natural source: `~/.claude`
   memory files + session transcripts (or any KB). Extract concepts/claims/entities, embed them.
   A few thousand nodes is plenty.
2. **Distance-forcing sampler (CONTRIBUTION #1).** Do NOT sample randomly, do NOT just crank
   temperature (temperature = risk param, not creativity param — Peeperkorn). Pick concept pairs/
   triples that are FAR in embedding space but have a plausible bridge. Controlled conceptual
   distance is the real novelty lever.
3. **Generator (the "dream").** Prompt Claude for a non-obvious connection/idea between the distant
   concepts. Generate many, cheaply, in a background idle loop (sleep-time-compute style).
4. **Critic / selective retention (CONTRIBUTION #2, the real bottleneck).** Multi-dimensional, not
   one "is this good?" call: novelty (embedding distance to whole corpus + prior survivors, so it's
   genuinely new not reworded) × usefulness/feasibility (rubric) × coherence gate (kills distance-
   forced garbage). The joint novelty-AND-useful frontier is where the field is stuck.
5. **Memory writeback + lineage.** Survivors compound and recombine across runs — closes the loop.

### The eval (this IS the paper; ~80% of the work)
Question: does the loop produce ideas humans rate novel AND useful, above baselines?
Baselines to beat, in priority: (1) raw high-temperature sampling ← beating this is THE headline
result; (2) reflection-style synthesis (Generative Agents); (3) random-pair (no distance control).
Human panel rates novelty + usefulness (small 3-5 rater study + LLM-judge validated against them).
Metrics: joint novelty×usefulness, diversity (escape the recycling ceiling?), survival rate. The
rated idea-set is itself a citable dataset artifact. Research risk = LLM-judges noisy on novelty;
a defensible novelty metric is part of the contribution.

### Effort (honest)
MVP that dreams + prints survivors: a weekend. Publishable version: ~3-5 focused weeks, ~80% eval +
writeup not code.

### Open-source + publish path (= the BRAND.md keystone, concrete)
Name it (short/greppable) → clean repo (reference impl + one-command demo + eval harness + results
table + rated-idea dataset) → canonical human-written blog post on own domain → HF Papers submit →
6-8pg paper → **ICCC (International Conference on Computational Creativity, natural home, friendlier
bar than NeurIPS)** or an EMNLP/NeurIPS creativity workshop. Citation lineage reviewers want: Gwern
DDL (the unbuilt proposal being realized), Sleep-time Compute (engine), Generative Agents
(reflection), Boden/Campbell/Mednick (theory), Si et al. (empirical anchor). Claim = NOT the idea
but the first working, evaluated, distance-controlled implementation with a principled critic, run
over real memory. That's the artifact chain: named method → runnable code → benchmark → paper.

### Recommended entry point
Build the weekend MVP first — dream over THIS session's memory + transcripts, eyeball the survivors.
If they make you go "huh, interesting" → the eval weeks are worth it. If mush → learned cheap, iterate
the critic. Proposed home: `~/Desktop/I/dreaming/` (extractor · distance-sampler · dream generator ·
first-pass critic, pointed at ~/.claude memory as the corpus).

## PRIOR-ART SCAN — is it already BUILT? (2026-07-24) → NO mature/evaluated version exists
- **sgoedecke/idea-mill** — closest built attempt; real public repo of Gwern's loop, but author
  calls it "pretty half-assed", semi-manual (hand-curated facts in YAML b/c model wouldn't generate
  them reliably), DID produce "a few genuinely novel ideas", est. needs ~30% more work. NO rigorous
  eval, no baselines. A blog prototype.
- **davidrd123/latent-dreamer** — 0 stars; implements Mueller's 1990 DAYDREAMER architecture, NOT
  Gwern's loop; cross-session accumulation "not proven yet"; tests architectural correctness, no
  novelty metrics.
- **RogueCtrl/OpenClawDreams** — OpenClaw plugin, nightly "dream cycle" / surreal narrative memory
  toy; not a novelty-gen-with-eval system.
- Academic cousins (Deep Ideation, SPARK, SciMON, AI Scientist) = generator→critic idea loops over
  SCIENTIFIC LITERATURE, not the "dream over accumulated personal/session memory" angle, none framed
  as the DDL.
VERDICT: the exact scoped artifact (distance-forcing generator + principled novelty+usefulness
critic + run over accumulated memory + real eval beating raw-temperature/reflection baselines +
named + open-sourced) DOES NOT EXIST. Ideal prior-art situation: validated-enough (idea-mill got
real ideas) but nobody did it rigorously → clear citable gap + low bar (beat "half-assed").

## ORDER-OF-MAGNITUDE PLAN (2026-07-24) — beyond the competent version
Competent version (fill gap, workshop paper) = linear. OOM = become the REFERENCE POINT. Four levers:
1. **Own a VERIFIABLE eval → become the benchmark.** Dream over a TIME-FROZEN corpus (pre-2025
   only), then measure how many dreamed connections were independently discovered/published in
   2025-26. Objective ground truth for novelty+value (no hand-wavy LLM judge panels). Headline
   number: "dreamed 400 connections, 23 later found independently, raw sampling got 3." The harness
   = THE benchmark for idea-generation → everyone who measures against it cites you (highest-
   citation act in ML per BRAND research).
2. **Ship a DAEMON, not a demo.** Background process pointed at any corpus (Obsidian vault,
   codebase, Zotero, Claude Code memory) that dreams overnight → morning connections. Two starving
   audiences: PKM/Obsidian crowd (dead-notes pain) + agent-memory ecosystem (Letta/Mem0/A-Mem all
   consolidate, none GENERATE). Adoption by a Letta-class framework = upstream dependency
   (llama.cpp lesson: dependency is the deepest citation).
3. **One undeniable dream.** Run until it produces ONE connection that leads to something
   verifiably real (finding/feature/bug), tell it with receipts + logs ("dreamed on date X").
   The AI-Scientist moment.
4. **Compounding curve over months.** Long-horizon run showing survivors seed better dreams —
   nobody has shown this; cheap (runs while sleeping); difference between technique and system.
Unfair advantages: distribution machine already built (LOOPS/X per BRAND.md); Gwern reliably links
serious implementations of his proposals → day-one reach. Cost answer to Gwern's "daydreaming tax":
cheap-model generator + expensive-model judge cascade (itself a publishable efficiency result).
Formula: verifiable eval (benchmark) + daemon (dependency) + one real hit (story) + compounding
curve (moat) × existing distribution = own the category.
