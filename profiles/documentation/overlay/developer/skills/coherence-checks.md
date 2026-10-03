# Coherence Check Rules

Reference file for `/stx-coherence:audit`. Defines 51 numbered checks plus 1-bis and 28a (28 standard + 13 AI quality + 4 CLI + 6 release & install integrity).

## Conventions (read before running any check)

**Workspace**: the directory holding `stx.toml` and the five repositories `streamtex/`, `streamtex-docs/`,
`streamtex-claude/`, `streamtex-packs/` and `streamtex-landing/`. There is **no** `projects/` folder by default:
a project (for example a CE project) is audited only when it is declared in the workspace `stx.toml` as a
`[repos.<name>]` entry with `type = "project"` (the list `stx workspace` itself uses). A check whose scope is
"declared projects" is **N/A** — reported as such, never as OK — when that list is empty. Paths that do not exist
(`streamtex-docs/README.md`, `streamtex-docs/references/`) are not audit targets.

**Introspection, not hand-written lists**: every list of names (exports, enums, signatures, install paths,
commands) is derived at audit time from the code that owns it — `streamtex.__all__`, `inspect.signature`, the
enum classes, `install.py` (`CATEGORY_PATHS`, `SHARED_DEST_PATHS`), the command files. A list written in this
catalog is only a list of **known exceptions**, and each audit re-checks that every exception still exists.

**How to run the commands**: from the `streamtex/` repository (so `..` is the workspace root), read-only:
`uv run --frozen python - <<'EOF' … EOF`. `--frozen` keeps `uv.lock` untouched. Scripts that write go to the
session scratchpad, never to `/tmp` or into a repository. Commands that use the network (PyPI JSON, `gh`) are
marked as such; report "not measured" when the network is unavailable.

**What counts as a justification**: an explanatory comment written by a person. `# noqa`, `# type: ignore`,
`# pragma` and `# nosec` silence a tool; they never justify a behaviour.

**Code that is shown is code**: code displayed to readers (strings passed to `show_code()`, files loaded by
`show_code(file=...)` from `static/`, fenced Python in skills, agents, commands, designer templates and
references) is held to the same API rules as executed code — readers copy it.

---

## Check 1: API Coverage (scope: library, all)

**Goal**: Every public export in the library should be discoverable by users — either via a manual block (preferred, with a live example) **or** via the cheatsheet / coding standards (acceptable for utility helpers and types that don't need a dedicated walkthrough).

**Sources** (introspected, never parsed by hand):
- `streamtex.__all__` — the public API (it is also exactly what `from streamtex import *` exports, see Check 1-bis)
- the modules deliberately kept **out** of the star import, imported explicitly by users: `streamtex.i18n`
  (`T`, `TF`, `current_lang`, `with_lang`, `set_languages`, `default_lang`, `languages`) and `streamtex.facts`
  (`fact`, `stale_facts`, `facts_file`, `StaleFacts`) — their public names are derived from the modules themselves

**Targets** (any of these counts as documentation):
- `streamtex-docs/manuals/**/blocks/**/*.py` and the `static/examples/**/*.py` files they show — preferred for user-facing widgets
- `streamtex-claude/shared/references/streamtex_cheatsheet_en.md` — acceptable for helpers, types, exceptions
- `streamtex-claude/shared/references/coding_standards.md` — acceptable for conventions / patterns
- `streamtex-docs/cheatsheets/stx_cheatsheet_python.md`

**Rules**:
- WARNING if a name of `__all__`, or a public name of `streamtex.i18n` / `streamtex.facts`, appears in **none** of the targets
- WARNING if a known exception below is no longer in `__all__` (stale exception — remove it from this list)
- INFO if an export only appears in blocks but has no `show_code()` example
- SKIP internal names (prefixed with `_`)

**Why both targets count**: helper functions (DI getters like `get_block_spacing`, introspection helpers like `is_cached` / `list_providers`, registries like `FileCategoryRegistry`) don't need a dedicated manual page — a clear cheatsheet entry with one usage example is sufficient documentation. Demanding a manual block for every export forced low-value pages.

**Known exceptions** (documented where they are used; not expected in blocks). The low-level export buffer
functions (`export_append`, `export_push_wrapper`, `export_pop_wrapper`, `generate_export_html`,
`reset_export_buffer`, `is_export_active`) and `StreamTeX_Styles` are **no longer exported** (they live in
`streamtex.export`, or were removed in 0.7.14) and were dropped from this list:
- Config internals: `get_block_helper_config`, `get_bib_config`, `get_gsheet_config`, `get_link_config`, `get_bib_registry`, `reset_bib_registry`, `get_ai_image_config`, `get_slide_break_config`, `get_presentation_config`
- Display/layout internals: `PageLayout`, `ViewMode`, `SlideBreakDisplayConfig`, `ProfileConfig`, `AssetMode`
- Parser internals: `parse_bibtex_string`, `parse_ris_string`, `register_bib_parser`
- Utility re-exports: `generate_bib_stubs`, `export_bibtex`, `load_css`, `exec_static`, `resolve_content`, `inject_link_preview_scaffold`, `add_wrap_all_option`, `add_slide_break_options`
- Error/result types: `AIImageError`, `AIImageResult`, `BibParseError`, `GSheetError`
- AI image internals: `is_cached`, `list_providers`
- Registry internals: `FileCategoryRegistry`

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import importlib, re
from pathlib import Path
import streamtex
WS = Path("..").resolve()
KNOWN = {"get_block_helper_config", "get_bib_config", "get_gsheet_config", "get_link_config", "get_bib_registry",
         "reset_bib_registry", "get_ai_image_config", "get_slide_break_config", "get_presentation_config",
         "PageLayout", "ViewMode", "SlideBreakDisplayConfig", "ProfileConfig", "AssetMode",
         "parse_bibtex_string", "parse_ris_string", "register_bib_parser", "generate_bib_stubs", "export_bibtex",
         "load_css", "exec_static", "resolve_content", "inject_link_preview_scaffold", "add_wrap_all_option",
         "add_slide_break_options", "AIImageError", "AIImageResult", "BibParseError", "GSheetError",
         "is_cached", "list_providers", "FileCategoryRegistry"}
targets = [*WS.glob("streamtex-docs/manuals/**/blocks/**/*.py"),
           *WS.glob("streamtex-docs/manuals/**/static/examples/**/*.py"),
           WS / "streamtex-claude/shared/references/streamtex_cheatsheet_en.md",
           WS / "streamtex-claude/shared/references/coding_standards.md",
           WS / "streamtex-docs/cheatsheets/stx_cheatsheet_python.md"]
corpus = "\n".join(p.read_text(encoding="utf-8") for p in targets if p.is_file())
outside = {f"{m}.{n}" for m in ("streamtex.i18n", "streamtex.facts")       # modules kept out of the star
           for n, o in vars(importlib.import_module(m)).items()
           if not n.startswith("_") and getattr(o, "__module__", None) == m}
undoc = [n for n in streamtex.__all__ if n not in KNOWN and not re.search(rf"\b{re.escape(n)}\b", corpus)]
undoc += [q for q in sorted(outside) if not re.search(rf"\b{re.escape(q.rsplit('.', 1)[1])}\b", corpus)]
print(f"__all__: {len(streamtex.__all__)} | known exceptions: {len(KNOWN)} | stale exceptions: {sorted(KNOWN - set(streamtex.__all__))}")
print(f"undocumented ({len(undoc)}):", ", ".join(undoc))
EOF
```

---

## Check 1-bis: Star-Import Boundary (scope: library, all)

**Goal**: `from streamtex import *` exports exactly `streamtex.__all__`, never a sub-module, and never the
names projects are expected to define themselves.

**Source of truth**: the automated test `tests/test_star_import.py` — in particular
`test_names_kept_out_of_the_star_import` (`T`, `TF`, `current_lang`, `with_lang`, `set_languages`, `fact`
stay out of the star), `test_star_import_never_exports_a_module` and `test_all_names_exist_and_are_public`.
The catalog does not duplicate the assertions: it runs the test and reports its result.

**How to check**:
```bash
uv run --frozen pytest -q -p no:cacheprovider tests/test_star_import.py
uv run --frozen python - <<'EOF'
import streamtex
ns = {}
exec("from streamtex import *", ns)
ns.pop("__builtins__", None)
print("star == __all__:", set(ns) == set(streamtex.__all__),
      "| leaked:", sorted({"T", "TF", "current_lang", "with_lang", "set_languages", "fact"} & set(ns)) or "none")
EOF
```

**Rules**:
- ERROR if `tests/test_star_import.py` fails
- ERROR if the test file no longer asserts the six excluded names (the assertion moved or was deleted)
- WARNING if the star namespace differs from `__all__`
- Correction: fix `__all__` / the module layout in the library, never relax the test

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
- WARNING if a block uses an old API pattern (e.g., deprecated parameter name)
- INFO if import styles differ between blocks in the same manual (e.g., some use `from streamtex import *`, others explicit imports)

The former `textwrap` rules (`textwrap.dedent(` / unused `import textwrap`, now auto-dedented) were removed:
0 occurrences in two consecutive audits. Unused imports are caught by Check 30 (ruff `F401`).

---

## Check 4: Profile File Sync (scope: profiles, all)

**Goal**: All copies of shared profile files are identical to their source of truth.

**Source of truth** → **Copies to check**:

The expected copies are **not** listed by hand: they are whatever the installed profile places, i.e. every
file `stx claude install <profile>` would write for the profile recorded in the target's `.claude/.stx-profile`
(or in its `.claude/stx.lock` in project mode). Targets:

| Target | Profile marker |
|--------|----------------|
| `streamtex/.claude/` | `streamtex/.claude/.stx-profile` (library) |
| `streamtex-docs/.claude/` | `streamtex-docs/.claude/.stx-profile` (documentation) |
| every declared project (`[repos]` with `type = "project"`, see Conventions) | its `.claude/.stx-profile` or `.claude/stx.lock` |

`streamtex-claude`, `streamtex-packs` and `streamtex-landing` carry no installed profile; nothing to compare there.

**Method**: run the read-only CLI comparison, which resolves the profile, its `extends` parent, the overlay and
the `[shared]` entries exactly like the installer:
```bash
uv run --frozen stx claude check                 # every target of the workspace
uv run --frozen stx claude diff ../streamtex-docs  # one target, file by file
```
For each file reported `Modified`, read both sides and determine the divergence direction by analyzing the diff.

**IMPORTANT**: Local `.claude/` files in projects are read-only copies installed by `stx claude update`. The audit MUST NOT modify them. Instead, it analyzes the divergence direction and reports appropriate actions.

**Divergence Direction Analysis**:
1. **Source newer** (source has content that local doesn't, local has no unique additions): the local copy is simply out of date → INFO recommending `stx claude update`
2. **Local has improvements** (local has content not in source, potentially useful): the local copy was legitimately improved → WARNING with BACKPORT task to propagate changes to `streamtex-claude/` source
3. **Bidirectional** (both have unique changes): requires manual decision → WARNING with detailed diff

**Rules**:
- ERROR if a source file declared in a manifest `[shared]` section does not exist in `shared/references/` or `shared/commands/` (source existence guard)
- WARNING if a source file exists but has no copy in an expected location
- WARNING + BACKPORT if local copy has relevant improvements not in source (include diff summary and target path in `streamtex-claude/`)
- WARNING if bidirectional divergence detected (both source and local have unique changes)
- INFO if local copy is simply out of date — recommend `stx claude update`
- INFO: report total files checked and sync status
- INFO: report any files found in `.claude/custom/` (user customizations detected)
- WARNING if a file in `.claude/custom/references/` has the same name as a file in `.claude/references/` (potential shadow/conflict)
- WARNING if a file in `.claude/custom/skills/` has the same name as a file in `.claude/developer/skills/` or `.claude/designer/skills/` (potential shadow/conflict)

**Prohibited actions** (the audit and fix MUST NOT):
- Overwrite local `.claude/` read-only files
- `chmod` read-only files to make them writable
- Copy from source to local (that's `stx claude update`'s job)

---

## Check 5: Version Alignment (scope: library, all)

**Goal**: Library version is consistent across all locations, what the CHANGELOG presents as released was
really released, and every dependent constraint is satisfiable. The same for `streamtex-claude`.

**Not a check any more**: comparing `pyproject.toml` with `streamtex.__version__`. `__version__` is read from the
installed metadata (`importlib.metadata.version("streamtex")`), so the comparison is always true — it was a
tautology.

**Source files**:
- `streamtex/pyproject.toml` → `[project] version`; `streamtex/CHANGELOG.md` → `## [X.Y.Z]` entries
- PyPI release list (`https://pypi.org/pypi/streamtex/json`, network) and the git tags of `streamtex`
- `streamtex-claude/pyproject.toml` → `[project] version`; `streamtex-claude/CHANGELOG.md`; tags of `streamtex-claude`

**Targets** (constraints `streamtex>=…`): `streamtex-docs/pyproject.toml`, `streamtex-packs/*/pyproject.toml`,
and every declared project's `pyproject.toml`

**Rules**:
- ERROR if the CHANGELOG top released entry (`[Unreleased]` excluded) differs from `pyproject.toml` version
- WARNING for each CHANGELOG version between the previous PyPI release and the current version that was never
  published on PyPI (it is dated as a release but no user can install it — merge it into the published entry or
  mark it as never published)
- WARNING for each `0.7.x` PyPI version without a `vX.Y.Z` tag; INFO for older gaps and tags without the `v` prefix
- ERROR if `streamtex-claude/pyproject.toml` version differs from the top `## [X.Y.Z]` of `streamtex-claude/CHANGELOG.md`
- WARNING if a dependent's `streamtex` constraint excludes the current version
- INFO: report current version, previous release, and all constraints found

**How to check** (network: PyPI):
```bash
uv run --frozen python - <<'EOF'
import json, re, subprocess, tomllib, urllib.request
from pathlib import Path
WS = Path("..").resolve()
V = lambda s: tuple(map(int, re.findall(r"\d+", s)))
chlog = lambda p: re.findall(r"^## \[(\d+\.\d+\.\d+)\]", (WS / p).read_text(encoding="utf-8"), re.M)
pyver = lambda p: tomllib.loads((WS / p).read_text(encoding="utf-8"))["project"]["version"]
tags = lambda r: set(subprocess.run(["git", "-C", str(WS / r), "tag"], capture_output=True, text=True).stdout.split())
lib, ch = pyver("streamtex/pyproject.toml"), chlog("streamtex/CHANGELOG.md")
pypi = set(json.load(urllib.request.urlopen("https://pypi.org/pypi/streamtex/json", timeout=20))["releases"])
prev = max((v for v in pypi if V(v) < V(lib)), key=V)
print(f"streamtex pyproject={lib} CHANGELOG-top={ch[0]} on-PyPI={lib in pypi} previous-release={prev}")
print("CHANGELOG versions since the previous release never published:",
      [v for v in ch if V(prev) < V(v) < V(lib) and v not in pypi])
print("older CHANGELOG versions never published (history):", sum(V(v) < V(prev) and v not in pypi for v in ch))
t = tags("streamtex")
print("0.7.x PyPI versions without tag:", sorted((v for v in pypi if v.startswith("0.7.") and f"v{v}" not in t), key=V))
print("tags without the v prefix:", sorted(x for x in t if re.fullmatch(r"\d+\.\d+\.\d+", x)))
cl, cc = pyver("streamtex-claude/pyproject.toml"), chlog("streamtex-claude/CHANGELOG.md")
print(f"streamtex-claude pyproject={cl} CHANGELOG-top={cc[0] if cc else None} tag v{cl}: {'v' + cl in tags('streamtex-claude')}")
for p in sorted(WS.glob("*/pyproject.toml")) + sorted(WS.glob("streamtex-packs/*/pyproject.toml")):
    for dep in tomllib.loads(p.read_text(encoding="utf-8")).get("project", {}).get("dependencies", []):
        if re.match(r"streamtex\b(?!-)", dep):
            print(f"constraint {p.relative_to(WS)}: {dep}")
EOF
```

---

## Check 6: Block Structure Compliance (scope: docs, blocks, all)

**Goal**: All blocks follow canonical structure.

**Scope**: `streamtex-docs/manuals/**/blocks/bck_*.py` + `streamtex-docs/templates/**/blocks/bck_*.py`

**Rules**:
- WARNING if block lacks `class BlockStyles`
- WARNING if block lacks `def build()` function
- WARNING if block lacks `bs = BlockStyles` alias
- INFO (not WARNING) if `build()` calls `st_write` / `st_list` / `st_image` / etc. **immediately after** `show_explanation(...)`, `show_details(...)`, or `show_code(...)` — these are functions (not context managers), so trailing content renders **outside** the box. This is usually the intended flat layout (see the note below; the former WARNING produced 27 false positives in one audit). Report it only to let the author confirm; WARNING only when the trailing content is visibly meant to be inside the box (indented as if in a `with`, or the explanation text says "below" / "in this box"). (Cf. CLAUDE.md gotcha "show_explanation() is a function, NOT a context manager".)
- INFO if block doesn't use `show_code()` or `show_explanation()` (may be intentional)

**Note on `with st_block(...)` usage** — `st_block` is for **individual styled containers inside** `build()` (cards, banners, decorated boxes). It is NOT required as an outer wrapper around the whole `build()` body. The block framework already provides the outer container; calling `st_write` / `st_space` / `show_explanation` directly at the top of `build()` is the canonical "flat" pattern and is correct. A block uses `with st_block(...)` only where it needs a custom visual container around a sub-section.

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

**Source**: `streamtex/README.md` (published on PyPI); also `streamtex-claude/README.md`,
`streamtex-packs/README.md` and `streamtex-packs/*/README.md` (published on GitHub / PyPI for the packs).
`streamtex-docs` and `streamtex-landing` have no README.

**Rules**:
- WARNING if any markdown link of `streamtex/README.md` (and of a pack README published on PyPI) uses a relative path (e.g., `[text](FILE.md)` instead of `[text](https://github.com/nicolasguelfi/streamtex/blob/main/FILE.md)`)
- PyPI renders README.md but does NOT resolve relative links — they become broken
- ERROR if an absolute `github.com/nicolasguelfi/<repo>/blob|tree/main/<path>` or `raw.githubusercontent.com/…/main/<path>` link points to a file that is **not tracked by git** in the local checkout of `<repo>` (it is a 404 on GitHub — e.g. a link into `.claude/references/`, which is installed, not versioned)
- `stx publish check` also detects relative links (check "README links")
- INFO: report total links found and how many are absolute vs relative

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import re, subprocess, urllib.parse
from pathlib import Path
WS = Path("..").resolve()
LINK = [re.compile(r"https://github\.com/nicolasguelfi/([\w.-]+)/(?:blob|tree)/main/([^)\s#?\"'>]+)"),
        re.compile(r"https://raw\.githubusercontent\.com/nicolasguelfi/([\w.-]+)/main/([^)\s#?\"'>]+)")]
cache = {}
def tracked(repo, rel):
    if repo not in cache:
        files = subprocess.run(["git", "-C", str(WS / repo), "ls-files"], capture_output=True, text=True).stdout.split("\n")
        cache[repo] = set(files) | {"/".join(f.split("/")[:i]) for f in files for i in range(1, f.count("/") + 1)}
    return rel.rstrip("/") in cache[repo]
for md in [WS / "streamtex/README.md", *sorted(WS.glob("streamtex-*/README.md")), *sorted(WS.glob("streamtex-packs/*/README.md"))]:
    text = md.read_text(encoding="utf-8")
    rel = re.findall(r"\[[^\]]*\]\((?!https?://|#|mailto:)([^)]+)\)", text)
    bad = [f"{r}/{p}" for rx in LINK for r, p in rx.findall(text)
           if (WS / r).is_dir() and not tracked(r, urllib.parse.unquote(p))]
    print(f"{md.relative_to(WS)}: {len(rel)} relative link(s) {rel[:5]} | absolute links to untracked files: {bad}")
EOF
```

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
| README files | `streamtex/README.md`, `streamtex-claude/README.md`, `streamtex-packs/**/README.md` | Full content |
| CLAUDE.md files | `streamtex/CLAUDE.md`, `streamtex-docs/CLAUDE.md`, declared projects' `CLAUDE.md` | Full content |
| Packs | `streamtex-packs/*/**/*.py`, `streamtex-packs/*/**/*.md` | Docstrings, component docstrings, markdown |
| Landing page | `streamtex-landing/index.html` | Visible text (the site is English) |
| CLI help | `streamtex/streamtex/cli/**/*.py` | `help=` strings and command docstrings (shown by `--help`) |

**Explicit exceptions** (allowed in French or other languages):
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

**Scope**: every `.md` file of `streamtex-claude` containing fenced Python (`_archive/` excluded), in particular:
- `streamtex-claude/profiles/**/skills/**/*.md`, `profiles/**/agents/**/*.md`, `profiles/**/commands/**/*.md`
- `streamtex-claude/profiles/**/designer/templates/*.md` and `profiles/**/designer/guidelines/*.md` — the
  blueprints `/stx-block:init` copies into every new project (a ghost here is inherited by each project)
- `streamtex-claude/shared/**/*.md` — commands, skills, agents, references, `import-formats/`

**Method**: run **Script G** (Appendix A). It extracts every fenced Python block, assumes the
`from streamtex import *` the snippets usually omit, follows explicit imports and aliases
(`from streamtex.x import y as z`, `import streamtex as stx`), lets local definitions and non-streamtex imports
shadow API names, and checks each call against `inspect.signature` of the **function or class constructor**
(dataclass configs included). Enum members are checked by Check 15's command over the same files.

**Rules**:

### Enum validation
- ERROR if code uses `lt.<name>` / `t.<name>` / `<Enum>.<NAME>` where the member does not exist (members are introspected by Check 15 — `ListTypes` has only `ordered` and `unordered`)

### Import validation
- ERROR if code does `from streamtex[.x] import y` and `y` does not exist there (e.g. `from streamtex import StreamTeX_Styles`)

### Function signature validation
- ERROR if code passes a keyword argument that does not exist in the function **or class constructor** signature (e.g. `st_book(design_system=...)`, `SlideBreakDisplayConfig(space=...)`, `Style(font_color=...)`)
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

**How to check**: Script G (Appendix A); keep the lines whose path starts with `streamtex-claude/`. Then the
enum part of Check 15's command (same files). Code blocks that do not parse (pseudo-code, `...` placeholders)
are skipped by the script — review them by eye.

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

**Method**: For each source module `streamtex/<module>.py` with public functions, check that the public functions are exercised by **any** test file (not necessarily a file named `tests/test_<module>.py`). The audit must follow imports: a `from streamtex.<module> import <func>` in any `tests/test_*.py` counts as coverage for `<func>`.

**Rules**:
- WARNING only if a source module has public functions AND **none** of those functions is referenced by any test file
- WARNING if `test_presentation.py` does not exist (presentation module must have dedicated tests — exception kept because of its size and visibility)
- INFO: report module → test files providing coverage (one module can be covered by several test files, that is normal)

**Note on file naming**: a strict `test_<module>.py` per `<module>.py` convention is **not required**. Functions are routinely grouped by feature rather than by source module — e.g., blocks.py functions are covered by test_lazy_blocks.py / test_load_atomic.py / test_resolve_content.py; book.py functions are covered by test_book_integration.py / test_book_search_markers.py / test_export_guard.py / test_bib.py / test_export_enrich.py. These are valid coverage arrangements and must NOT trigger the warning.

**Known exceptions** (modules genuinely without public surface to test):
- `__init__.py`, `constants.py`, `enums.py`, `utils.py` (re-exports / constants / type aliases)
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
uv run --frozen python - <<'EOF'
import inspect, streamtex
for name in streamtex.__all__:          # the public API; dir(streamtex) would also list sub-modules
    obj = getattr(streamtex, name)
    if callable(obj):                   # functions AND classes (constructor signature)
        try:
            print(f"{name}{inspect.signature(obj)}")
        except (TypeError, ValueError):
            pass
EOF
```
Then for each test file, parse function calls and compare keyword arguments against introspected signatures.

### Sub-check 12c: Deprecated API in tests

**Method**: Scan all `test_*.py` files for usage of deprecated patterns.

**Rules**:
- WARNING if a test imports a name that is no longer exported from `__init__.py`
- WARNING if a test uses a deprecated parameter (same list as Check 11 cross-reference)
- WARNING if a test mocks a function path that has been moved or renamed

### Sub-check 12d: New features without tests

**Method**: Compare the library against the **previous release** — the newest `vX.Y.Z` tag reachable from HEAD
other than the current version's own tag. (`git describe --tags --abbrev=0` alone is wrong right after a release:
HEAD *is* the tag, the diff is empty and the check silently passes.) For exports added and functions modified
since that release, check that tests exist.

**Rules**:
- WARNING if a new public export (in `__all__` now, absent from the previous release's `__init__.py`) is named in no test file
- WARNING if a function with modified signature (since the previous release) has no test exercising the new/changed parameters
- INFO: report the previous release, files changed since, and the added exports with their test status

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import ast, re, subprocess, tomllib
from pathlib import Path
import streamtex
cur = tomllib.load(open("pyproject.toml", "rb"))["project"]["version"]
git = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout
prev = git("describe", "--tags", "--abbrev=0", "--match", "v[0-9]*", "--exclude", f"v{cur}", "HEAD").strip()
def names(src):  # public names of an __init__.py: __all__ if present, else every imported name
    tree = ast.parse(src)
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "__all__" for t in n.targets):
            return set(ast.literal_eval(n.value))
    return {a.asname or a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) for a in n.names} - {"*"}
