<!-- prompt: generate_single | version: 1 | role: generator, reflection control (B4) | model: sonnet-class -->
You will see one claim taken from a person's private notes.

State one implication of this claim that the note owner has not written down. If the claim has
no non-obvious implication, output exactly `NONE` and nothing else.

Otherwise output one JSON object and nothing else:
{"connection": "<at most 40 words: the implication>",
 "mechanism": "<why it follows, concretely>",
 "testable_implication": "<one concrete thing the note owner could check or do this week>",
 "needs": "<what the claim supplies>"}

Rules:
- Do not restate the claim.
- Do not invent facts absent from the claim.
- A generic implication that would follow from almost any claim is not an implication. Output
  `NONE` instead.

CLAIM: {{claim}}
