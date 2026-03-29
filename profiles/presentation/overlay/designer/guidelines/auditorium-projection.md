# Design Guideline: Auditorium Projection

> **Scope**: This skill defines a graphical design philosophy optimized for
> **large room projection** (10-20m viewing distance, 50-200+ audience).
> It extends `maximize-viewport` with projection-specific constraints.
> Load this guideline for auditorium-scale presentations.

---

## Philosophy

Every element must be readable from the back row. Typography is XXL,
contrast is maximum, and visual noise is eliminated. The projector
is your enemy — it washes out colors and blurs fine details.

---

## Principles (ordered by priority)

### P1 — Readability at 20 meters

Font sizes are dramatically larger than screen-reading defaults.
- Minimum body text: 48pt (`s.Large`)
- Minimum headlines: 80pt (`s.Huge`)
- Preferred body: 64pt (`s.huge`) when content allows
- No fine details, thin lines, or small annotations

### P2 — Maximum contrast

Projectors reduce contrast. Compensate:
- Pure white text on dark backgrounds (not light gray)
- Accent colors must be vivid and saturated (no pastels)
- Avoid color pairs that wash out under projection (yellow on white, light blue on gray)
- Test: if you squint and it's still readable, contrast is sufficient

### P3 — Content fills the viewport (inherits from maximize-viewport)

Same as `maximize-viewport` P1 — no artificial void. But with the additional
constraint that LARGER fonts are always preferred, even if it means fewer
words per slide.

### P4 — Simplicity over density

When in doubt between "more information" and "bigger/clearer":
- Choose bigger/clearer — the audience can't pause or zoom
- One concept per slide, no exceptions
- Split aggressively — 3 simple slides > 1 dense slide

---

## Application par type de contenu

### Quand la slide a 1-3 éléments textuels courts

- Font: `giant` (128pt) minimum for 1-2 words, `Huge` (80pt) for a phrase
- Centered in full viewport (90vh container)
- High-contrast accent color for key words
- Goal: visible from 20 meters instantly

### Quand la slide a 4-7 bullets

- Maximum 4 bullets (not 7 — auditorium constraint)
- Font: `Large` (48pt) minimum, prefer `huge` (64pt)
- Maximum 5 words per bullet
- Generous spacing (justify-content: space-evenly)
- Bold colored keywords mandatory for each bullet
- Goal: scannable in 3 seconds from any seat

### Quand la slide a une image dominante

- Image: 80%+ of viewport
- Ensure image is high-resolution (projectors amplify pixelation)
- No small labels or annotations on the image
- Title as overlay with high-contrast background strip
- Goal: image visible and clear from back row

### Quand la slide a texte + image (balanced)

- Image: 60% minimum (larger than standard balanced)
- Text: 3 bullets maximum, `Large` (48pt) font
- High contrast between columns
- Goal: both elements readable at distance

### Quand la slide a un diagramme/code

- Diagram: simplified for projection — fewer nodes, thicker lines, larger labels
- Code: maximum 8 lines, `large` (32pt) minimum font, syntax highlighting with vivid colors
- Avoid detailed UML — prefer simplified block diagrams
- Goal: the diagram's message is clear without reading fine print

### Quand la slide est une transition

- Single phrase in `GIANT` (196pt) or `giant` (128pt)
- Vivid accent color
- Full viewport, centered
- Goal: impossible to miss

---

## Recommended PresentationProfile

```python
PresentationProfile(
    name="Auditorium",
    mode=ViewMode.PAGINATED,
    layout=PageLayout(width=100, zoom=80),
    breaks=SlideBreakDisplayConfig(mode=SlideBreakMode.HIDDEN, space=0),
)
```

---

## Constraints (absolute)

- No font below 48pt for body text (24pt is too small for projection)
- No font below 80pt for headlines
- Maximum 4 bullets per list
- Maximum 5 words per bullet
- No thin lines (< 2px) in diagrams
- No pastel or low-saturation colors
- No fine-print annotations or footnotes
- Dark theme mandatory
- 16:9 viewport ratio

---

## Anti-patterns

- Font sizes appropriate for screen reading (24-32pt) — too small for projection
- Subtle color differences to distinguish elements
- Detailed diagrams with small labels
- Code blocks with 15+ lines
- Dense tables with many columns
- Footnotes, source citations in small print (move to handout)

---

## Combinability

### Combines well with
- **`maximize-viewport`** — natural extension, auditorium adds projection constraints
- **`minimalist-visual`** — simple + large = perfect for auditoriums

### Conflicts with
- **`dense-informative`** — density is the enemy of projection readability
- **`academic-structured`** — academic detail levels are too fine for projection
  (use academic for handout mode, auditorium for presenter mode)
