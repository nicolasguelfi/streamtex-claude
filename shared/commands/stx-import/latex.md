# /stx-import:latex — Import LaTeX documents into StreamTeX

Convert a LaTeX document (article, beamer, book, report) into native StreamTeX blocks
in the current working directory.

Arguments: $ARGUMENTS

## Argument parsing

Parse `$ARGUMENTS` as: `<source_file_or_directory> [OPTIONS]`

**Options**:
- `--profile slides` — Beamer presentations: paginated, slide breaks, large fonts
- `--profile document` (default) — Articles/reports/books: continuous scroll, full text
- `--mode full` (default) — Import everything from scratch
- `--mode incremental` — Convert only missing files, keep existing blocks as-is
- `--dry-run` — Show what would be created without writing files
- `--help` — Show usage and document class mapping overview

### Examples

```
/stx-import:latex ../paper/main.tex
/stx-import:latex ../slides/presentation.tex --profile slides
/stx-import:latex ../thesis/ --mode incremental
/stx-import:latex --help
```

## Required readings BEFORE execution

1. `.claude/developer/agents/import-converter.md` — import agent role
2. `.claude/developer/skills/import-conventions.md` — shared import rules
3. `.claude/import-formats/latex/conventions.md` — LaTeX-specific rules
4. `.claude/references/coding_standards.md` — coding rules
5. Existing blocks in the target project (for style conventions already in use)

## Prerequisites

- An existing StreamTeX project (created via `/stx-designer:init` or `stx install --project`)
- LaTeX source files (`.tex`, with optional `.bib`, `.sty`, images)
- For multi-file projects: a main `.tex` file that `\input` or `\include` sub-files

## What it does

Converts LaTeX documents — including structure, formatting, math, TikZ graphics,
bibliography, and beamer slides — into native StreamTeX blocks with full graphical
quality and responsive design.

**Principle: Zero residual LaTeX** — every LaTeX element is converted to a native `stx.*` component.

## Workflow

Execute each step in order.

### Step 1 — Analyze

1. **Detect document class**: `\documentclass{article|beamer|book|report|...}`
2. **Inventory packages**: List all `\usepackage` declarations, note which have StreamTeX equivalents
3. **Resolve file structure**: Follow `\input{...}` and `\include{...}` to build complete document tree
4. **Inventory content**:
   - Count sections/chapters/frames
   - List images (`\includegraphics` paths)
   - Detect math environments (`equation`, `align`, `$...$`, `$$...$$`)
   - Detect TikZ/PGF blocks (`tikzpicture`, `pgfplots`)
   - Detect bibliography (`\bibliography{...}` or `\addbibresource{...}`)
5. **Determine profile**: Beamer -> `slides`, all others -> `document` (unless overridden)
6. **Report findings and ask user for confirmation** before proceeding

### Step 2 — Map Structure

Map LaTeX sectioning commands to StreamTeX TOC hierarchy:

| LaTeX | StreamTeX | TOC |
|---|---|---|
| `\chapter{...}` | `st_write(bs.headline, "...", toc_lvl="1")` | Block root |
| `\section{...}` | `st_write(bs.headline, "...", toc_lvl="+1")` | Section |
| `\subsection{...}` | `st_write(bs.subheadline, "...", toc_lvl="+2")` | Subsection |
| `\subsubsection{...}` | `st_write(bs.subheadline, "...", toc_lvl="+3")` | Sub-subsection |
| `\begin{frame}{Title}` | `st_slide_break()` + `st_write(bs.headline, "Title", toc_lvl="+1")` | Slide |

- For `book` class: each `\chapter` becomes a separate block with `toc_lvl="1"`
- For `article`/`report`: each `\section` becomes the root or a major division
- For `beamer`: each `\begin{frame}` becomes a slide with `st_slide_break()`

### Step 3 — Map Content

Convert LaTeX content elements to StreamTeX components:

