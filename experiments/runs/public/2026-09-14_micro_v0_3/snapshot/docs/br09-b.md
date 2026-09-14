## Judge plateau above 12k tokens

Testing a client's LLM eval framework. Their judge model returns 3.5 consistently on every criterion when content exceeds about 12k tokens. Rationale field is empty in those rows. No explanatory text, which makes the eval framework unusable. Can't debug what's actually being scored.

## Test observations

Ran batches of document reviews, some running 35-40k tokens for the full material. Hit the 3.5 plateau consistently on longer items. The empty rationale is the killer: zero signal about what's being assessed. These consistent 3.5 responses yield no debugging info. Blocks progress on client work.

## Next

Isolate the exact boundary. Check logs for what happens when material gets substantial. Empty justifications break the framework entirely. Planning shorter batches to test boundary behavior and whether anything changes in the model's output. Need to figure out if it's architectural or configurable.