added = sorted(set(streamtex.__all__) - names(git("show", f"{prev}:streamtex/__init__.py")))
tests = "\n".join(p.read_text(encoding="utf-8") for p in Path("tests").rglob("test_*.py"))
changed = git("diff", "--name-only", f"{prev}..HEAD", "--", "streamtex").split()
print(f"current {cur}, previous release {prev}: {len(changed)} library files changed")
print(f"exports added since {prev} ({len(added)}):", added)
print("added exports never named in tests/:", [n for n in added if not re.search(rf"\b{n}\b", tests)])
EOF
# then, for each changed module: git diff <prev>..HEAD -- <module> and compare the changed `def` lines with the tests
```

---

## Check 13: Manual Blocks → Library API Existence (scope: docs, all)

**Goal**: Every `st_*` / `stx.*` function call in manual block **rendered code** must exist in the current library API. This is the reverse of Check 1.

**Why this check is critical**: Manuals are the user-facing documentation. If a block calls a function that was renamed, removed, or restructured in the library, the manual will crash at runtime — or worse, silently show nothing.

**Scope**: `streamtex-docs/manuals/**/blocks/**/*.py`

**What to check**: Rendered code ONLY — skip example strings inside `show_code()`, `show_explanation()`, `show_details()`.

**Method**:
1. Build the list of all valid exports: `streamtex.__all__` (introspected, command below)
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
uv run --frozen python -c "import streamtex; print('\n'.join(sorted(streamtex.__all__)))"
```
Then for each block, parse rendered `st_*()` calls and verify against the exports list.

---

## Check 14: Manual Examples Signature Coherence (scope: docs, all)

**Goal**: Function call signatures used in manual `show_code()` examples must match the current library function signatures (parameter names, parameter existence).

**Why this check is critical**: Users copy-paste code from `show_code()` examples. If an example uses a parameter that was renamed or removed, the user's code breaks. This erodes trust in the documentation.

**Scope** — all the code a reader of the manuals sees:
- the strings passed to `show_code()` / `show_code_inline()` in `streamtex-docs/manuals/**/*.py` and `streamtex-docs/templates/**/*.py`
- the files loaded by `show_code(file="...")`, resolved against the manual's `static/` directory (`static/examples/**/*.py`)
- the fenced Python of `streamtex-docs/cheatsheets/*.md`
- the executed code of the blocks themselves (complements Check 13 with keyword arguments)

**Method**: run **Script G** (Appendix A). The API surface is **every callable of `streamtex.__all__`** —
functions, classes (constructor signature, dataclass configs such as `ExportConfig`, `ListStyle`,
`LazyBlockRegistry`, `TOCConfig`) — plus every name reachable through an explicit
`from streamtex.<module> import <name>` (e.g. `streamtex.export`, `streamtex.cli.console`). Aliases
(`import streamtex as stx`, `from … import … as …`) are resolved; there is no hand-maintained list of functions.

