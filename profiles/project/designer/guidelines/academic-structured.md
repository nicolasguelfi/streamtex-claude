# Design Guideline: Academic Structured

> **Scope**: This skill defines a graphical design philosophy for StreamTeX presentations
> in academic and educational contexts. It is loaded by stx-block and stx-ce commands
> when the project or block references this guideline. It **complements**
> `slide-design-rules.md` and `visual-design-rules.md` — where a directive here
> conflicts with those base rules, **this file wins**.

---

## Philosophy

Structured, rigorous, and pedagogically sound. Every slide advances the learner's
understanding through clear hierarchy, logical progression, and visual support.
Content density is moderate — enough information to be a useful reference,
not so much that it overwhelms during presentation.

---

## Principles (ordered by priority)

### P1 — Clear hierarchical structure

Every slide shows WHERE the audience is in the overall argument or curriculum.
- Consistent heading levels (section → subsection → point)
- Numbered sections when order matters
- Breadcrumb-like context (section title always visible or implied)

### P2 — Balance between text and visual

Neither pure text nor pure image — academic slides need both:
- Text provides precise definitions and terminology
- Diagrams/figures provide intuition and spatial understanding
- Aim for 40-60% text, 40-60% visual per content slide

### P3 — Terminology precision over brevity

Unlike minimalist, academic slides CAN use complete phrases when precision requires it.
- Technical terms in bold colored keywords (first occurrence)
- Short definitions are acceptable (1 sentence max)
- Acronyms defined on first use
- But still avoid paragraphs — use structured lists

### P4 — Progressive disclosure

Build complexity gradually across slides:
- Introduce concept → example → formal definition → application
- Each slide adds ONE new idea to the mental model
- Back-references to previous slides when building on established concepts

---

## Application par type de contenu

### When the slide has 1-3 short text elements

- Section title slide: clear heading + 1-2 line description of what follows
- Font: `huge` (64pt) for title, `Large` (48pt) for description
- Centered, with moderate white space
- Optional: section number or breadcrumb
- Goal: clear signposting

### When the slide has 4-7 bullets

- THIS is the bread-and-butter of academic slides
- Structured list with bold colored key terms
- Font: `Large` (48pt) for title, `large` (32pt) for body
- Numbered when order matters, bulleted when order doesn't
- Each bullet: key term + short explanation (up to 10 words acceptable)
- Goal: structured, scannable, referenceable

### When the slide has a dominant image

- Figure/diagram with caption and optional source citation
- Image: 60% of viewport
- Caption below: italicized, smaller font, includes source if applicable
- Title above: describes what the figure shows
- Goal: the figure supports the argument with clear labeling

### When the slide has text + image (balanced)

- Standard L1/L2 layout: title + 2-column grid
- Text column: structured list (3-5 items) with key terms
- Image column: labeled diagram or figure
- Both columns same visual weight
- Goal: concept (text) + illustration (image) side by side

### When the slide has a diagram/code

- Diagram or code block: 65-75% of viewport
- Title: what the diagram/code demonstrates
- Optional: 2-3 annotation callouts pointing to key parts
- Code: syntax-highlighted, line numbers, relevant lines highlighted
- Goal: the code/diagram is readable AND annotated

### When the slide is a transition

- Section transition: new section title + brief overview of upcoming content
- Font: `Huge` (80pt) for section title, `Large` (48pt) for overview
- 1-3 bullet overview of what's coming
- Goal: orient the audience, reset attention

---

## Recommended PresentationProfile

```python
PresentationProfile(
    name="Presenter",
    mode=ViewMode.PAGINATED,
    layout=PageLayout(width=90, zoom=90),
    breaks=SlideBreakDisplayConfig(mode=SlideBreakMode.HIDDEN, space=0),
)
```

---

## Constraints (absolute — never violated)

- No font below 24pt (body) — `s.big` minimum
- Preferred body font: 32pt (`s.large`)
- Maximum 7 bullets per list (5 preferred)
- Maximum 12 words per bullet (10 preferred)
- Every technical term bold-highlighted on first use
- Citations formatted consistently (author, year) or footnote style
- Dark theme assumed unless explicitly overridden
- 16:9 viewport ratio

---

## Anti-patterns (this guideline forbids)

- Paragraphs of text (use structured lists instead)
- Unlabeled diagrams or figures
- Jumping between topics without transition slides
- Code without syntax highlighting
- Slides with ONLY text and no visual element for 3+ consecutive slides
- Inconsistent heading styles across slides

---

## Interaction with base skills

- **slide-design-rules.md**: L1/L2/L3 grid is the standard. L3 (question/transition)
  is used for pedagogical questions ("What would happen if...?").
- **visual-design-rules.md**: Font sizes follow the standard hierarchy.
  Line length constraint (45 chars) is important for readability.
- **style-conventions.md**: Unchanged. Add citation-related styles to `custom/styles.py`
  (e.g., `citation`, `definition`, `theorem`).

---

## Combinability

### Combines well with
- **`maximize-viewport`** — structured content fills the viewport methodically.
  Result: academic rigor with no wasted space.
- **`minimalist-visual`** — clean structure with image-first approach.
  Result: elegant academic slides (fewer bullets, more figures).

### Conflicts with
- **`dense-informative`** — both are text-tolerant but differ on density.
  If combined: academic P4 (progressive disclosure) wins over dense's "pack everything".
  Result is structured but with more content per slide than academic alone.
