# Web Document Design Rules — `manual`, `report`, collection hubs

**Scope**: the default design rules for StreamTeX **reading documents** —
manuals, reports, web-books, and the hub page of a collection. Primary
reference for the `web-document-designer` agent and for `/stx-block:new`
when the project's `identity.type` is `manual`, `report`, or `collection`.

This file **extends** the neutral base `visual-design-rules.md` (always read
that first). Where a rule here conflicts with the base, **this file wins**.
Unlike slides, a reading document is **scrolled**, read up close, and
information-dense — so the constraints differ from `slide-design-rules.md`.

## 1. Reading flow, not a viewport

- **Scrolling is expected.** Do not force 16:9 / one-screen fit. A block may be
  as tall as its content needs; vertical rhythm matters more than fitting.
- **Linear reading order.** Content flows top-to-bottom; each block is one
  coherent unit of reading (one idea / one feature / one section).
- **Scannability.** Use subtitles, short paragraphs, lists, and callouts so a
  reader can skim. No wall of text: break every ~4-5 lines with structure.

## 2. Section hierarchy & navigation

- Register the section title in the TOC: `st_write(bs.heading, "...", tag=t.div, toc_lvl="1")`; sub-sections with `toc_lvl="+1"`.
- One H1-equivalent per block; sub-sections use the subtitle style.
- Long documents rely on the sidebar TOC for navigation — every section **must**
  register an entry (this is how the reader moves around).

## 3. Typography & density (reading, not projection)

- Body text floor: `s.text_base` (palier 7, 18pt at base) — readable on a
  laptop at arm's length. No projection floor is imposed (that is a slide rule).
- Denser layouts are acceptable: multi-paragraph explanations, tables, and
  side-by-side comparisons are normal in a reading document.
- Line length may be longer than on slides, but keep measure comfortable
  (~60-90 characters) for body prose.

## 4. Responsive layout

- Prefer responsive grids: `st_grid(cols="repeat(auto-fit, minmax(320px, 1fr))")`
  so columns reflow on narrow viewports instead of overflowing.
- Two- and three-column reading layouts are fine; ensure each cell's text is
  centered/aligned consistently and wraps (use `s.text.wrap.hyphens` as a net).

## 5. Content idioms (documentation / teaching)

These idioms — relocated here from the base because they are reading-document
patterns, **not** slide patterns — are the backbone of StreamTeX manuals.

### 5.1 Canonical section structure

Every documented feature follows this order:

```python
# 1. Subtitle with TOC registration
st_write(bs.sub, "Feature Name", toc_lvl="+1")
st_space("v", 1)

# 2. Explanation box (what & why)
show_explanation("""\
    What this feature does.
    Why you would use it.
""")
st_space("v", 1)

# 3. Code box (syntax-highlighted)
show_code("""\
    st_write(s.text_base, "Example code")
""")
st_space("v", 1)

# 4. Live rendering
st_write(s.text_base, "Example code")
st_space("v", 2)

# 5. Optional: details box (defaults & tips)
show_details("""\
    Default: param=value.
    Additional tips about this feature.
""")
```

### 5.2 Every example must have code

- **Every live rendering** is preceded by a `show_code()` call.
- The code shown must match the rendering below it.
- Only exceptions: headings, subtitles, spacers, helper calls.

### 5.3 WRONG / CORRECT boxes

- Always explain **WHY** the WRONG code is wrong.
- Use `st_write()` + `st_br()` for the explanation, never concatenation.
- Then show the code with `show_code_inline()`.

```python
with st_block(s.project.containers.bad_callout):
    st_write(bs.wrong_label, "WRONG:")
    st_space("v", 1)
    st_write(s.text_base, "Explanation line 1.")
    st_br()
    st_write(s.text_base, "Explanation line 2.")
    st_space("v", 1)
    show_code_inline("""\
        # the wrong code here
    """)
```

## 6. Detail-on-hover stays available

The `st_hover_tooltip` widget (core `streamtex`) is useful in reading documents
too — for glossary terms or optional asides — though less critical than on
slides since the reader can simply scroll to a details box. Same placement
rules apply (open opposite the icon; readable content).

## 7. Interaction with design guidelines

If a guideline is active (`custom/design-guideline.md`), it wins over these
defaults (it may raise font floors or change density). For reading documents,
`dense-informative` and `academic-structured` are the usual fits;
`maximize-viewport` suits landing/hub pages. See `designer/guidelines/_index.md`.