**Rules**:
- ERROR if an example uses a keyword argument that does not exist in the function or constructor signature
  - Example: `st_image(caption="...")` but `st_image` has no `caption` parameter
  - Example: `ListStyle(style=...)` but `ListStyle` takes `(css, style_id, symbols)`
- ERROR if an example imports a name that does not exist (`from streamtex import export_append`, `from streamtex.cli.console import console`)
- ERROR if an example calls a function that no longer exists in the library
- WARNING if an example uses a deprecated parameter (even if still accepted for backward compat)
- WARNING if an example shows a context manager usage for a non-context-manager function, or vice versa
  - Example: `with st_write(...)` — `st_write` is NOT a context manager
  - Example: `st_list(style, items=[...])` — `st_list` IS a context manager
- WARNING if an example shows positional arguments in the wrong order vs the signature
- INFO: report total examples checked, total `st_*` calls in examples, issues found

**How to check**: Script G (Appendix A); keep the lines whose path starts with `streamtex-docs/`. To print the
surface it checks against:
```bash
uv run --frozen python - <<'EOF'
import inspect, streamtex
for n in streamtex.__all__:
    o = getattr(streamtex, n)
    if callable(o):
        try:
            print(f"{n}{inspect.signature(o)}")
        except (TypeError, ValueError):
            print(f"{n}: <no signature>")
EOF
```

**Interaction with Check 11**: Check 11 validates code in Claude artifacts (skills, agents, commands). Check 14 validates code in manual `show_code()` examples. Together they cover all user-facing code examples in the ecosystem.

---

## Check 15: Manual Enum & Constant Coherence (scope: docs, all)

**Goal**: All enum members, class attributes, and constant values referenced in manual blocks (both rendered and examples) must exist in the current library.

**Why this check is critical**: Enums and constants are frequently refactored (renamed, reorganized, deprecated). A block using `ListTypes.ul` when the correct member is `ListTypes.unordered` will crash silently or raise an AttributeError at runtime.

**Scope**: `streamtex-docs/manuals/**/*.py`, `streamtex-docs/templates/**/*.py` (rendered code, `show_code()`
strings and `static/examples`), plus the fenced Python of `streamtex-claude/**/*.md` and
`streamtex-docs/cheatsheets/*.md`.

**Method**: no hand-written member table. The enums to validate are **every `enum.Enum` subclass in
`streamtex.__all__`** (today `AssetMode`, `BannerMode`, `BibFormat`, `CitationStyle`, `ExportMode`, `PdfMode`,
`ScaleCurve`, `SlideBreakMode`, `ViewMode` — this list is printed by the command, not maintained here) plus the
attribute-namespace classes of `streamtex.enums` (`Tags`, `ListTypes`). Members come from `__members__` (enums)
or the class attributes. Conventional aliases `t` → `Tags`, `lt` → `ListTypes` and any `X as y` alias found in the
file are resolved. Constructor keyword arguments of config classes (`PdfConfig`, `ExportConfig`, ...) are
validated by Script G (Check 14).

`ListTypes` has exactly `ordered` and `unordered` — the former catalog listed a `custom` member that does not
exist (custom bullets are a `ListStyle(symbols=...)`, not a list type).

**Rules**:
- ERROR if code accesses `<Enum or alias>.<member>` where the member does not exist (e.g. `lt.ul`, `AssetMode.INLINE`)
- WARNING if code uses an enum member that exists but is deprecated
- INFO: report the enums introspected and the number of references checked

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import enum, inspect, re
from pathlib import Path
import streamtex, streamtex.enums
WS = Path("..").resolve()
kinds = {n: o for n, o in ((n, getattr(streamtex, n)) for n in streamtex.__all__)
         if inspect.isclass(o) and issubclass(o, enum.Enum)}
kinds |= {n: o for n, o in vars(streamtex.enums).items()
          if inspect.isclass(o) and o.__module__ == "streamtex.enums" and not n.endswith(("Tag", "Type"))}
members = {n: set(o.__members__) if issubclass(o, enum.Enum) else {m for m in vars(o) if not m.startswith("_")}
           for n, o in kinds.items()}
files = [*WS.glob("streamtex-docs/manuals/**/*.py"), *WS.glob("streamtex-docs/templates/**/*.py"),
         *WS.glob("streamtex-claude/**/*.md"), *WS.glob("streamtex-docs/cheatsheets/*.md")]
bad = set()
for p in files:
    if ".venv" in p.parts or "_archive" in p.parts or p.name == "coherence-checks.md":
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    if p.suffix == ".md":  # keep only the python fences of markdown files (line numbers preserved)
        text = re.sub(r"```python\n(.*?)```|[^`]+|`", lambda m: m.group(1) or re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)
    local = {"lt": "ListTypes", "t": "Tags"} | {a: n for n, a in re.findall(r"\b(\w+) as (\w+)", text) if n in kinds}
    for i, line in enumerate(text.splitlines(), 1):
        for owner, attr in re.findall(r"(?<![\w.])(\w+)\.(\w+)", line):
            cls = local.get(owner, owner if owner in kinds else None)
            if cls and attr not in members[cls]:
                bad.add(f"{p.relative_to(WS)}:{i}: {owner}.{attr} — not a member of {cls}")
for n in sorted(members):
    print(f"{n}: {sorted(members[n])}")
print(f"\n{len(bad)} invalid member reference(s)")
print("\n".join(sorted(bad)))
EOF
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

**Computed paths must be evaluated, not eyeballed**: blocks build paths such as
`_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(_project_root)))`. A `dirname` too many points
outside the repository, the block's `try/except` shows "# ci.yml not found", and nothing fails. The command below
evaluates every module-level path assignment with `__file__` set to the block's real path, then resolves each
`open()`, `show_code(file=)`, `st_image/st_audio/st_video` argument it can compute.

**Git LFS pointers**: a media file committed as a ~130-byte LFS pointer **without** a `filter=lfs` attribute in
`.gitattributes` is not a binary at all — clones, Docker builds and wheels receive a text file. Detected from the
committed blob (not the working tree) in all five repositories.

**Rules**:
- ERROR if a rendered `st_image(uri=)` references a local file that does not exist
- ERROR if a `show_code(file=)` references a file that does not exist
- ERROR if an `open()` call (computed path included) references a file that does not exist
- ERROR if a committed blob is an LFS pointer while its path has no `filter=lfs` attribute
- WARNING if `st_audio()` or `st_video()` references a missing local file
- WARNING if a repo-level file reference (Dockerfile, CI config, etc.) does not exist
- INFO: report total static references evaluated, and references not statically computable (inspect those by hand)

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import ast, os, subprocess
from pathlib import Path
WS = Path("..").resolve()
SIG = b"version https://git-lfs.github.com/spec"
problems, checked = [], 0
for py in sorted(WS.glob("streamtex-docs/manuals/**/blocks/**/*.py")) + sorted(WS.glob("streamtex-docs/templates/**/blocks/**/*.py")):
    tree = ast.parse(py.read_text(encoding="utf-8"))
    ns = {"os": os, "Path": Path, "str": str, "__file__": str(py)}
    for node in tree.body:                      # evaluate the module-level path computations
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                ns[node.targets[0].id] = eval(compile(ast.Expression(node.value), str(py), "eval"), {"__builtins__": {}}, ns)
            except Exception:
                pass
    static = next((p / "static" for p in py.parents if (p / "static").is_dir()), None)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = getattr(node.func, "id", getattr(node.func, "attr", ""))
        target = None
        if fn == "open" and node.args:
            target = node.args[0]
        elif fn in ("show_code", "show_code_inline"):
            target = next((k.value for k in node.keywords if k.arg == "file"), None)
        elif fn in ("st_image", "st_audio", "st_video"):
            target = next((k.value for k in node.keywords if k.arg in ("uri", "src", "path")), node.args[-1] if node.args else None)
        if target is None:
            continue
        try:
            val = eval(compile(ast.Expression(target), str(py), "eval"), {"__builtins__": {}}, ns)
        except Exception:
            continue                            # not statically computable: inspect by hand
        if not isinstance(val, (str, Path)) or str(val).startswith(("http://", "https://", "data:")):
            continue
        p = Path(val)
        if not p.is_absolute():
            cands = ([static / p] + ([static / "images" / p] if fn == "st_image" else [])) if static else [py.parent / p]
            p = next((c for c in cands if c.exists()), cands[0])
        checked += 1
        if not p.exists():
            problems.append(f"{py.relative_to(WS)}:{node.lineno}: {fn}() -> {p} does not exist")
print(f"{checked} computed file references evaluated, {len(problems)} missing")
print("\n".join(problems))
git = lambda d, *a: subprocess.run(["git", "-C", str(d), *a], capture_output=True, text=True).stdout
for repo in ("streamtex", "streamtex-docs", "streamtex-claude", "streamtex-packs", "streamtex-landing"):
    d = WS / repo
    if not (d / ".git").exists():
        continue
    rows = [l.split(None, 4) for l in git(d, "ls-tree", "-r", "-l", "HEAD").splitlines()]
    ptr = [path for _, _, sha, size, path in rows if size.isdigit() and int(size) < 200
           and git(d, "cat-file", "-p", sha).encode()[:len(SIG)] == SIG
           and not git(d, "check-attr", "filter", "--", path).rstrip().endswith(": lfs")]
    print(f"{repo}: LFS pointers committed without an LFS attribute: {ptr or 'none'}")
EOF
```

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

**Goal**: Every file declared in a profile's `manifest.toml` must physically exist at the path resolved by `install.py` — its `CATEGORY_PATHS` / `_resolve_path` for profile categories and its `SHARED_DEST_PATHS` for `[shared]` entries.

**Why this check is critical**: The CI (`validate.yml`) catches this on push, but catching it locally before pushing avoids broken CI runs. A manifest that declares files which don't exist means `install.py` will silently skip them, and users won't get the expected commands/skills/agents.

**Scope**: `streamtex-claude/profiles/*/manifest.toml`

**Method** (no path table in this catalog — the mapping is **imported from `install.py`**, so a new category
or a renamed path is picked up automatically):
1. Load `streamtex-claude/install.py` as a module (it only defines constants and functions at import time).
2. For each profile: a profile **with** `[profile] extends` keeps its own files under `profiles/<name>/overlay/`
   (the parent is installed first, the overlay copied on top); a profile without `extends` keeps them at
   `profiles/<name>/`. Resolve each `[category] subdir = [files]` entry with `install._resolve_path(category, subdir)`.
3. For each `[shared] <kind> = [...]` entry: the source is `shared/<kind>/<entry>` (file or directory); the
   installed destination is `.claude/<SHARED_DEST_PATHS[kind]>/`.
4. Report categories of a manifest that `CATEGORY_PATHS` does not know (they would install under an improvised path).

**Rules**:
- ERROR if a declared file does not exist at the resolved path
- ERROR if a `[shared]` entry does not exist under `shared/<kind>/`
- WARNING if a manifest uses a category unknown to `CATEGORY_PATHS`, or a `[shared]` kind unknown to `SHARED_DEST_PATHS`
- WARNING if a profile has no `manifest.toml`
- INFO: report total entries declared and problems found
- The opposite direction (files in `overlay/` declared nowhere) is enforced by the CI job "Validate profile manifests" ("silent-extra")

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import importlib.util, tomllib
from pathlib import Path
CL = Path("../streamtex-claude").resolve()
spec = importlib.util.spec_from_file_location("stx_claude_install", CL / "install.py")
inst = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inst)              # defines CATEGORY_PATHS, SHARED_DEST_PATHS, _resolve_path; installs nothing
problems, declared = [], 0
for prof in sorted(p for p in (CL / "profiles").iterdir() if p.is_dir()):
    if not (prof / "manifest.toml").is_file():
        problems.append(f"{prof.name}: no manifest.toml")
        continue
    man = tomllib.loads((prof / "manifest.toml").read_text(encoding="utf-8"))
    base = prof / "overlay" if man.get("profile", {}).get("extends") else prof   # overlay/ rule of inheriting profiles
    for cat, subdirs in man.items():
        if cat in ("profile", "shared"):
            continue
        if cat not in inst.CATEGORY_PATHS:
            problems.append(f"{prof.name}: category [{cat}] unknown to install.py CATEGORY_PATHS")
            continue
        for sub, files in subdirs.items():
            for f in files:
                declared += 1
                if not (base / inst._resolve_path(cat, sub) / f).exists():
                    problems.append(f"{prof.name}: [{cat}] {sub} -> {(base / inst._resolve_path(cat, sub) / f).relative_to(CL)} missing")
    for kind, entries in man.get("shared", {}).items():
        if kind not in inst.SHARED_DEST_PATHS:
            problems.append(f"{prof.name}: [shared] {kind} unknown to install.py SHARED_DEST_PATHS")
        for e in entries:
            declared += 1
            if not (CL / "shared" / kind / e).exists():
                problems.append(f"{prof.name}: [shared] {kind} -> shared/{kind}/{e} missing "
                                f"(installed under .claude/{inst.SHARED_DEST_PATHS.get(kind, kind)}/)")
print(f"{declared} declared entries, {len(problems)} problem(s)")
print("\n".join(problems))
EOF
```

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

**Goal**: The three StreamTeX repositories that accept issues (`streamtex`, `streamtex-docs`, `streamtex-claude`) have consistent GitHub issue templates, and the shared `stx-issue/` command directory exists with all 6 command files. `streamtex-packs` and `streamtex-landing` have no issue templates today: report it as INFO, not as an error.

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
- `streamtex-claude/profiles/*/commands/`, `profiles/*/overlay/commands/`, `shared/commands/` → the commands that exist (`<namespace>/<name>.md` = `/<namespace>:<name>`; `shared/commands/<name>.md` = `/<name>`)
- `streamtex-claude/profiles/*/manifest.toml` → `[commands]` keys
- All git-tracked `.md`, `.j2`, `.py`, `.toml`, `.html` files across the 5 repos → slash command references (`_archive/` and CHANGELOGs excluded: history may cite retired commands)

**Method**:
1. Scan all command directories — every namespace directory name must start with `stx-`
2. Scan all `manifest.toml` `[commands]` keys — every key must start with `stx-`
3. Grep the 5 repos for bare namespace patterns: `/project:`, `/designer:`, `/developer:`, `/migration:`, `/coherence:`, `/presentation:` (without `stx-` prefix)
4. Grep for old path references: `commands/project/`, `commands/developer/`, `commands/designer/`, `commands/migration/`, `commands/coherence/`, `commands/presentation/`
5. **Existence**: every `/stx-<ns>:<name>` cited anywhere must be a command file that exists (command below)

**Rules**:
- ERROR if a command directory under `commands/` does not start with `stx-`
- ERROR if a manifest `[commands]` key does not start with `stx-`
- ERROR if any file contains a bare namespace slash command reference (e.g. `/developer:test-run` instead of `/stx-block:test`)
- ERROR if a cited `/stx-<ns>:<name>` command does not exist (a user typing it gets "unknown command"; an agent following the instruction stalls)
- WARNING if any file contains a bare namespace path reference (e.g. `commands/project/` instead of `commands/stx-block/`)
- INFO: report all namespace directories found and their prefix status

**How to check** (existence):
```bash
uv run --frozen python - <<'EOF'
import re, subprocess
from collections import defaultdict
from pathlib import Path
WS = Path("..").resolve()
CL = WS / "streamtex-claude"
cmds = {f"/{p.parent.name}:{p.stem}" for p in [*CL.glob("profiles/*/commands/*/*.md"),
        *CL.glob("profiles/*/overlay/commands/*/*.md"), *CL.glob("shared/commands/*/*.md")]}
