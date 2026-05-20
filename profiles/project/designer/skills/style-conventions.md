# Style Conventions for StreamTeX Slides

## Style Composition

- Use `+` to combine styles: `s.bold + s.large + s.text.colors.blue`
- Use `-` to remove styles: `combined - s.bold`
- Use `Style.create(composed, "style_id")` for themed styles.
- Use `ns("css-property: value;")` only for one-off inline styles.

## Style Storage (pack-first)

Reusable styles belong in a **pack**, not in `custom/styles.py`. The
legacy `custom/styles.py` mechanism is supported for backward
compatibility, but new projects should prefer the pack-first layout.

| Style scope | Location | Example |
|---|---|---|
| Used by 2+ blocks of THIS project | `./mypack/design_systems/default.py` + `./mypack/components/` | Color palette, project-wide CTA |
| Used by 1 block only | `BlockStyles` class inside the block file | Block-specific spacing variant |
| Used across multiple projects | Upstream pack (`streamtex-design` or domain pack) | `callout`, `comparison_table` |

Naming conventions:
- Use **English-only** names (no French, no abbreviations).
- Follow the existing naming pattern: `colors.primary_blue`, `containers.good_callout`.
- New projects: extend the pack's `design_systems/default.py` with project bundles.

See the `modular-design-philosophy` skill for the full decision tree.

## BlockStyles Class

- Define **only block-local** compositions in `BlockStyles`.
- Always include `heading` and `sub` for consistency.
- Use `bs = BlockStyles` alias for clean code.

## Project Style Hierarchy

```
s.project.colors.*       # Text colors (primary_blue, accent_teal, ...)
s.project.titles.*       # Pre-composed titles (course_title, section_title, ...)
s.project.containers.*   # Container styles (good_callout, bad_callout, code_box, ...)
```

## Theme Support

- NEVER hardcode `color: black` or `background-color: white`.
- Use `style_id` with `Style.create()` for styles that need dark mode overrides.
- Theme overrides go in `custom/themes.py`.

## Helper Functions

| Helper | Purpose | Used for |
|--------|---------|----------|
| `show_code(text)` | Syntax-highlighted code box | All code examples |
| `show_code_inline(text)` | Code without box wrapper | Inside callout containers |
| `show_explanation(text)` | Blue "Purpose" box | Before each example |
| `show_details(text)` | Amber "Details" box | Defaults, tips, after examples |

---

## Guidelines and Style Constraints

If the project follows a design guideline (`custom/design-guideline.md`), check whether
the guideline prescribes:

- **Color palette**: Mandatory colors to use in `custom/styles.py` project styles
- **Naming patterns**: Specific naming conventions for BlockStyles attributes
- **Container patterns**: Preferred CSS layout strategy (flex-viewport, natural, grid)
- **Font size ranges**: Minimum/maximum sizes that override the base defaults

Guideline-prescribed constraints override the defaults in this file.
When refactoring or creating styles, verify compliance with the active guideline.

The `@guideline` annotation system allows different guidelines per block or fragment.
See `.claude/designer/guidelines/_index.md` for details.

## Patterns interaction

When the project has a the active packs (see reuse-architecture skill) catalog, the patterns
encode the visual conventions. **Patterns must respect** the style
conventions of this skill — they don't override them. If a pattern's
code skeleton appears to deviate from these conventions, treat it as a
bug in the pattern (open an issue / propose a fix), not as a license to
break conventions.

In particular, the following conventions apply both to ad-hoc blocks
**and** to pattern code skeletons:

- Use `stx.*` for content rendering (no raw `st.*` for content).
- Use `Style` composition (`Style + Style`, `Style + string`) — no
  inline HTML/CSS.
- One `st_write()` with tuples for inline mixed-style text.
- No hardcoded black/white — let Streamlit handle themes.
- Block files declare a `BlockStyles` class + `build()` function.

When applying a pattern, **adapt** its code skeleton to use the
project's `custom/styles.py` palette — never copy-paste the skeleton
verbatim if the styles don't match the project.
