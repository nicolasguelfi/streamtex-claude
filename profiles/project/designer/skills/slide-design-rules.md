# Slide Design Rules — StreamTeX Presentations

> **Scope**: This skill defines the default design rules for StreamTeX presentation slides.
> It is the primary reference for the `slide-designer` agent and `/stx-block:update` command (add slide).
> It **extends** `visual-design-rules.md` and `style-conventions.md` — where a rule here
> conflicts with those base files, **this file wins**.

---

## Rule 1 — Viewport Constraint (16:9)

Every slide MUST fit entirely on a **16:9 screen** without scrolling.

| Constraint | Value |
|---|---|
| Aspect ratio | 16:9 |
| Max content height | ~90vh (leave margins for Streamlit chrome) |
| Overflow | NEVER — if content overflows, split into multiple slides |

**Technical implementation**: Use `PresentationConfig(enforce_ratio=True)` in `book.py`
to enforce the 16:9 aspect ratio constraint programmatically. This ensures the viewport
is locked to the correct proportions in fullscreen mode.

**Implication**: content density must be low. Prefer fewer elements with larger fonts
over cramming information. When in doubt, **split the slide**.

---

## Rule 2 — Standard Grid Layout (L1 / L2 / L3)

Every slide uses a **3-row grid** structure. Each slide may use 1, 2, or all 3 rows.

```
┌─────────────────────────────────────────┐
│              L1 — Full width            │  Message / citation / hook
│           (centered H & V)              │
├───────────────────┬─────────────────────┤
│     L2C1 (50%)    │     L2C2 (50%)      │  Image + Text (or Text + Image)
│  (centered H & V) │  (centered H & V)   │
├───────────────────┴─────────────────────┤
│              L3 — Full width            │  Question / transition / teaser
│           (centered H & V)              │
└─────────────────────────────────────────┘
```

### Row Roles

| Row | Role | Usage |
|---|---|---|
| **L1** | Headline / citation / hook | Puts forward a key message, quote, or provocative statement |
| **L2** | Main content (2 columns) | One cell = image/diagram, other cell = main text (list) |
| **L3** | Question / transition | Raises a point, a question, or prepares the next slide |

### Column Roles in L2

| Cell | Content type |
|---|---|
| Image cell | Diagram, schema, photo, chart, or placeholder |
| Text cell | Main information as **numbered or bulleted list** |

The image cell and text cell positions are interchangeable (left/right) depending on
visual flow. Alternate sides across slides for visual variety.

### StreamTeX Implementation

```python
def build():
    with st_block(s.center_txt):
        # === L1 — Headline ===
        st_write(bs.headline, "Key Message Here", tag=t.div)
        st_space(size=2)

        # === L2 — Two-column content ===
        with st_grid(
            cols="repeat(auto-fit, minmax(350px, 1fr))",
            gap="24px",
        ) as g:
            with g.cell():
                # Image cell
                st_image(uri="static/images/slide_topic.png", width="100%")
            with g.cell():
                # Text cell — bulleted list
                with st_list(
                    l_style=bs.body, li_style=bs.body,
                    list_type=lt.unordered,
                ) as l:
                    with l.item(): st_write(bs.body, "Key point 1")
                    with l.item(): st_write(bs.body, "Key point 2")
                    with l.item(): st_write(bs.body, "Key point 3")
        st_space(size=2)

        # === L3 — Question / transition ===
        st_write(bs.question, "What does this mean for...?", tag=t.div)
```

### Partial Grid Usage

Not every slide needs all 3 rows:

| Slide type | Rows used | Example |
|---|---|---|
| Title slide | L1 only | Course title + subtitle + author |
| Content slide | L1 + L2 | Headline + image/text grid |
| Full slide | L1 + L2 + L3 | Headline + content + transition question |
| Question slide | L1 + L3 | Provocative statement + follow-up question |

---

## Rule 3 — Responsive Reorganization

Grids MUST use responsive CSS for narrow screens. The L2 two-column layout
must stack vertically below the breakpoint.

### Responsive Stacking Order

On narrow screens, L2 reorganizes as:

```
L1
L2C1 (image cell — always first when stacking)
L2C2 (text cell)
L3
```

### Implementation