cmds |= {f"/{p.stem}" for p in CL.glob("shared/commands/*.md")}
cited = defaultdict(set)
for repo in ("streamtex", "streamtex-docs", "streamtex-claude", "streamtex-packs", "streamtex-landing"):
    d = WS / repo
    files = subprocess.run(["git", "-C", str(d), "ls-files", "*.md", "*.py", "*.j2", "*.toml", "*.html"],
                           capture_output=True, text=True).stdout.split("\n")
    for f in filter(None, files):
        if "_archive/" in f or f.endswith("CHANGELOG.md"):
            continue
        for m in re.finditer(r"(?<![\w/.-])/(stx-[a-z-]+):([a-z][a-z0-9-]*)", (d / f).read_text(encoding="utf-8", errors="replace")):
            if f"/{m.group(1)}:{m.group(2)}" not in cmds:
                cited[f"/{m.group(1)}:{m.group(2)}"].add(f"{repo}/{f}")
print(f"{len(cmds)} commands exist; {len(cited)} cited command(s) do not exist:")
for c in sorted(cited):
    print(f"  {c}  <- {', '.join(sorted(cited[c])[:4])}{' ...' if len(cited[c]) > 4 else ''}")
EOF
```

---

## Check 22: Release & Deploy Pipeline Coherence (scope: library, all)

**Goal**: The catalog describes the release pipeline **as it really works**, the published state is coherent
(version → PyPI → tag → GitHub Release), and what the documentation site deploys is exactly what its CI tested.

**How a release really happens** (read `streamtex/.github/workflows/auto-tag.yml` at each audit; if it changed,
update this description first):
1. **Publication is automatic.** Any push to `main` that touches `pyproject.toml` runs `auto-tag.yml`. It compares
   the `version` line of `HEAD` with `HEAD~1`; when they differ it runs tests + lint, builds, checks the
   artifacts for LFS pointers, **publishes to PyPI** (trusted publishing, `skip-existing: true`), then creates the
   `vX.Y.Z` GitHub Release (notes = the CHANGELOG section of that version only, `--target main`).
2. **There is no approval gate.** The GitHub environment `pypi` has no protection rule: nobody is asked.
3. **Cancelling does not help.** Once the "Publish to PyPI" step has run, the wheel is on PyPI; cancelling the run
   afterwards only marks it "cancelled" (seen on 0.7.40: published 00:36:31Z, cancelled 00:46:58Z). PyPI versions
   cannot be re-used.
4. **Several bumps in one push = one release.** Only the last commit's version is compared with its parent:
   intermediate versions of the push are never published (0.7.35-0.7.39 were never on PyPI), and a bump that is
   not in the **last** commit of the push publishes nothing (`bumped=false`).
5. **Consequence — no push without an explicit request to the author.** Never push to any StreamTeX repository
   unless the author (NG) explicitly asked for that specific push, in a dedicated question stating repository,
   branch, commits, the workflows the push triggers and whether it **publishes**. Local commits on branches are
   fine; changing the `streamtex` version needs the author's explicit line.

The former manual checklist (`uv build && uv publish`, `git tag`, `gh release create`) is **removed**: running it
by hand next to `auto-tag.yml` races the workflow (double publication attempt, tag/release created twice or
pointing at different commits). The only manual release step is the reviewed bump commit on `main`.

**Docs site — tested version = deployed version**: `streamtex-docs` must install in its Docker image the exact
`streamtex` version recorded in its `uv.lock` (the version its CI tests) and `.stx-version`. A
`--upgrade-package streamtex` (or `--upgrade`) in the Dockerfile installs the latest PyPI release at every Coolify
build — an untested version reaches production on the next rebuild.

**Source files**:
- `streamtex/pyproject.toml` (version), `streamtex/CHANGELOG.md`, `streamtex/.github/workflows/auto-tag.yml`
- PyPI (`https://pypi.org/pypi/streamtex/json`), git tags, GitHub Releases and workflow runs (`gh`, network)
- `streamtex-docs/uv.lock`, `streamtex-docs/.stx-version`, `streamtex-docs/Dockerfile`, `streamtex-docs/.github/workflows/{ci,hetzner-deploy}.yml`

**Rules**:
- ERROR if the library version is not on PyPI while `main` already carries it (the publish step failed)
- ERROR if there is no `v{version}` tag or no GitHub Release for a version that is on PyPI
- ERROR if `streamtex-docs/Dockerfile` upgrades `streamtex` at build time (`--upgrade-package streamtex`, `--upgrade`)
- ERROR if `streamtex-docs/uv.lock` and `streamtex-docs/.stx-version` name different `streamtex` versions
- ERROR if any document (skill, command, README, manual) prescribes a manual `uv publish` / `git tag` / `gh release create` for `streamtex`
- WARNING if `auto-tag.yml` no longer matches the description above (gate added, trigger changed, comparison changed): update this check
- WARNING if the last `auto-tag.yml` run is not `success` — read its steps: "cancelled" after "Publish to PyPI" still means published
- WARNING if the GitHub Release notes cover only the last CHANGELOG section while intermediate versions were never published (their changes are invisible in the release)
- WARNING if the latest `ci.yml` or `hetzner-deploy.yml` run of `streamtex-docs` failed
- INFO: report the complete pipeline state (version, PyPI, tag, release, last runs, docs lock / pin / Dockerfile)

**How to check** (network: PyPI and `gh`, read-only):
```bash
uv run --frozen python - <<'EOF'
import json, subprocess, tomllib, urllib.request
from pathlib import Path
WS = Path("..").resolve()
sh = lambda *a: subprocess.run(a, capture_output=True, text=True).stdout.strip()
lib = tomllib.loads((WS / "streamtex/pyproject.toml").read_text())["project"]["version"]
pypi = set(json.load(urllib.request.urlopen("https://pypi.org/pypi/streamtex/json", timeout=20))["releases"])
wf = (WS / "streamtex/.github/workflows/auto-tag.yml").read_text()
print(f"library {lib} | on PyPI: {lib in pypi} | tag v{lib}: {bool(sh('git', '-C', str(WS / 'streamtex'), 'tag', '-l', f'v{lib}'))}")
print("auto-tag.yml: push to main on pyproject.toml:", "branches: [main]" in wf and "pyproject.toml" in wf,
      "| compares HEAD with HEAD~1 only:", "HEAD~1:pyproject.toml" in wf, "| skip-existing:", "skip-existing: true" in wf)
print("GitHub release:", sh("gh", "release", "view", f"v{lib}", "-R", "nicolasguelfi/streamtex", "--json", "tagName,isDraft,targetCommitish") or "NONE")
print("last auto-tag run:", sh("gh", "run", "list", "-R", "nicolasguelfi/streamtex", "--workflow=auto-tag.yml",
                                "--limit", "1", "--json", "conclusion,headSha,createdAt"))
print("pypi environment protection rules:", sh("gh", "api", "repos/nicolasguelfi/streamtex/environments/pypi",
                                                "--jq", "[.protection_rules[].type]") or "not readable")
lock = tomllib.loads((WS / "streamtex-docs/uv.lock").read_text())
locked = next(p["version"] for p in lock["package"] if p["name"] == "streamtex")
pin = (WS / "streamtex-docs/.stx-version").read_text().strip()
upg = [l.strip() for l in (WS / "streamtex-docs/Dockerfile").read_text().splitlines()
       if "--upgrade" in l and not l.strip().startswith("#")]
print(f"streamtex-docs: uv.lock {locked} | .stx-version {pin} | Dockerfile upgrades at build: {upg or 'no'}")
for wfn in ("ci.yml", "hetzner-deploy.yml"):
    print(f"streamtex-docs {wfn}:", sh("gh", "run", "list", "-R", "nicolasguelfi/streamtex-docs", f"--workflow={wfn}",
                                       "--limit", "1", "--json", "conclusion,headSha"))
EOF
```

**Correct release procedure** (the author decides each step; an agent proposes, never pushes on its own):
1. On a branch: bump `version` in `streamtex/pyproject.toml`, add the `## [X.Y.Z]` CHANGELOG entry (one entry per published version), run tests and lint
2. Author reviews and merges into `main` **with the bump in the last commit**, then pushes himself (or explicitly asks for that push) — `auto-tag.yml` publishes, tags and releases
3. Verify with the command above (PyPI, tag, release, run)
4. `streamtex-docs`: `uv lock --upgrade-package streamtex`, set `.stx-version` to the same version, let its CI pass, then the author pushes (`hetzner-deploy.yml` deploys); re-run the command above

---

## Check 23: CE Agent Sync (scope: profiles, all)

**Goal**: All CE agents declared in `manifest.toml` (`[agents] ce`) exist as files in `ce/agents/`, and reciprocally every file in `ce/agents/` is declared in the manifest.

**Source files**: `streamtex-claude/profiles/project/manifest.toml` — `[agents] ce` list.

**Target files**: `streamtex-claude/profiles/project/ce/agents/*.md`

**Rules**:
- ERROR if a manifest entry has no corresponding `.md` file in `ce/agents/`
- ERROR if a `.md` file exists in `ce/agents/` but is not listed in the manifest
- INFO: report total agents declared vs found

The expected agent names are derived from the manifest at audit time — the list itself is not hardcoded here, to stay self-maintaining as the cycle evolves.

---

## Check 24: CE Template Sync (scope: profiles, all)

**Goal**: All CE templates declared in `manifest.toml` (`[templates] ce`) exist as files in `ce/templates/`, and reciprocally every file in `ce/templates/` is declared in the manifest.

**Source files**: `streamtex-claude/profiles/project/manifest.toml` — `[templates] ce` list.

**Target files**: `streamtex-claude/profiles/project/ce/templates/*.md`

**Rules**:
- ERROR if a manifest entry has no corresponding `.md` file in `ce/templates/`
- ERROR if a `.md` file exists in `ce/templates/` but is not listed in the manifest
- INFO: report total templates declared vs found

The expected template names are derived from the manifest at audit time — the list itself is not hardcoded here, to stay self-maintaining as the cycle evolves.

---

## Check 25: CE Docs Structure (scope: ce, all — N/A if no CE project is declared)

**Goal**: Projects with CE profile installed have the correct `docs/` directory structure for all CE artifacts.

**Scope**: the declared CE projects (below). Nothing else: there is no `projects/` folder convention.

**Declared CE projects** (shared by Checks 25 and 28): the workspace `stx.toml` entries `[repos.<name>]` with
`type = "project"` whose directory has `.claude/.stx-profile` and a `.claude/ce/` folder (CE installed). When the
list is empty the check is reported **N/A — no CE project declared** (never "OK"). To audit a project, declare it
in `[repos]` first.

```bash
uv run --frozen python - <<'EOF'
import tomllib
from pathlib import Path
WS = Path("..").resolve()
repos = tomllib.loads((WS / "stx.toml").read_text(encoding="utf-8")).get("repos", {})
projects = [WS / r.get("path", n) for n, r in repos.items() if r.get("type") == "project"]
ce = [p for p in projects if (p / ".claude/.stx-profile").is_file() and (p / ".claude/ce").is_dir()]
print("declared [repos] of type project:", [p.name for p in projects] or "none")
print("CE projects:", [p.name for p in ce] or "none -> checks 25 and 28 are N/A")
EOF
```

**Rules**:
- N/A (reported as such) if no CE project is declared
- WARNING if `docs/` directory does not exist (CE artifacts have nowhere to go)
- WARNING if any of the required subdirectories are missing: `collect/`, `assess/`, `plans/`, `prototypes/`, `reviews/`, `solutions/`, `master-plan/archive/`
- WARNING if `docs/solutions/` is missing any of the category subdirectories declared in the CE conventions (see `.claude/ce/skills/ce-conventions.md` and the solutions template for the authoritative list)
- INFO: report projects scanned and structure status

The required subdirectory list mirrors the artifact paths produced by CE skills; it is updated here whenever a new phase introduces a new artifact directory.

---

## Check 26: CE Cheatsheet Sync (scope: profiles, all)

**Goal**: The CE cheatsheet is present, up-to-date, and consistent with the manifest.

**Source files**: `streamtex-claude/shared/references/ce_cheatsheet_en.md`

**Rules**:
- ERROR if `ce_cheatsheet_en.md` does not exist
- ERROR if any CE command declared in `manifest.toml` (`[commands] stx-ce`) is missing from the cheatsheet
- WARNING if the cheatsheet agent count does not match the count in `manifest.toml` (`[agents] ce`)
- WARNING if the cheatsheet template count does not match the count in `manifest.toml` (`[templates] ce`)
- WARNING if the cheatsheet does not describe the current CE cycle (must mention the PROTOTYPE phase between PLAN and PRODUCE, and the INTEGRATE phase after COMPOUND)
- INFO: report cheatsheet presence and consistency

