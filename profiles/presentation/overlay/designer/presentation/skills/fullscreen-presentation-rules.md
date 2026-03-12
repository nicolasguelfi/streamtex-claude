# Fullscreen Presentation Rules (16:9)

> **Relationship**: This skill **extends** `presentation-design-rules.md` with fullscreen-specific constraints.
> All base presentation rules still apply. Where a rule here conflicts, **this file wins**.

These rules target **fullscreen 16:9 presentations** where each slide must fill
the viewport without any scrolling. They complement the base presentation rules
with viewport-fitting constraints.

---

## FS-1 — Ratio 16/9

Content must fit within a **16:9 rectangle**. No horizontal or vertical scrolling.
Configure via `PresentationConfig(aspect_ratio="16/9")`.

---

## FS-2 — Structure: Title / Content / Footer

Each slide follows a **3-zone layout**:

| Zone | Level | Content |
|------|-------|---------|
| Title | L1 | Section heading (`s.Huge` or `s.huge`) |
| Content | L2 | Grid-based content (`st_grid`) |
| Footer | auto | Managed by `PresentationConfig(footer=True)` — never manual |

---

## FS-3 — Density

**Maximum 60% of the slide surface** should be occupied by content.
The remaining 40% is whitespace for readability at distance.

| Element | Max per slide |
|---------|---------------|
| Bullets | 3 |
| Ideas | 1 |
| Grid columns | 2 (rarely 3) |

---

## FS-4 — Height Constraint

All content (title + body + spacing) must fit within:

```
100vh - footer_height - padding
```

If content overflows, **reduce or split** into multiple slides. Never allow scrolling.

---

## FS-5 — Images: Viewport Units

Use **vh or %** units for image sizing, never **px**.
Pixel values do not adapt to viewport size changes.

### WRONG
```python
st_image(uri=img, width="600px")
```

### CORRECT
```python
st_image(uri=img, width="80%")
st_image(uri=img, width="50vh")
```

---

## FS-6 — Grid L2

Use `st_grid(cols="1fr 1fr")` for two-column layouts within the content zone.

```python
with st_grid(cols="1fr 1fr", gap="2em"):
    with st_grid_item():
        st_write(bs.body, "Left column content")
    with st_grid_item():
        st_image(uri=img, width="100%")
```

---

## FS-7 — No Scroll

Apply `overflow: hidden` at the slide level. If content overflows:

1. **Reduce** — fewer bullets, shorter text
2. **Split** — move overflow to the next slide
3. **Resize** — use smaller images or fewer grid items

Never add scroll bars to a presentation slide.

---

## FS-8 — Slide Break

Use `st_slide_break(marker_label="...")` between each slide section.

Configure globally in `book.py`:

```python
set_slide_break_config(SlideBreakConfig(
    mode=SlideBreakMode.HIDDEN,
    fullscreen=True,
    marker=True,
))
```

Each block should end with a slide break (or begin with one after the first slide).

---

## FS-9 — Footer Auto

**Never generate footer content manually.** Use `PresentationConfig(footer=True)`
which renders a consistent footer automatically via `st_presentation_footer()`.

### WRONG
```python
# Manual footer in block
st_write(s.small, "Course Title — Page 3")
```

### CORRECT
```python
# In book.py — footer is automatic
set_presentation_config(PresentationConfig(
    title="My Presentation",
    footer=True,
))
```
