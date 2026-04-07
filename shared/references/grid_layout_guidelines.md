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
