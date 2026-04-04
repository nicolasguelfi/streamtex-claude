# Design Guideline: Maximize Viewport

> **Scope**: This skill defines a graphical design philosophy for StreamTeX presentations.
> It is loaded by stx-block and stx-ce commands when the project or block references
> this guideline. It **complements** `slide-design-rules.md` and `visual-design-rules.md` —
> where a directive here conflicts with those base rules, **this file wins**.

---

## Philosophy

Every pixel serves the content. No artificial void. The slide breathes through
rhythm between elements, not through emptiness. If space is visible, the content
isn't big enough.

---

## Principles (ordered by priority)

### P1 — Content expands to fill the viewport

Typography is the primary space-filling lever. Adjust font size FIRST.
- Few words → giant fonts, centered in full viewport
- Many words → smaller fonts but distributed to fill the full vertical space
- NEVER leave the bottom 30% of a slide empty
- Flex containers with `justify-content: space-between` or `space-evenly` to distribute

### P2 — One clear visual hierarchy per slide

Every slide has exactly one dominant element (title, image, key phrase).
Supporting elements are clearly subordinate — at least 1.5x size difference
between dominant and secondary elements. The dominant element anchors the layout.

### P3 — Images fill their allocated zone completely

No thumbnail floating in space. Images use full width or height of their area.
- `object-fit: cover` preferred over `contain`
- If an image is present, it anchors the layout — minimum 50% of its zone
- No letterboxing, no pillarboxing

### P4 — All content is centered by default

In a presentation, all elements are horizontally centered unless explicitly left-aligned.

**Implementation**: Wrap ALL slide content in `st_block(s.center_txt)` as the outermost
container inside the page-fill block. This ensures text, images, and all inline elements
are centered without needing per-element centering.

```python
with st_block(_page_fill):
    with st_block(s.center_txt):       # ← ALL content centered
        st_write(bs.heading, "Title")
        st_image(s.none, uri="...", width="80%")
        st_write(bs.body, "Description")
```

**Never** rely on `s.center_txt` on individual `st_write` styles alone — it applies to
the `<span>` tag, which may not center within Streamlit's wrappers. Always use the
**container** approach.

### P5 — Spacing serves rhythm, not fill

Gaps between elements create visual rhythm (like music beats).
- Equal-sized gaps = monotone → vary gap sizes to create emphasis
- Larger gap before important element, smaller gap after
- NEVER use large gaps to fill empty space — that's P1's job (bigger fonts)

---

## Application par type de contenu

### Quand la slide a 1-3 éléments textuels courts

- Container: `display:flex; flex-direction:column; justify-content:center; min-height:85vh;`
- Font: largest size that fits without line wrapping
- Minimum title size: `giant` (128pt) for 1-2 words, `Huge` (80pt) for a short phrase
- Vertical distribution: centered with generous gap between elements
- Goal: the text IS the slide, nothing else competes

### Quand la slide a 4-7 bullets

- Container: `display:flex; flex-direction:column; justify-content:space-between; min-height:85vh;`
- Title: occupies 20-25% of vertical space
- Body: fills remaining 75-80%, bullets evenly distributed
- Font: largest size where no bullet wraps to 2 lines (typically `Large` 48pt → `large` 32pt)
- Equal vertical spacing between bullets — no clustering
- Goal: the list fills the viewport edge to edge vertically

### Quand la slide a une image dominante

- Image: 70-80% of viewport area
- Text: title or caption only, fills remaining space with large font
- Image sizing: `width:100%` or `height:80vh`, whichever fills more
- Layout: image top + text bottom, or image left (65%) + text right (35%)
- **Centering**: Always wrap `st_image()` in `st_block(s.center_txt)` to center it.
  Never pass centering styles directly to `st_image()` — they apply to the `<img>` tag,
  not to its container, so `text-align:center` has no effect on the image itself.
- Goal: image IS the slide, text is a label

### Quand la slide a texte + image (balanced)

- Two columns via `st_grid`, each fills its space completely
- Text column: font sized to fill, bullets evenly distributed vertically
- Image column: `object-fit:cover`, full height of the column
- No gap larger than 24px between columns
- Goal: no visible void in either column

### Quand la slide a un diagramme/code

- Diagram/code: 75-80% of viewport, centered
- Title: compact, above, no more than 15% of viewport height
- Font size of diagram: fill available space (use `font_size` parameter if available)
- No body text competing with diagram — title + diagram only
- Goal: diagram readable from back row of auditorium

### Quand la slide est une transition

- Single phrase or question, centered in full viewport (`min-height:85vh`)
- Font: `giant` (128pt) or `GIANT` (196pt) — as large as possible
- Accent color acceptable for emphasis
- No other elements on the slide
- Goal: the phrase hits like a billboard

---

## Recommended book.py Configuration

```python
# Slide breaks: minimal space, hidden separators
set_slide_break_config(SlideBreakConfig(
    mode=SlideBreakMode.HIDDEN,
    space="5vh",
))

# Presentation profile
PresentationProfile(
    name="Presenter",
    mode=ViewMode.PAGINATED,
    layout=PageLayout(width=100, zoom=80),
    breaks=SlideBreakDisplayConfig(mode=SlideBreakMode.HIDDEN, space=0),
)
```

---

## Standard Slide Template

Every slide MUST follow this structure:

