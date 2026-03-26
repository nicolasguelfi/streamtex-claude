# LaTeX Import Conventions

> Reference document for LaTeX -> StreamTeX conversion.
> Read this before any LaTeX import operation.

## 1. Document Class Mapping

| LaTeX Document Class | StreamTeX Target | Profile | Notes |
|---|---|---|---|
| `article` | Document project | `document` | Sections become block divisions |
| `beamer` | Presentation project | `slides` | Frames become slides with `st_slide_break()` |
| `book` | Multi-part project | `document` | Chapters become separate blocks |
| `report` | Document project | `document` | Similar to article but with chapters |
| `memoir` | Document project | `document` | Treat like book |
| `standalone` | Single block | `document` | Often TikZ figures |

## 2. Package Handling

### Packages with StreamTeX equivalents

| LaTeX Package | StreamTeX Equivalent | Action |
|---|---|---|
| `hyperref` | Built-in link styles | Map `\href` to link tuples |
| `graphicx` | `st_image()` | Convert `\includegraphics` |
| `tikz` / `pgf` | `st_tikz()` | Extract with `extract_tikz()` |
| `amsmath` / `mathtools` | `st_latex()` | Convert math environments |
| `listings` / `minted` | `st_code()` | Convert code blocks |
| `biblatex` / `natbib` | `cite()` + `load_bibtex()` | Convert bibliography |
| `booktabs` / `tabularx` | `st_grid()` / `st_table()` | Convert tables |
| `enumitem` | `st_list()` | Convert customized lists |
| `xcolor` | `ColorsCustom` | Map `\definecolor` to style definitions |
| `geometry` | Page width in `book.py` | Inform layout configuration |
| `fontspec` / `helvet` | Font settings | Map to closest StreamTeX font |
| `beamertheme*` | `SlideStylesCustom` | Extract theme colors |

### Packages to ignore (no StreamTeX equivalent needed)

- `inputenc`, `fontenc`, `babel` — encoding/language (handled by Streamlit)
- `microtype` — typographic micro-adjustments
- `parskip` — paragraph spacing (theme-controlled)
- `setspace` — line spacing (theme-controlled)
- `fancyhdr` — headers/footers (handled by StreamTeX navigation)

## 3. Structure Mapping

| LaTeX Command | StreamTeX | TOC Level |
|---|---|---|
| `\part{...}` | Separate block or major division | `toc_lvl="1"` |
| `\chapter{...}` | Block root (book/report) | `toc_lvl="1"` |
| `\section{...}` | Block root (article) or section | `toc_lvl="1"` or `toc_lvl="+1"` |
| `\subsection{...}` | Subsection | `toc_lvl="+2"` |
| `\subsubsection{...}` | Sub-subsection | `toc_lvl="+3"` |
| `\paragraph{...}` | Bold inline heading via `st_write()` | No TOC entry |
| `\begin{frame}{Title}` | `st_slide_break()` + `st_write(bs.headline, ...)` | `toc_lvl="+1"` |
| `\frametitle{...}` | `st_write(bs.headline, ...)` | `toc_lvl="+1"` |
| `\begin{block}{Title}` (beamer) | `st_block(container_style)` + title | No TOC entry |

### Rules

- ONE absolute `"1"` per block (the root title)
- ALL other headings use relative `"+N"` syntax
- NEVER use absolute `"2"`, `"3"`, etc.
- For `book` class: each `\chapter` becomes a separate block file
- For `article` class: `\section` may be root or `"+1"` depending on scope
- Starred variants (`\section*{...}`) become `st_write()` without `toc_lvl`

## 4. Content Mapping

### Inline Formatting

| LaTeX | StreamTeX |
|---|---|
| `\textbf{text}` | `(s.bold, "text")` tuple in `st_write()` |
| `\emph{text}` / `\textit{text}` | `(s.italic, "text")` tuple in `st_write()` |
| `\underline{text}` | `(s.underline, "text")` tuple in `st_write()` |
| `\texttt{text}` | `(s.code, "text")` tuple in `st_write()` |
| `\textsc{text}` | `(s.bold, "text")` (approximate) |
| `{\color{red} text}` | `(color_style, "text")` tuple with mapped color |
| `\href{url}{text}` | `(link_style, "text")` tuple |

### Block Elements