The audit derives expected commands, agents, and templates from the manifest at audit time — no enumeration is hardcoded here, to stay self-maintaining as the cycle evolves.

---

## Check 27: CE Command Registration (scope: profiles, all)

**Goal**: All CE commands declared in `manifest.toml` (`[commands] stx-ce`) exist as files in `commands/stx-ce/`, and reciprocally every file in `commands/stx-ce/` is declared in the manifest.

**Source files**: `streamtex-claude/profiles/project/manifest.toml` — `[commands] stx-ce` list.

**Target files**: `streamtex-claude/profiles/project/commands/stx-ce/*.md`

**Rules**:
- ERROR if a manifest entry has no corresponding `.md` file in `commands/stx-ce/`
- ERROR if a `.md` file exists in `commands/stx-ce/` but is not listed in the manifest
- WARNING if the corresponding skill file in `ce/skills/` does not exist for each command (skill name = `ce-<command>`)
- INFO: report total commands declared vs found

The expected command and skill names are derived from the manifest at audit time — the list itself is not hardcoded here, to stay self-maintaining as the cycle evolves.

---

## Check 28: CE Plan-Solution Coherence (scope: ce, all — N/A if no CE project is declared)

**Goal**: CE artifacts within a project are internally consistent.

**Scope**: the declared CE projects (same source and command as Check 25) that have a `docs/plans/` directory with
at least one plan file. N/A — reported as such — when no CE project is declared.

**Rules**:
- WARNING if a plan references block names (e.g., `bck_xxx`) that do not exist in `blocks/`
- WARNING if `docs/reviews/` contains a review but `docs/plans/` is empty (review without plan)
- WARNING if `docs/solutions/` contains solutions but `docs/reviews/` is empty (compound without review)
- WARNING if `docs/solutions/producer-profile.md` has `projects_count` > 0 but `last_updated` is more than 90 days old (stale profile)
- INFO: report CE artifact presence and coherence per project

---

## Check 28a: CE Master Plan Schema Integrity (scope: profiles, all)

**Goal**: Every `master-plan.yaml -> <field>` reference across CE skills, agents, templates, and the cheatsheet corresponds to a field actually defined in the master plan schema. This catches drift between the canonical schema and how the various CE artifacts read/write it.

**Source files**:
- `streamtex-claude/profiles/project/ce/templates/master-plan.md` — canonical schema (the YAML block under `## File 1 — docs/master-plan.yaml`)

**Target files** (referencing files to scan):
- `streamtex-claude/profiles/project/ce/skills/*.md`
- `streamtex-claude/profiles/project/ce/agents/*.md`
- `streamtex-claude/profiles/project/ce/templates/*.md`
- `streamtex-claude/shared/references/ce_cheatsheet_en.md`

