<!-- prompt: cards | version: 1 | role: concept-card extraction | model: haiku-class -->
You are extracting concept cards from one note written by a single person for their own use.

A concept card is one atomic, self-contained claim from the note. Extract between 3 and 6 cards.
Rules:
- Each `claim` is at most 30 words and must stand alone without the note.
- Each `why_it_matters` is at most 20 words.
- `entities` lists the specific named things the claim depends on (products, people, tools, places).
- `confidence` is `high` if the note states it as fact, `med` if implied, `low` if speculative.
- Do not invent anything absent from the note. Do not merge unrelated claims into one card.
- Skip secrets, credentials, and anything that looks like a key, password, or personal identifier.

Return a JSON array of concept cards and nothing else:
[{"claim": "...", "entities": ["..."], "why_it_matters": "...", "confidence": "high|med|low"}]

NOTE (id: {{note_id}}):
<<<
{{note_text}}
>>>