```python
# Viewport-filling + centered container
_page_fill = ns(
    "display:flex;flex-direction:column;justify-content:center;"
    "align-items:center;min-height:85vh;gap:1.5rem;",
    "page_fill",
)

def build():
    with st_block(_page_fill):
        with st_block(s.center_txt):       # ← ALL content centered
            st_write(bs.heading, "Title", tag=t.div, toc_lvl="1")
            # ... all content here is centered by default
```

**Two mandatory wrappers**:
1. `st_block(_page_fill)` — fills the viewport, centers vertically
2. `st_block(s.center_txt)` — centers all content horizontally

---

## Icon and Logo Sizing

Small icons and logos (institution logos, social icons, tech badges) must use
**viewport-relative sizing** for consistent display across screen sizes:

- Icons/logos in grids: `width="5vw"` (5% of viewport width)
- Small inline icons: `width="3vw"`
- Medium logos (standalone): `width="10vw"`
- Never use pixel sizes for icons in presentations — they don't scale

---

## Constraints (absolute — never violated)

- No font below 24pt (projection readability)
- No unintentional line wrapping — every text element fits on its intended line count
- No visible empty space greater than 15% of viewport height at slide bottom
- Dark theme assumed unless explicitly overridden
- 16:9 viewport ratio
- Per-block `BlockStyles` — font sizes are calibrated per slide, not global
- All content centered by default (P4)
- Icons/logos sized in `vw` units, never pixels

---

## Named Patterns

Reusable visual recipes that follow maximize-viewport principles. Reference these by name in block annotations: `# @pattern: spectrum-bar`.

### Pattern: spectrum-bar

Horizontal gradient bar visualizing a continuum (0%↔100%, Never↔Always, Low↔High).

**Layout**: Full-width block with a gradient `<div>`, labels at extremes.

**Implementation**:
```python
_gradient = ns(
    "background: linear-gradient(90deg, rgba(108,154,239,0.8) 0%, rgba(255,181,71,0.8) 100%);"
    "border-radius: 12px; padding: 16px 24px; display: flex; justify-content: space-between;",
    "spectrum_bar"
)
with st_block(_gradient):
    st_write(s.bold + s.Large, "Never")
    st_write(s.bold + s.Large, "Always")
```

**Rules**: Gradient colors derived from project palette. Labels in bold contrasting color. Minimum height 48px. Border-radius 12px.

### Pattern: exercise-flow

3-phase structure for training exercises: briefing → timer → debrief.

**Layout**: 3 consecutive sections separated by `st_slide_break()`.

**Implementation**:
```python
# Phase 1 — Briefing
st_write(bs.headline, "Exercise: Design a Pipeline", toc_lvl="1")
st_write(bs.body, "Instructions...")
with st_list("ol") as l:
    with l.item(): st_write(bs.body, "Step 1...")
    with l.item(): st_write(bs.body, "Step 2...")

st_slide_break()

# Phase 2 — Timer
st_write(s.Giant + s.bold + s.center_txt, "15:00")
st_write(s.Large + s.center_txt, "Time remaining")

st_slide_break()

# Phase 3 — Debrief
st_write(bs.headline, "Debrief", toc_lvl="2")
st_write(bs.body, "Discussion questions...")
```

**Rules**: Briefing phase uses structured list. Timer phase uses Giant font centered. Debrief phase uses open questions. Each phase fills the viewport independently.

### Pattern: stat-hero

Giant statistic with supporting context — classic keynote pattern for memorable data points.

**Layout**: Centered number (Giant/GIANT) + subtitle below.

**Implementation**:
```python
st_write(s.GIANT + s.bold + s.center_txt + s.project.colors.highlight, "73%")
st_write(s.Large + s.center_txt, "of developers use AI coding assistants daily")
st_write(s.large + s.center_txt + s.project.colors.muted, "Source: Stack Overflow Survey 2025")
```

**Rules**: Statistic in GIANT or Giant (96-196pt). Highlight color from palette. Supporting text max 2 lines. Source in muted color. The number must be the dominant visual element (>50% of viewport attention).

---

## Anti-patterns (this guideline forbids)

- Small text centered in large void
- Thumbnail image (< 50% of its allocated zone)
- Uniform spacing between all elements (monotone rhythm)
- Same font size on every slide regardless of content volume
- Wide margins "to let it breathe" — breathing comes from rhythm, not emptiness
- `st_space()` used as filler between sections
- Left-aligned content in presentation slides (center is default)
- `st_image(s.center_txt, ...)` — centering style on `<img>` has no effect
- Pixel-sized icons (`width="75px"`) — use `vw` units instead
- Large slide break spacing in paginated mode (use `5vh` max)

---

## Interaction with base skills

- **slide-design-rules.md**: The L1/L2/L3 grid remains the structural skeleton.
  This guideline IMPOSES that each zone L is visually filled — no zone left sparse.
- **visual-design-rules.md**: Readability constraints (45 chars/line, min font sizes) apply,
  but this guideline pushes toward LARGER fonts than the minimums.
- **style-conventions.md**: Unchanged — BlockStyles compose project styles, never raw CSS.

---

## Combinability

### Combines well with
- **`dense-informative`** — fonts fill space AND maximize information density.
  Result: large fonts + many bullets = visually packed slide.
- **`academic-structured`** — structured content fills space methodically.
  Result: rigorous structure with no wasted viewport.

### Conflicts with
- **`minimalist-visual`** — P1 (fill viewport) contradicts minimalist P4 (intentional white space).
  If combined (`maximize-viewport + minimalist-visual`): P1 takes precedence → result is closer
  to maximize-viewport but with image-first content approach from minimalist.
