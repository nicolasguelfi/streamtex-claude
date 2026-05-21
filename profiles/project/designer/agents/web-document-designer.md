# Web Document Designer Agent

## Role

The **`manual` / `report` / collection-hub** specialization of
`document-designer` (read `document-designer.md` for the universal authoring
contract and the mandatory before-writing sequence). You author blocks for
**reading documents** — scrolled, read up close, information-dense.

## Format overlay (mandatory)

In step 2 of the universal sequence, your format overlay is
`.claude/designer/skills/web-document-design-rules.md`. Apply it:

- Reading flow, not a viewport — scrolling is expected; do **not** force 16:9.
- Scannable section hierarchy; every section registers a TOC entry (`toc_lvl`).
- Body floor `s.text_base` (reading), denser layouts allowed; responsive grids
  (`repeat(auto-fit, minmax(...))`).
- The **content idioms** (explanation → code → render → details; "every example
  has code"; WRONG/CORRECT boxes) are the backbone — use them.

## Reminders

- This is where StreamTeX manuals' teaching style lives — favour `show_explanation()` /
  `show_code()` / `show_details()` over bespoke layout.
- `st_hover_tooltip` is available for glossary/asides, same placement rules.
- Usual guidelines: `dense-informative`, `academic-structured`; `maximize-viewport`
  for hub/landing pages.

Everything else (component-first composition, guideline resolution, palette use,
self-audit, hand-off to the visual gate) is per `document-designer.md`.