| LaTeX | StreamTeX |
|---|---|
| `\textbf{...}` | `(s.bold, "...")` tuple in `st_write()` |
| `\emph{...}` / `\textit{...}` | `(s.italic, "...")` tuple in `st_write()` |
| `\underline{...}` | `(s.underline, "...")` tuple in `st_write()` |
| `\texttt{...}` | `(s.code, "...")` tuple in `st_write()` |
| `\begin{itemize}` | `st_list()` with `l.item()` |
| `\begin{enumerate}` | `st_list(list_type=lt.numbered)` with `l.item()` |
| `\begin{figure}` / `\includegraphics` | `st_image(uri="images/...", width="...")` |
| `\begin{tikzpicture}` | `st_tikz(code="...")` via `extract_tikz()` |
| `$...$` | `st_latex(code="...")` (inline) |
| `$$...$$` / `\[...\]` | `st_latex(code="...", display=True)` |
| `\begin{equation}` | `st_latex(code="...")` |
| `\begin{align}` | `st_latex(code="\\begin{align}...\\end{align}")` |
| `\begin{verbatim}` / `\begin{lstlisting}` | `st_code(code="...", language="...")` |
| `\begin{table}` / `\begin{tabular}` | `st_grid()` with cells or `st_table()` |
| `\footnote{...}` | Inline parenthetical or `show_details()` |
| `\href{url}{text}` | `(link_style, "text")` tuple with URL |
| `\cite{key}` | `cite("key")` |
| `\begin{abstract}` | `st_block()` with abstract styling |
| `\begin{quote}` / `\begin{quotation}` | `st_block(container_style)` + `st_write()` |
| `\begin{description}` | `st_list()` with styled label items |

### Step 4 — Map Theme

1. **Beamer themes**: Map `\usetheme{...}` and `\usecolortheme{...}` to StreamTeX styles
   - Extract primary/secondary/accent colors from the beamer theme
   - Create `BlockStyles` class with mapped colors
   - Use `SlideStylesCustom` for presentation profile
2. **Article/report**: Extract custom colors from `\definecolor` and `\colorlet`
   - Map to `ColorsCustom` / `BackgroundsCustom` in `custom/styles.py`
   - Use `DocumentStylesCustom` for document profile
3. **Font mappings**: Map `\usepackage{helvet}` etc. to closest StreamTeX font settings

### Step 5 — Migrate Assets

1. **Images**: Resolve all `\includegraphics` paths relative to the LaTeX project root
   - Copy images to `static/images/`
   - Rename per convention: `[block_name]_image_[00index].[ext]`
   - Update URIs to be relative to static source (no `static/` prefix)
2. **TikZ figures**: Extract with `extract_tikz()` for `st_tikz()` rendering
3. **Bibliography**: Copy `.bib` files to project, configure `load_bibtex()` in `book.py`
4. **Missing images**: Generate placeholder code with IMAGE PROMPT comments

### Step 6 — Configure book.py

1. **Beamer** (`--profile slides`):
   - `paginate=True`
   - `PresentationConfig(...)` with 16:9 format
   - `page_width=100`, `zoom=80`
2. **Article/report/book** (`--profile document`):
   - `paginate=False`
   - No `PresentationConfig`
   - `page_width=90`, `zoom=100`
3. **Common settings**:
   - `ExportMode.MANUAL` for HTML and PDF exports
   - `sidebar_max_level=3` in TOCConfig
   - `auto_marker_on_toc=1` in MarkerConfig
4. **Bibliography** (if `\bibliography` or `\addbibresource` detected):
   - Add `set_bib_config(BibConfig(...))` call
   - Add `load_bibtex("references.bib")` call
5. Wire all blocks in `st_book()` in document order
6. Verify: `python -c "import setup; import blocks"` (all blocks load)

## Post-import checklist

After all steps complete, verify:

- [ ] Document class correctly identified and mapped to profile
- [ ] All `\input`/`\include` files resolved and converted
- [ ] All images copied to `static/images/` and URIs have no `static/` prefix
- [ ] All blocks have exactly ONE `toc_lvl="1"` and all others use `"+N"`
- [ ] **slides profile:** Every frame has a `st_slide_break()` before it
- [ ] **document profile:** No `st_slide_break()`, only `st_br()` separators
- [ ] No raw LaTeX syntax in any `st_write()` calls (math goes in `st_latex()`)
- [ ] All enumerations use `st_list()`, not `st_write("- ...")`
- [ ] Math environments converted to `st_latex()` calls
- [ ] TikZ figures converted to `st_tikz()` calls
- [ ] Bibliography configured if source uses `\cite`
- [ ] Exports are `ExportMode.MANUAL`
- [ ] Style API uses correct names (`center_align`, `italic_text`, `decors`)
- [ ] `stx run` launches without errors

## Phase: Second-Pass Verification (MANDATORY)

After the first complete implementation:
1. **Re-read the source LaTeX** top-to-bottom. For each element, confirm a corresponding structure exists in the block.
2. **Re-read the import rules** (both shared and LaTeX-specific conventions).
3. **Fix any mismatches**: update styles, layout, or content.
4. **Run the verification checklist** above.
