# Coherence Check Rules

Reference file for `/stx-coherence:audit`. Defines 45 check categories (28 standard + 13 AI quality + 4 CLI).

---

## Check 1: API Coverage (scope: library, all)

**Goal**: Every public export in the library should be documented in at least one manual.

**Source**: `streamtex/streamtex/__init__.py` — extract all names from import statements.
**Target**: `streamtex-docs/manuals/**/blocks/**/*.py` — grep for usage of each export.

**Rules**:
- WARNING if an exported function/class appears in ZERO block files
- INFO if an export appears in blocks but has no `show_code()` example
- SKIP internal names (prefixed with `_`), type aliases, and re-exports of enums

**Presentation exports to verify**: `PresentationConfig`, `set_presentation_config`, `get_presentation_config`, `st_presentation_footer`, `add_presentation_options`

**Known exceptions** (not expected in blocks):
- Low-level exports: `export_append`, `export_push_wrapper`, `export_pop_wrapper`, `generate_export_html`, `reset_export_buffer`, `is_export_active`
- Config internals: `get_block_helper_config`, `get_bib_config`, `get_gsheet_config`, `get_link_config`, `get_bib_registry`, `reset_bib_registry`, `get_ai_image_config`, `get_slide_break_config`, `get_presentation_config`
- Display/layout internals: `PageLayout`, `ViewMode`, `SlideBreakDisplayConfig`, `ProfileConfig`, `AssetMode`
- Parser internals: `parse_bibtex_string`, `parse_ris_string`, `register_bib_parser`
- Utility re-exports: `generate_bib_stubs`, `export_bibtex`, `load_css`, `exec_static`, `resolve_content`, `inject_link_preview_scaffold`, `add_wrap_all_option`, `add_slide_break_options`
- Error/result types: `AIImageError`, `AIImageResult`, `BibParseError`, `GSheetError`
- AI image internals: `is_cached`, `list_providers`
- Registry internals: `FileCategoryRegistry`
- Style internals: `StreamTeX_Styles`

---

## Check 2: Cheatsheet & Coding Standards Sync (scope: library, all)

**Goal**: The cheatsheet and coding standards reflect the current library API.

**Source files**:
- `streamtex/streamtex/__init__.py` (exports)
- Key module files: `write.py`, `code.py`, `book.py`, `grid.py`, `list.py`, `container.py`, `block_helpers.py`, `presentation.py`

**Target files**:
- `streamtex-claude/shared/references/streamtex_cheatsheet_en.md`
- `streamtex-claude/shared/references/coding_standards.md`

**Rules**:
- WARNING if a function's signature (new parameter) is not reflected in the cheatsheet
- ERROR if the coding standards recommend a pattern that contradicts current library behavior
- WARNING if the cheatsheet documents a function that no longer exists in `__init__.py`
- WARNING if `presentation.py` signatures (`PresentationConfig`, `set_presentation_config`, `get_presentation_config`, `st_presentation_footer`, `add_presentation_options`) are missing from the cheatsheet

**How to check signatures**: For each major function, read the `def` line in the source module. Compare parameter names with those listed in the cheatsheet.

---

## Check 3: Cross-Manual Block Consistency (scope: docs, blocks, all)

**Goal**: All manual blocks use consistent, up-to-date patterns.

**Scope**: `streamtex-docs/manuals/**/blocks/**/*.py`

**Rules**:
- WARNING if a block uses `textwrap.dedent(` in code (now auto-dedented)
- WARNING if a block has `import textwrap` but doesn't use it in code
- WARNING if a block uses an old API pattern (e.g., deprecated parameter name)
- WARNING if a `show_code()` example inside a block shows `import textwrap` as part of the example code (inside triple-quoted strings)
- INFO if import styles differ between blocks in the same manual (e.g., some use `from streamtex import *`, others explicit imports)

---

## Check 4: Profile File Sync (scope: profiles, all)

**Goal**: All copies of shared profile files are identical to their source of truth.

**Source of truth** → **Copies to check**:

| Source | Copies |
|--------|--------|
| `streamtex-claude/shared/references/coding_standards.md` | `streamtex/.claude/references/`, `streamtex-docs/.claude/references/`, `streamtex-docs/references/`, `projects/*/.claude/references/` |
| `streamtex-claude/shared/references/streamtex_cheatsheet_en.md` | Same locations as above |
| `streamtex-claude/profiles/project/commands/stx-block/*.md` | `projects/*/.claude/commands/stx-block/` |
| `streamtex-claude/profiles/project/designer/agents/*.md` | `projects/*/.claude/designer/agents/` |
| `streamtex-claude/profiles/project/designer/skills/*.md` | `projects/*/.claude/designer/skills/` |
| `streamtex-claude/profiles/project/designer/templates/*.md` | `projects/*/.claude/designer/templates/` |
| `streamtex-claude/profiles/project/designer/tools/*.md` | `projects/*/.claude/designer/tools/` |
| `streamtex-claude/profiles/documentation/designer/agents/*.md` | `streamtex-docs/.claude/designer/agents/` |
| `streamtex-claude/shared/commands/stx-guide.md` | `streamtex/.claude/commands/`, `streamtex-docs/.claude/commands/`, `projects/*/.claude/commands/` |

**Method**: First verify source existence, then read both files, compare content. If different, report as ERROR.

**Rules**:
- ERROR if a source file declared in a manifest `[shared]` section does not exist in `shared/references/` or `shared/commands/` (source existence guard)
- ERROR if file content differs between source and copy
- WARNING if a source file exists but has no copy in an expected location
- INFO: report total files checked and sync status
- INFO: report any files found in `.claude/custom/` (user customizations detected)
- WARNING if a file in `.claude/custom/references/` has the same name as a file in `.claude/references/` (potential shadow/conflict)
- WARNING if a file in `.claude/custom/skills/` has the same name as a file in `.claude/developer/skills/` or `.claude/designer/skills/` (potential shadow/conflict)

---

## Check 5: Version Alignment (scope: library, all)

**Goal**: Library version is consistent across all locations and satisfies all dependency constraints.

**Source files**:
- `streamtex/pyproject.toml` → `[project] version`
- `streamtex/streamtex/__init__.py` → `__version__`
- `streamtex/CHANGELOG.md` → latest `## [X.Y.Z]` entry

**Targets**: All `pyproject.toml` files in `streamtex-docs/`, `projects/*/`

**Rules**:
- ERROR if `pyproject.toml` version differs from `__init__.py` `__version__`
- ERROR if CHANGELOG.md latest entry version differs from `pyproject.toml` version
- WARNING if library version doesn't satisfy a `streamtex>=X.Y.Z` constraint
- INFO: report current library version and all constraints found

---

## Check 6: Block Structure Compliance (scope: docs, blocks, all)

**Goal**: All blocks follow canonical structure.

**Scope**: `streamtex-docs/manuals/**/blocks/bck_*.py` + `streamtex-docs/templates/**/blocks/bck_*.py`

**Rules**:
- WARNING if block lacks `class BlockStyles`
- WARNING if block lacks `def build()` function
- WARNING if block lacks `bs = BlockStyles` alias
- WARNING if block has `build()` not wrapped in `with st_block(...):`
- INFO if block doesn't use `show_code()` or `show_explanation()` (may be intentional)

---

## Check 7: Template Freshness (scope: blocks, all)

**Goal**: Project template reflects latest practices.

**Source**: `streamtex-docs/templates/template_project/`
**Compare with**: Latest patterns in `streamtex-docs/manuals/stx_manual_intro/blocks/`

**Rules**:
- WARNING if template has obsolete imports
- WARNING if template pyproject.toml is missing ruff ignore rules
- WARNING if template pyproject.toml is missing `[tool.pyright] extraPaths`
- INFO: report template version vs latest manual patterns

---

## Check 8: stx-guide Knowledge Base Sync (scope: profiles, all)

**Goal**: The global `stx-guide.md` skill accurately reflects the current ecosystem state.

**Source**: `streamtex-claude/shared/commands/stx-guide.md`

**Cross-reference with**:
- All `manifest.toml` files in `streamtex-claude/profiles/*/` — command categories and counts
- `streamtex-claude/profiles/*/commands/*/` — actual command files
- `streamtex/streamtex/__init__.py` — public API (gotchas section)
- `streamtex-docs/manuals/` — manual list and ports

**Rules**:
- WARNING if a command category listed in a manifest.toml is missing from Section 4.2b table
- WARNING if the command count in Section 4.2b doesn't match the manifest
- WARNING if a profile listed by `install.py --list` is missing from stx-guide
- WARNING if a manual in `streamtex-docs/manuals/` is missing from Section 2 layout
- WARNING if a gotcha in Section 5 references deprecated behavior
- WARNING if topic "presentation" is missing from the topics table or does not document PresentationConfig
- WARNING if CLI templates documented in stx-guide do not match `AVAILABLE_TEMPLATES` in `install_cmd.py`
- WARNING if presets documented in stx-guide do not match `PRESET_ORDER` in `workspace_cmd.py`
- WARNING if the distinction between CLI templates and stx-block templates is not documented
- WARNING if `/stx-issue:*` commands are missing from the stx-guide topics table or Section 4e
- WARNING if `/stx-issue:bug`, `/stx-issue:feature`, `/stx-issue:question`, `/stx-issue:docs`, `/stx-issue:comment`, `/stx-issue:list` are missing from the quick reference table (Section 6)
- INFO: report stx-guide line count and last-known sync date

---

## Check 9: README Links for PyPI (scope: library, all)

