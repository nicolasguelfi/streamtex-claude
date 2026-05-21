Create a new StreamTeX block file.

Arguments: $ARGUMENTS (block name and optional description, e.g. "bck_intro_welcome - Welcome screen with title and subtitle")

## Authoring gate (MANDATORY before authoring content)

When this command authors real block **content** (not just an empty scaffold),
run the **`authoring-gate`** skill first
(`.claude/shared/skills/authoring-gate.md`). It enforces the trinity — plan +
design rules/agent for the document's `identity.type` + component resolution —
and delegates authoring to the right designer specialization (`slide-designer`
/ `web-document-designer` / `course-designer`). The steps below are the
scaffolding mechanics the gate relies on; do not bypass it to write content
freehand. (For a genuine one-off, the gate offers an "ad-hoc assumed" path.)

## Steps

### Step 0 — Read pattern catalog (MANDATORY)

Before generating any block code, read
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

1. **Load context**: Read `documentation/streamtex_cheatsheet_en.md` for syntax reference.
2. **Read architecture**: Read the target project's `book.py` to understand how blocks are wired. For reference, see `documentation/template_project/book.py` or `documentation/manuals/stx_manual_intro/book.py`.
3. **Check the component catalog**: Read `.claude/shared/skills/reuse-architecture.md` for the pack/component vocabulary, then run `stx component list --granularity block` to enumerate block-tier components available in installed packs (default: `streamtex_design`). If a component matches the requested block intent, import and call it from the new block file. Common matches:
   - "title slide" → `title_slide` (streamtex_design.components)
   - "comparison X vs Y" → `comparison_table`
   - "code demo / walkthrough" → `feature_walkthrough`
   - "steps / process / exercise" → `exercise_flow`
   - "summary / conclusion / takeaways" → `takeaways` or `narrative_transition`
   For unmatched intents, scaffold from scratch and consider `/stx-component:new` to capture the new component into the project's primary local pack.
3a. **Load guideline**: If `custom/design-guideline.md` exists in the target project,
    read it and load the referenced guideline from `.claude/designer/guidelines/`.
3b. **Load patterns**: Check `custom/design-guideline.md` for a `## Patterns` section.
    If the user's request matches a named pattern (e.g., "create a table like table-roadmap"),
    load the pattern and use it as the blueprint for the component.
4. **Parse arguments**: Extract the block name (must follow `bck_[description]_[suffix]` format). If only a description is given, generate an appropriate name.
5. **Determine target project**: Look at the current working directory or ask the user which project to use.
6. **Create the block file** in `[project]/blocks/` with:
   - Standard mandatory imports (streamtex, styles, enums, custom.styles)
   - Import helpers from `blocks.helpers` (show_code, show_explanation, show_details)
   - A `BlockStyles` class with relevant styles for the described content
   - A `build()` function implementing the described content using `stx.*` functions
   - Proper TOC entries if the block has headings
   - If a guideline is active, classify the block's content → match archetype
   - Apply archetype directives to BlockStyles composition and build() layout
   - Add `# @guideline: <name>` annotation at top of the new block file
7. **Update `blocks/__init__.py`**: Add the new module to the dynamic import list if it uses explicit imports (not needed with `ProjectBlockRegistry` lazy loader).
8. **Show wiring instructions**: Tell the user how to add the block to `book.py`:
   ```python
   import blocks
   # Add to the module list in st_book():
   st_book([..., blocks.bck_new_block_name], toc_config=toc)
   ```
9. **Validate**: Check that all referenced styles exist and all image URIs point to existing files.
   - Follows active design guideline (if present)

## Constraints
- Follow ALL rules from CLAUDE.md
- No raw HTML/CSS strings
- Use English-only style names
- Block must have a `build()` function
- Use `stx.*` functions, never raw `st.*` for content
