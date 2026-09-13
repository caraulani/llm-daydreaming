# Prior-art refresh, 2026-07-15 to 2026-09-13

*Produced 2026-09-13 by a literature-sweep agent (Claude Fable 5.1, fork of the founding session). Covers only the window after BRIEF v3 (2026-07-25). Reproduced verbatim.*

---

Task restated: prior-art refresh for mid-Jul to mid-Sep 2026, four gap checks, Gwern/Vault Daydream/zby status, name collisions.

# Prior-art refresh, 2026-07-15 → 2026-09-13

**Method note.** Web search + direct arXiv abstract fetches + GitHub/PyPI/npm/crates APIs + HN Algolia. The arXiv export API rate-limited then 503'd on every listing query, so the "new papers" list comes from search engines, not an exhaustive listing sweep. Treat "not found" as "not surfaced," not "does not exist."

## 1. What changed (new since the brief)

**Papers in-window or newly surfaced (not in BRIEF):**

- **Discovery by Dreaming: Cross-Domain Recombination in Artificial Memory** (arXiv:2607.16256, Zahn, Evans, Eagleman; v1 28 Jun 2026, v2 21 Jul 2026, CC BY 4.0). *The single biggest change.* Thesis: memory consolidation exists to drive cross-domain recombination, not to prevent forgetting. Two arms: DREAMS (LoRA fine-tune on LMSYS split coding/non-coding, +14.5 pp cross-domain transfer) and SAPIENCE (symbolic knowledge-object engine over 4,797 KOs / 3,532 papers in pharmacology, materials, neuro, cosmology; 85.7%, +21 pp). Validates against 50,000 OpenAlex cross-field pairs (35/37 historical bridges at 99.8th percentile) plus a **held-out 2026 OpenAlex window** (1,319 pairs at 95.6th percentile). Post-hoc: replay-surfaced bridges sit at greater embedding distance (ρ=0.54, n=32). **Not a temporal holdout by construction** (authors concede the evaluating LLM was pre-trained on the breakthroughs), **no distance control at selection, no critic/filter, no personal corpus, no Gwern citation.** Three credentialed authors (Evans = UChicago knowledge lab; Eagleman = Stanford neuro) now own "dreaming = cross-domain recombination" as a theoretical frame, and they have a falsifiable hippocampal prediction. Our Hoel-overfitted-brain framing is still separate from theirs, but "dreaming as recombination" is no longer white space.
- **Ideation Arena** (arXiv:2608.29696, Chen et al., 30 Aug 2026). 6,000+ double-blind pairwise comparisons from 105 CS researchers over 14 LLMs × 5 agent scaffolds; releases **Ideation Arena Eval** and a **public leaderboard** (github.com/foss12138/Research-Ideation-Arena, pushed 30 Aug, 2★). LLM judges align with expert preference only 72.56%. Scaffolds vary wildly, some underperform their base model. Human-preference, not temporal validation.
- **AgentIdeaBench** (arXiv:2609.07611, Mo, Zheng et al., HKUST-KnowComp, 7 Sep 2026). 33 LLMs × 40 subfields, static-observation vs active-exploration settings; "literature-verified" critics score originality against retrieved prior art. Code at github.com/HKUST-KnowComp/AgentIdeaBench. No leaderboard stated, no temporal holdout, no personal corpus.
- **On the Limits of LLM-as-Judge for Scientific Novelty Assessment** (arXiv:2606.12071, Sinhahajari, Majumder, Poria, 10 Jun 2026). RQ-Bench. LLM judges systematically rate model-generated research questions as highly novel ("novelty mirage"); experts prefer author-anchored questions. Direct reinforcement of HindSight ρ=−0.29 and the forced "judge is not an opinion" design change.
- **RINoBench** (arXiv:2603.10303, Schopf & Färber, 11 Mar 2026). 1,381 expert-judged ideas, 9 automated novelty metrics; reasoning aligns with human rationales but "does not reliably translate into accurate novelty judgments." Pre-window but absent from BRIEF; it is the closest existing "novelty-judgment benchmark" and must be cited when we claim ours.
- **Auto-Dreamer** (arXiv:2605.20616, Ye … McAuley, You, 20 May 2026). Learned offline consolidation (fast per-session acquisition, slow cross-session consolidation), 7 pts on ScienceWorld at 12× less memory. Consolidation, not divergent generation. Pre-window, missing from BRIEF.
- **SCM: Sleep-Consolidated Memory** (arXiv:2604.20943, Shinde, 22 Apr 2026). NREM/REM stages, forgetting; no novelty evaluation. Minor, cite in the "consolidation is commoditized" list.

**Products / repos in-window:**
- OpenClaw 2.0 (v2026.8.1, 30 Aug) shipped; its "Dreaming" (Light/REM/Deep sleep → MEMORY.md) is still consolidation-only.
- OpenDream (pylit-ai/opendream, Show HN 11 Jun, 7★, Apache-2) explicitly defines dreaming as "background memory review and cleanup, not an opaque model behavior." Consolidation, no novelty eval.
- Wienerdog (Show HN 1 Aug 2026, "memory and self-improving skills for Claude Code/Codex"): skills/memory, not ideation.
- Anthropic Auto Dream / Dreams: no new announcements found Aug–Sep; still research-preview consolidation (dedupe, contradiction resolution, date normalisation).
- `dreamd` on crates.io (botzrDev/dreamd, created 8 May 2026, v0.0.0): "Portable memory layer for AI coding agents." Same neighbourhood, name collision.

