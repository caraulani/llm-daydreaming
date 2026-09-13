<!-- prompt: synth_note | version: 2 | role: synthetic corpus note writer | model: haiku-class -->
Write one working note in the voice of this person:
{{persona}}

The note is about: {{topic}}
Domain: {{domain_label}}

Format: YAML frontmatter (`---`, `name`, `description`, `type: project`, `---`), then a short
title line, then 2 to 4 short sections with `##` headers, mostly bullet facts. 150 to 300 words.
Terse working memory, concrete details, dates and numbers where natural. No essay tone.

{{ingredients_block}}
Hard rules:
- Never mention these words or topics: {{forbidden}}
- Do not explain why anything happens beyond what is listed. Do not draw lessons or generalise.
- Do not mention any other area of this person's life.
- No em dashes anywhere; use commas, colons or full stops.
- Output the note only, starting with `---`.
