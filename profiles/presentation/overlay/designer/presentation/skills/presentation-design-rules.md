# Presentation Design Rules — `presentation`

> **Relationship to base rules**: This file **extends** `visual-design-rules.md` (shared skills).
> Where a rule here conflicts with the base, **this file wins**.
> Base rules still apply for anything not overridden here.

These rules target **live presentations** projected at 10–20 m distance.
They optimize for instant readability and visual impact.

---

## Rule 1 — Keywords Only

**No sentences on slides.** Each bullet is a keyword phrase.

| Constraint | Limit |
|---|---|
| Words per bullet | 5–7 max |
| Bullets per section | 3 max |

### WRONG
```python
st_write(bs.body, "84% of respondents are using or planning to use AI tools "
    "in their development process, an increase over last year.")
```

### CORRECT
```python
st_write(bs.body, "84% use or plan AI tools")
st_write(bs.body, "51% daily usage among pros")
st_write(bs.body, "+8% vs 2023")
```

---

## Rule 2 — Font Size for Distance

Audience at 10–20 m needs large text, but sizes must stay **proportional**
so that the full slide fits on one screen.

> **v2 architecture**: pick `base_pt_desktop=24` for projection in
> `book.py`. Every palier in the 29-palier scale scales up uniformly.
> Legacy tokens shown in the rightmost column remain valid for
> existing decks.

| Element | Indexed alias (primary) | Palier | pt @ base 18 | pt @ base 24 (projection) | Legacy equivalent |
|---|---|---|---|---|---|
| Course title | `s.text_8xl` | 17 | 72pt | 96pt | `s.Huge` |
| Section titles | `s.text_7xl` | 16 | 60pt | 80pt | `s.huge` |
| Subtitles | `s.text_6xl + s.bold` | 15 | 48pt | 64pt | `s.Large + s.bold` |
| Body text | `s.text_base` | 7 | 18pt | 24pt | `s.big` (also valid: `s.Large` for legacy) |
| Attribution/source | `s.text_xs` | 5 | 14pt | 18.7pt | `s.medium` |
| Caption/footer | `s.text_xs` | 5 | 14pt | 18.7pt | `s.medium` |

> **Giant paliers (`s.text_9xl` and `s.scale[27]`) are exceptional** —
> use only for single-word decorative elements (e.g. a number, an icon
> label). Never use them for multi-word titles: they overflow the
> viewport.

> **Recommended setup**: `st_book([...], scale=ScaleConfig(base_pt_desktop=24))`
> in `book.py`. With this base, `s.text_base` renders at 24pt (32px) —
> the readable body size for projection. Avoid hand-tuning individual
> paliers; the WORD_PROCESSOR curve already balances the scale.

### WRONG
```python
st_write(s.text_xs, "Key takeaway")       # palier 5 — too small for body
```

### CORRECT
```python
# In book.py:
st_book([...], scale=ScaleConfig(base_pt_desktop=24))

# In bck_*.py:
st_write(s.text_base, "Key takeaway")     # palier 7 — 24pt @ base 24 = 32px
st_write(s.text_xs, "Source: Survey 2024")  # palier 5 — caption / attribution
```

---

## Rule 3 — Visual First

Prefer symbols, icons, and images over text. A chart or diagram replaces a paragraph.

### WRONG
```python
st_write(bs.body, "The adoption rate increased significantly over the past year")
```

### CORRECT
```python
st_write(bs.body, "Adoption rate: 76% → 84%")
# or better: show a chart
```

---

## Rule 4 — One Idea Per Section

Each section conveys **one concept**. If you need to explain two things, use two sections (or two slides).

---

## Rule 5 — High Contrast

Never use `muted` or `subtle` colors on body text. Reserve them for attribution only.

| Color usage | Allowed elements |
|---|---|
| `s.project.colors.primary` | Titles, emphasis |
| `s.project.colors.accent` | Subtitles, highlights |
| `s.project.colors.muted` | Source lines, footers ONLY |
| `s.project.colors.subtle` | NEVER on readable content |

### WRONG
```python
st_write(s.project.colors.muted + s.Large, "Important takeaway")
```

### CORRECT
```python
st_write(s.project.colors.accent + s.Large + s.bold, "Important takeaway")
```

---

## Rule 6 — Generous Spacing

Presentation slides need breathing room.

| Between | Spacing |
|---|---|
| Major sections | `st_space(size=4)` |
| Sub-sections | `st_space(size=3)` |
| Elements within a section | `st_space(size=2)` |

> **Override**: base rules use `st_space("v", 2)` between sections.
> Presentations use `st_space(size=4)` between major sections.

---

## Rule 7 — No Helper Boxes

Presentation slides do NOT use `show_explanation()`, `show_details()`, `show_code()`.
These are for pedagogical/tutorial slides, not live presentations.

Use direct `st_write()` calls instead.

### WRONG
```python
show_explanation("Key findings from the survey")
```

### CORRECT
```python
st_write(bs.body, "Key findings from the survey")
```

---

## Rule 8 — Image Sizing

Images must be large enough to see from the back of the room.

| Constraint | Minimum |
|---|---|
| Image width | 400px |
| Preferred width | 600px+ |
| Logo (decorative) | 160px acceptable |

> **AI Generation**: If `AIImageConfig` is configured, use
> `st_image(prompt="prompt...", editable=True, name="...")` instead of static placeholders.
> For batch generation, use `generate_image("prompt...", provider="openai")`
> then `st_image(uri=path)`. Images are cached on disk — no API cost on Streamlit reruns.

---

## Rule 9 — Simplified Block Structure

Presentation blocks use a reduced set of style roles:

```python
class BlockStyles:
    heading = ...    # Section title (Huge 96pt or huge 80pt — never Giant)
    sub = ...        # Subtitle (Large + bold)
    body = ...       # Body text (Large) — the main content style
    body_accent = ...  # Accented body (Large + accent color)
    caption = ...    # Attribution/source (large, muted)
```

No `explanation`, `details`, `code_example` — those belong to tutorial slides.
