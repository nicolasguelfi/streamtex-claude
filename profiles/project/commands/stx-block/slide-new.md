Create a new slide (block file) for a StreamTeX presentation project.

Arguments: $ARGUMENTS (slide name and description, e.g. "bck_zoom - Zoom controls demo")

## Steps

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
   - Body text uses `s.large` (32pt)
   - No concatenated multi-string `st_write()` calls
   - Follows active design guideline principles (if guideline active)
   - `# @guideline: <name>` annotation present at top of file
8. **Show wiring**: Tell user how to add to `book.py` module list.

## Constraints
- Follow ALL rules from `.claude/designer/skills/visual-design-rules.md`
- No raw HTML/CSS strings
- Use `st_write()` + `st_br()` for multi-line text, not string concatenation
- Use `s.large` for all body text