| LaTeX | StreamTeX |
|---|---|
| `\begin{itemize}` | `with st_list(...) as l:` + `with l.item():` |
| `\begin{enumerate}` | `with st_list(list_type=lt.numbered) as l:` + `with l.item():` |
| `\begin{description}` | `with st_list(...) as l:` with styled label items |
| `\begin{figure}` | `st_image(uri="images/...", width="...")` |
| `\begin{table}` / `\begin{tabular}` | `st_grid()` with `cell_styles` or `st_table()` |
| `\begin{verbatim}` | `st_code(code="...", language="text")` |
| `\begin{lstlisting}` | `st_code(code="...", language="...")` |
| `\begin{minted}{python}` | `st_code(code="...", language="python")` |
| `\begin{quote}` | `st_block(container_style)` + `st_write()` |
| `\begin{abstract}` | `st_block(abstract_style)` + `st_write()` |
| `\begin{center}` | `st_write(s.center_txt, ...)` |
| `\rule{...}{...}` | `st_br()` (horizontal rule equivalent) |
| `\newpage` / `\clearpage` | `st_slide_break()` (slides) or `st_br()` (document) |

### Nested Lists

LaTeX nested `itemize`/`enumerate` map to nested `st_list()`:

```python
with st_list(...) as l:
    with l.item():
        st_write(bs.body, "Top-level item")
        with st_list(...) as l2:
            with l2.item():
                st_write(bs.body, "Nested item")
```

## 5. Math Handling

### Inline Math

| LaTeX | StreamTeX |
|---|---|
| `$x^2 + y^2$` | `st_latex(code="x^2 + y^2")` |
| `\(x^2 + y^2\)` | `st_latex(code="x^2 + y^2")` |

### Display Math

| LaTeX | StreamTeX |
|---|---|
| `$$E = mc^2$$` | `st_latex(code="E = mc^2", display=True)` |
| `\[E = mc^2\]` | `st_latex(code="E = mc^2", display=True)` |
| `\begin{equation}` | `st_latex(code="...")` |
| `\begin{align}` | `st_latex(code="\\begin{align}...\\end{align}")` |
| `\begin{gather}` | `st_latex(code="\\begin{gather}...\\end{gather}")` |
| `\begin{multline}` | `st_latex(code="\\begin{multline}...\\end{multline}")` |

### Rules

- Strip `\label{...}` from equations (StreamTeX does not use LaTeX labels)
- Strip `\nonumber` and `\notag` (no effect in StreamTeX rendering)
- Preserve `\\` line breaks inside multi-line environments
- Use `extract_math()` utility when available for automated extraction
- Custom macros (`\newcommand`) should be expanded or defined in a preamble block

## 6. TikZ / PGF Handling

TikZ figures are rendered natively by StreamTeX via `st_tikz()`.

```python
# Extract TikZ code from LaTeX source
tikz_code = r"""
\begin{tikzpicture}
  \draw (0,0) -- (1,1);
  \node at (0.5, 0.5) {Hello};
\end{tikzpicture}
"""

# Render in StreamTeX
st_tikz(code=tikz_code)
```

### Rules

- Use `extract_tikz()` utility to extract TikZ blocks from source
- Preserve the full `\begin{tikzpicture}...\end{tikzpicture}` block
- Include required TikZ libraries in the code string if non-standard
- For `pgfplots`: include the full `\begin{axis}...\end{axis}` inside the tikzpicture
- `standalone` document class files are typically single TikZ figures
- Use `is_full_document()` and `strip_document_wrapper()` to extract TikZ from standalone files

## 7. Beamer Frame Handling

Each beamer `\begin{frame}` becomes a slide in StreamTeX.

```python
# Before each frame (except the first in a block)
st_slide_break(marker_label="frame_topic_name")
st_write(bs.headline, "Frame Title", toc_lvl="+1")
# ... frame content ...
```

### Rules

- Use `extract_frames()` utility to split beamer source into individual frames
- `\begin{frame}[fragile]` — code frames: extract listings to `st_code()`
- `\begin{frame}{Title}` or `\frametitle{Title}` — both map to `st_write()` with headline style
- `\pause` commands — ignored (StreamTeX uses slide breaks, not incremental reveal)
- `\only<N>{...}` / `\visible<N>{...}` — flatten overlays, show final state
- `\begin{columns}` — map to `st_grid()` with appropriate column widths
- `\begin{block}{Title}` (beamer block) — map to `st_block(container_style)`
- `\begin{alertblock}` — map to `st_block()` with warning/alert style
- `\begin{exampleblock}` — map to `st_block()` with accent/example style
- Title frames with `\titlepage` — map to block root with `toc_lvl="1"`

## 8. Bibliography Handling

| LaTeX | StreamTeX |
|---|---|
| `\bibliography{refs}` | `load_bibtex("refs.bib")` in `book.py` |
| `\addbibresource{refs.bib}` | `load_bibtex("refs.bib")` in `book.py` |
| `\cite{key}` | `cite("key")` |
| `\citep{key}` | `cite("key")` |
| `\citet{key}` | `cite("key")` |
| `\autocite{key}` | `cite("key")` |
| `\printbibliography` | `st_bibliography()` in a dedicated block |

