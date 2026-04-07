# Plotly Charts in StreamTeX — Integration Guidelines

## Problem

`st.plotly_chart()` does **not** work correctly with StreamTeX's CSS `zoom` system.

When `st_book(zoom=90)` applies `zoom: 0.9` on the page container, Plotly.js measures
the container width via JavaScript **before** the CSS zoom is applied. This causes the
chart to render at the pre-zoom width, then be visually shrunk — leaving empty space
on the right. The lower the zoom, the worse the misalignment.

`use_container_width=True` does not fix this because it relies on the same JavaScript
measurement that is broken by CSS zoom.

## Solution — MANDATORY

**Always render Plotly charts via `stx.st_html()` (iframe), never via `st.plotly_chart()`.**

The iframe is a standard HTML element that scales correctly with CSS zoom, just like
images, text, and grids. Plotly.js inside the iframe measures its own iframe width
(unaffected by parent zoom) and fills it correctly.

### Pattern

```python
import plotly.graph_objects as go
import streamtex as stx

# ── Chart sizing ─────────────────────────────────────────────────────
_HEIGHT = 900        # chart height in pixels (width auto-fills iframe)
_SCALE_FONT = 1.0    # font/stroke multiplier for projection visibility

# Base values (at _SCALE_FONT = 1.0)
_BASE_TITLE = 36
_BASE_AXIS_TITLE = 30
_BASE_TICK_X = 26
_BASE_TICK_Y = 24
_BASE_LEGEND = 22
_BASE_HOVER = 24
_BASE_DATA_LABEL = 20
_BASE_LINE_WIDTH = 4
_BASE_MARKER_SIZE = 14

_sf = _SCALE_FONT  # shorthand


def _build_chart() -> go.Figure:
    fig = go.Figure()
    # ... add traces with scaled fonts/strokes:
    #   line={"width": round(_BASE_LINE_WIDTH * _sf)}
    #   marker={"size": round(_BASE_MARKER_SIZE * _sf)}
    #   textfont={"size": round(_BASE_DATA_LABEL * _sf)}

    fig.update_layout(
        autosize=True,           # MANDATORY: fills iframe width
        height=_HEIGHT,          # fixed height in pixels
        # Do NOT set width — let autosize handle it
        template="plotly_dark",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        title={"font": {"size": round(_BASE_TITLE * _sf)}, "x": 0.5},
        xaxis={"tickfont": {"size": round(_BASE_TICK_X * _sf)}},
        yaxis={"tickfont": {"size": round(_BASE_TICK_Y * _sf)}},
        legend={"font": {"size": round(_BASE_LEGEND * _sf)}},
        hoverlabel={"font": {"size": round(_BASE_HOVER * _sf)}},
    )
    return fig


# In build():
fig = _build_chart()
fig_html = fig.to_html(
    include_plotlyjs="cdn",
    full_html=True,
    config={"scrollZoom": True},
)
stx.st_html(fig_html, height=_HEIGHT + 50)
```

## Key Rules

1. **No `st.plotly_chart()`** — always use `stx.st_html(fig.to_html(...), height=...)`
2. **No `width=` in layout** — use `autosize=True` so Plotly fills the iframe
3. **`full_html=True`** — required for `stx.st_html()` to render a standalone page
4. **`include_plotlyjs="cdn"`** — loads Plotly.js from CDN inside the iframe
5. **`height=_HEIGHT + 50`** on `st_html()` — add margin for axes/labels below the chart
6. **`_SCALE_FONT`** — single multiplier to scale all text/strokes for projection
7. **`config={"scrollZoom": True}`** — enables mouse wheel zoom on the chart

## Export Support

Wrap with `stx.st_export()` for HTML export fallback:

```python
with stx.st_export(fig.to_html(include_plotlyjs="cdn", full_html=False)):
    stx.st_html(fig_html, height=_HEIGHT + 50)
```

Note: use `full_html=False` for the export fallback (inline), but `full_html=True`
for the `st_html()` rendering (standalone iframe).

## What NOT to Do

- `st.plotly_chart(fig, use_container_width=True)` — broken with CSS zoom
- `st.plotly_chart(fig)` without `use_container_width` — fixed 700px default
- Setting `width=` in `fig.update_layout()` — creates aspect ratio constraints
- CSS hacks to compensate zoom — fragile and non-portable