Always use `repeat(auto-fit, minmax(...))` instead of fixed `cols=2`:

```python
# CORRECT — responsive
with st_grid(cols="repeat(auto-fit, minmax(350px, 1fr))", gap="24px") as g:
    ...

# WRONG — fixed columns, never wraps
with st_grid(cols=2) as g:
    ...
```

If the project defines responsive presets in `custom/styles.py`, prefer those:
```python
with st_grid(cols=s.project.containers.responsive_2col, gap="24px") as g:
    ...
```

---

## Rule 4 — Text Style: Telegraphic / Keywords

All slide text MUST be **short, telegraphic, keyword-driven**.

| Constraint | Limit |
|---|---|
| Words per bullet | 3–7 max |
| Bullets per list | 3–5 max |
| Sentence style | Keywords / telegraphic — NO full sentences |

### WRONG
```python
st_write(bs.body, "The containerization technology allows developers "
    "to package applications with their dependencies.")
```

### CORRECT
```python
with st_list(l_style=bs.body, li_style=bs.body, list_type=lt.unordered) as l:
    with l.item(): st_write(bs.body, "Package apps + dependencies")
    with l.item(): st_write(bs.body, "Isolated environments")
    with l.item(): st_write(bs.body, "Portable across platforms")
```

### Bold Colored Keywords

Use **targeted bold colored keywords** to draw attention to the most important terms.
Do NOT overuse — max 1-2 highlighted words per bullet.

```python
with l.item():
    st_write(bs.body,
        (bs.keyword, "Isolation"), " — one process per container",
    )
```

Where `bs.keyword` is defined as:
```python
keyword = s.bold + s.project.colors.accent
```

---

## Rule 5 — Font Size Hierarchy

| Element | Min size | StreamTeX style | Notes |
|---|---|---|---|
| Slide title (L1) | 48pt | `s.Large` or `s.huge` | Depends on text length |
| Body text (L2) | 24pt | `s.big` minimum | Default target: `s.large` (32pt) |
| List items | 24pt | `s.big` minimum | Prefer `s.large` (32pt) |
| Question (L3) | 24pt | `s.big + s.italic` | Stylized for transition |
| Keywords emphasis | same as body | `s.bold + s.project.colors.accent` | Same size, colored + bold |

> **Minimum absolute**: 24pt (`s.big`). In rare cases with dense content, 18pt is acceptable
> but should be avoided. If content requires 18pt, consider **splitting the slide**.

> **Preferred default**: 32pt (`s.large`) for body text when space allows.

---

## Rule 6 — Dark Theme by Default

All slides use a **dark theme** unless the user explicitly requests otherwise.

### Implications

- NEVER hardcode `color: black`, `color: #000`, `background-color: white`
- Use theme-aware styles from `custom/styles.py`
- Use `Style.create(composed, "style_id")` for styles needing dark/light overrides
- Background colors should use dark palette (e.g., `#1a1a2e`, `#16213e`, `#0f3460`)
- Text colors should be light (e.g., `#e0e0e0`, `#ffffff`, accent colors)

### Default Dark Palette (when no project palette exists)

```python
# In custom/styles.py — dark theme defaults
class DarkTheme:
    bg_primary = ns("background-color: #1a1a2e;", "dark_bg_primary")
    bg_secondary = ns("background-color: #16213e;", "dark_bg_secondary")
    bg_accent = ns("background-color: #0f3460;", "dark_bg_accent")
    text_primary = ns("color: #e8e8e8;", "dark_text_primary")
    text_accent = ns("color: #00d4ff;", "dark_text_accent")
    text_highlight = ns("color: #e94560;", "dark_text_highlight")
    text_muted = ns("color: #8892b0;", "dark_text_muted")
```

---

## Rule 7 — Image Handling & Placeholders

### Image centering (MANDATORY)

To center an image horizontally, wrap `st_image()` in `st_block(s.center_txt)`:

```python
# CORRECT — center via container
with st_block(s.center_txt):
    st_image(s.none, width="80%", editable=True, name="hero", prompt="...")

# WRONG — style on st_image applies to <img> tag, not its container
st_image(s.center_txt, width="80%", ...)  # text-align has no effect on <img>
```

