# Exploratory runs

Nothing in this directory is preregistered. Every config states the date it was written and
whether the sealed run's results had been read at that time. Exploratory results are reported
in the paper under a separate heading, never merged into tables T1 to T6, and never used to
change the sealed decision rule.

| Run | Question | Written | Sealed results read? |
|---|---|---|---|
| X1_partner_control | does the gold mechanism appear when the partner note is replaced by a mechanism-free filler from the same domain? | 2026-09-13 | no |
| X2_generator_haiku | does selection quality track generator size (smaller)? | 2026-09-13 | no |
| X2_generator_opus | does selection quality track generator size (larger)? | 2026-09-13 | no |
| X3_cross_domain_near | does sampling near-in-embedding, far-in-domain pairs (B7) enrich planted pairs and recall where far-band sampling cannot? | 2026-09-13 | sampled units and embeddings only; no generation output |
| X4_critic_ablation | is the critic's recall loss a model-size effect? Same generations, critic alias sonnet | 2026-09-13 | yes (sealed results read) |
