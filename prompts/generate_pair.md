<!-- prompt: generate_pair | version: 1 | role: generator, pair arms (B1, B3, B6) | model: sonnet-class -->
You will see two claims taken from one person's private notes.

Most pairs are unrelated. If no genuine, non-obvious connection exists between them, output
exactly `NONE` and nothing else.

Otherwise output one JSON object and nothing else:
{"connection": "<at most 40 words: the non-obvious link>",
 "mechanism": "<why the link holds, concretely>",
 "testable_implication": "<one concrete thing the note owner could check or do this week>",
 "needs": "<which claim supplies what: 'A supplies ..., B supplies ...'>"}

Rules:
- Do not restate either claim.
- Do not invent facts absent from the two claims.
- A connection that would apply to almost any two claims (both involve people, both involve
  software) is not a connection. Output `NONE` instead.

CLAIM A: {{claim_a}}
CLAIM B: {{claim_b}}