**Why**: `st_image()` renders an `<img>` tag. CSS `text-align: center` only works
on a **container**, not on the element itself. The `style` parameter of `st_image()`
applies to the `<img>` tag directly, so centering styles are ignored.
Always use the **parent container** (`st_block`) for positioning.

### When user provides images

Place them in `static/images/` with a clear naming convention:
```
static/images/bck_description.png
```
Example: `static/images/bck_architecture_overview.png`

### When NO image is provided

The designer MUST:

1. **Insert a placeholder** image in the layout:
```python
with g.cell():
    # PLACEHOLDER — replace with generated image
    st_write(
        bs.placeholder,
        "[Image: description of ideal visual]",
        tag=t.div,
    )
```

2. **Propose an image generation prompt** as a Python comment below the placeholder:
```python
    # IMAGE PROMPT: "Clean flat vector illustration of [concept],
    #   dark background (#1a1a2e), accent color (#00d4ff),
    #   minimalist style, no text, 16:9 aspect ratio"
    # SUGGESTED FILENAME: static/images/bck_concept_name.png
```

> **AI alternative**: If `AIImageConfig` is configured in `book.py`, replace the placeholder
> with `st_ai_image("prompt...")` to generate and display the image directly.
> For batch workflows, use `generate_image("prompt...", provider="openai")` to save to disk,
> then reference with `st_image(uri=path)`. See `streamtex_cheatsheet_en.md` Section 8.

3. **Naming convention** for suggested filenames:
```
static/images/bck_{short_description}.{ext}
```
Where:
- `short_description` = 2-3 words, snake_case, matching the block name
- `ext` = `png` (preferred) or `svg`

> **Important**: Do NOT use numbered prefixes (`bck_01_`, `bck_02_`, ...).
> Numbered names are not maintainable — inserting a block between two existing ones
> forces renaming all subsequent files. Use descriptive names only; ordering is
> defined in `book.py`.

---

## Rule 8 — Block Composition & Slide Breaks

### One block per logical section

Each block file (`bck_description.py`) represents one logical unit.
If a block contains multiple sections that work as independent slides,
use `st_slide_break()` to separate them.

### Recommended slide break config for presentations

For fullscreen presentations, use `SlideBreakConfig(fullscreen=True)` to enable
viewport-height slide separation optimized for presentation mode:

```python
set_slide_break_config(SlideBreakConfig(fullscreen=True, mode=SlideBreakMode.HIDDEN, marker=True))
```

### Slide break naming

```python
st_slide_break(marker_label="concept_overview")
# ... next slide content ...
st_slide_break(marker_label="concept_details")
```

Label names should be:
- **Descriptive** of the slide content
- **snake_case**
- **Unique** within the block

### Block file naming

```
bck_title.py
bck_introduction.py
bck_concept_overview.py
bck_architecture.py
bck_conclusion.py
```

> Use descriptive names without numeric prefixes. Block ordering is controlled
> by the `st_book([...])` list in `book.py`, not by filenames.

---

## Rule 9 — Modularity & Style Reuse

### Project-level styles are the rule

- ALL reusable styles MUST be defined in `custom/styles.py`
- Block-local `BlockStyles` only composes project styles, never creates raw CSS
- Color palette, font sizes, container styles → project level
- Only unique per-block compositions → `BlockStyles`

### Style naming convention

```python
# custom/styles.py
class Styles:
    class project:
        class colors:
            primary = ...     # Main brand color
            accent = ...      # Secondary highlight
            muted = ...       # Low-emphasis text
            highlight = ...   # Call-to-action emphasis

        class titles:
            slide_title = ...      # L1 headline
            section_title = ...    # Major section
            section_subtitle = ... # Sub-section

        class containers:
            responsive_2col = ... # Grid preset
            card = ...            # Content card
            quote_box = ...       # Citation container

        class slide:
            headline = ...    # L1 style
            body = ...        # L2 text style
            question = ...    # L3 transition style
            keyword = ...     # Bold + accent for emphasis
            placeholder = ... # Placeholder image style
```

### BlockStyles pattern

