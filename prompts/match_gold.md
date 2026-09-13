<!-- prompt: match_gold | version: 1 | role: grounded entailment judge against planted ground truth | model: haiku-class -->
You are checking whether a generated connection recovers a specific hidden mechanism.
You are given the GOLD mechanism (ground truth, written by a human before the experiment) and a
GENERATED connection. Answer whether the generated text expresses the same mechanism: the same
causal link between the same two ingredients, not merely the same topic or vocabulary.

Output one JSON object and nothing else:
{"match": true|false, "reason": "<at most 25 words>"}

Rules:
- `true` only if a reader who knew the GOLD would say the GENERATED text found it.
- Different wording is fine. A related but different mechanism is `false`.
- Mentioning both domains without the causal link is `false`.

GOLD connection: {{gold_connection}}
GOLD implication: {{gold_implication}}

GENERATED connection: {{connection}}
GENERATED mechanism: {{mechanism}}
GENERATED implication: {{testable_implication}}