**Net:** the consolidation crowd got bigger (Auto-Dreamer, SCM, OpenClaw 2.0, OpenDream, Wienerdog); nobody in it filters for novelty or validates against later discovery. The generation/eval crowd got two new benchmarks (Ideation Arena, AgentIdeaBench) and one more judge-is-unreliable result (RQ-Bench). One credentialed paper (2607.16256) planted a flag on "dreaming = cross-domain recombination in memory."

## 2. The four gap checks

| Gap | Status | Nearest claimant |
|---|---|---|
| (a) private corpus × temporal validation join | **Still unclaimed.** | 2607.16256 does recombination × held-out-window validation, but over public OpenAlex/LMSYS, and the holdout is not leakage-safe. No paper found generating from a personal/private corpus. |
| (b) usable-idea yield (novelty × feasibility) vs semantic distance | **Still unclaimed.** | 2607.16256 reports only that surfaced bridges sit farther apart (ρ=0.54, n=32), post-hoc, no yield curve. 2604.20548 measures novelty/diversity by semantic distance but plots no product. |
| (c) runnable idea-novelty benchmark with leaderboard | **Now claimed, twice, for public-literature ideas.** | Ideation Arena (leaderboard live, human pairwise), RINoBench (expert labels, code+data), AgentIdeaBench (code). None uses temporal ground truth or a permutation null; HindSight remains the only time-split one and has no leaderboard. Our differentiator narrows to: **temporal + permutation-null + private-corpus** benchmark. "First idea-novelty leaderboard" is dead as a claim. |
| (d) held-out last-N-months of a personal corpus | **Still unclaimed.** Not found anywhere. | — |

## 3. Gwern / Vault Daydream / zby

- **gwern.net/ai-daydreaming**: created 2025-07-12, **modified 2025-07-14, unchanged.** Links only zby/DayDreamingDayDreaming, HN, Reddit, one X thread. No implementation linked. BRIEF's read holds.
- **glebis/claude-skills** (Vault Daydream): 376★ (was 329). 5 commits since 15 Jul, all on unrelated skills (cull-release, repo-publish, gpt-image-2, trail-checkin). **No Vault Daydream activity.**
- **zby/DayDreamingDayDreaming**: last push 2025-10-18, 4★, 0 commits since July. Dormant. (His substack "Reinventing Daydreaming Machines" is the citable statement of the two walls.)
- **shahgahmed/toy-llm-daydream**: Show HN 18 Jul 2025 (7 pts), 4★, one-day repo, dead. Add to the "prior toy implementations" footnote.

## 4. Threats to priority

1. **2607.16256 (Zahn/Evans/Eagleman)** owns "Discovery by Dreaming" as a phrase and "consolidation-for-recombination" as theory, with a 50k-paper validation. Reviewers will ask how we differ. Answer is already in BRIEF's structure: they have no critic, no distance control, no leakage-safe holdout, no private corpus, no human ground truth, and their own limitations section concedes memorization. Cite them in the first paragraph, not the related-work tail.
2. **Ideation Arena + AgentIdeaBench** occupy the "benchmark" slot for ideation in Sep 2026. Rename our artifact around the *temporal/permutation* property, not "novelty benchmark."
3. "Dream/dreaming" is now used by Google (2606.03979), Anthropic, OpenClaw, OpenDream, MemexAI, botzrDev/dreamd, and 2607.16256. The word is saturated; a distinctive name matters more than in July.

## 5. Naming availability (fetched 2026-09-13)

| Name | GitHub | PyPI | npm | crates.io | Verdict |
|---|---|---|---|---|---|
| **daydreamd** | user `daydreamD` exists (2013, 1 repo, dormant); 23 repos match substring, none relevant | **free** | **free** | **free** | Clean on all registries; only an idle username. Best of the set. |
| dreamd | 1,512 substring hits (NVIDIA/DreamDojo etc.) | free | free | **TAKEN** (botzrDev/dreamd, "memory layer for AI coding agents", May 2026) | Avoid: direct-neighbour collision. |
| nightshift | marcus/nightshift 1,014★ | TAKEN (2021 plotting lib) | free | TAKEN (renamed) | Avoid. |
| somnia | many | TAKEN ("modular AI agent CLI", May 2026) | TAKEN | TAKEN (SurrealDB ORM) | Avoid: AI-agent collision on PyPI. |
| remd | remdx 396★ etc. | free | TAKEN (react-markdown) | free | Weak. |
| incubate | 440 hits | TAKEN | free | free | Weak; also a generic verb. |
| hypnagogia | 25 minor hits (philpax 4★) | free | free | free | Fully free, but ungreppable/misspellable. |

## 6. Citations to add to the paper

1. Zahn, Evans, Eagleman. *Discovery by Dreaming: Cross-Domain Recombination in Artificial Memory.* arXiv:2607.16256 (2026). Intro + related work; the frame we must differentiate from.
2. Chen et al. *Ideation Arena.* arXiv:2608.29696 (2026). Benchmarks; 72.56% judge-expert alignment; scaffold variance.
3. Mo, Zheng et al. *AgentIdeaBench.* arXiv:2609.07611 (2026). Benchmarks.
4. Sinhahajari, Majumder, Poria. *On the Limits of LLM-as-Judge for Scientific Novelty Assessment.* arXiv:2606.12071 (2026). "Novelty mirage"; supports retrieval-grounded judging.
5. Schopf, Färber. *Is this Idea Novel? RINoBench.* arXiv:2603.10303 (2026). Novelty-judgment benchmark prior art.
6. Ye et al. *Auto-Dreamer.* arXiv:2605.20616 (2026), and Shinde, *SCM*, arXiv:2604.20943 (2026). Consolidation-is-commoditized list.

Out of scope but noticed: 2510.27313 ("LLM generation novelty through the lens of semantic similarity") is Oct 2025, not Aug 2026 as one search result claimed; verify before citing.
