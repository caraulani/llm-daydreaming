<!-- prompt: generate_single_strict | version: 1 | role: one-side gate for corpus building (ADR-014), and the strict single-note control | model: sonnet-class -->
STRICT SINGLE-NOTE TASK. You will see the content of ONE note from a person's private working
notes. Most notes carry no non-obvious implication, and the correct answer for most notes is
exactly `NONE`.

Output `NONE` (and nothing else) if any of these holds:
- The implication would be a general principle a careful reader already knows (for example
  regression to the mean, a sampling interval that is longer than the event, anchoring, a
  device change producing a step in a series). Naming a known principle is not an implication.
- The implication restates or lightly rephrases what the note already says.
- The implication needs information that is not in this note.
- The implication is generic enough to follow from almost any note.

Only if the note, on its own, contains a specific, non-obvious, checkable implication that the
owner has not written down, output one JSON object and nothing else:
{"connection": "<at most 40 words: the implication>",
 "mechanism": "<why it follows from THIS note's specifics, concretely>",
 "testable_implication": "<one concrete thing the owner could check or do this week>",
 "needs": "<what in the note supplies it>"}

NOTE:
{{claim}}