### Rules

- Copy `.bib` files to the project root
- Configure `set_bib_config(BibConfig(format=..., style=...))` in `book.py`
- All citation variants (`\cite`, `\citep`, `\citet`, `\autocite`, `\parencite`) map to `cite()`
- `\nocite{*}` — ignored (StreamTeX shows only cited entries)
- Multiple citations `\cite{a,b,c}` — split into `cite("a")`, `cite("b")`, `cite("c")`

## 9. Color and Theme Mapping

### Custom Colors

```latex
% LaTeX
\definecolor{myblue}{HTML}{3498DB}
\colorlet{accent}{blue!60}
```

Map to `custom/styles.py`:

```python
class ColorsCustom:
    myblue = Style(font_color="#3498DB")
    accent = Style(font_color="#5DADE2")  # resolved color value
```

### Beamer Themes

Extract the color palette from the beamer theme and map to StreamTeX:

| Beamer Element | StreamTeX Style |
|---|---|
| `structure` color | Primary heading color |
| `alerted text` color | Warning/accent color |
| `example text` color | Example/secondary color |
| `palette primary` | Background/container styles |
| `footline` | Not migrated (StreamTeX has own navigation) |

Document dropped theme elements with justification in `BlockStyles`.

## 10. Forbidden Patterns

These patterns must NEVER appear in generated code:

```python
# Raw LaTeX in st_write (math goes in st_latex)
st_write(bs.body, "$x^2$")                 # use st_latex(code="x^2")
st_write(bs.body, "\\textbf{bold}")         # use (s.bold, "bold") tuple

# Unresolved \input
# All \input{file} must be resolved before conversion

# Wrong image function
st.image("path/to/image.png")              # use st_image()

# Static prefix in URIs
st_image(uri="static/images/file.png")     # remove "static/"

# Simulated lists
st_write(bs.body, "- Item 1\n- Item 2")   # use st_list()

# Absolute toc levels (except root)
st_write(..., toc_lvl="2")                 # use "+1"

# Raw \begin{tikzpicture} in st_write
st_write(bs.body, "\\begin{tikzpicture}")  # use st_tikz()

# Markdown in st_write strings
st_write(bs.body, "**bold text**")          # use tuples

# LaTeX comments in output
st_write(bs.body, "text % comment")        # strip comments

# Unresolved cross-references
st_write(bs.body, "See \\ref{fig:1}")      # resolve or remove
```

## 11. Library Utilities

Use these StreamTeX utilities when available:

| Utility | Purpose |
|---|---|
| `extract_tikz()` | Extract TikZ code blocks from LaTeX source |
| `extract_math()` | Extract math environments from LaTeX source |
| `extract_frames()` | Split beamer source into individual frames |
| `is_full_document()` | Check if string is a complete LaTeX document |
| `strip_document_wrapper()` | Remove `\documentclass` / `\begin{document}` wrapper |

## 12. Multi-file Projects

LaTeX projects often span multiple files:

1. **Resolve `\input{file}`**: Read the referenced file and inline its content
2. **Resolve `\include{file}`**: Same as `\input` but adds `\clearpage`
3. **Resolve `\subfile{file}`** (subfiles package): Extract document body
4. **Search paths**: Check relative to main file, then project root
5. **Circular references**: Detect and report (do not recurse infinitely)

## 13. Verification Checklist

After conversion, verify:

- [ ] No raw LaTeX syntax in Python code (no `\textbf`, `\emph`, `$...$` in `st_write`)
- [ ] All math in `st_latex()` calls
- [ ] All TikZ in `st_tikz()` calls
- [ ] All `\input`/`\include` resolved (no unresolved file references)
- [ ] Images renamed per convention and copied to `static/images/`
- [ ] Lists use `st_list()` (not simulated bullets)
- [ ] Inline mixed-style text uses ONE `st_write()` with tuples
- [ ] `st_br()` for spacing / horizontal rules
- [ ] `st_grid()` with `cell_styles` for tables
- [ ] No hardcoded black/white (theme-controlled)
- [ ] Custom colors mapped to `ColorsCustom` / `BackgroundsCustom`
- [ ] Bibliography configured if source uses `\cite`
- [ ] All `\cite` commands converted to `cite()` calls
- [ ] Beamer overlays flattened (no `\pause`, `\only`, `\visible` in output)
- [ ] LaTeX comments stripped from output
- [ ] Cross-references resolved or removed (no `\ref`, `\label` in output)