```python
class BlockStyles:
    """Slide: Topic Name."""
    headline = s.project.slide.headline
    body = s.project.slide.body
    keyword = s.project.slide.keyword
    question = s.project.slide.question
    # Block-specific compositions only:
    special_emphasis = s.project.colors.highlight + s.bold + s.Large
bs = BlockStyles
```

---

## Rule 10 — Emoji Usage

Use emojis **sparingly and purposefully**. They are acceptable as visual markers
but must not replace meaningful content.

| Usage | Acceptable |
|---|---|
| Section icon (1 per title) | Yes — e.g., heading with a single icon |
| Bullet decoration | Sparingly — max 1 per list, not every bullet |
| Inline emphasis | No — use bold colored keywords instead |
| Multiple emojis in one line | Never |

### WRONG
```python
st_write(bs.body, "🚀 🎯 💡 Key innovation in the field! 🔥")
```

### CORRECT
```python
st_write(bs.headline, "Key Innovation")
# or with a single purposeful icon:
st_write(bs.headline, "Key Innovation 🎯")
```

---

## Rule 11 — Slide Self-Audit Checklist

Before completing any slide, verify:

- [ ] Fits on 16:9 screen without scrolling
- [ ] Uses L1/L2/L3 grid structure (or valid subset)
- [ ] Grid is responsive (`repeat(auto-fit, minmax(...))`)
- [ ] All text is telegraphic/keywords (3-7 words per bullet)
- [ ] Font sizes >= 24pt (body), >= 48pt (titles)
- [ ] Dark theme — no hardcoded light colors
- [ ] Image present or placeholder with generation prompt
- [ ] Max 3-5 bullets per list
- [ ] Bold colored keywords used for emphasis (not overused)
- [ ] Styles defined at project level in `custom/styles.py`
- [ ] `BlockStyles` only composes, never creates raw CSS
- [ ] Slide breaks named descriptively (`marker_label`)
- [ ] Emojis used sparingly (0-1 per slide)

---

## Quick Reference — Slide Types

| User requests... | Grid rows | Key elements |
|---|---|---|
| "title slide" | L1 | Title + subtitle + author, centered |
| "content slide" | L1 + L2 | Headline + image/text grid |
| "full slide" | L1 + L2 + L3 | Headline + content + question |
| "comparison slide" | L1 + L2 | Headline + 2-column comparison |
| "quote slide" | L1 | Citation + attribution, generous spacing |
| "question slide" | L1 + L3 | Statement + open question |
| "conclusion slide" | L1 + L2 | Key takeaways + next steps |
| "image gallery" | L1 + L2 | Title + multi-image grid |

---

## Full Slide Template (Copy-Paste Ready)

```python
"""Slide: Topic Description."""
from streamtex import *
from streamtex.styles import Style as ns
from streamtex.enums import Tags as t, ListTypes as lt
from custom.styles import Styles as s


class BlockStyles:
    """Slide: Topic Description."""
    headline = s.project.slide.headline
    body = s.project.slide.body
    keyword = s.project.slide.keyword
    question = s.project.slide.question
bs = BlockStyles


def build():
    with st_block(s.center_txt):
        # === L1 — Headline ===
        st_write(bs.headline, "Slide Title", tag=t.div, toc_lvl="2")
        st_space(size=2)

        # === L2 — Two-column content ===
        with st_grid(
            cols="repeat(auto-fit, minmax(350px, 1fr))",
            gap="24px",
        ) as g:
            with g.cell():
                st_image(uri="static/images/bck_topic.png", width="100%")
                # IMAGE PROMPT: "..."
                # SUGGESTED FILENAME: static/images/bck_topic.png
            with g.cell():
                with st_list(
                    l_style=bs.body, li_style=bs.body,
                    list_type=lt.unordered,
                ) as l:
                    with l.item():
                        st_write(bs.body,
                            (bs.keyword, "Keyword"), " — short point",
                        )
                    with l.item():
                        st_write(bs.body, "Second key point")
                    with l.item():
                        st_write(bs.body, "Third key point")

        st_space(size=2)

        # === L3 — Transition question ===
        st_write(bs.question, "What implications for...?", tag=t.div)
```

---

## Rule 12 — Grid Design Checklist (MANDATORY before writing any st_grid)

Before writing ANY `st_grid` code, follow this checklist IN ORDER:

