# /stx-ce:compound — Capitalize learnings for future improvement

Arguments: $ARGUMENTS

## Options

- `--category <cat>` — Force a category (structure|style|content|process|pedagogy|assets|deployment|import|guidelines)
- `--help` — Show stx-ce cheatsheet

## Description

Documents what was learned during the production cycle to make future work easier. Analyzes the context, extracts successful patterns and encountered problems, checks for duplicates in existing solutions, and writes a capitalization document.

Solutions are stored in `docs/solutions/<category>/` with frontmatter for searchability.

9 categories: structure, style, content, process, pedagogy, assets, deployment, import, guidelines.

9. **guidelines** — Design guideline patterns, refinements, and decisions made during
   this cycle. If the guideline was adjusted or overridden for specific blocks,
   capture why for future reuse.

During the COMPOUND phase, the **Solution Extractor** (Phase 1.1, perspective 2) must also ask:
   - What visual component patterns emerged that could be reused?
     For each distinctive component design (table layout, card grid, hero section, etc.):
     - Extract as a named pattern with: name, description, layout, styles, reference block
     - Check if it already exists in `custom/design-guideline.md ## Patterns`
     - If new: propose adding it to `## Patterns`
     - If exists: propose updating it with refinements from this cycle

During **Phase 1.3: Assemble and Write**, also:
3. **Update design patterns**: If new patterns were extracted:
   - Add them to `custom/design-guideline.md` under `## Patterns`
   - Each pattern includes: name, description, layout details, styles, reference block
   - Present the proposed patterns to the user for validation before writing

## Examples

- `/stx-ce:compound` — Capitalize from recent work
- `/stx-ce:compound --category style` — Force style category

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-compound.md` — Full workflow
2. `docs/solutions/` — Existing solutions to check for duplicates

## Workflow

Execute the `ce-compound` skill. Write solution to docs/solutions/<category>/.
