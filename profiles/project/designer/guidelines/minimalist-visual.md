# Design Guideline: Minimalist Visual

> **Scope**: This skill defines a graphical design philosophy for StreamTeX presentations.
> It is loaded by stx-block and stx-ce commands when the project or block references
> this guideline. It **complements** `slide-design-rules.md` and `visual-design-rules.md` —
> where a directive here conflicts with those base rules, **this file wins**.

---

## Philosophy

One idea, one image, maximum white space. The slide communicates through what
it DOESN'T show. Every element earns its place — if it doesn't serve the single
focal point, it's removed.

---

## Principles (ordered by priority)

### P1 — Single focal point per slide

Every slide has ONE thing the eye goes to first. Everything else is subordinate
or absent. Ask: "What is the ONE takeaway?" — that's the focal point.

### P2 — Images are the primary content carriers

Text supports images, not the reverse. If a concept can be conveyed by an
illustration, use the illustration and reduce text to a headline.
- Full-bleed images when possible
- Icons and diagrams over bullet lists
- High-quality, evocative images that convey the main idea

### P3 — Text is telegraphic

Keywords only. No full sentences on slides. The presenter provides the narrative.
- 3-7 words per bullet maximum
- 5 bullets maximum per list
- Headlines, not paragraphs
- Bold colored keywords for the ONE key term per bullet

### P4 — White space is intentional and generous

Empty space creates focus, calm, and visual hierarchy. Do NOT fill it.
- A slide with 30% content and 70% void is correct
- White space frames the focal point
- Margins and padding are design elements, not waste

---

## Application par type de contenu

### When the slide has 1-3 short text elements

- Center vertically and horizontally in viewport
- Use large fonts but NOT the maximum that fits — leave generous margins
- Title: `Huge` (80pt) to `huge` (64pt), centered
- Generous `st_space()` above and below — the void IS the design
- Goal: elegant simplicity, like a book title page

### When the slide has 4-7 bullets

- AVOID this archetype — prefer splitting into 2-3 slides with 2 bullets each
- If unavoidable: max 5 bullets, 7 words each
- Generous vertical spacing between bullets (more space than text height)
- Font: `Large` (48pt) for body — do NOT go smaller to fit more
- If it doesn't fit at 48pt, SPLIT the slide
- Goal: each bullet has room to breathe

### When the slide has a dominant image

- THIS is the preferred archetype for minimalist design
- Image takes 70-80% of slide area
- Full-bleed when possible (edge-to-edge, no padding)
- Title or short caption only — no body text
- Text overlaid on image (with contrast background) or below
- Goal: the image tells the story

### When the slide has text + image (balanced)

- Image always dominates: 60-70% image, 30-40% text
- Text column: 3 keywords max, large font, generous spacing
- Image column: full height, no borders, no frames
- Asymmetric layout preferred (not 50/50)
- Goal: image is the message, text is the label

### When the slide has a diagram/code

- Diagram: centered, 60-70% of viewport
- Generous white space around the diagram (frame it)
- Title only — no explanatory text on the slide
- Use the simplest possible diagram (fewer nodes, fewer connections)
- Goal: the diagram is instantly readable, not detailed

### When the slide is a transition

- Single question or statement, centered
- Font: `huge` (64pt) to `Huge` (80pt) — large but not screaming
- Accent color for emphasis
- Maximum white space around the text
- Goal: a pause, a breath, a moment to think

---

## Recommended PresentationProfile

```python
PresentationProfile(
    name="Presenter",
    mode=ViewMode.PAGINATED,
    layout=PageLayout(width=90, zoom=100),
    breaks=SlideBreakDisplayConfig(mode=SlideBreakMode.HIDDEN, space=0),
)
```

---

## Constraints (absolute — never violated)

- No font below 48pt for body text (projection readability + visual calm)
- No font below 80pt for headlines
- Maximum 5 bullets per list
- Maximum 7 words per bullet
- Maximum 1 emoji per slide (0 is preferred)
- One main idea per slide — if two ideas, split into two slides
- Dark theme assumed unless explicitly overridden
- 16:9 viewport ratio

---

## Anti-patterns (this guideline forbids)

- Walls of text (more than 5 lines of body text)
- Small font sizes to "fit everything" — split the slide instead
- Multiple competing focal points (image + diagram + text all fighting for attention)
- Decorative elements that don't serve the message
- Busy backgrounds or patterns
- Bullet points as the primary content format (prefer images)

---

## Interaction with base skills

- **slide-design-rules.md**: L1/L2/L3 grid applies, but L3 is often omitted
  (minimalist slides rarely need a transition question at the bottom).
  L2 often uses a single column (image only) rather than the default 2-column.
- **visual-design-rules.md**: Font size minimums are RAISED (48pt body, 80pt headline).
  Spacing rules are amplified — more generous than the defaults.
- **style-conventions.md**: Unchanged — composition rules still apply.

---

## Combinability

### Combines well with
- **`academic-structured`** — rigorous structure with minimalist presentation.
  Result: clean, structured slides with image-first approach and citation support.

### Conflicts with
- **`maximize-viewport`** — P4 (intentional white space) contradicts maximize P1 (fill viewport).
  If combined (`minimalist-visual + maximize-viewport`): minimalist P4 takes precedence
  → result is minimalist with slightly larger fonts from maximize influence.
- **`dense-informative`** — directly contradicts P3 (telegraphic text) and P4 (white space).
  Combination not recommended.
