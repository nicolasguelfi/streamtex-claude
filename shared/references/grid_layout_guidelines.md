# Grid Layout in StreamTeX — Guidelines

## st_zoom inside grid cells

### Problem

Wrapping `st_zoom()` **around** a `g.cell()` breaks CSS Grid vertical centering.

```python
# BAD — st_zoom wraps the cell, breaking vertical centering
with st_zoom(130), g.cell():
    with st_list(...) as l:
        ...
```

`st_zoom` creates an intermediate `<div>` wrapper **around** the cell. The cell is no
longer a direct child of the CSS Grid container, so `align-items: center` (vertical
centering from `cell_styles`) no longer applies.

### Solution

Place `st_zoom()` **inside** the cell, not around it:

```python
# GOOD — st_zoom is inside the cell, grid layout preserved
with g.cell():
    with st_zoom(130):
        with st_list(...) as l:
            ...
```

The cell remains a direct child of the grid container. Vertical centering via
`s.container.layouts.vertical_center_layout` in `cell_styles` works correctly.
The zoom applies only to the content inside the cell.

### Rule

**MANDATORY**: Never wrap `st_zoom()` around `g.cell()`. Always nest `st_zoom()`
inside the cell context manager.

## Aligning text inside a cell

`cell_styles` carries `text-align` like any CSS, and it is INHERITED by
everything in the cell — paragraphs, blocks, and (since 0.7.33) lists, which
used to force themselves back to the left.

```python
# The whole cell, list included, is centred
with st_grid(2, cell_styles=Style("text-align:center;", "cell_c")) as g:
    with g.cell():
        st_write("centred")
        with st_list() as l:            # inherits the centring
            with l.item(): st_write("centred too")
```

Inherited centring leaves the bullet OUTSIDE the text, which is what plain
CSS does. To pull the bullet into the line so bullet and text centre as one
unit, declare it on the list:

```python
        with st_list(text_align="center") as l:
            with l.item(): st_write("bullet centred with its text")
```

### Rule

**Prefer `text_align=` over `block_align=` inside a grid.** `text_align`
never changes the list width, so the cell geometry stays stable;
`block_align` (and its deprecated synonym `align`) resizes the list to its
content, so editing one item moves the layout.