**Goal**: README.md uses only absolute URLs so links work on PyPI, GitHub, and locally.

**Source**: `streamtex/README.md`

**Rules**:
- WARNING if any markdown link uses a relative path (e.g., `[text](FILE.md)` instead of `[text](https://github.com/nicolasguelfi/streamtex/blob/main/FILE.md)`)
- PyPI renders README.md but does NOT resolve relative links — they become broken
- `stx publish check` also detects this (check "README links")
- INFO: report total links found and how many are absolute vs relative

**How to check**: Regex `\[([^\]]+)\]\((?!https?://|#)([^)]+)\)` finds relative links.

---

## Check 10: Language Consistency — English (scope: all)

**Goal**: All ecosystem content must be written in English, except explicitly exempted files.

**Scope**: All text content across the ecosystem.

**Files to check**:

| Category | Paths | What to check |
|----------|-------|---------------|
| Library code | `streamtex/streamtex/**/*.py` | Docstrings, comments, string literals in error messages |
| Manual blocks | `streamtex-docs/manuals/**/blocks/**/*.py` | `st_write()` text, `show_explanation()`, `show_details()`, `show_code()` descriptions, docstrings, comments |
| Manual book.py | `streamtex-docs/manuals/**/book.py` | TOC entries, banner text, section titles |
| Claude profiles | `streamtex-claude/profiles/**/*.md` | All markdown content |
| Claude commands | `streamtex-claude/profiles/**/commands/**/*.md` | Command descriptions and instructions |
| Claude skills | `streamtex-claude/profiles/**/skills/**/*.md` | Skill content |
| Claude agents | `streamtex-claude/profiles/**/agents/**/*.md` | Agent prompts and instructions |
| Shared references | `streamtex-claude/shared/references/*.md` | Cheatsheet, coding standards |
| Project templates | `streamtex-docs/templates/**/*.py` | Same rules as manual blocks |
| README files | `*/README.md` | Full content |
| CLAUDE.md files | `*/CLAUDE.md`, `projects/*/CLAUDE.md` | Full content |

**Explicit exceptions** (allowed in French or other languages):
- `streamtex-claude/shared/commands/stx-guide.md` — French by design (user-facing guide)
- `streamtex-claude/cursor/*.md` — Internal planning documents (not user-facing)
- Manual content that demonstrates multilingual features (e.g., i18n examples)
- Inline code identifiers (variable/function names are language-neutral)

**Rules**:
- ERROR if a Claude profile/command/skill/agent file contains non-English prose
- WARNING if a manual block contains non-English text in `st_write()`, `show_explanation()`, or `show_details()`
- WARNING if docstrings or comments in library code are not in English
- WARNING if a `CLAUDE.md` or `README.md` contains non-English prose
- INFO: report total files scanned and language status

**How to check**: For each file, sample text passages (docstrings, markdown paragraphs, `st_write()` string arguments). Flag content containing common non-English patterns:
- French indicators: words like `le`, `la`, `les`, `un`, `une`, `des`, `est`, `sont`, `avec`, `pour`, `dans`, `cette`, `nous`, `vous` in prose context
- Look for accented characters typical of French (`é`, `è`, `ê`, `ë`, `à`, `ù`, `ç`, `ô`, `î`) in non-code text
- Ignore: code identifiers, URLs, file paths, proper nouns

---

## Check 11: Claude Artifact API Validation (scope: profiles, all)

**Goal**: All Python code examples in Claude artifacts (skills, agents, commands) use correct, current StreamTeX API.

**Why this check is critical**: Users generate most of their project code via Claude artifacts (`/stx-block:update`, `/stx-block:init`, agents). If these artifacts contain incorrect API usage, every generated project inherits the bugs.

**Scope**: All `.md` files containing Python code blocks in:
- `streamtex-claude/profiles/**/skills/**/*.md`
- `streamtex-claude/profiles/**/agents/**/*.md`
- `streamtex-claude/profiles/**/commands/**/*.md`
- `streamtex-claude/shared/commands/*.md`

**Method**:
1. Extract all fenced Python code blocks (` ```python ... ``` `) from each `.md` file
2. For each code block, check the rules below against the actual library API
3. To verify the actual API, introspect the library:
   - `from streamtex.enums import ListTypes; dir(ListTypes)` → valid enum members
   - `from streamtex.enums import Tags; dir(Tags)` → valid tag names
   - `from streamtex import *; inspect.signature(st_list)` → valid parameters
   - `from streamtex import *; inspect.signature(st_image)` → valid parameters
   - (repeat for all `st_*` functions used in code blocks)

**Rules**:

### Enum validation
- ERROR if code uses `lt.ul` or `lt.ol` (correct: `lt.unordered`, `lt.ordered`)
- ERROR if code uses any `lt.<name>` where `<name>` is not in `dir(ListTypes)`
- ERROR if code uses any `t.<name>` where `<name>` is not in `dir(Tags)`

### Function signature validation
- ERROR if code passes a keyword argument that does not exist in the function signature
  - Example: `st_list(..., items=[...])` — `items` is not a parameter of `st_list()`
  - Example: `st_image(..., caption="...")` — `caption` is not a parameter of `st_image()`
- ERROR if code uses a function as a regular call when it is a context manager
  - Example: `st_list(style, items=[...])` should be `with st_list(...) as l:` + `l.item()`
- WARNING if code passes positional arguments in the wrong order vs. the signature

### st_grid validation
- ERROR if `cols` receives a Python list (e.g., `st_grid([1, 1])`) — must be `int` or `str`
- WARNING if code uses fixed columns without responsive pattern (same as coding standards rule)

### Cross-reference with cheatsheet
- WARNING if an artifact shows a pattern that contradicts the cheatsheet
- WARNING if an artifact uses a deprecated parameter (e.g., `banner_color` instead of `banner=BannerConfig(...)`)

**How to check** (automated introspection):
```bash
uv run python -c "
from streamtex.enums import ListTypes, Tags
print('ListTypes:', [x for x in dir(ListTypes) if not x.startswith('_')])
print('Tags:', [x for x in dir(Tags) if not x.startswith('_')])
"
uv run python -c "
import inspect
from streamtex import st_list, st_image, st_grid, st_write, st_code, st_space, st_block, st_overlay
for fn in [st_list, st_image, st_grid, st_write, st_code, st_space, st_block, st_overlay]:
    print(f'{fn.__name__}: {inspect.signature(fn)}')
"
```
Then for each code block, parse function calls and verify parameter names and enum values against the introspected API.

---

## Check 12: Test Coverage Sync (scope: library, tests, all)

**Goal**: Tests stay up-to-date when the library API changes. A modified or new public function should have corresponding test coverage, and existing tests should not use stale signatures.

**Why this check is critical**: Library changes (new parameters, renamed functions, modified behavior) can silently invalidate existing tests. Tests that pass but test the wrong thing (e.g., missing a new required parameter) give a false sense of safety.

**Source files**:
- `streamtex/streamtex/__init__.py` — public exports
- `streamtex/streamtex/*.py` — module source files (function signatures, classes)

**Target files**:
- `streamtex/tests/test_*.py` — all test files

### Sub-check 12a: Test file coverage

**Method**: For each source module `streamtex/<module>.py`, check if a corresponding `tests/test_<module>.py` exists.

**Rules**:
- WARNING if a source module with public functions has no corresponding test file
- WARNING if `test_presentation.py` does not exist (presentation module must have dedicated tests)
- INFO: report module → test file mapping and coverage ratio

**Known exceptions** (modules not expected to have dedicated test files):
- `__init__.py`, `constants.py`, `enums.py`, `utils.py` (tested indirectly)
- `block_helpers.py` — covered indirectly by `test_export_guard.py`
- `search.py` — covered indirectly by `test_book_search_markers.py`
- `loading.py` — JS overlay injection, requires live Streamlit runtime (tested indirectly via `test_book_integration.py`)
- Modules with only re-exports or trivial wrappers

### Sub-check 12b: Signature drift

**Method**: For each public function in `__init__.py`, introspect its current signature. Then grep all `test_*.py` files for calls to that function. Compare keyword arguments used in tests against the actual signature.

**Rules**:
- ERROR if a test calls a function with a keyword argument that no longer exists in the signature
- WARNING if a function gained a new parameter (not default-only) and no test exercises it
- WARNING if a function's parameter was renamed but tests still use the old name
- INFO: report total public functions checked and how many have test coverage

**How to check** (automated introspection):
```bash
uv run python -c "
import inspect, importlib
import streamtex
# Get all public exports
exports = [name for name in dir(streamtex) if not name.startswith('_')]
for name in sorted(exports):
    obj = getattr(streamtex, name)
    if callable(obj) and not isinstance(obj, type):
        sig = inspect.signature(obj)
        print(f'{name}: {sig}')
"
```
Then for each test file, parse function calls and compare keyword arguments against introspected signatures.

### Sub-check 12c: Deprecated API in tests

**Method**: Scan all `test_*.py` files for usage of deprecated patterns.

**Rules**:
- WARNING if a test imports a name that is no longer exported from `__init__.py`
- WARNING if a test uses a deprecated parameter (same list as Check 11 cross-reference)
- WARNING if a test mocks a function path that has been moved or renamed

### Sub-check 12d: New features without tests

**Method**: Compare recent git changes in `streamtex/*.py` against `tests/test_*.py`. For functions modified or added since the last release tag, check if corresponding tests exist.

**Rules**:
- WARNING if a new public function (added since last release) has zero test assertions
- WARNING if a function with modified signature (since last release) has no test exercising the new/changed parameters
- INFO: report functions changed since last release and their test status

