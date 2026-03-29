# Design Guidelines — Catalog & Conventions

> **Purpose**: Design guidelines are AI skills that define a graphical design philosophy
> for StreamTeX documents. They guide the AI's design decisions — font sizing, spacing,
> layout, image treatment — differently for each slide based on its content.
>
> Guidelines complement the base skills (`slide-design-rules.md`, `visual-design-rules.md`,
> `style-conventions.md`). Where a guideline conflicts with a base rule, **the guideline wins**.

---

## Available Built-in Guidelines

| Guideline | Philosophy | Best for |
|-----------|-----------|----------|
| [`maximize-viewport`](maximize-viewport.md) | Every pixel serves the content. No artificial void. | Auditorium presentations, data-heavy talks |
| [`minimalist-visual`](minimalist-visual.md) | One idea, one image, maximum white space. | Executive presentations, keynotes |
| [`academic-structured`](academic-structured.md) | Structured, rigorous, citation-rich. | University lectures, research talks |
| [`dense-informative`](dense-informative.md) | Maximum information per slide. | Technical workshops, reference material |

---

## How Guidelines Are Applied — Scoping

Guidelines follow a **CSS-like specificity model**: the most specific declaration wins.

### Level 1 — Project default (`custom/design-guideline.md`)

```markdown
# Design Guideline — My Project

guideline: maximize-viewport

## Overrides
- bck_title, bck_conclusion: minimalist-visual
- bck_exercises_*: dense-informative + maximize-viewport
```

This file is **free-form text** that Claude interprets. No rigid schema.

### Level 2 — Block-level annotation (comment at top of block file)

```python
"""Slide: Architecture Overview."""
# @guideline: minimize-viewport
```

### Level 3 — Fragment-level annotation (inline comment)

```python
# === L1 — Headline ===
# @guideline: minimalist-visual
st_write(bs.headline, "Architecture", tag=t.div)

# === L2 — Content ===
# @guideline: maximize-viewport + dense-informative
with st_grid(...) as g:
    ...
```

### Resolution order (most specific wins)

```
1. Inline @guideline annotation     → wins over everything
2. Block-level @guideline annotation → wins over project defaults
3. Override in design-guideline.md   → wins over project default
4. Default in design-guideline.md    → applies everywhere else
5. No guideline                      → base skills only
```

---

## Annotation Syntax

```python
# @guideline: <name>                     — apply this guideline here
# @guideline: <name1> + <name2>          — combine (name1 has priority)
# @guideline: <name> (scope description) — human-readable scope note
# @guideline: none                        — disable guidelines for this zone
```

---

## Combining Guidelines

When combining with `A + B`:

1. **Principles**: A's principles have priority. B's principles apply where they don't contradict A.
2. **Constraints**: The **stricter** constraint wins (e.g., min font = max of both minimums).
3. **Anti-patterns**: **Union** — anything forbidden by A or B is forbidden.
4. **Archetypes**: A's archetype directives apply first; B complements gaps.

Each builtin guideline documents its **combinability** — which others it pairs well with and which it conflicts with.

---

## How Commands Use Guidelines

### During production (`/stx-designer:*`, `/stx-ce:produce`)

1. Read `custom/design-guideline.md` for project default + overrides
2. Read block-level `@guideline` annotation (if present)
3. Resolve the effective guideline (specificity rules above)
4. Load the guideline file(s) from `.claude/designer/guidelines/`
5. Classify the content → find the applicable archetype section
6. Apply principles in priority order
7. Verify constraints

### During audit (`/stx-designer:audit`, `/stx-ce:review`)

1. Same resolution as above
2. For each block/fragment, verify conformance to its effective guideline
3. Report: which guideline applies, compliance status, violations

---

## Named Design Patterns

Projects can define **reusable design patterns** in `custom/design-guideline.md`
under a `## Patterns` section. A pattern is a named, concrete recipe for a
recurring visual component (table, card grid, timeline, hero section...).

### What a pattern contains

Each pattern has:
- A **name** (e.g., `table-roadmap`) — usable in prompts and `@pattern:` annotations
- A **description** of the visual layout, colors, fonts, spacing
- **StreamTeX implementation notes** — which styles, grid settings, cell_styles to use
- A **reference block** — pointing to a working implementation in the project

### Where patterns live

Patterns are defined in `custom/design-guideline.md` under `## Patterns`:

```markdown
## Patterns

### table-roadmap
A responsive 3-column table with bordered cells for schedules.
- Layout: `repeat(auto-fit, minmax(250px, 1fr))`, gap 12px
- Cell style: rounded border, semi-transparent background,
  `vertical_center_layout + center_txt`, padding 8px 12px
- Font: `s.Large` (48pt), bold for labels, `s.text.wrap.hyphens`
- Responsive: columns stack on narrow screens
- Reference: `bck_p1_roadmap.py`
```

### How to reference patterns

**In a prompt:**
> "Create a feature comparison table using the `table-roadmap` pattern"

**In a block annotation:**
```python
# @pattern: table-roadmap
```

**With modifications:**
> "Use `table-roadmap` but with 2 columns instead of 3"

### Resolution order

Patterns are resolved AFTER guidelines:
1. Resolve the active **guideline** (philosophy + principles)
2. Check for a **@pattern** annotation or prompt reference
3. Load the pattern from `custom/design-guideline.md ## Patterns`
4. Apply the pattern's concrete recipe within the guideline's constraints

### Guidelines vs Patterns

| Aspect | Guideline | Pattern |
|--------|-----------|---------|
| **What** | Philosophy + principles | Concrete component recipe |
| **Scope** | Whole document/block | One component type |
| **Example** | "fill the viewport, no void" | "3-col table with bordered cells" |
| **Named** | `@guideline: maximize-viewport` | `@pattern: table-roadmap` |
| **Location** | `.claude/designer/guidelines/` | `custom/design-guideline.md ## Patterns` |

---

## Creating a Custom Guideline

Users can create project-specific guidelines in `custom/design-guideline.md`
using `extends:` to build on a builtin:

```markdown
# Design Guideline — Corporate DLH

extends: maximize-viewport

## Additional Principles
- P5: All diagrams must use Mermaid (no PlantUML)
- P6: Corporate blue (#003399) for all titles

## Override: Transition slides
For transition slides, use minimalist-visual approach instead
of filling the viewport — single centered phrase.
```

Or create a standalone guideline as a `.md` file in `.claude/custom/references/`
following the structure of the builtins.
