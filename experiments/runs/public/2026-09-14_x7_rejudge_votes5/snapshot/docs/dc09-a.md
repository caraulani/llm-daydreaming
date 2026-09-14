Calibration Set 4 Bias Test

## Setup
- Built a test set with 47 judge samples, all pre-scored as 4 (neutral, mid-scale)
- Running against three LLM evaluation frameworks: Claude API scorer, custom heuristic, and fine-tuned model
- Hypothesis: judges will cluster near 4 due to anchoring, regardless of actual content quality

## Observations
- Claude API scorer: mean 3.8, std 0.6, centered hard at 4 (23 of 47 returned exactly 4)
- Heuristic model: mean 4.1, std 1.1, more spread but still modal at 4
- Fine-tuned: mean 3.9, std 0.7 (training data had natural distribution)
- All judges show mode-shift toward 4 vs. baseline runs with mixed seed values

## Next Steps
- Randomize seed scores across 1-5 range in follow-up set to break the anchor
- Measure judge variance when no explicit prior given
- Compare to client gold labels (actual utility judgments, not synthetic)
- Document anchoring magnitude for next evaluation system proposal