**Method**:
1. Parse the YAML schema from `master-plan.md` (the canonical schema source). Build the set of valid top-level keys and nested paths, treating array index placeholders `[*]` and dict-key wildcards `*` as accepted shapes (e.g., `toc[*].sections[*].blocks[*].status` matches the schema's `toc: [parts: [sections: [blocks: [status: ...]]]]` structure).
2. In each target file, extract every occurrence of `master-plan.yaml -> <path>` with the regex
   `master-plan\.yaml\s*->\s*([A-Za-z_]\w*(?:\.[A-Za-z_*]\w*|\[[^\]]*\])*)` — a bracket group is `\[[^\]]*\]`,
   so placeholders such as `iterations[<current>]` are captured whole, and a trailing sentence dot is not part of
   the path (the former character class `[A-Za-z0-9_.\[\]*]*` cut `iterations[<current>]` to `iterations[` and
   kept `decisions_log.`).
3. For each extracted path, verify it corresponds to a defined field in the schema (after normalising index/wildcard placeholders).

**Rules**:
- ERROR if a `master-plan.yaml -> <path>` reference points to a path absent from the schema (drift detected)
- WARNING if the schema defines a top-level section never referenced by any target file (potential dead schema entry — except for `identity`, `pointers`, `iterations`, which are written but not deep-referenced)
- INFO: report total references checked and unique paths used

**Why this check matters**: the master plan schema is the single source of truth for orchestration metadata. References dispersed across 17+ skills/agents/templates are vulnerable to silent drift when the schema evolves. This check enforces the contract documented in the master-plan template header (commit `50f983d`).

---

# AI Quality Checks (scope: ai, all)

These checks detect problems specifically caused by AI-generated code and content. They address known failure modes of generative AI: hallucinated APIs, semantic drift between explanations and code, redundant abstractions, optimistic tests, and leaked secrets.

---

## Check 29: Ghost API Calls (scope: ai, all)

**Goal**: Detect function calls, parameters, and imports that reference StreamTeX API symbols which do not exist — "hallucinated" by the AI during code generation.

**Why this check is critical**: When AI generates code, it may invent plausible-sounding functions (`st_card()`, `st_tabs()`, `st_sidebar()`), parameters (`st_write(font_size=12)`), or imports (`from streamtex import st_dashboard`). These errors propagate to every project generated in the same session. Checks 13-14 partially cover this for docs blocks and show_code() examples, but this check extends coverage to **all generated code** across the ecosystem.

**Scope**: All Python files and Python code blocks in markdown across the entire ecosystem:
- `streamtex-docs/manuals/**/*.py` (rendered code, `show_code()` strings, and the `static/examples/**/*.py` files loaded by `show_code(file=)`)
- `streamtex-docs/templates/**/*.py`, `streamtex-docs/cheatsheets/*.md`
- `streamtex-claude/**/*.md` (Python fences — skills, agents, commands, designer templates and guidelines, references, import formats)
- `streamtex-packs/*/**/*.py` (components and design systems call the API too)
- declared projects (`[repos]` with `type = "project"`): their `blocks/**/*.py` and `book.py`

**Method**: run **Script G** (Appendix A) — it implements all of the following, so no step is skipped:
1. The valid API surface is `streamtex.__all__` plus every name importable from a `streamtex.<module>` that a file explicitly imports
2. Calls are resolved through aliases (`import streamtex as stx`, `from streamtex.x import y as z`); local definitions and non-streamtex imports shadow API names (a pack's own `cite` is not `streamtex.cite`)
3. Keyword arguments are checked against `inspect.signature()` of the function **or the class constructor**
4. Displayed snippets (show_code strings, static examples, markdown fences) are assumed to star-import streamtex; an unknown `st_*()` call there is a ghost
5. `from streamtex[.x] import X` statements are verified — `X` must exist in that module
6. Packs and declared projects are scanned by pointing the same script at them (extend `snippets()` with their files)

**Rules**:
- ERROR if a `st_*()` call references a function not in `__init__.py` exports
- ERROR if a `from streamtex import X` imports a name not in `__init__.py` exports
- ERROR if a keyword argument does not exist in the function's signature
- WARNING if a function is called with positional arguments in wrong order vs signature
- INFO: report total calls scanned, total files scanned, and ghost calls found

**How to check**: Script G (Appendix A), all lines.

**Difference from Checks 11, 13, 14**: Those checks cover specific scopes (Claude artifacts, rendered block code, show_code examples) and filter Script G's output by path. Check 29 is the **unified cross-ecosystem run** (packs and declared projects included) and specifically targets AI hallucination patterns (invented functions, plausible but non-existent parameters).

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
   - `import` statements where the imported name is never used in the file **and** there is no `# noqa: F401` marker on the import (which signals "intentional re-export")
   - `if False:` or `if 0:` blocks (AI sometimes disables code this way)
   - Consecutive duplicate function calls with identical arguments (AI stuttering)
3. Exclude framework-required patterns: `bs = BlockStyles`, `def build()`, `class BlockStyles`
4. **Skip re-export modules**: a file is considered a re-export shim when its only top-level content is `from X import a, b, c` lines (no logic, no `def`, no `class`, no `if __name__ ...`). The block-helper modules (e.g., `manuals/<name>/blocks/helpers.py`) are typical re-export shims that route a curated subset of streamtex names into a single local import path.

**How to check** (unused imports `F401`, unused local variables `F841`, redefinitions `F811` — ruff respects
`# noqa: F401` re-export markers and `.gitignore`; `--isolated` ignores the docs' own ruff ignores):
```bash
uv run --frozen ruff check --no-cache --isolated --select F401,F841,F811 --output-format concise \
    ../streamtex-docs/manuals ../streamtex-docs/templates
```
Unused module-level functions, `if False:` blocks and consecutive identical calls are not covered by ruff: review
them by reading the blocks flagged by Check 31/32, or grep `if False:` / `if 0:`.

**Rules**:
- WARNING if a variable is assigned but never referenced (excluding `bs`, `_static_dir`, `_repo_root`)
- WARNING if a function is defined but never called in the file
- WARNING if an import is never used **AND** has no `# noqa: F401` AND the file is not a re-export shim (per step 4)
- WARNING if consecutive identical calls exist (e.g., two `st_write()` with same content)
- INFO: report total blocks scanned, total dead code instances found

**Known exceptions**:
- `bs = BlockStyles` — used by the framework's block rendering
- `_static_dir`, `_repo_root` — path variables used in file operations
- Variables starting with `_` — intentionally unused (Python convention)
- Imports tagged `# noqa: F401` — intentional re-exports (Python convention, also respected by ruff)
- Re-export shim files (per step 4)

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

**Method** (frozen in the command below, so two audits give the same numbers):
1. **A — identical normalised bodies**: for every function of more than 5 lines, the body (docstring removed) is
   dumped as an AST in which the function's **own** locals (arguments and assigned names) are renamed `_`;
   globals, called functions and attributes keep their names. Equal dumps = copy-paste with renamed variables.
2. **B — private homonyms**: the same `_helper` name defined in several modules is a strong duplicate signal
   (each module re-implemented "its" helper).
3. **C — families to watch**: concepts already re-implemented several times. Any **new** member of a family is a
   WARNING; the fix is to reuse the existing helper. Families today: project/workspace root lookup, version
   string → tuple, `.env` parsing, `.gitignore` append, free-port test. Add a family when an audit finds a third copy.
4. Exclude tests, `__init__.py` re-exports and `@overload` stubs.

**Rules**:
- WARNING for each group of identical normalised bodies (A) across functions
- WARNING for each private homonym (B) whose bodies do the same job (read both before reporting)
- WARNING for each family (C) with a member added since the previous release (compare with Check 12d's release)
- INFO: report total functions scanned and the family sizes

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import ast, hashlib, re
from collections import defaultdict
from pathlib import Path
class Norm(ast.NodeTransformer):           # rename the function's own locals (args + assigned names) only
    def __init__(self, fn):
        self.local = {a.arg for a in ast.walk(fn.args) if isinstance(a, ast.arg)}
        self.local |= {n.id for n in ast.walk(fn) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
    def visit_Name(self, n):
        return ast.copy_location(ast.Name(id="_" if n.id in self.local else n.id, ctx=n.ctx), n)
bodies, private, defs = defaultdict(list), defaultdict(list), []
for py in sorted(Path("streamtex").rglob("*.py")):
    for fn in ast.walk(ast.parse(py.read_text(encoding="utf-8"))):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = fn.body[1:] if fn.body and isinstance(fn.body[0], ast.Expr) and isinstance(getattr(fn.body[0], "value", None), ast.Constant) else fn.body
        where = f"{py}:{fn.lineno} {fn.name}"
        defs.append((fn.name, where))
        if (fn.end_lineno - fn.lineno) >= 5 and body:
            dump = ast.dump(Norm(fn).visit(ast.Module(body=body, type_ignores=[])), annotate_fields=False)
            bodies[hashlib.sha1(dump.encode()).hexdigest()].append(where)
        if fn.name.startswith("_") and not fn.name.startswith("__"):
            private[fn.name].append(str(py))
print("A. identical normalised bodies (>5 lines):")
for locs in bodies.values():
    if len(locs) > 1:
        print("   ", " == ".join(locs))
print("B. private helpers defined in several modules:")
for name, mods in sorted(private.items()):
    if len(set(mods)) > 1:
        print(f"    {name}: {sorted(set(mods))}")
FAMILIES = {"project/workspace root lookup": r"find_.*root|_find_project_dir",
            "version string -> tuple": r"_?v(ersion)?_?tuple|parse_version|_vtuple",
            ".env parsing": r"(parse|read|load)_?(dot)?env",
            ".gitignore append": r"gitignore",
            "free/used port test": r"port_(free|in_use|available)|_is_port|free_port"}
print("C. families to watch:")
for fam, rx in FAMILIES.items():
    hits = [w for n, w in defs if re.search(rx, n, re.I)]
    print(f"    {fam} ({len(hits)}): {hits}")
EOF
```

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
- Project / pack usage: `streamtex-packs/*/**/*.py` and the declared projects (`[repos]` with `type = "project"`)

**Method**:
1. Extract all names from `__init__.py` exports
2. For each name, search for usage in: test files, documentation blocks, project files
3. Flag names with zero usage across all three categories

**Rules**:
- WARNING if an export has no usage in tests AND no usage in documentation AND no usage in packs or declared projects
- WARNING if an exported exception class is never raised by the library (`grep -rn "raise <Name>" streamtex/`) — users would catch something that cannot happen (e.g. `BibParseError`)
- INFO: report total exports, coverage breakdown (tested/documented/used/orphan)

**Known exceptions**: Same as Check 1 known exceptions (low-level internals, config getters, etc.)

---

## Check 36: Version Claims Accuracy (scope: ai, all)

**Goal**: Detect incorrect version claims in documentation and comments — where AI mentions "new in v0.X" or "since v0.X" or "deprecated in v0.X" but the version is wrong.

**Why this check is critical**: AI confabulates version numbers. It may write "new in v0.5" for a feature that was actually added in v0.3, or "deprecated in v0.4" for something still active. These claims mislead users about API stability and upgrade paths.

**Scope**: claims about **streamtex** versions, wherever they are written:
- library code: docstrings and comments of `streamtex/streamtex/**/*.py`
- `streamtex-docs/manuals/**/blocks/**/*.py` (in `show_explanation()`, `show_details()`, `st_write()` strings)
- `streamtex-claude/shared/references/*.md`, `streamtex/README.md`, `streamtex-packs/*/README.md`
- `streamtex/CHANGELOG.md` is the **reference**, not a target

**Out of scope**: versions of third-party software (Python, Streamlit, Click, uv, Playwright, Docker, ...) — a claim
is ignored when a third-party name appears in the 40 characters before it, or when the version is not a `0.x`
streamtex version.

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

**How to check** (finds the claims and verifies that the version exists; whether the feature really arrived in it
is then read in the CHANGELOG entry):
```bash
uv run --frozen python - <<'EOF'
import re
from pathlib import Path
WS = Path("..").resolve()
CLAIM = re.compile(r"\b(since|new in|added in|deprecated in|removed in|requires|available from)\s+(?:streamtex\s+|stx\s+)?v?(\d+\.\d+(?:\.\d+)?)", re.I)
THIRD = re.compile(r"\b(python|streamlit|click|uv|pydantic|node|npm|pip|playwright|docker|ruff|pytest|jinja2?|coolify|pygments|openai|plotly|numpy|pandas|chrome|tex|mermaid|plantuml|git|github|claude|macos|ubuntu)\b", re.I)
released = set(re.findall(r"^## \[(\d+\.\d+\.\d+)\]", (WS / "streamtex/CHANGELOG.md").read_text(encoding="utf-8"), re.M))
minors = {v.rsplit(".", 1)[0] for v in released}
files = [*WS.glob("streamtex/streamtex/**/*.py"), *WS.glob("streamtex-docs/manuals/**/blocks/**/*.py"),
         *WS.glob("streamtex-claude/shared/references/*.md"), WS / "streamtex/README.md", *WS.glob("streamtex-packs/*/README.md")]
total, bad = 0, []
for f in files:
    for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for m in CLAIM.finditer(line):
            if THIRD.search(line[max(0, m.start() - 40):m.end() + 15]) or not m.group(2).startswith("0."):
                continue                     # a third-party / Python version, not a streamtex claim
            total += 1
            if m.group(2) not in released and m.group(2) not in minors:
                bad.append(f"{f.relative_to(WS)}:{i}: '{m.group(0)}' — no {m.group(2)} in the streamtex CHANGELOG")
print(f"{total} streamtex version claims, {len(bad)} not backed by a CHANGELOG version")
print("\n".join(bad))
EOF
```

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
- `assert callable(f)` where `f` comes from `from M import f` — the import already guarantees it
- `assert hasattr(M, "n")` in a file that also does `from M import n` — same: true by import, tests nothing
  (`hasattr(streamtex, "X")` **alone** is a legitimate export test and is not flagged)

### 37b: Empty tests

A valid assertion is any of: a bare `assert ...` statement, a mock-validation method call (`mock.assert_called_once_with(...)`, `mock.assert_any_call(...)`, `mock.assert_not_called()`, etc.), or a `pytest.raises(...)` / `pytest.warns(...)` context manager. Counting only the keyword `assert` is incorrect — it misses the entire mock-validation pattern, which is the standard way to test wrapper functions that delegate to an external API.

- Test functions with **no** assertion of any of the kinds above
- Test functions where the only assertion is in a `try/except` that catches the assertion error
- Test functions that only call the function without checking anything (no `assert`, no `mock.assert_*`, no `pytest.raises`)

### 37c: Over-mocked tests

When comparing `@patch` count against "assertion" count, the assertion side MUST include `mock.assert_*` method calls (see 37b). A test that has 3 `@patch` decorators and 1 `mock.assert_called_once_with(...)` is NOT over-mocked — the mock-validation IS the assertion.

- Tests where `@patch` decorators **clearly** outnumber assertions of any kind (bare `assert` + `mock.assert_*` + `pytest.raises`)
- Tests where the mock's return value IS the expected value (testing the mock, not the code)
- Tests that mock internal implementation details (brittle coupling)

### 37d: Copy-paste tests and duplicated fixtures
- Two or more test functions with identical bodies (ignoring the function name)
- Test functions that differ by only one literal value but don't use parametrize
- Fixtures with identical bodies in several test files — move them to `tests/conftest.py`

### 37e: Missing edge cases
- Test functions that only test the happy path (no error/exception tests for a function that can raise)
- Functions with `Optional` parameters but no test with `None` value

**Rules**:
- WARNING for each tautological assertion found (37a)
- WARNING for each test function with no meaningful assertions (37b)
- WARNING for each over-mocked test (37c)
- WARNING for each copy-pasted test pair and each duplicated fixture (37d)
- INFO for missing edge case suggestions (37e)
- INFO: report total tests scanned, quality score (% of tests with meaningful assertions)

**How to check** (37a, 37b, 37d-fixtures; Playwright `expect(...)` counts as an assertion; a test that delegates
to an asserting helper is listed under "no assertion" — open it before reporting):
```bash
uv run --frozen python - <<'EOF'
import ast, hashlib
from collections import defaultdict
from pathlib import Path
taut, fixtures, empty, ntests = [], defaultdict(list), [], 0
for py in sorted(Path("tests").rglob("*.py")):
    tree = ast.parse(py.read_text(encoding="utf-8"))
    modalias = {a.asname or a.name: a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    fromimp = {(n.module, a.name): a.asname or a.name for n in ast.walk(tree)
               if isinstance(n, ast.ImportFrom) and n.module for a in n.names}
    fromnames = set(fromimp.values())
    for fn in ast.walk(tree):
        if not isinstance(fn, ast.FunctionDef):
            continue
        if any("fixture" in ast.unparse(d) for d in fn.decorator_list):
            body = ast.dump(ast.Module(body=fn.body, type_ignores=[]), annotate_fields=False)
            fixtures[hashlib.sha1(body.encode()).hexdigest()].append(f"{py}:{fn.lineno} {fn.name}")
            continue
        if not fn.name.startswith("test"):
            continue
        ntests += 1
        asserts = [n for n in ast.walk(fn) if isinstance(n, ast.Assert)]
        checks = asserts + [n for n in ast.walk(fn) if isinstance(n, ast.Call)
                            and (getattr(n.func, "attr", "").startswith("assert_") or getattr(n.func, "id", "") == "expect"
                                 or ast.unparse(n.func) in ("pytest.raises", "pytest.warns", "pytest.fail"))]
        if not checks:
            empty.append(f"{py}:{fn.lineno} {fn.name} — no assertion")
        for a in asserts:
            t = a.test
            if isinstance(t, ast.Constant) and t.value:
                taut.append(f"{py}:{a.lineno} assert {t.value!r}")
            elif isinstance(t, ast.Call) and getattr(t.func, "id", "") == "callable" and t.args \
                    and isinstance(t.args[0], ast.Name) and t.args[0].id in fromnames:
                taut.append(f"{py}:{a.lineno} {ast.unparse(t)} — the from-import already guarantees it")
            elif isinstance(t, ast.Call) and getattr(t.func, "id", "") == "hasattr" and len(t.args) == 2 \
                    and isinstance(t.args[0], ast.Name) and isinstance(t.args[1], ast.Constant) \
                    and (modalias.get(t.args[0].id), t.args[1].value) in fromimp:
                taut.append(f"{py}:{a.lineno} {ast.unparse(t)} — the file already imports {t.args[1].value}")
print(f"{ntests} tests | no assertion: {len(empty)} | tautological: {len(taut)}")
print("\n".join(empty + taut))
print("duplicated fixtures (identical bodies):")
for locs in fixtures.values():
    if len(locs) > 1:
        print("   ", " == ".join(locs))
EOF
```

---

## Check 38: Silent Failures (scope: ai, all)

**Goal**: Detect error handling patterns that silently swallow exceptions — a common AI pattern where `try/except` blocks catch errors but do nothing with them.

**Why this check is critical**: AI adds defensive `try/except` blocks around code it's unsure about. These hide bugs during development and cause mysterious failures in production. Silent failures are especially dangerous in a documentation/rendering library where a swallowed exception means missing content with no error message.

**Scope**: `streamtex/streamtex/**/*.py` (library source code)

**Method** (frozen — the command below is the method; a count that cannot be reproduced with it is not a
finding. The "32 silent excepts" of an earlier audit could not be reproduced by any method: that is why the method
is now fixed):
1. Parse each source file's AST — code inside strings (templates, generated scripts, `show_code` text) is
   therefore never counted, unlike a grep
2. A handler is **broad** when it catches nothing specific: bare `except:`, `except Exception`,
   `except BaseException` (alone or in a tuple). A narrow type (`ImportError`, `OSError`, `(TypeError, ValueError)`,
   ...) documents the intent and is out of scope
3. A broad handler is **silent** when its body only contains these forms (enumerated, nothing else):
   - `pass`, `...`, `continue`, `break`, a bare string
   - `return`, `return None`, `return <constant>` (`""`, `0`, `False`), `return []` / `{}` / `()` / `set()`-like literals, `return <name>`
   - `<name> = <constant | literal | name>` (falling back to a default)
4. A silent handler is **reported** (it does something observable) when its text contains logging, a warning,
   `print`, `console`, `click.echo/secho`, `st.error/warning/exception`, `raise`, or a call to a `report*` helper —
   then it is not silent and not counted
5. A silent broad handler is **justified** only by an explanatory comment written by a person, inside the
   handler or on the line just before `except`. **`# noqa` (e.g. `# noqa: BLE001`), `# type: ignore`, `# pragma`
   and `# nosec` are NOT justifications** — they silence a linter, they do not explain why swallowing is right

**Rules**:
- WARNING if a **bare** `except:` is found (always a code smell — too broad, even with a comment)
- WARNING for each broad + silent + unjustified handler (step 5); give file:line and what the swallowed failure hides
- INFO: report total handlers, broad handlers, silent+justified, silent+unjustified — and the delta with the previous audit

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import ast, re
from pathlib import Path
BROAD = {None, "Exception", "BaseException"}
LOUD = re.compile(r"(log(ger|ging)?\.|warn|print|console|echo|secho|st\.(error|warning|exception)|raise|ClickException|report)", re.I)
def silent(body):
    for s in body:
        if isinstance(s, (ast.Pass, ast.Continue, ast.Break)):
            continue
        if isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant):
            continue
        if isinstance(s, ast.Return) and (s.value is None or isinstance(s.value, (ast.Constant, ast.List, ast.Dict, ast.Tuple, ast.Set, ast.Name))):
            continue
        if isinstance(s, ast.Assign) and isinstance(s.value, (ast.Constant, ast.List, ast.Dict, ast.Name)):
            continue
        return False
    return True
total = broad = 0
justified, unjustified = [], []
for py in sorted(Path("streamtex").rglob("*.py")):
    lines = py.read_text(encoding="utf-8").splitlines()
    for h in ast.walk(ast.parse("\n".join(lines))):
        if not isinstance(h, ast.ExceptHandler):
            continue
        total += 1
        names = {None} if h.type is None else {getattr(e, "id", getattr(e, "attr", "?"))
                                               for e in (h.type.elts if isinstance(h.type, ast.Tuple) else [h.type])}
        if not names & BROAD:
            continue
        broad += 1
        src = "\n".join(lines[h.lineno - 1:h.end_lineno])
        if not silent(h.body) or LOUD.search(src.split("\n", 1)[-1] if "\n" in src else ""):
            continue
        comments = [c for c in re.findall(r"#(.*)", src + "\n" + lines[h.lineno - 2])
                    if not re.match(r"\s*(noqa|type:|pragma|nosec)", c)]
        (justified if comments else unjustified).append(f"{py}:{h.lineno} except {'/'.join(sorted(n or 'bare' for n in names))}")
print(f"{total} handlers | broad: {broad} | silent+justified: {len(justified)} | silent+UNJUSTIFIED: {len(unjustified)}")
print("\n".join(unjustified))
EOF
```

**Why these escape hatches**: in a rendering library the right pattern is often "try the enriched render, fall back to plain text on any error". Forcing logging on every such fallback creates noise; an explanatory comment + narrow exception type already conveys intent to the next reader.

---

## Check 39: Naming Coherence (scope: ai, all)

**Goal**: Detect inconsistent naming for the same concept across the codebase — where AI used different terms for identical things in different sessions.

**Why this check is critical**: AI lacks naming memory across sessions. The same concept may be called `config` in one module, `settings` in another, and `options` in a third. For parameters: `style` vs `l_style` vs `list_style`. This inconsistency confuses users and makes the API harder to learn.

**Scope**: `streamtex/streamtex/**/*.py` (library source code, public API) and `streamtex/tests/` (file names,
identifiers cited)

**Method**:
1. Extract all public function parameter names across the library
2. Group parameters by semantic concept (NOT by surface name — see "Known accepted variations" below for why `title` / `label` / `name` belong to different semantic groups despite often being grouped at first glance):
   - Style-related: `style`, `l_style`, `list_style`, `grid_style`, `block_style`
   - Content-related: `text`, `content`, `body`, `value`, `data`
   - Configuration: `config`, `settings`, `options`, `params`
3. Flag cases where the same concept uses different names across functions at the same level of API

4. **Test file names**: a test file is named after **what it tests** (`test_i18n.py`, `test_run_set.py`), never
   after the work package, ticket, board or session that produced it (`test_lot_c_production.py`,
   `test_audit1.py`, `test_fix2.py`): those names say nothing once the session is over and hide which module is covered
5. **Identifiers cited in code**: tracking identifiers written in library or test code — `(L14)`, `lot C`, ... —
   must be **defined** in a versioned document of the repository (CHANGELOG entry, design note) that says what
   they mean. An identifier defined nowhere is noise for every future reader. Prefer describing the behaviour
   in the comment over citing an identifier.

**Rules**:
- WARNING if two `st_*` functions use different parameter names for semantically identical concepts (e.g., one uses `style` and another uses `s` for the block style parameter)
- WARNING if a parameter name changed between function versions but the old name still appears in docs/examples
- WARNING if a public parameter's annotation contradicts its use (e.g. `style: str` where a `Style` object is expected)
- WARNING for each test file named after a work package / ticket / session (step 4) — rename after the subject
- WARNING for each identifier cited in code and defined in no tracked `.md` (step 5)
- INFO: report naming patterns found, consistency score

**How to check** (steps 4 and 5):
```bash
uv run --frozen python - <<'EOF'
import re, subprocess
from pathlib import Path
WORK = re.compile(r"^test_(lot|l\d+|audit\d*|board|batch|sprint|ticket|issue\d+|fix\d*|misc|new|tmp|wip)(_|\.py$)", re.I)
print("test files named after a work package:", sorted(str(p) for p in Path("tests").rglob("test_*.py") if WORK.match(p.name)) or "none")
ID = re.compile(r"\((L\d{1,2})\)|\b[Ll]ot ([A-F])\b")
cited = {}
for p in [*Path("streamtex").rglob("*.py"), *Path("tests").rglob("*.py")]:
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        for m in ID.finditer(line):
            cited.setdefault(m.group(1) or f"lot {m.group(2)}", []).append(f"{p}:{i}")
docs = "\n".join(Path(f).read_text(encoding="utf-8", errors="replace")
                 for f in subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True).stdout.split())
undefined = {k: v for k, v in cited.items() if not re.search(rf"(^|\n)\s*[-*|#]*\s*\**{re.escape(k)}\**\s*[:—|-]", docs, re.I)}
print(f"{len(cited)} identifiers cited in code, {len(undefined)} defined nowhere in a tracked .md:")
for k, v in sorted(undefined.items()):
    print(f"  {k}: {len(v)} site(s), e.g. {v[0]}")
EOF
```

**Known accepted variations** (NOT inconsistencies — distinct semantic concepts):
- `l_style` (st_list) vs `style` (st_block) — different component types, different naming is acceptable
- Abbreviated vs full names within the same function (e.g., `t` for Tags alias) — convention, not inconsistency
- **`title` vs `label` vs `name`** — these denote three different concepts and must NOT be flagged together:
  - **`title`** = section / panel / heading text shown to the user (used by `st_bibliography`, `st_presentation_footer`, `st_hover_tooltip`)
  - **`label`** = caption or label text that annotates something else (used by `st_metric`, `st_write`, `st_marker`)
  - **`name`** = semantic identifier used for filename / cache key / DOM id (used by `st_image` where `name="hero_intro"` controls the on-disk filename of an AI-generated image)
  - The audit's older grouping "Label/title" lumped these three; that grouping was wrong and is removed from the Method step above.

---

## Check 40: Secret Leak Scan (scope: ai, all)

**Goal**: Detect API keys, tokens, passwords, and other secrets accidentally committed to version control — a risk when AI copies configuration examples with real values.

**Why this check is critical**: AI may copy a working `.env` example or API key from context into generated code. Unlike human developers who know to redact secrets, AI treats all context as valid content. One leaked token in a committed file can compromise external services.

**Scope**: every **git-tracked** file of the 5 repositories (`git -C <repo> ls-files`), so ignored files and
`.venv` / `node_modules` are excluded by construction — `streamtex`, `streamtex-docs`, `streamtex-claude`,
`streamtex-packs`, `streamtex-landing` — plus the declared projects. Also check that each repo's `.gitignore`
ignores a `.venv` **symlink** (`.venv`, not only `.venv/`, which matches directories only): a `git add -A` would
otherwise version the link and leak the local path.

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
- WARNING if a repository's `.gitignore` does not ignore a `.venv` symlink:
  ```bash
  for r in streamtex streamtex-docs streamtex-claude streamtex-packs streamtex-landing; do
    git -C ../$r check-ignore -q --no-index .venv && echo "$r: .venv ignored" || echo "$r: .venv NOT ignored"
  done
  ```
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
- The templates **generated** by `stx deploy` (Dockerfile, entrypoint, CI workflow) are checked by Check 49

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
- WARNING if a package is imported (even inside `try`) but declared nowhere — neither in `dependencies` nor in an extra (it only works when another package happens to pull it in); silent fallbacks on such packages are Check 50
- WARNING if a declared dependency is never imported (e.g. a leftover after a refactoring)
- INFO: report optional dependency groups, their packages, and import coverage

---

# Release & Install Integrity Checks (scope: integrity, all)

These checks protect what users install: the Claude profile files, the files `stx` writes into projects, the
`stx.toml` sections the library reads, the deploy templates it generates, and the dependencies it silently relies
on. Where an automated test exists, the check **runs the test** instead of re-implementing it, and the test is the
source of truth.

---

## Check 46: Identical Installers (scope: integrity, profiles, all)

**Goal**: `stx claude install <profile>` (the library installer, `streamtex/cli/claude_cmd.py`,
`collect_source_files`) places **at least** every file that the standalone `streamtex-claude/install.py` places
for the same profile — `[shared] skills`, `agents` and `import-formats` included. Two installers that diverge
give two different `.claude/` trees depending on how a user installed (the 0.7.40 audit measured 20 missing files
per profile: no `reuse-architecture.md`, empty `developer/agents/` and `import-formats/`).

**Source of truth**: the automated test
`tests/test_cli_claude.py::test_library_installer_places_every_file_of_the_standalone_installer`, parametrized over
the four profiles (`project`, `presentation`, `library`, `documentation`). It installs each profile with
`install.py`'s own code path into a pytest temporary directory and asserts that `collect_source_files` covers
every file (the rendered `CLAUDE.md` and the `.stx-profile` marker excepted). It is skipped when the sibling
`streamtex-claude` checkout is absent — in the workspace it must **run**, not skip.

**How to check**:
```bash
uv run --frozen pytest -q -p no:cacheprovider -rs \
    "tests/test_cli_claude.py::test_library_installer_places_every_file_of_the_standalone_installer"
```

**Rules**:
- ERROR if the test fails (the failure lists the missing files per profile)
- ERROR if the test is skipped inside the workspace (the comparison did not happen)
- WARNING if a file installed **only** by the library installer is not a generated file (`CLAUDE.md`, `.stx-profile`, `stx.lock`): the standalone installer should place it too, or the library should not
- Correction: fix the installer that misses files (usually by reading the manifest `[shared]` entries) — never remove files from the expected set to make the test pass
- After a change to either installer or to a manifest, run this check before Check 4

---

## Check 47: Formats of `.claude/stx.lock` and `.claude/.stx-profile` (scope: integrity, profiles, all)

**Goal**: the two files `stx` writes into projects and that are versioned with them keep a stable, readable format
across streamtex versions:
- `.claude/stx.lock` (project mode) carries `[lock] format = 1`. A lock without `format` (written by 0.7.35-0.7.40)
  is read as format 1. A **higher** format comes from a newer `stx` and must be **refused** with a clear message,
  never rewritten or deleted. `stx.lock` must never be treated as an orphan by `stx claude update`
  (it is in `claude_cmd._GENERATED_PATHS`).
- `.claude/.stx-profile` holds a single line: the profile name. The CLI writes `profile + "\n"`, `install.py` writes
  the bare name; the reader strips whitespace — both must stay readable by both.

**Source of truth**: `streamtex/cli/claude_project.py` (`LOCK_FORMAT`, `read_lock`, `write_lock`, `Lock`),
`streamtex/cli/claude_cmd.py` (`read_installed_profile`, `_GENERATED_PATHS`), `streamtex-claude/install.py`, and
the tests `tests/test_cli_claude_project_mode.py::test_lock_records_its_format_and_refuses_a_newer_one`,
`tests/test_cli_claude.py::test_install_writes_stx_profile`, `test_read_installed_profile*`.

**How to check**:
```bash
uv run --frozen pytest -q -p no:cacheprovider \
    "tests/test_cli_claude_project_mode.py::test_lock_records_its_format_and_refuses_a_newer_one" \
    tests/test_cli_claude.py -k "lock_records or stx_profile or read_installed_profile"
uv run --frozen python - <<'EOF'
import dataclasses, inspect, re
from pathlib import Path
from streamtex.cli import claude_cmd as cc, claude_project as cp
r, w = inspect.getsource(cp.read_lock), inspect.getsource(cp.write_lock)
fields = [f.name for f in dataclasses.fields(cp.Lock)]
print("stx.lock LOCK_FORMAT =", cp.LOCK_FORMAT,
      "| writer stamps format:", "format = {LOCK_FORMAT}" in w,
      "| missing format read as 1:", 'get("format", 1)' in r,
      "| higher format refused:", "fmt > LOCK_FORMAT" in r and "ClickException" in r)
print("Lock fields not written:", [f for f in fields if f not in w] or "none", "| not read:", [f for f in fields if f not in r] or "none")
print("stx.lock protected from orphan pruning:", cp.LOCK_PATH in cc._GENERATED_PATHS)
std = Path("../streamtex-claude/install.py").read_text(encoding="utf-8")
print(".stx-profile writers: CLI", re.findall(r'f\.write\((profile \+ "\\n")\)', inspect.getsource(cc)),
      "| install.py", re.findall(r'\.stx-profile"\)\.write_text\((\w+)', std),
      "| reader strips:", ".strip()" in inspect.getsource(cc.read_installed_profile))
EOF
```

**Rules**:
- ERROR if one of the tests fails
- ERROR if the writer no longer stamps `format`, a missing format is not read as 1, or a higher format is not refused
- ERROR if `stx.lock` can be pruned as an orphan
- ERROR if a field of `Lock` is written but not read (or the reverse) — a silent data loss at the next sync
- WARNING if the format changed (new key, renamed key, changed meaning) without bumping `LOCK_FORMAT`, a CHANGELOG
  note and a compatibility test for the previous format
- WARNING if the two `.stx-profile` writers stop agreeing on "one line = profile name"

---

## Check 48: `stx.toml` Sections Read by the Library (scope: integrity, cli, all)

**Goal**: every `stx.toml` section the library reads is documented for users and validated by `stx validate`
(a typo in an unvalidated section is silently ignored). Sections in scope today:

| Section | Read by | Keys |
|---|---|---|
| `[claude]` | `streamtex/cli/claude_project.py` (`read_declaration`) | `profile`, `include`, `exclude`, `mode`, ... |
| `[book.defaults]` | `streamtex/book.py` | exactly `BOOK_DEFAULT_KEYS` (introspected; unknown keys are warned at run time) |
| `[[run.documents]]` | `streamtex/cli/run_set.py` | `id`, `book`, `port` |
| `[[validate.rules]]` | `streamtex/cli/project_rules.py` | rule tables (`id`, ...) |

When a module starts reading a new section, add it to this table and to the command.

**Targets** (documentation): `streamtex/README.md`, `streamtex-claude/shared/commands/stx-guide.md`,
`streamtex-claude/shared/references/streamtex_cheatsheet_en.md`, `coding_standards.md`, the manual blocks.
**Validation**: `streamtex/cli/validate_cmd.py` and the modules it calls.

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import re
from pathlib import Path
from streamtex.book import BOOK_DEFAULT_KEYS
WS = Path("..").resolve()
SECTIONS = {"[claude]": ("claude", "streamtex/cli/claude_project.py"),
            "[book.defaults]": ("book", "streamtex/book.py"),
            "[[run.documents]]": ("run", "streamtex/cli/run_set.py"),
            "[[validate.rules]]": ("validate", "streamtex/cli/project_rules.py")}
docs = {p: p.read_text(encoding="utf-8", errors="replace") for p in [
    WS / "streamtex/README.md", WS / "streamtex-claude/shared/commands/stx-guide.md",
    WS / "streamtex-claude/shared/references/streamtex_cheatsheet_en.md",
    WS / "streamtex-claude/shared/references/coding_standards.md",
    *WS.glob("streamtex-docs/manuals/**/blocks/**/*.py")] if p.is_file()}
validate = "\n".join(Path(f).read_text(encoding="utf-8") for f in ("streamtex/cli/validate_cmd.py", "streamtex/cli/project_rules.py"))
for sec, (head, owner) in SECTIONS.items():
    assert re.search(rf'get\(["\']{head}["\']', Path(owner).read_text(encoding="utf-8")), f"{owner} no longer reads {sec}"
    documented = sorted(str(p.relative_to(WS)) for p, t in docs.items() if sec in t)
    validated = bool(re.search(rf'get\(["\']{head}["\']', validate))
    print(f"{sec:20} documented in: {documented or 'NOWHERE'} | validated by stx validate: {validated}")
undoc = [k for k in sorted(BOOK_DEFAULT_KEYS)
         if not any("[book.defaults]" in t and re.search(rf"^\s*{k}\s*=", t, re.M) for t in docs.values())]
print(f"BOOK_DEFAULT_KEYS ({len(BOOK_DEFAULT_KEYS)}) never shown in a [book.defaults] example: {undoc}")
EOF
```

**Rules**:
- WARNING if a section is documented nowhere (users cannot discover it)
- WARNING if `stx validate` does not validate a section: unknown keys (`[book.defaults]` vs `BOOK_DEFAULT_KEYS`), duplicate ids or ports (`[[run.documents]]`), rules without `id` (`[[validate.rules]]`) must be reported by `stx validate`, not discovered at run time
- WARNING if a key of `BOOK_DEFAULT_KEYS` is never shown in a `[book.defaults]` example
- ERROR if the command's assertion fails (the owner module no longer reads the section: update the table)
- INFO: report sections, documentation sites and validation status

---

## Check 49: Generated Deploy Templates ↔ `UV_NO_SOURCES` Discipline (scope: integrity, cli, all)

**Goal**: the files `stx deploy` generates (`generate_dockerfile()`, `generate_entrypoint()`,
`generate_ci_workflow()` in `streamtex/cli/deploy_cmd.py`) and the hand-written ones of `streamtex-docs`
(`Dockerfile`, `entrypoint.sh`, `.github/workflows/*.yml`) never let `uv` resolve `[tool.uv.sources]` (local
editable paths that do not exist in the image or on the CI runner). `uv sync --no-sources` covers **only that
command**: every later `uv run` / `uv pip` re-reads `pyproject.toml` and may re-sync from the local sources.

A uv command is covered when one of these holds:
- `UV_NO_SOURCES=1` is set for the whole file / job (`ENV UV_NO_SOURCES=1`, job-level `env: UV_NO_SOURCES: 1`, `export UV_NO_SOURCES=1`)
- the command itself has `--no-sources` or `UV_NO_SOURCES=1` in front
- the image deletes `[tool.uv.sources]` from `pyproject.toml` right after `uv sync --no-sources` (the
  `streamtex-docs/Dockerfile` pattern); an entrypoint inherits the coverage of the Dockerfile that built its image

Also: an image must not upgrade `streamtex` at build time (`--upgrade-package`, see Check 22), and
`uv run playwright install` requires the `pdf` extra to be installed by the same image.

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import re
from pathlib import Path
from streamtex.cli import deploy_cmd as d
WS = Path("..").resolve()
gens = {"generate_dockerfile()": d.generate_dockerfile(), "generate_entrypoint()": d.generate_entrypoint(),
        "generate_ci_workflow()": d.generate_ci_workflow()}
for f in ("streamtex-docs/Dockerfile", "streamtex-docs/entrypoint.sh", *[str(p.relative_to(WS)) for p in WS.glob("streamtex-docs/.github/workflows/*.yml")]):
    gens[f] = (WS / f).read_text(encoding="utf-8")
INHERIT = {"generate_entrypoint()": "generate_dockerfile()", "streamtex-docs/entrypoint.sh": "streamtex-docs/Dockerfile"}
strip_of = {}
for name, text in gens.items():
    file_level = bool(re.search(r"^\s*(ENV\s+UV_NO_SOURCES[= ]1|UV_NO_SOURCES:\s*[\"']?1|export\s+UV_NO_SOURCES=1)", text, re.M))
    stripped = bool(re.search(r"sed\s+-i\s+'/\^\\\[tool\\\.uv\\\.sources", text)) or strip_of.get(INHERIT.get(name), False)
    strip_of[name] = stripped
    uv = [(i, l.strip()) for i, l in enumerate(text.splitlines(), 1)
          if re.search(r"\buv (sync|run|lock|pip)\b", l) and not l.strip().startswith("#")]
    bad = [f"{i}: {l[:90]}" for i, l in uv if not (file_level or stripped) and "--no-sources" not in l and "UV_NO_SOURCES=1" not in l]
    upg = [f"{i}: {l[:90]}" for i, l in uv if "--upgrade-package" in l or "--upgrade" in l.split()]
    print(f"{name}: {len(uv)} uv command(s), file-level={file_level}, sources stripped={stripped}, uncovered={len(bad)}, upgrade-at-build={len(upg)}")
    for b in bad + [f"UPGRADE {u}" for u in upg]:
        print("    ", b)
EOF
uv run --frozen pytest -q -p no:cacheprovider tests/test_deploy_templates.py
```

**Rules**:
- ERROR for each uncovered `uv run` / `uv pip` / `uv sync` in a generated template (every user project deployed with `stx deploy` inherits it)
- ERROR for each uncovered uv command in a `streamtex-docs` deploy file
- ERROR if a template or Dockerfile upgrades `streamtex` at build time
- WARNING if a generated Dockerfile runs `uv run playwright install` while the dependencies it installs do not include the `pdf` extra
- Correction: set `ENV UV_NO_SOURCES=1` once in the generated Dockerfile (covers build and entrypoint) and `env: UV_NO_SOURCES: 1` at job level in the generated workflow; add a test in `tests/test_deploy_templates.py`

---

## Check 50: Silent Fallback on an Undeclared Dependency (scope: integrity, cli, all)

**Goal**: an `except ImportError` / `except ModuleNotFoundError` that **degrades silently** (no log, no warning,
no message) is acceptable only when the package it tries is **declared** — in `[project] dependencies` or in an
extra whose name the feature documents. A silent fallback on an undeclared package means the feature never works
for most users and nobody is told (0.7.40: `markdown` absent → `st_markdown`'s HTML export never converts;
`pygments` only present transitively).

**Scope**: `streamtex/streamtex/**/*.py`; packages mapped to distributions with
`importlib.metadata.packages_distributions()`; relative imports and the standard library are ignored.

**Known exceptions**: `tomli` (backport imported only on Python < 3.11, behind a `tomllib` import).

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import ast, re, sys, tomllib
from importlib.metadata import packages_distributions
from pathlib import Path
proj = tomllib.load(open("pyproject.toml", "rb"))["project"]
norm = lambda s: re.split(r"[\s\[<>=!~;]", s, maxsplit=1)[0].lower().replace("_", "-")
declared = {norm(d) for d in proj.get("dependencies", [])}
extras = {norm(d): g for g, ds in proj.get("optional-dependencies", {}).items() for d in ds}
dist_of = {k: [norm(v) for v in vs] for k, vs in packages_distributions().items()}
KNOWN = {"tomli"}
LOUD = re.compile(r"log(ger|ging)?\.|warn|print|console|raise|st\.(error|warning)|echo")
rows = []
for py in sorted(Path("streamtex").rglob("*.py")):
    for t in ast.walk(ast.parse(py.read_text(encoding="utf-8"))):
        if not isinstance(t, ast.Try):
            continue
        handlers = [h for h in t.handlers if h.type is not None and
                    {getattr(e, "id", "") for e in (h.type.elts if isinstance(h.type, ast.Tuple) else [h.type])} & {"ImportError", "ModuleNotFoundError"}]
        if not handlers:
            continue
        mods = {(a.name if isinstance(n, ast.Import) else n.module).split(".")[0]
                for n in t.body if isinstance(n, ast.Import) or (isinstance(n, ast.ImportFrom) and n.module and not n.level)
                for a in n.names} - {"streamtex"} - set(sys.stdlib_module_names)
        loud = any(LOUD.search(ast.unparse(h)) for h in handlers)
        for m in sorted(mods - KNOWN):
            dists = dist_of.get(m, [m.replace("_", "-")])
            if not (set(dists) & declared or set(dists) & set(extras)):
                rows.append(f"{py}:{t.lineno}: import {m} ({'/'.join(dists)}) -> UNDECLARED; fallback {'reports' if loud else 'is SILENT'}")
print("\n".join(rows))
print(f"{len(rows)} fallback(s) on an undeclared package, {sum('SILENT' in r for r in rows)} of them silent")
EOF
```

**Rules**:
- ERROR for each **silent** fallback on an undeclared package — declare the package (core or extra), or make the fallback report what is lost
- WARNING for each reporting fallback on an undeclared package — declare it as an extra and name the extra in the message
- INFO: silent fallbacks on declared extras (acceptable when the feature's documentation names the extra)

---

## Check 51: No Absolute Path Outside the Repository in `tests/` (scope: integrity, tests, all)

**Goal**: tests run anywhere — on CI, on another machine, in a fresh clone. A test that reads an absolute path
of one laptop (`/Volumes/...`, `/Users/...`, `~/.venvs/...`, a Dropbox folder) silently skips or fails everywhere
else, and leaks a private path. Fake absolute paths used only **as data** (a string compared in an assertion,
`"/Users/dev/external-pack"` in a generated `stx.toml`) are fine.

**Scope**: `streamtex/tests/**/*.py` (e2e included). The command flags absolute-path literals that reach a
filesystem call (`Path`, `open`, `os.path.*`, `shutil`, `subprocess`, `pytest.mark.skipif`, `.exists()` ...),
directly or through a module-level constant.

**How to check**:
```bash
uv run --frozen python - <<'EOF'
import ast, re
from pathlib import Path
ABS = re.compile(r"^(/Users/|/Volumes/|/home/|/opt/|/private/|[A-Za-z]:\\|~/)")
FS = re.compile(r"^(Path|open|os\.path\.\w+|os\.listdir|os\.scandir|shutil\.\w+|subprocess\.\w+|.*skipif|.*\.(exists|is_dir|is_file|read_text|read_bytes|iterdir|glob|resolve))$")
hits = set()
for py in sorted(Path("tests").rglob("*.py")):
    tree = ast.parse(py.read_text(encoding="utf-8"))
    consts = {t.id: n.value for n in ast.walk(tree) if isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant)
              and isinstance(n.value.value, str) and ABS.match(n.value.value) for t in n.targets if isinstance(t, ast.Name)}
    for c in ast.walk(tree):
        if isinstance(c, ast.Call) and FS.match(ast.unparse(c.func)):
            for a in [*c.args, *(k.value for k in c.keywords)]:
                for sub in ast.walk(a):
                    lit = sub if isinstance(sub, ast.Constant) and isinstance(sub.value, str) and ABS.match(sub.value) else \
                          consts.get(sub.id) if isinstance(sub, ast.Name) else None
                    if lit is not None:
                        hits.add(f"{py}:{c.lineno}: {ast.unparse(c.func)}(...) reads {lit.value[:70]!r}")
print(f"{len(hits)} filesystem access(es) to an absolute path outside the repo in tests/:")
print("\n".join(sorted(hits)))
EOF
```

**Rules**:
- ERROR for each test reading an absolute path outside the repository — use `tmp_path`, a fixture under `tests/`, or an environment variable with a documented `skipif`
- WARNING if such a test is in `tests/e2e/` and the CI never runs e2e (it then only ever runs on one machine)
- INFO: report the number of e2e tests and whether `.github/workflows/ci.yml` runs them

---

# Appendix A — Script G: ghost-API scanner (Checks 11, 14, 29)

One script, three checks: Check 11 keeps the `streamtex-claude/` lines, Check 14 the `streamtex-docs/` lines,
Check 29 all of them. Read-only. It scans:
- every `streamtex-docs/manuals/**/*.py` and `templates/**/*.py` file, the strings passed to `show_code()` /
  `show_code_inline()`, and the `static/**.py` files loaded by `show_code(file=...)`
- every `streamtex-packs/*/**/*.py` and every declared project's `.py` files (tests and caches excluded)
- the fenced Python of every `streamtex-claude/**/*.md` (except `_archive/`) and `streamtex-docs/cheatsheets/*.md`

Displayed snippets are assumed to star-import streamtex; local definitions and non-streamtex imports shadow API
names; `ILLUSTRATIVE` lists modules a manual invents on purpose ("add your own module") — keep it short and
re-check it at each audit. Output: one line per ghost (`path:line: call(kw=) — not in signature`, missing imported
name, missing module, unknown `st_*()`), then a count on stderr. `STX_WS=<dir>` points it at another workspace
copy (e.g. a `git archive` of an older commit, to verify the script still finds known ghosts).

```bash
uv run --frozen python - <<'EOF'
import ast, importlib, inspect, os, re, sys, textwrap, tomllib
from pathlib import Path
import streamtex
WS = Path(os.environ.get("STX_WS", "..")).resolve()
ILLUSTRATIVE = {"streamtex.my_feature", "streamtex.cli.mycommand_cmd"}
API = {n: getattr(streamtex, n) for n in streamtex.__all__}

def snippets():
    repos = tomllib.loads((WS / "stx.toml").read_text(encoding="utf-8")).get("repos", {}) if (WS / "stx.toml").is_file() else {}
    projects = [WS / r.get("path", n) for n, r in repos.items() if r.get("type") == "project"]
    for py in sorted([*WS.glob("streamtex-docs/manuals/**/*.py"), *WS.glob("streamtex-docs/templates/**/*.py"),
                      *WS.glob("streamtex-packs/*/**/*.py"), *(p for d in projects for p in d.glob("**/*.py"))]):
        if {".venv", "tests", "node_modules", ".stx_cache"} & set(py.parts):
            continue
        src = py.read_text(encoding="utf-8", errors="replace")
        yield py, src, False, 0
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        static = next((p / "static" for p in py.parents if (p / "static").is_dir()), None)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", "")) in ("show_code", "show_code_inline"):
                for a in node.args[:1]:
                    if isinstance(a, ast.Constant) and isinstance(a.value, str):
                        yield py, a.value, True, a.lineno - 1
                for kw in node.keywords:
                    if kw.arg == "file" and isinstance(kw.value, ast.Constant) and static:
                        f = static / kw.value.value
                        if f.suffix == ".py" and f.is_file():
                            yield f, f.read_text(encoding="utf-8"), True, 0
    for md in sorted([*WS.glob("streamtex-claude/**/*.md"), *WS.glob("streamtex-docs/cheatsheets/*.md")]):
        if ".venv" in md.parts or "_archive" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        for m in re.finditer(r"```python\n(.*?)```", text, re.S):
            yield md, m.group(1), True, text[:m.start(1)].count("\n")

def check(path, code, out, snippet, off):
    try:
        tree = ast.parse(textwrap.dedent(code))
    except SyntaxError:
        return
    alias = dict(API) if snippet else {}       # a displayed snippet usually omits `from streamtex import *`
    defined = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    for name in defined:                        # local definitions shadow the API
        alias.pop(name, None)
    mods = {"streamtex"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] != "streamtex":
            for a in node.names:                # a non-streamtex import shadows a star-imported name
                alias.pop(a.asname or a.name, None)
        if isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] == "streamtex":
            if node.module in ILLUSTRATIVE:
                continue
            try:
                mod = importlib.import_module(node.module)
            except ImportError:
                out.append(f"{path}: no module {node.module}")
                continue
            for a in node.names:
                if a.name == "*":
                    alias.update(API)
                elif not hasattr(mod, a.name):
                    out.append(f"{path}: from {node.module} import {a.name} — name does not exist")
                else:
                    alias[a.asname or a.name] = getattr(mod, a.name)
        elif isinstance(node, ast.Import):
            mods |= {a.asname or "streamtex" for a in node.names if a.name == "streamtex"}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if isinstance(f, ast.Name):
            name, obj = f.id, alias.get(f.id)
        elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id in mods:
            name, obj = f"{f.value.id}.{f.attr}", getattr(streamtex, f.attr, None)
            if obj is None:
                out.append(f"{path}:{node.lineno + off}: {name} does not exist")
                continue
        else:
            continue
        if obj is None and snippet and isinstance(f, ast.Name) and name.startswith("st_") and name not in defined:
            out.append(f"{path}:{node.lineno + off}: {name}() is not a streamtex export")
            continue
        if obj is None or not callable(obj):
            continue
        try:
            sig = inspect.signature(obj)            # functions and class constructors (dataclass configs included)
        except (TypeError, ValueError):
            continue
        if any(p.kind is p.VAR_KEYWORD for p in sig.parameters.values()):
            continue
        for kw in node.keywords:
            if kw.arg and kw.arg not in sig.parameters:
                out.append(f"{path}:{node.lineno + off}: {name}({kw.arg}=) — not in {name}{sig}")

out, n = [], 0
for path, code, snippet, off in snippets():
    n += 1
    check(path.relative_to(WS), code, out, snippet, off)
print("\n".join(sorted(set(out))))
print(f"{n} code units scanned, {len(set(out))} ghost(s)", file=sys.stderr)
EOF
```