### Step 1 — Find a working example first
Search the StreamTeX manuals (`stx_manual_intro/blocks/_atomic/bck_grid_*.py`) for a
pattern that matches your use case. Copy the working pattern, then adapt it.
**Never invent a grid layout from scratch when an example exists.**

### Step 2 — Use the correct cell styling pattern
The ONLY reliable way to style grid cells (background, border, centering) is:
```python
cell = (
    my_background_style
    + s.container.layouts.vertical_center_layout  # vertical centering
    + s.center_txt                                 # horizontal centering
    + s.container.paddings.small_padding           # padding
)

with st_grid(cols=3, cell_styles=cell, gap="12px") as g:
    with g.cell():
        st_write(style, "content")
```

**Rules:**
- Pass ALL cell styling via `cell_styles=` parameter — NOT via `st_block()` inside cells
- Use `g.cell()` context manager — NOT `st_block()` as a cell wrapper
- Use `s.container.layouts.vertical_center_layout` for vertical centering — NOT manual flex CSS
- Use `s.center_txt` for horizontal centering — it works because it sets `text-align`
- Use `gap="12px"` parameter for spacing — NOT gap in `grid_style`
- Do NOT nest `st_block()` inside `g.cell()` for styling — it creates extra Streamlit wrappers
  that break flex centering

### Step 3 — Verify column width vs content
See Rule 13 below for the calibration formula.

### Anti-patterns (NEVER do these)
- `st_block(cell_style)` inside a grid cell → extra wrapper breaks centering
- `display:flex; align-items:center;` in `grid_style` → targets wrong element
- `st_block(s.container.flex.center_flex)` inside `g.cell()` → doesn't propagate
- Fixed column width without checking font size fit → overflow

---

## Rule 13 — Column Width vs Font Size Calibration

When using fixed-width columns in a grid, ALWAYS verify that the column is wide enough
for the text it contains at the chosen font size. **Never guess — calculate.**

### Calibration formula

```
minimum_column_width = longest_text_chars × 0.6 × font_size_px + (2 × padding_px)
```

Where `font_size_px ≈ font_size_pt × 1.33` and `0.6` is the average width/height ratio
for sans-serif fonts.

### Reference table

| Font | 5 chars (e.g., "Day 1") | 8 chars (e.g., "Mastering") | 12 chars (e.g., "Requirements") |
|------|------------------------|----------------------------|-------------------------------|
| `s.large` (32pt ≈ 43px) | ~160px | ~240px | ~340px |
| `s.Large` (48pt ≈ 64px) | ~220px | ~340px | ~490px |
| `s.huge` (64pt ≈ 85px) | ~290px | ~440px | ~640px |
| `s.Huge` (80pt ≈ 107px) | ~350px | ~550px | ~800px |

*Values include ~30px padding. Actual results vary by font and character mix.*

### Rules

1. **Before setting a fixed column width**: count the characters of the longest content
   in that column, look up the reference table, and set the width accordingly.
2. **If the text doesn't fit**: either widen the column OR reduce the font size.
   Never let text overflow or wrap unintentionally.
3. **For variable-length content**: prefer responsive columns (`minmax()`) over fixed widths.
   Fixed widths are only for short, predictable content (e.g., "Day 1" to "Day 6").
4. **Use `s.text.wrap.hyphens`** as a safety net on text in grid cells — it enables
   automatic hyphenation so long words break cleanly with a hyphen instead of overflowing.

---

## Rule 13 — Interaction with Design Guidelines

The rules in this file define the **structural and technical baseline** for all slides.
Design guidelines (`.claude/designer/guidelines/`) define the **visual philosophy**.

When a project has an active guideline:
- The L1/L2/L3 grid structure (Rule 2) remains mandatory — guidelines don't change the skeleton
- Font size minimums (Rule 5) may be RAISED by the guideline (never lowered)
- Text constraints (Rule 4) may be tightened by the guideline (fewer words, fewer bullets)
- The guideline determines HOW each zone is filled (generously, densely, minimally)

The `@guideline` annotation in block files indicates which guideline applies.
Resolution: inline annotation > block annotation > project override > project default.
See `.claude/designer/guidelines/_index.md` for the complete scoping system.
