<!-- prompt: leak_judge | version: 1 | role: single-note paraphrase-leak judge | model: haiku-class -->
You will see ONE note from a person's working notes, and a hidden connection that this note is
supposed to carry only HALF of. The other half lives in a different note you cannot see.

Decide whether this note, read on its own, already states or directly implies the connection.
It counts as a leak if a careful reader of this note alone could write down the mechanism or
the recommended check without needing the other note. Restating the observations is not a leak.
Naming the cause, the diagnosis, the general rule, or the fix is a leak, in any wording.

Output one JSON object and nothing else:
{"verdict": "LEAK|CLEAN", "evidence": "one sentence quoting or pointing to the part of the note that decides it"}

NOTE:
{{note_text}}

HIDDEN CONNECTION (must not be inferable from this note alone):
connection: {{gold_connection}}
implication: {{gold_implication}}
