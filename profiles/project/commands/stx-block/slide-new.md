Create a new slide (block file) for a StreamTeX presentation project.

Arguments: $ARGUMENTS (slide name and description, e.g. "bck_zoom - Zoom controls demo")

## Authoring gate (MANDATORY before authoring content)

When this command authors real slide **content** (not just an empty scaffold),
run the **`authoring-gate`** skill first
(`.claude/shared/skills/authoring-gate.md`). It enforces the trinity — plan +
design rules/agent (here the `presentation` overlay → `slide-designer`) +
component resolution — then delegates authoring. The steps below are the
scaffolding mechanics the gate relies on; do not bypass it to write content
freehand.

## Steps

### Step 0 — Read pattern catalog (MANDATORY)

Before generating any slide code, read
``stx component list` (reuse-architecture skill)` if it exists.
This lists the available named patterns in the project.

If the user **named a pattern** explicitly in their request (e.g.
"use stat_hero", "like grid_boston"):
- Read the full `<patterns-dir>/<name>.md` file.
- Respect strictly the INVARIANTS section.
- Adjust within PARAMS only.
- Refuse anything matching INTERDITS; propose creating a new pattern
  with `/stx-component:new` instead.

If the user did NOT name a pattern but the request matches one in the
catalog, mention it as an option ("This looks like the `stat_hero`
pattern — apply it?") before proceeding.

The pattern's code skeleton is a **starting point** — adapt it to the
project's `custom/styles.py` and palette, not a copy-paste.

1. **Load rules**: Read `.claude/designer/skills/visual-design-rules.md` for the full design ruleset.
2. **Read style conventions**: Read `.claude/designer/skills/style-conventions.md`.
3. **Load guideline**: If `custom/design-guideline.md` exists, read it and load the referenced
   guideline from `.claude/designer/guidelines/`. Check for `@guideline` annotations in
   the target block file if it already exists.
4. **Load patterns**: Check `custom/design-guideline.md` for a `## Patterns` section.
   If the user's request matches a named pattern (e.g., "create a table like table-roadmap"),
   load the pattern and use it as the blueprint for the component.
5. **Parse arguments**: Extract block name (must follow `bck_description` format — semantic name, no numbered prefix).
5. **Determine target project**: Use current working directory or ask the user.
6. **Create the block file** in `[project]/blocks/` with:
   - Standard imports including `from blocks.helpers import show_code, show_explanation, show_details`
   - `BlockStyles` class with `heading` and `sub` styles
   - `bs = BlockStyles` alias
   - `build()` function wrapping all content in `with st_block(s.center_txt):`
   - Main heading with `tag=t.div, toc_lvl="1"`
   - Each subsection following the canonical structure:
     - `st_write(bs.sub, ..., toc_lvl="+1")` + `st_space("v", 1)`
     - `show_explanation("""\...""")`  + `st_space("v", 1)`
     - `show_code("""\...""")` + `st_space("v", 1)`
     - Live rendering + `st_space("v", 2)`
     - Optional `show_details("""\...""")` with defaults
   - Classify the slide content → match to the guideline's applicable archetype
   - Apply archetype-specific directives for font sizing, layout, and spacing
7. **Validate**:
   - No line of visible text exceeds ~45 characters
   - Every live rendering has a preceding `show_code()`
   - All multi-line text blocks use `"""\..."""`
   - Body text uses `s.text_base` (palier 7) — or the deck's `ScaleConfig(base_pt_desktop=X)` if non-default audience
   - No concatenated multi-string `st_write()` calls
   - Follows active design guideline principles (if guideline active)
   - `# @guideline: <name>` annotation present at top of file
8. **Show wiring**: Tell user how to add to `book.py` module list.

## Constraints
- Follow ALL rules from `.claude/designer/skills/visual-design-rules.md`
- No raw HTML/CSS strings
- Use `st_write()` + `st_br()` for multi-line text, not string concatenation
- Use `s.text_base` (indexed scale) for all body text — legacy `s.large` remains valid on existing decks