**How to check**:
```bash
# List functions changed since last release tag
git diff $(git describe --tags --abbrev=0)..HEAD --name-only -- 'streamtex/*.py' | sort
# Then introspect each changed module for new/modified function signatures
```

---

## Check 13: Manual Blocks → Library API Existence (scope: docs, all)

**Goal**: Every `st_*` / `stx.*` function call in manual block **rendered code** must exist in the current library API. This is the reverse of Check 1.

**Why this check is critical**: Manuals are the user-facing documentation. If a block calls a function that was renamed, removed, or restructured in the library, the manual will crash at runtime — or worse, silently show nothing.

**Scope**: `streamtex-docs/manuals/**/blocks/**/*.py`

**What to check**: Rendered code ONLY — skip example strings inside `show_code()`, `show_explanation()`, `show_details()`.

**Method**:
1. Build the list of all valid exports: read `streamtex/streamtex/__init__.py`, extract all names
2. For each block file, extract all `st_*` and `stx.*` function calls at **block indentation level** (outside triple-quoted strings)
3. Verify each call exists in the exports list

**How to distinguish rendered vs example code**:
- Code **inside** `show_code("""...""")`, `show_explanation("""...""")`, `show_details("""...""")` string arguments → SKIP (example only, shown to user)
- Code **inside** `show_code(file="...")` → SKIP (example loaded from file)
- `st_*()` calls at block indentation level (inside `def build():`) → CHECK (executed at runtime)
- Calls inside `with st_block(...)`, `with st_grid(...)`, `with st_list(...)` → CHECK

**Rules**:
- ERROR if a rendered `st_*()` call references a function not in `__init__.py` exports
- ERROR if a rendered call uses `stx.<name>` where `<name>` is not an attribute of the `streamtex` module
- WARNING if a block imports a submodule path that no longer exists (e.g., `from streamtex.foo import bar`)
- INFO: report total rendered calls checked, how many are valid, how many blocks scanned

**How to check** (automated introspection):
```bash
uv run python -c "
import streamtex
exports = [n for n in dir(streamtex) if not n.startswith('_')]
print('\n'.join(sorted(exports)))
"
```
Then for each block, parse rendered `st_*()` calls and verify against the exports list.

---

## Check 14: Manual Examples Signature Coherence (scope: docs, all)

**Goal**: Function call signatures used in manual `show_code()` examples must match the current library function signatures (parameter names, parameter existence).

**Why this check is critical**: Users copy-paste code from `show_code()` examples. If an example uses a parameter that was renamed or removed, the user's code breaks. This erodes trust in the documentation.

**Scope**: `streamtex-docs/manuals/**/blocks/**/*.py` — specifically the content inside `show_code()` string arguments.

**Method**:
1. Introspect the library to get current signatures for all major `st_*` functions
2. For each block file, extract code from `show_code("""...""")` string arguments
3. Parse `st_*()` function calls within those strings
4. Compare keyword arguments against the actual function signature

**Rules**:
- ERROR if an example uses a keyword argument that does not exist in the function signature
  - Example: `st_image(caption="...")` but `st_image` has no `caption` parameter
  - Example: `st_list(items=[...])` but `st_list` has no `items` parameter
- ERROR if an example calls a function that no longer exists in the library
- WARNING if an example uses a deprecated parameter (even if still accepted for backward compat)
- WARNING if an example shows a context manager usage for a non-context-manager function, or vice versa
  - Example: `with st_write(...)` — `st_write` is NOT a context manager
  - Example: `st_list(style, items=[...])` — `st_list` IS a context manager
- WARNING if an example shows positional arguments in the wrong order vs the signature
- INFO: report total examples checked, total `st_*` calls in examples, issues found

**How to check** (automated introspection):
```bash
uv run python -c "
import inspect
from streamtex import st_list, st_image, st_grid, st_write, st_code, st_space, st_block, st_span
from streamtex import st_book, st_collection, st_markdown, st_mermaid, st_plantuml, st_tikz, st_latex
from streamtex import st_ai_image, st_ai_image_widget, st_slide_break, st_br, st_overlay
from streamtex import show_code, show_explanation, show_details, show_code_inline
for fn in [st_list, st_image, st_grid, st_write, st_code, st_space, st_block, st_span,
           st_book, st_collection, st_markdown, st_mermaid, st_plantuml, st_tikz, st_latex,
           st_ai_image, st_ai_image_widget, st_slide_break, st_br, st_overlay,
           show_code, show_explanation, show_details, show_code_inline]:
    print(f'{fn.__name__}: {inspect.signature(fn)}')
"
```
Then for each `show_code()` string, parse function calls and verify keyword arguments.

**Interaction with Check 11**: Check 11 validates code in Claude artifacts (skills, agents, commands). Check 14 validates code in manual `show_code()` examples. Together they cover all user-facing code examples in the ecosystem.

---

## Check 15: Manual Enum & Constant Coherence (scope: docs, all)

**Goal**: All enum members, class attributes, and constant values referenced in manual blocks (both rendered and examples) must exist in the current library.

**Why this check is critical**: Enums and constants are frequently refactored (renamed, reorganized, deprecated). A block using `ListTypes.ul` when the correct member is `ListTypes.unordered` will crash silently or raise an AttributeError at runtime.

**Scope**: `streamtex-docs/manuals/**/blocks/**/*.py` (both rendered code and `show_code()` examples)

**Method**:
1. Introspect the library to get valid members for all key enums and classes
2. For each block file, extract all attribute accesses on known types
3. Verify each attribute exists

**Enums and classes to validate**:

| Import | Variable | Valid members (introspect to get full list) |
|--------|----------|---------------------------------------------|
| `from streamtex.enums import ListTypes` | `lt` | `unordered`, `ordered`, `custom`, ... |
| `from streamtex.enums import Tags` | `t` | `div`, `span`, `p`, `h1`-`h6`, ... |
| `from streamtex import PdfMode` | — | `CONTINUOUS`, `PAGINATED` |
| `from streamtex import PdfConfig` | — | `mode`, `format`, `landscape`, `scale`, `margins`, ... |
| `from streamtex import ExportConfig` | — | Constructor parameters |
| `from streamtex import BannerConfig` | — | Constructor parameters |
| `from streamtex import AIImageConfig` | — | Constructor parameters |
| `from streamtex import PresentationConfig` | — | Constructor parameters (`title`, `aspect_ratio`, `footer`, `center_content`, `hide_streamlit_header`, `enforce_ratio`) |
| `from custom.styles import Styles` | `s` | Project-specific (skip — not library) |

**Rules**:
- ERROR if code accesses `lt.<member>` where `<member>` is not in `dir(ListTypes)`
- ERROR if code accesses `t.<member>` where `<member>` is not in `dir(Tags)`
- ERROR if code accesses `PdfMode.<member>` where `<member>` is not a valid variant
- ERROR if code constructs `PdfConfig(...)` or `ExportConfig(...)` with invalid keyword arguments
- WARNING if code uses an enum member that exists but is deprecated
- INFO: report total enum/constant references checked and validation results

**How to check** (automated introspection):
```bash
uv run python -c "
from streamtex.enums import ListTypes, Tags
from streamtex import PdfMode, PdfConfig, ExportConfig, BannerConfig
import inspect
for cls in [ListTypes, Tags, PdfMode]:
    members = [x for x in dir(cls) if not x.startswith('_')]
    print(f'{cls.__name__}: {members}')
for cls in [PdfConfig, ExportConfig, BannerConfig]:
    print(f'{cls.__name__}: {inspect.signature(cls)}')
"
```

---

## Check 16: Static File Existence (scope: docs, blocks, all)

**Goal**: Every file referenced by a rendered call in manual blocks must exist on disk.

**Scope**: `streamtex-docs/manuals/**/blocks/**/*.py`

**What to check**: Scan block files for runtime file references (NOT inside `show_code()` strings — those are examples). Specifically:

1. **Images**: `st_image(uri="<path>")` where `<path>` is NOT a URL (`https://` or `http://`). Resolve against the manual's `static/images/` directory (or the path set by `configure_image_path()`).
2. **show_code(file="<path>")**: Resolve against the manual's `static/` directory.
3. **open() calls**: e.g., `open(text_path)` where path is built with `os.path.join(_static_dir, ...)`. Verify the target file exists.
4. **st_audio() / st_video()**: Local file paths (not URLs). Resolve against `static/`.
5. **Repo-level files**: Blocks reading files from `_repo_root` or similar variables. Verify the file exists at the repo root.

