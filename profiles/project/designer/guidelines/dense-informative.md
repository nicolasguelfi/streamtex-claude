# Design Guideline: Dense Informative

> **Scope**: This skill defines a graphical design philosophy for StreamTeX documents
> that prioritize information density. It is loaded by stx-block and stx-ce commands
> when the project or block references this guideline. It **complements**
> `slide-design-rules.md` and `visual-design-rules.md` — where a directive here
> conflicts with those base rules, **this file wins**.

---

## Philosophy

Maximum information per slide. Every slide is a self-contained reference card
that the audience can photograph and use later. Density is a feature, not a bug —
but density must be organized, not chaotic.

---

## Principles (ordered by priority)

### P1 — Maximize information density through structure

Pack more content by using better structure, not smaller fonts:
- Multi-column layouts (2 or 3 columns)
- Tables over prose
- Comparison grids (before/after, pros/cons)
- Side-by-side code examples
- Structured lists with sub-items

### P2 — Every slide is a self-contained reference

Each slide should be useful as a standalone screenshot:
- Title clearly states the topic
- All context needed to understand is on the slide
- No "as we saw earlier" references — repeat key info if needed
- Source/citation included when applicable

### P3 — Visual hierarchy through typography, not space

Differentiate elements through font size, weight, color, and alignment — not
through generous spacing:
- Tight but readable spacing
- Clear size hierarchy: title > subtitle > body > annotation
- Color-coded categories (e.g., green=good, red=bad, blue=info)
- Bold for emphasis, italic for definitions

### P4 — Code and diagrams are first-class content

Technical slides should show real code, real diagrams, real data:
- Code blocks with syntax highlighting and line numbers
- Diagrams with labels and annotations
- Tables with actual data, not placeholders
- Side-by-side comparisons (WRONG vs CORRECT)

---

## Application par type de contenu

### Quand la slide a 1-3 éléments textuels courts

- AVOID single-element slides — combine with related content from adjacent slides
- If unavoidable: use `Large` (48pt) font, add context (subtitle, annotation)
- Consider: is this slide necessary, or can it merge with the next?
- Goal: no "wasted" slide with little content

### Quand la slide a 4-7 bullets

- Standard density: use full L1/L2/L3 layout
- Font: `large` (32pt) for body, can go to `big` (24pt) for dense lists
- Sub-bullets allowed (2 levels max)
- Up to 7 bullets with sub-items
- Add a summary annotation or "key takeaway" in L3
- Goal: comprehensive but scannable

### Quand la slide a 8+ items

- ACCEPTABLE in this guideline (unlike others)
- Use 2-column layout to fit more items
- Font: `big` (24pt) minimum
- Group items into categories with colored headers
- Or use a table format instead of bullets
- Goal: reference card density

### Quand la slide a une image dominante

- Image: 50-60% of viewport (not 70-80% like other guidelines)
- Add annotations, labels, callouts ON the image or beside it
- Caption with technical details
- Goal: informative image, not decorative

### Quand la slide a texte + image (balanced)

- True 50/50 split
- Both columns dense with content
- Text: structured list with details
- Image: annotated diagram or data visualization
- Goal: maximum information in both columns

### Quand la slide a un diagramme/code

- Code can be longer (up to 15-20 lines with `big` 24pt font)
- Side-by-side WRONG/CORRECT patterns
- Multiple code blocks on one slide (with tabs or grid)
- Annotations pointing to key lines
- Goal: complete code examples, not snippets

### Quand la slide est une transition

- Keep transitions brief — don't waste a full slide
- Section title + 3-5 bullet overview of upcoming topics
- Or combine transition with first content of new section
- Goal: minimal interruption to information flow

---

## Recommended PresentationProfile

```python
PresentationProfile(
    name="Presenter",
    mode=ViewMode.PAGINATED,
    layout=PageLayout(width=100, zoom=80),
    breaks=SlideBreakDisplayConfig(mode=SlideBreakMode.HIDDEN, space=0),
)
```

---

## Constraints (absolute — never violated)

- No font below 24pt (`s.big`) — absolute minimum for projection
- Preferred body font: 24-32pt depending on content volume
- Maximum 3 nesting levels (title > item > sub-item)
- Tables: maximum 6 columns, readable cell content
- Code blocks: syntax highlighting mandatory, line numbers on
- Dark theme assumed unless explicitly overridden
- 16:9 viewport ratio

---

## Anti-patterns (this guideline forbids)

- Unstructured walls of text (dense ≠ messy)
- Slides with only 1-2 short elements (wasteful)
- Decorative images that don't convey information
- Large empty zones between content blocks
- Font sizes below 24pt (readability trumps density)
- Slides that require scrolling (still must fit 16:9)

---

## Interaction with base skills

- **slide-design-rules.md**: L1/L2/L3 grid applies. L2 may use 3 columns instead of 2
  for comparison slides. All 3 rows (L1+L2+L3) should be used on most slides.
- **visual-design-rules.md**: Font size minimums apply (24pt). Line length constraint
  (45 chars) may be relaxed to 55 chars for multi-column layouts.
- **style-conventions.md**: Unchanged. Consider adding comparison-related styles
  (e.g., `good_highlight`, `bad_highlight`, `info_highlight`) to `custom/styles.py`.

---

## Combinability

### Combines well with
- **`maximize-viewport`** — fill the viewport with dense structured content.
  Result: information-packed slides with no void.
- **`academic-structured`** — rigorous structure with high density.
  Result: detailed academic reference slides.

### Conflicts with
- **`minimalist-visual`** — directly contradicts P1 (maximize density) and minimalist P3/P4.
  Combination not recommended — the philosophies are fundamentally opposed.