**How to distinguish example vs rendered code**:
- Code inside `show_code("""...""")` string arguments → SKIP (example only)
- Code inside `show_code(file="...")` → CHECK the `file=` path (it's loaded at runtime)
- Bare `st_image()`, `open()`, `st_audio()`, `st_video()` calls at block indentation level → CHECK

**Resolution rules**:
- Each manual has its own `static/` directory at `manuals/<manual_name>/static/`
- `configure_image_path("app/static/images")` → files served by Streamlit at `static/images/<file>`
- `set_static_sources([...])` in `book.py` adds additional search paths
- `resolve_static("path")` uses the block registry's static sources

**Rules**:
- ERROR if a rendered `st_image(uri=)` references a local file that does not exist
- ERROR if a `show_code(file=)` references a file that does not exist
- ERROR if an `open()` call references a file that does not exist
- WARNING if `st_audio()` or `st_video()` references a missing local file
- WARNING if a repo-level file reference (Dockerfile, CI config, etc.) does not exist
- INFO: report total static references checked and how many are valid

---

## Check 17: CHANGELOG Freshness (scope: library, all)

**Goal**: The CHANGELOG.md accurately reflects the current library version and recent changes.

**Source**: `streamtex/CHANGELOG.md` + `streamtex/pyproject.toml` (version)

**Rules**:
- ERROR if the library version in `pyproject.toml` has no matching `## [X.Y.Z]` entry in CHANGELOG.md
- WARNING if the latest CHANGELOG entry has no `### Added`, `### Changed`, `### Fixed`, or `### Removed` subsection
- WARNING if CHANGELOG entries are not in reverse chronological order
- INFO: report current library version and latest CHANGELOG version

---

## Check 18: Manifest File Existence (scope: profiles, all)

**Goal**: Every file declared in a profile's `manifest.toml` must physically exist at the path resolved by `install.py`'s `CATEGORY_PATHS` mapping.

**Why this check is critical**: The CI (`validate.yml`) catches this on push, but catching it locally before pushing avoids broken CI runs. A manifest that declares files which don't exist means `install.py` will silently skip them, and users won't get the expected commands/skills/agents.

**Scope**: `streamtex-claude/profiles/*/manifest.toml`

**Method**:
1. For each profile directory in `streamtex-claude/profiles/`:
   - Read `manifest.toml`
   - For each category (`[commands]`, `[skills]`, `[agents]`, `[templates]`, `[tools]`):
     - Resolve the subdirectory using `CATEGORY_PATHS` mapping:
       - `commands.<subdir>` → `commands/<subdir>/`
       - `skills.designer` → `designer/skills/`
       - `skills.developer` → `developer/skills/`
       - `agents.designer` → `designer/agents/`
       - `templates.designer` → `designer/templates/`
       - `tools.designer` → `designer/tools/`
     - For each file in the list, verify `profiles/<profile>/<resolved_path>/<file>` exists
   - For `[shared]`:
     - `references` → verify each file exists in `shared/references/`
     - `commands` → verify each file exists in `shared/commands/`

**Rules**:
- ERROR if a declared file does not exist at the resolved path
- ERROR if a `[shared]` reference file does not exist in `shared/references/` or `shared/commands/`
- WARNING if a profile has no `manifest.toml`
- INFO: report total files declared vs found per profile

**Example of what this catches**:
- `documentation/manifest.toml` declares `stx-block = ["init.md", ...]` but `documentation/commands/stx-block/` does not exist → 5 ERRORS
- `project/manifest.toml` declares `shared.references = ["presentation_cheatsheet_en.md"]` but `shared/references/presentation_cheatsheet_en.md` is missing → 1 ERROR

---

## Check 19: CLI Template Registry Sync (scope: profiles, all)

**Goal**: The CLI template registry, the `click.Choice` validator, the template directories on disk, and the documentation are all synchronized.

**Why this check is critical**: A template can be added to `AVAILABLE_TEMPLATES` but forgotten in `click.Choice` (users get a rejection error), or a template directory can be created but never registered (users can't use it). The documentation may also list incorrect templates, confusing users.

**Source files**:
- `streamtex/streamtex/cli/install_cmd.py` → `AVAILABLE_TEMPLATES` list
- `streamtex/streamtex/cli/project_cmd.py` → `click.Choice([...])` in `--template` option
- `streamtex-docs/templates/` → directories matching `template_*/`
- `streamtex-claude/shared/commands/stx-guide.md` → CLI template references
- `streamtex/README.md` → template references in Quick Start section

**Method**:
1. Extract `AVAILABLE_TEMPLATES` from `install_cmd.py` (parse the Python list literal)
2. Extract the `click.Choice` list from `project_cmd.py` (parse the list in `type=click.Choice([...])`)
3. List directories matching `streamtex-docs/templates/template_*/`, extract names (strip `template_` prefix)
4. Extract template names mentioned in stx-guide.md CLI sections (look for `--template` references with `[...|...|...]` syntax)
5. Extract template names mentioned in README.md (look for `--template` in code blocks)

**Rules**:
- ERROR if `AVAILABLE_TEMPLATES` differs from the `click.Choice` list (these MUST be identical)
- ERROR if a directory `template_<name>` exists in `streamtex-docs/templates/` but `<name>` is not in `AVAILABLE_TEMPLATES`
- ERROR if a name is in `AVAILABLE_TEMPLATES` but no `template_<name>` directory exists
- WARNING if stx-guide.md CLI template list differs from `AVAILABLE_TEMPLATES`
- WARNING if README.md template list differs from `AVAILABLE_TEMPLATES`
- INFO: report all 4 sets and their alignment status

**Important distinction** (do NOT flag as errors):
- stx-block templates (`/stx-block:init --template`) are Claude AI blueprints stored in `profiles/project/designer/templates/`. These are a DIFFERENT system from CLI templates and should NOT be compared to `AVAILABLE_TEMPLATES`.
- Only flag mismatches for CLI template references (identified by `stx project new --template` or `stx install --template` context).

---

## Check 20: GitHub Issue Template & Command Sync (scope: profiles, all)

**Goal**: All three StreamTeX repositories have consistent GitHub issue templates, and the shared `stx-issue/` command directory exists with all 6 command files.

**Why this check is critical**: Issue templates ensure a consistent experience for users creating issues via the web or via `/stx-issue:*`. Missing templates in one repo but not others creates confusion. Missing command files cause silent installation failures.

**Source files**:
- `streamtex/.github/ISSUE_TEMPLATE/` → bug_report.md, feature_request.md, question.md, docs.md
- `streamtex-docs/.github/ISSUE_TEMPLATE/` → same 4 files
- `streamtex-claude/.github/ISSUE_TEMPLATE/` → same 4 files
- `streamtex-claude/shared/commands/stx-issue/` → 6 files: bug.md, feature.md, question.md, docs.md, comment.md, list.md
- `streamtex-claude/profiles/*/manifest.toml` → `[shared] commands` must include `"stx-issue"`

**Method**:
1. For each repo (streamtex, streamtex-docs, streamtex-claude):
   - Verify `.github/ISSUE_TEMPLATE/` directory exists
   - Verify all 4 template files exist: `bug_report.md`, `feature_request.md`, `question.md`, `docs.md`
   - Verify templates have correct YAML frontmatter (name, about, labels)
2. Verify `shared/commands/stx-issue/` contains all 6 files: `bug.md`, `feature.md`, `question.md`, `docs.md`, `comment.md`, `list.md`
3. Verify all profiles include `"stx-issue"` in their `[shared] commands` list
4. Verify stx-guide.md references `/stx-issue:*` in topics table and Section 6
5. Verify NO profile still has legacy `commands/stx-project/` directory (migrated to stx-issue)

**Rules**:
- ERROR if a repo is missing `.github/ISSUE_TEMPLATE/` directory
- ERROR if any of the 4 template files is missing from a repo
- ERROR if `shared/commands/stx-issue/` is missing any of the 6 command files
- ERROR if a profile does not include `"stx-issue"` in `[shared] commands`
- ERROR if any profile still has legacy `commands/stx-project/` or `commands/stx-designer/` or `commands/stx-developer/` directories
- WARNING if issue templates differ between repos (content should be consistent)
- WARNING if stx-guide.md does not reference `/stx-issue:*`
- INFO: report template existence status across all repos and profiles

---

## Check 21: Command Namespace stx- Prefix Convention (scope: profiles, all)

**What**: All command namespace directories and their references must use the `stx-` prefix convention. No bare namespace directories (e.g. `developer/`, `project/`, `designer/`) should exist under `commands/`.

**Why**: Consistent `stx-` prefix avoids user confusion — if `/stx-block:init` exists, users expect `/stx-block:collection-new`, not `/project:collection-new`.

**Source files**:
- `streamtex-claude/profiles/*/commands/` → directory names
- `streamtex-claude/profiles/*/manifest.toml` → `[commands]` keys
- All `.md`, `.j2`, `.py` files across the 3 repos → slash command references

**Method**:
1. Scan all `profiles/*/commands/` directories — every subdirectory name must start with `stx-`
2. Scan all `manifest.toml` `[commands]` keys — every key must start with `stx-`
3. Grep all 3 repos for bare namespace patterns: `/project:`, `/designer:`, `/developer:`, `/migration:`, `/coherence:`, `/presentation:` (without `stx-` prefix)
4. Grep for old path references: `commands/project/`, `commands/developer/`, `commands/designer/`, `commands/migration/`, `commands/coherence/`, `commands/presentation/`

**Rules**:
- ERROR if a command directory under `commands/` does not start with `stx-`
- ERROR if a manifest `[commands]` key does not start with `stx-`
- ERROR if any file contains a bare namespace slash command reference (e.g. `/developer:test-run` instead of `/stx-block:test`)
- WARNING if any file contains a bare namespace path reference (e.g. `commands/project/` instead of `commands/stx-block/`)
- INFO: report all namespace directories found and their prefix status

---

## Check 22: Release & Deploy Pipeline Coherence (scope: library, all)

**Goal**: The release pipeline (git tag → PyPI → lock file → Render deploy → GitHub Release) is fully consistent. Every step must be completed and synchronized.

**Why this check is critical**: Missing any step in the release pipeline causes silent failures: Render installs the wrong version from PyPI, GitHub shows an outdated "Latest" badge, lock files reference non-existent versions, or users install an old version. This check was added after a session where multiple pipeline steps were skipped, causing hours of debugging.

**Source files**:
- `streamtex/pyproject.toml` → `[project] version`
- `streamtex/streamtex/__init__.py` → `__version__`
- `streamtex/CHANGELOG.md` → latest `## [X.Y.Z]` entry
- Git tags: `git tag --sort=-creatordate | head -1`
- PyPI: `curl -s https://pypi.org/pypi/streamtex/json | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])"`
- `streamtex-docs/uv.lock` → `name = "streamtex"` version
- GitHub Releases: `gh release list -R nicolasguelfi/streamtex --limit 1`
- Render deploy: `gh run list -R nicolasguelfi/streamtex-docs --workflow=render-deploy.yml --limit=1 --json conclusion`

**Method**:
1. Read the library version from `pyproject.toml` and `__init__.py` — they MUST match
2. Read the latest CHANGELOG entry version — MUST match library version
3. Read the latest git tag — MUST match library version (format: `vX.Y.Z`)
4. Query PyPI for the latest published version — MUST match library version
5. Read `streamtex-docs/uv.lock` streamtex version — MUST match PyPI version
6. Query GitHub Releases for the latest release — MUST match library version
7. Query the last Render deploy workflow run — MUST be `success`

**Rules**:
- ERROR if `pyproject.toml` version ≠ `__init__.py` `__version__`
- ERROR if CHANGELOG latest entry ≠ library version
- ERROR if latest git tag ≠ `v{library_version}`
- ERROR if PyPI latest version ≠ library version (library not published)
- ERROR if `streamtex-docs/uv.lock` streamtex version ≠ PyPI latest (lock file stale)
- ERROR if no GitHub Release exists for the library version
- WARNING if the latest Render deploy workflow run is `failure`
- WARNING if the GitHub Release for the library version is not marked as "Latest"
- INFO: report the complete pipeline state (version, tag, PyPI, lock, release, deploy)

**How to check** (automated):
```bash
# Library version
LIB_VER=$(grep 'version =' streamtex/pyproject.toml | head -1 | sed 's/.*"\(.*\)".*/\1/')
INIT_VER=$(grep '__version__' streamtex/streamtex/__init__.py | sed 's/.*"\(.*\)".*/\1/')
CHANGELOG_VER=$(grep '^## \[' streamtex/CHANGELOG.md | head -1 | sed 's/.*\[\(.*\)\].*/\1/')
GIT_TAG=$(cd streamtex && git tag --sort=-creatordate | head -1)
PYPI_VER=$(curl -s https://pypi.org/pypi/streamtex/json | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])")
LOCK_VER=$(grep -A1 'name = "streamtex"' streamtex-docs/uv.lock | grep version | head -1 | sed 's/.*"\(.*\)".*/\1/')
GH_RELEASE=$(gh release list -R nicolasguelfi/streamtex --limit 1 --json tagName,isLatest -q '.[0].tagName')
RENDER_STATUS=$(gh run list -R nicolasguelfi/streamtex-docs --workflow=render-deploy.yml --limit=1 --json conclusion -q '.[0].conclusion')

echo "pyproject.toml: $LIB_VER"
echo "__init__.py:    $INIT_VER"
echo "CHANGELOG:      $CHANGELOG_VER"
echo "Git tag:        $GIT_TAG"
echo "PyPI:           $PYPI_VER"
echo "Lock file:      $LOCK_VER"
echo "GitHub Release: $GH_RELEASE"
echo "Render deploy:  $RENDER_STATUS"
```

**Release pipeline checklist** (correct order):
1. Bump version in `pyproject.toml` + `__init__.py` + `CHANGELOG.md`
2. Commit + push to GitHub
3. `uv build && uv publish --token $PYPI_TOKEN`
4. `git tag vX.Y.Z && git push origin vX.Y.Z`
5. `gh release create vX.Y.Z --title "..." --notes "..." --latest`
6. Update `streamtex-docs/uv.lock`: `uv lock --upgrade-package streamtex`
7. Commit + push streamtex-docs
8. `gh workflow run render-deploy.yml -R nicolasguelfi/streamtex-docs`
9. Verify deploy success

---

## Check 23: CE Agent Sync (scope: profiles, all)

**Goal**: All 18 CE agents declared in `manifest.toml` exist as files in `ce/agents/`.

**Source files**: `streamtex-claude/profiles/project/manifest.toml` — `[agents] ce` list.

**Target files**: `streamtex-claude/profiles/project/ce/agents/*.md`

**Rules**:
- ERROR if a manifest entry has no corresponding `.md` file in `ce/agents/`
- ERROR if a `.md` file exists in `ce/agents/` but is not listed in the manifest
- INFO: report total agents declared vs found

**Expected agents (18)**: source-scanner, import-assessor, audience-analyst, content-strategist, gap-analyst, format-explorer, angle-generator, structure-architect, domain-researcher, learnings-researcher, audience-advocate, pedagogy-analyst, visual-reviewer, style-consistency-checker, content-editor, feedback-detector, dev-governance, ad-hoc-reviewer.

---

## Check 24: CE Template Sync (scope: profiles, all)

**Goal**: All 16 CE templates declared in `manifest.toml` exist as files in `ce/templates/`.

**Source files**: `streamtex-claude/profiles/project/manifest.toml` — `[templates] ce` list.

**Target files**: `streamtex-claude/profiles/project/ce/templates/*.md`

**Rules**:
- ERROR if a manifest entry has no corresponding `.md` file in `ce/templates/`
- ERROR if a `.md` file exists in `ce/templates/` but is not listed in the manifest
- INFO: report total templates declared vs found

**Expected templates (16)**: collect-report, assess-import, assess-improve, assess-create, plan-import, plan-improve, plan-create, review-report, solution, producer-profile, feedback-summary, dev-report, task-review, coverage-matrix, task-analysis, task-report.

---

## Check 25: CE Docs Structure (scope: projects, all)

**Goal**: Projects with CE profile installed have the correct `docs/` directory structure.

**Scope**: All directories in `projects/` with `.claude/.stx-profile` marker.

**Rules**:
- WARNING if `docs/` directory does not exist (CE artifacts have nowhere to go)
- WARNING if any of the 5 required subdirectories are missing: `collect/`, `assess/`, `plans/`, `reviews/`, `solutions/`
- WARNING if `docs/solutions/` is missing any of the 9 category subdirectories: `structure/`, `style/`, `content/`, `process/`, `pedagogy/`, `assets/`, `deployment/`, `import/`, `governance/`
- INFO: report projects scanned and structure status

---

## Check 26: CE Cheatsheet Sync (scope: profiles, all)

**Goal**: The CE cheatsheet is present, up-to-date, and consistent with the manifest.

**Source files**: `streamtex-claude/shared/references/ce_cheatsheet_en.md`

**Rules**:
- ERROR if `ce_cheatsheet_en.md` does not exist
- ERROR if the cheatsheet does not list all 11 commands (`collect`, `assess`, `plan`, `produce`, `review`, `fix`, `compound`, `go`, `status`, `task`, `continue`)
- WARNING if the cheatsheet agent count does not match manifest (expected: 18)
- WARNING if the cheatsheet template count does not match manifest (expected: 16)
- WARNING if the cheatsheet does not mention the 7-phase cycle with FIX
- INFO: report cheatsheet presence and consistency

---

## Check 27: CE Command Registration (scope: profiles, all)

**Goal**: All 11 CE commands declared in `manifest.toml` exist as files in `commands/stx-ce/`.

**Source files**: `streamtex-claude/profiles/project/manifest.toml` — `[commands] stx-ce` list.

**Target files**: `streamtex-claude/profiles/project/commands/stx-ce/*.md`

**Rules**:
- ERROR if a manifest entry has no corresponding `.md` file in `commands/stx-ce/`
- ERROR if a `.md` file exists in `commands/stx-ce/` but is not listed in the manifest
- WARNING if the corresponding skill file in `ce/skills/` does not exist for each command
- INFO: report total commands declared vs found

**Expected commands (11)**: collect, assess, plan, produce, review, fix, compound, go, status, task, continue.
**Expected skills (11)**: ce-collect, ce-assess, ce-plan, ce-produce, ce-review, ce-fix, ce-compound, ce-go, ce-status, ce-task, ce-continue.

---

## Check 28: CE Plan-Solution Coherence (scope: projects, all)

**Goal**: CE artifacts within a project are internally consistent.

**Scope**: All projects in `projects/` that have a `docs/plans/` directory with at least one plan file.

**Rules**:
- WARNING if a plan references block names (e.g., `bck_xxx`) that do not exist in `blocks/`
- WARNING if `docs/reviews/` contains a review but `docs/plans/` is empty (review without plan)
- WARNING if `docs/solutions/` contains solutions but `docs/reviews/` is empty (compound without review)
- WARNING if `docs/solutions/producer-profile.md` has `projects_count` > 0 but `last_updated` is more than 90 days old (stale profile)
- INFO: report CE artifact presence and coherence per project

---

# AI Quality Checks (scope: ai, all)

These checks detect problems specifically caused by AI-generated code and content. They address known failure modes of generative AI: hallucinated APIs, semantic drift between explanations and code, redundant abstractions, optimistic tests, and leaked secrets.

---

## Check 29: Ghost API Calls (scope: ai, all)

**Goal**: Detect function calls, parameters, and imports that reference StreamTeX API symbols which do not exist — "hallucinated" by the AI during code generation.

**Why this check is critical**: When AI generates code, it may invent plausible-sounding functions (`st_card()`, `st_tabs()`, `st_sidebar()`), parameters (`st_write(font_size=12)`), or imports (`from streamtex import st_dashboard`). These errors propagate to every project generated in the same session. Checks 13-14 partially cover this for docs blocks and show_code() examples, but this check extends coverage to **all generated code** across the ecosystem.

**Scope**: All Python files and Python code blocks in markdown across the entire ecosystem:
- `streamtex-docs/manuals/**/blocks/**/*.py` (rendered code — complements Check 13)
- `streamtex-docs/templates/**/*.py`
- `projects/**/*.py`
- `streamtex-claude/profiles/**/*.md` (Python code blocks — complements Check 11)
- `streamtex-claude/shared/**/*.md` (Python code blocks)

**Method**:
1. Build the complete valid API surface: read `streamtex/streamtex/__init__.py`, extract all exported names
2. For Python files: extract all `st_*()` and `stx.*` calls, verify each exists in exports
3. For Markdown files: extract fenced Python code blocks (` ```python ... ``` `), parse `st_*()` calls within them
4. For each call, also verify keyword arguments against `inspect.signature()` of the function
5. Cross-reference `from streamtex import X` statements — verify `X` exists in exports

**Rules**:
- ERROR if a `st_*()` call references a function not in `__init__.py` exports
- ERROR if a `from streamtex import X` imports a name not in `__init__.py` exports
- ERROR if a keyword argument does not exist in the function's signature
- WARNING if a function is called with positional arguments in wrong order vs signature
- INFO: report total calls scanned, total files scanned, and ghost calls found

**How to check** (automated introspection):
```bash
uv run python -c "
import inspect, streamtex
exports = {n for n in dir(streamtex) if not n.startswith('_')}
st_fns = {n: getattr(streamtex, n) for n in exports if n.startswith('st_') and callable(getattr(streamtex, n))}
for name, fn in sorted(st_fns.items()):
    print(f'{name}: {inspect.signature(fn)}')
print(f'\nTotal exports: {len(exports)}')
print(f'st_* functions: {len(st_fns)}')
"
```

**Difference from Checks 11, 13, 14**: Those checks cover specific scopes (Claude artifacts, rendered block code, show_code examples). Check 29 provides **unified cross-ecosystem coverage** including projects and templates, and specifically targets AI hallucination patterns (invented functions, plausible but non-existent parameters).

---

## Check 30: Dead Code in Documentation Blocks (scope: ai, all)

**Goal**: Detect unused variables, unreachable code, and orphan definitions in documentation blocks — artifacts of AI copy-paste patterns where code is duplicated then partially modified.

**Why this check is critical**: AI frequently copies a working pattern, modifies part of it, but leaves the original code in place. This results in variables assigned but never read, functions defined but never called, and imports used only in commented-out code. These create confusion for users reading the blocks as learning material.

**Scope**: `streamtex-docs/manuals/**/blocks/**/*.py` + `streamtex-docs/templates/**/*.py`

**Method**:
1. For each block file, parse the Python AST
2. Detect dead code patterns:
   - Variables assigned but never referenced after assignment (excluding `bs = BlockStyles` which is used by the framework)
   - Functions `def` defined but never called within the same file
   - `import` statements where the imported name is never used in the file (beyond ruff F401 which is suppressed)
   - `if False:` or `if 0:` blocks (AI sometimes disables code this way)
   - Consecutive duplicate function calls with identical arguments (AI stuttering)
3. Exclude framework-required patterns: `bs = BlockStyles`, `def build()`, `class BlockStyles`

**Rules**:
- WARNING if a variable is assigned but never referenced (excluding `bs`, `_static_dir`, `_repo_root`)
- WARNING if a function is defined but never called in the file
- WARNING if an import is never used (and is not `streamtex` or `custom.styles`)
- WARNING if consecutive identical calls exist (e.g., two `st_write()` with same content)
- INFO: report total blocks scanned, total dead code instances found

**Known exceptions**:
- `bs = BlockStyles` — used by the framework's block rendering
- `_static_dir`, `_repo_root` — path variables used in file operations
- Variables starting with `_` — intentionally unused (Python convention)

---

## Check 31: Explanation ↔ Code Drift (scope: ai, all)

**Goal**: Detect inconsistencies between `show_explanation()` text and the actual code demonstrated in the same block — where the AI updated the code but forgot to update the explanation, or vice versa.

**Why this check is critical**: AI updates code and explanations independently. When modifying a block, it may change a function call (e.g., rename a parameter) but leave the explanation referring to the old parameter name. Users then see a correct code example accompanied by an incorrect explanation, which is more confusing than no explanation at all.

**Scope**: `streamtex-docs/manuals/**/blocks/**/*.py` — blocks that contain both `show_explanation()` and either rendered code or `show_code()`.

**Method**:
1. For each block file, extract:
   - All `st_*` function names and parameter names used in rendered code and `show_code()` examples
   - All function/parameter names mentioned in `show_explanation()` and `show_details()` text
2. Cross-reference:
   - Function names mentioned in explanation but not present in code → drift
   - Parameter names mentioned in explanation but not used in code → drift
   - Code uses a function/parameter not mentioned in explanation → acceptable (explanation may be selective)
3. Verify mentioned names against actual library API (combining with Check 29 data)

**Rules**:
- WARNING if `show_explanation()` mentions a function name that does not appear in the block's code
- WARNING if `show_explanation()` mentions a parameter name (in backticks like `` `param_name` `` or in prose like "the param_name argument") that is not used in the block's code
- WARNING if `show_explanation()` mentions an enum member (e.g., "ListTypes.ul") that differs from what the code actually uses
- WARNING if `show_explanation()` describes a behavior ("returns X", "takes Y as input") that contradicts the function's current signature
- INFO: report total blocks with explanations, total drift instances found

**How to detect parameter/function mentions in prose**:
- Backtick patterns: `` `st_list` ``, `` `l_style` ``, `` `font_size` ``
- Prose patterns: "the `st_list` function", "using the `l_style` parameter", "pass `ordered` to"
- Ignore: generic English words that happen to match parameter names (context-dependent)

---

## Check 32: Cross-Block Contradictions (scope: ai, all)

**Goal**: Detect cases where two or more blocks demonstrate the same feature with contradictory patterns — where AI generated inconsistent examples across separate sessions.

**Why this check is critical**: AI lacks memory between sessions. If block A was generated in session 1 showing `st_list(style=arrows)` and block B was generated in session 2 showing `with st_list(l_style="arrows") as l:`, users encounter contradictory documentation. One pattern may be correct and the other hallucinated.

**Scope**: `streamtex-docs/manuals/**/blocks/**/*.py`

**Method**:
1. Build an index: for each `st_*` function, collect all blocks that use it (both rendered and show_code)
2. For each function used in 2+ blocks:
   - Extract the usage pattern (parameter names, context manager vs direct call, style patterns)
   - Compare patterns across blocks
   - Flag contradictions
3. Focus on high-value functions: `st_list`, `st_grid`, `st_image`, `st_block`, `st_write`, `st_code`, `st_overlay`, `st_space`, `st_marker`, `st_mermaid`, `show_code`, `show_explanation`, `show_details`

**Rules**:
- ERROR if one block uses a function as a context manager while another uses it as a direct call (for functions that are exclusively one or the other)
- WARNING if two blocks use different parameter names for the same concept on the same function (e.g., `style=` vs `l_style=`)
- WARNING if two blocks show mutually exclusive enum values as defaults (e.g., one says default is `ListTypes.unordered`, another says `ListTypes.ordered`)
- WARNING if two blocks show contradictory style patterns for the same visual effect
- INFO: report total functions indexed, total blocks per function, contradictions found

**Known acceptable variations**:
- Different examples showing different use cases of the same function (e.g., `st_list` with ordered vs unordered) — these are NOT contradictions
- Progressive complexity (intro block shows simple usage, advanced block shows full API) — NOT a contradiction
- The check targets **structural contradictions** (wrong parameter names, wrong call patterns), not **pedagogical variations**

---

## Check 33: Duplicate Logic Detection (scope: ai, all)

**Goal**: Detect cases where AI recreated existing utility functions or patterns instead of reusing them — resulting in duplicated logic across the codebase.

**Why this check is critical**: AI cannot browse the full codebase before generating code. It may recreate a helper function that already exists in a different module, leading to maintenance burden and potential divergence between the copies.

**Scope**: `streamtex/streamtex/**/*.py` (library source code)

**Method**:
1. Scan all Python files in the library for function definitions (`def` statements)
2. For each pair of functions, compare:
   - Function names: flag if two functions have very similar names (edit distance ≤ 2)
   - Function bodies: flag if two functions have structurally identical bodies (ignoring variable names)
   - Docstrings: flag if two functions have identical docstrings but different implementations
3. Exclude test files, `__init__.py` re-exports, and `@overload` decorators

**Rules**:
- WARNING if two functions in different modules have identical bodies (>5 lines)
- WARNING if two functions have near-identical names but different signatures (potential naming collision)
- INFO: report total functions scanned, duplicates found

---

## Check 34: Orphan Abstractions (scope: ai, all)

**Goal**: Detect configuration classes, registries, or factory patterns that are used by only one caller — over-engineering introduced by AI's tendency to abstract prematurely.

**Why this check is critical**: AI tends to create elaborate abstractions (config dataclasses, registry patterns, strategy patterns) even for functionality with a single use site. These orphan abstractions add cognitive load without providing reuse value.

**Scope**: `streamtex/streamtex/**/*.py` (library source code)

**Method**:
1. Identify abstraction patterns: classes with "Config", "Registry", "Factory", "Manager", "Provider" in their name
2. For each, count the number of distinct call sites across the library (excluding tests and the file where it's defined)
3. Flag abstractions with ≤ 1 external call site

**Rules**:
- INFO if a Config/Registry/Factory class is used by only 1 external caller (potential over-abstraction)
- INFO: report total abstractions found, usage counts

**Known exceptions**:
- `AIImageConfig`, `BibConfig`, `GSheetConfig`, `LinkConfig`, `BlockHelperConfig` — DI pattern, used via `set_*/get_*` in user code (book.py)
- `PresentationConfig`, `SlideBreakConfig`, `SpacingConfig` — same DI pattern
- Any class exported in `__init__.py` — intended for user consumption

---

## Check 35: Unused Exports (scope: ai, all)

**Goal**: Detect symbols exported in `__init__.py` that are neither tested, nor documented, nor used in any project — potentially dead API surface that AI added but nothing consumes.

**Why this check is critical**: AI may add exports during a refactoring session and forget to wire them up. Unlike Check 1 (documentation only) and Check 12 (tests only), this check requires **at least one** of: test, documentation, or project usage.

**Scope**:
- Source: `streamtex/streamtex/__init__.py` — all exported names
- Test coverage: `streamtex/tests/**/*.py`
- Documentation: `streamtex-docs/manuals/**/blocks/**/*.py`
- Project usage: `projects/**/*.py`

**Method**:
1. Extract all names from `__init__.py` exports
2. For each name, search for usage in: test files, documentation blocks, project files
3. Flag names with zero usage across all three categories

**Rules**:
- WARNING if an export has no usage in tests AND no usage in documentation AND no usage in projects
- INFO: report total exports, coverage breakdown (tested/documented/used/orphan)

**Known exceptions**: Same as Check 1 known exceptions (low-level internals, config getters, etc.)

---

## Check 36: Version Claims Accuracy (scope: ai, all)

**Goal**: Detect incorrect version claims in documentation and comments — where AI mentions "new in v0.X" or "since v0.X" or "deprecated in v0.X" but the version is wrong.

**Why this check is critical**: AI confabulates version numbers. It may write "new in v0.5" for a feature that was actually added in v0.3, or "deprecated in v0.4" for something still active. These claims mislead users about API stability and upgrade paths.

**Scope**: All documentation and reference files:
- `streamtex-docs/manuals/**/blocks/**/*.py` (in `show_explanation()`, `show_details()`, `st_write()` strings)
- `streamtex-claude/shared/references/*.md`
- `streamtex/README.md`, `streamtex/CHANGELOG.md`
- `streamtex-docs/README.md`

**Method**:
1. Extract all version claims using regex patterns:
   - `since v?(\d+\.\d+(\.\d+)?)` / `new in v?(\d+\.\d+(\.\d+)?)` / `added in v?(\d+\.\d+(\.\d+)?)`
   - `deprecated in v?(\d+\.\d+(\.\d+)?)` / `removed in v?(\d+\.\d+(\.\d+)?)`
   - `requires v?(\d+\.\d+(\.\d+)?)` / `available from v?(\d+\.\d+(\.\d+)?)`
2. For each claim:
   - If "new/added/since": verify the feature/function existed in CHANGELOG at that version
   - If "deprecated": verify a deprecation entry exists in CHANGELOG at that version
   - If "removed": verify the symbol no longer exists in current API
   - If "requires": verify the constraint is consistent with current `pyproject.toml`
3. Cross-reference with `streamtex/CHANGELOG.md` entries

**Rules**:
- WARNING if a "new in vX.Y" claim cannot be verified in CHANGELOG
- WARNING if a "deprecated in vX.Y" claim references something that is not deprecated
- ERROR if a "removed in vX.Y" claim references something that still exists in the API
- INFO: report total version claims found, verified, unverifiable

---

## Check 37: Test Quality Audit (scope: ai, all)

**Goal**: Detect weak, tautological, or superficial tests that give a false sense of coverage — a known pattern when AI generates test suites.

**Why this check is critical**: AI generates tests that reflect its *intention* rather than the *actual behavior*. Common failure modes: assertions that can never fail (`assert True`, `assert x is not None` for a function that never returns None), tests that mock away all real logic, and copy-pasted tests with different names but identical bodies.

**Scope**: `streamtex/tests/test_*.py`

**Method**:
1. Parse each test file's AST
2. Detect weak test patterns:

### 37a: Tautological assertions
- `assert True`
- `assert x is not None` where `x` is a function return that is always non-None by type
- `assert isinstance(x, str)` without checking the string's content
- `assert len(x) > 0` without checking content

### 37b: Empty tests
- Test functions with no `assert` statement
- Test functions where the only assertion is in a `try/except` that catches the assertion error
- Test functions that only call the function without asserting anything about the result

### 37c: Over-mocked tests
- Tests where `@patch` decorators outnumber `assert` statements
- Tests where the mock's return value IS the expected value (testing the mock, not the code)
- Tests that mock internal implementation details (brittle coupling)

### 37d: Copy-paste tests
- Two or more test functions with identical bodies (ignoring the function name)
- Test functions that differ by only one literal value but don't use parametrize

### 37e: Missing edge cases
- Test functions that only test the happy path (no error/exception tests for a function that can raise)
- Functions with `Optional` parameters but no test with `None` value

**Rules**:
- WARNING for each tautological assertion found (37a)
- WARNING for each test function with no meaningful assertions (37b)
- WARNING for each over-mocked test (37c)
- WARNING for each copy-pasted test pair (37d)
- INFO for missing edge case suggestions (37e)
- INFO: report total tests scanned, quality score (% of tests with meaningful assertions)

---

## Check 38: Silent Failures (scope: ai, all)

**Goal**: Detect error handling patterns that silently swallow exceptions — a common AI pattern where `try/except` blocks catch errors but do nothing with them.

**Why this check is critical**: AI adds defensive `try/except` blocks around code it's unsure about. These hide bugs during development and cause mysterious failures in production. Silent failures are especially dangerous in a documentation/rendering library where a swallowed exception means missing content with no error message.

**Scope**: `streamtex/streamtex/**/*.py` (library source code)

**Method**:
1. Parse each source file's AST
2. Detect silent failure patterns:
   - `except: pass` (bare except with pass)
   - `except Exception: pass` (broad except with pass)
   - `except Exception as e: pass` (caught but ignored)
   - `except Exception: return None` (swallowing exception, returning default)
   - `except Exception: return ""` / `return []` / `return {}` (swallowing with empty default)
   - `except Exception: ...` (ellipsis body — Python 3 equivalent of pass)
3. Exclude patterns that are intentionally silent:
   - `except ImportError: pass` — valid for optional dependency checks
   - `except (FileNotFoundError, OSError): pass` — valid for optional file operations
   - Blocks with logging/warning before the pass/return

**Rules**:
- WARNING if a bare `except: pass` is found (always a code smell)
- WARNING if `except Exception: pass` is found without logging
- WARNING if `except Exception: return <default>` swallows errors without logging
- INFO: report total try/except blocks, silent ones, and patterns

---

## Check 39: Naming Coherence (scope: ai, all)

**Goal**: Detect inconsistent naming for the same concept across the codebase — where AI used different terms for identical things in different sessions.

**Why this check is critical**: AI lacks naming memory across sessions. The same concept may be called `config` in one module, `settings` in another, and `options` in a third. For parameters: `style` vs `l_style` vs `list_style`. This inconsistency confuses users and makes the API harder to learn.

**Scope**: `streamtex/streamtex/**/*.py` (library source code, public API)

**Method**:
1. Extract all public function parameter names across the library
2. Group parameters by semantic concept:
   - Style-related: `style`, `l_style`, `list_style`, `grid_style`, `block_style`
   - Content-related: `text`, `content`, `body`, `value`, `data`
   - Configuration: `config`, `settings`, `options`, `params`
   - Label/title: `label`, `title`, `name`, `heading`, `caption`
3. Flag cases where the same concept uses different names across functions at the same level of API

**Rules**:
- WARNING if two `st_*` functions use different parameter names for semantically identical concepts (e.g., one uses `style` and another uses `s` for the block style parameter)
- WARNING if a parameter name changed between function versions but the old name still appears in docs/examples
- INFO: report naming patterns found, consistency score

**Known accepted variations**:
- `l_style` (st_list) vs `style` (st_block) — different component types, different naming is acceptable
- Abbreviated vs full names within the same function (e.g., `t` for Tags alias) — convention, not inconsistency

---

## Check 40: Secret Leak Scan (scope: ai, all)

**Goal**: Detect API keys, tokens, passwords, and other secrets accidentally committed to version control — a risk when AI copies configuration examples with real values.

**Why this check is critical**: AI may copy a working `.env` example or API key from context into generated code. Unlike human developers who know to redact secrets, AI treats all context as valid content. One leaked token in a committed file can compromise external services.

**Scope**: All files across the 3 repos (excluding `.git/`, `node_modules/`, `__pycache__/`, `.venv/`):
- `streamtex/**/*.py`, `streamtex/**/*.toml`, `streamtex/**/*.md`
- `streamtex-docs/**/*.py`, `streamtex-docs/**/*.toml`, `streamtex-docs/**/*.md`
- `streamtex-claude/**/*.md`, `streamtex-claude/**/*.toml`
- `projects/**/*.py`, `projects/**/*.toml`

**Excluded files** (allowed to contain secrets):
- `*/.env` — gitignored by design
- `*/.stx-deploy.env` — gitignored by design
- `streamtex/.env` — local-only secrets file

**Method**:
1. Scan all files for secret patterns:
   - API key patterns: `sk-[a-zA-Z0-9]{20,}`, `pypi-[a-zA-Z0-9]{20,}`, `rnd_[a-zA-Z0-9]{20,}`
   - Generic key patterns: `(?i)(api[_-]?key|secret|token|password|credential)\s*[=:]\s*["'][^"']{8,}["']`
   - AWS patterns: `AKIA[0-9A-Z]{16}`, `(?i)aws[_-]?secret`
   - Base64-encoded long strings in non-binary files (potential encoded secrets)
   - Private key markers: `-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----`
2. Verify each match is not:
   - Inside a comment explaining the format (e.g., "# format: sk-xxx")
   - A placeholder (e.g., `"your-api-key-here"`, `"xxx"`, `"..."`)
   - In a `.gitignore`d file
   - A test fixture with obviously fake values

**Rules**:
- ERROR if a real-looking API key or token is found in a versioned file
- ERROR if a private key file is found in a versioned directory
- WARNING if a generic secret pattern is found (may be a false positive)
- INFO: report total files scanned, patterns checked, matches found

---

## Check 41: Hardcoded URLs (scope: ai, all)

**Goal**: Detect hardcoded URLs for staging, development, or internal services in production code — where AI embedded environment-specific URLs instead of using configuration.

**Why this check is critical**: AI copies URLs from context (dev servers, staging endpoints, internal tools) into generated code. These URLs break when the environment changes and may expose internal infrastructure details.

**Scope**: `streamtex/streamtex/**/*.py` (library source code, excluding tests)

**Method**:
1. Extract all URL strings from Python files: `https?://[^\s"']+`
2. Classify each URL:
   - **Production**: `streamtex.org`, `pypi.org`, `github.com` → OK
   - **Staging/dev**: `localhost`, `127.0.0.1`, `0.0.0.0`, `*.local`, `staging.*`, `dev.*` → flag
   - **Internal**: IP addresses (non-loopback), internal hostnames → flag
   - **Deprecated**: `streamtex.ros.lu`, `*.onrender.com` → flag (legacy domain)
3. Exclude:
   - URLs in test files
   - URLs in comments explaining infrastructure
   - URLs that are clearly configuration defaults (e.g., `DEFAULT_HOST = "http://localhost:8501"`)

**Rules**:
- WARNING if a staging/dev URL is found in non-test production code
- WARNING if a deprecated domain (`streamtex.ros.lu`, `*.onrender.com`) is found in production code
- WARNING if a raw IP address (non-loopback) is found in production code
- INFO: report total URLs found, classified by category

**Known exceptions**:
- `localhost:8501` in Streamlit runner code — required for local execution
- `pypi.org/pypi/streamtex/json` in version checking — required for update checks

---

# CLI Coherence Checks (scope: cli, all)

These checks validate that the CLI commands, their documentation, and their implementation are synchronized.

---

## Check 42: CLI Help ↔ Code Coherence (scope: cli, all)

**Goal**: Verify that CLI command help text, argument definitions, and actual behavior are synchronized.

**Why this check is critical**: AI modifies CLI command implementations (adding/removing/renaming options) without updating the help text, or updates help text without matching the code. Users then see `--help` output that doesn't match the actual available options.

**Scope**:
- `streamtex/streamtex/cli/*.py` — all CLI command modules
- `streamtex/README.md` — CLI usage examples

**Method**:
1. For each CLI module (`run_cmd.py`, `deploy_cmd.py`, `project_cmd.py`, `export_cmd.py`, `claude_cmd.py`, `install_cmd.py`, `workspace_cmd.py`, `upgrade_cmd.py`, `status_cmd.py`, `publish_cmd.py`, `dev_cmd.py`, `cache_cmd.py`, `bib_cmd.py`, `shortcuts.py`):
   - Extract all `@click.command()` / `@click.group()` / `@app.command()` decorated functions
   - Extract all `@click.option()` / `@click.argument()` decorators with their names and help text
   - Extract the function's docstring (used as command help)
2. Cross-reference:
   - Every option defined in code should be mentioned in the command's docstring or help text
   - Every option mentioned in README.md CLI examples should exist in the code
   - Default values in help text should match default values in code

**Rules**:
- WARNING if a CLI option exists in code but has no help text (empty `help=""` or missing `help=`)
- WARNING if README.md shows a CLI option that does not exist in the code
- WARNING if README.md shows a CLI command that does not exist
- WARNING if a CLI command's docstring mentions options not present in the code
- INFO: report total commands, total options, help coverage percentage

---

## Check 43: stx-guide ↔ CLI Commands Sync (scope: cli, all)

**Goal**: Verify that `stx-guide.md` accurately documents all CLI commands, their options, and their behavior.

**Why this check is critical**: The stx-guide is the primary reference for users. When CLI commands change, the guide often lags behind. Check 8 partially covers this but focuses on profile-level references. This check does a deep comparison of actual CLI commands vs. stx-guide documentation.

**Scope**:
- `streamtex-claude/shared/commands/stx-guide.md` — CLI documentation sections
- `streamtex/streamtex/cli/*.py` — all CLI command modules

**Method**:
1. Extract all CLI commands from code (command names, subcommands, groups)
2. Extract all CLI commands documented in stx-guide.md
3. Compare:
   - Commands in code but not in guide → missing documentation
   - Commands in guide but not in code → stale documentation
   - Subcommand counts: guide should match code
4. For key commands (`stx deploy`, `stx install`, `stx project`, `stx run`, `stx export`, `stx claude`):
   - Compare the option list in guide vs. code
   - Verify example commands in guide are syntactically valid

**Rules**:
- WARNING if a CLI command exists in code but is not documented in stx-guide
- WARNING if stx-guide documents a CLI command that does not exist in code
- WARNING if stx-guide shows incorrect option names for a command
- WARNING if the number of subcommands for a group differs between guide and code
- INFO: report total commands in code vs guide, sync percentage

---

## Check 44: Deploy Scripts ↔ Docker Coherence (scope: cli, all)

**Goal**: Verify that deployment scripts, Dockerfiles, CI workflows, and the `stx deploy` CLI are synchronized.

**Why this check is critical**: Deployment involves multiple interconnected files (Dockerfiles, CI workflows, CLI deploy commands, environment variables). AI modifies one without updating the others, causing deploy failures that are hard to debug.

**Scope**:
- `streamtex-docs/Dockerfile` — shared Docker build
- `streamtex-docs/.github/workflows/hetzner-deploy.yml` — Hetzner auto-deploy
- `streamtex-docs/.github/workflows/ci.yml` — Docs CI
- `streamtex/streamtex/cli/deploy_cmd.py` — deploy CLI commands
- `streamtex/streamtex/cli/coolify.py` — Coolify API client

**Method**:
1. **Dockerfile checks**:
   - `ARG SOURCE_COMMIT` must exist before `uv sync` (cache-bust guard)
   - Python version in Dockerfile must match `pyproject.toml` `requires-python`
   - `UV_NO_SOURCES=1` or `--no-sources` must be present
   - Port exposed must match Streamlit default (8501)
2. **CI workflow checks**:
   - `UV_NO_SOURCES=1` must be set as job-level env
   - Python version must match library `requires-python`
   - Workflow references to deploy commands must match actual CLI commands
3. **Deploy CLI checks**:
   - All Coolify service UUIDs in `deploy_cmd.py` constants should match `.stx-deploy.json`
   - All environment variable names referenced in deploy code should be documented

**Rules**:
- ERROR if Dockerfile is missing `ARG SOURCE_COMMIT` before `uv sync`
- ERROR if Dockerfile Python version doesn't match `pyproject.toml`
- ERROR if CI workflow is missing `UV_NO_SOURCES=1`
- WARNING if Dockerfile port doesn't match expected Streamlit port
- WARNING if deploy CLI references services not in `.stx-deploy.json`
- INFO: report deployment infrastructure consistency status

---

## Check 45: Optional Dependencies ↔ Imports Coherence (scope: cli, all)

**Goal**: Verify that optional dependency groups in `pyproject.toml` match the actual imports in the code, and that missing optional deps produce clear error messages.

**Why this check is critical**: AI adds new features that depend on optional packages but forgets to add them to the correct extras group in `pyproject.toml`, or adds them to extras but never imports them. Users then get cryptic `ImportError`s instead of a clear "install streamtex[ai] for this feature" message.

**Scope**:
- `streamtex/pyproject.toml` — `[project.optional-dependencies]`
- `streamtex/streamtex/**/*.py` — all library source files

**Method**:
1. Parse `pyproject.toml` optional dependencies: extract each group (`ai`, `pdf`, `cli`, `inspector`, `ai-openai`, `ai-google`, `ai-fal`) and their package lists
2. For each source file, extract all imports
3. Map imports to optional dependency groups:
   - `openai` → `ai-openai` or `ai`
   - `google.genai` → `ai-google` or `ai`
   - `fal_client` → `ai-fal` or `ai`
   - `playwright` → `pdf`
   - `click`, `rich`, `jinja2` → `cli`
   - `streamlit_ace` → `inspector`
4. Verify:
   - Every optional import has a corresponding extras group
   - Every package in an extras group is actually imported somewhere
   - Optional imports are wrapped in `try/except ImportError` with a clear message

**Rules**:
- ERROR if a package is imported at top level (not in try/except) but is only in optional deps
- WARNING if an extras group lists a package that is never imported in the codebase
- WARNING if an optional import's error message doesn't mention the correct extras group name
- WARNING if a new optional import was added without updating the extras groups
- INFO: report optional dependency groups, their packages, and import coverage
