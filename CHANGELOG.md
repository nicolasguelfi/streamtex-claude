# Changelog — StreamTeX Claude Profiles

All notable changes to the StreamTeX Claude Code profiles will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Prior to this Changelog, changes are tracked in the git history of this repository (see `git log` on `main`).

## [Unreleased]

Coherence-check catalog repaired after the 0.7.40 coherence audit (board `audit1`, 2026-10-03): the catalog had
let the most serious defects of that audit through. Both copies of `coherence-checks.md` (library and
documentation overlays) stay identical.

### Added

- **Conventions** section at the top of `coherence-checks.md`: the five repositories (`streamtex`,
  `streamtex-docs`, `streamtex-claude`, `streamtex-packs`, `streamtex-landing`), projects audited only when
  declared in `stx.toml` `[repos]` with `type = "project"` (N/A otherwise), introspection instead of
  hand-written lists, read-only commands run from `streamtex/` with `uv run --frozen python`, and
  "`# noqa` is not a justification".
- **Check 1-bis — Star-import boundary**: runs `tests/test_star_import.py` (the star import exports exactly
  `__all__`, never a module, never `T`, `TF`, `current_lang`, `with_lang`, `set_languages`, `fact`).
- **Checks 46-51 — Release & install integrity** (new `integrity` scope; the numbers 46-49 were last used by
  the `patterns` checks retired in 0.2.0):
  46 identical installers (runs
  `tests/test_cli_claude.py::test_library_installer_places_every_file_of_the_standalone_installer`),
  47 `.claude/stx.lock` format (`format = 1`, higher format refused, never pruned) and `.claude/.stx-profile`,
  48 `stx.toml` sections read by the library (`[claude]`, `[book.defaults]` / `BOOK_DEFAULT_KEYS`,
  `[[run.documents]]`, `[[validate.rules]]`) documented and validated by `stx validate`,
  49 generated deploy templates (`generate_dockerfile` / `generate_entrypoint` / `generate_ci_workflow`) and the
  docs deploy files against the `UV_NO_SOURCES` discipline,
  50 silent `except ImportError` fallback on an undeclared dependency,
  51 no absolute path outside the repository read by `tests/`.
- **Appendix A — Script G**, one ghost-API scanner shared by Checks 11, 14 and 29: displayed code
  (`show_code()` strings, `static/examples` files loaded by `show_code(file=)`), designer templates and
  guidelines, packs, class constructors, `from streamtex.x import y`, alias resolution and shadowing.
- Every check that measures something now has an exact, runnable "How to check" command.

### Changed

- **Dead scopes removed**: `projects/`, `streamtex-docs/references/`, `streamtex-docs/README.md`; scopes
  extended to `streamtex-packs` and `streamtex-landing` where relevant (Checks 4, 5, 9, 10, 21, 29, 35, 36, 40).
  Checks 25 and 28 read the declared CE projects and are reported "N/A" when there is none.
- **Introspection instead of lists**: Check 1 from `streamtex.__all__` plus the explicit `streamtex.i18n` /
  `streamtex.facts` modules (7 vanished exceptions removed: the `export_*` buffer functions,
  `StreamTeX_Styles`); Check 14 from every callable of `__all__` (classes and configs included) instead of 22
  fixed functions; Check 15 from the enums of `__all__` and `streamtex.enums` (the non-existent
  `ListTypes.custom` is gone); Check 18 from `install.py` `CATEGORY_PATHS` / `SHARED_DEST_PATHS` and the
  `overlay/` rule of inheriting profiles; Check 4 from `stx claude check` / `stx claude diff`.
- **Check 22 rewritten** to the real pipeline: `auto-tag.yml` publishes to PyPI on any push to `main` that
  changes the version line (no approval gate; cancelling after the Publish step does nothing; several bumps in
  one push publish only the last); the manual `uv publish` / `git tag` / `gh release` checklist is removed;
  the docs image must install the version its CI tested (no `--upgrade-package`); no push without an explicit
  request to the author.
- **Wrong or tautological rules fixed**: Check 5 no longer compares `pyproject.toml` with `__version__` (read
  from installed metadata) and checks PyPI, tags, CHANGELOG versions never published and the
  `streamtex-claude` version; Check 12d compares with the previous release, not `git describe` on a tagged HEAD;
  Check 3 drops the `textwrap` rules; Check 6 "content after `show_*`" becomes INFO; Check 28a regex captures
  `[...]` groups; Check 30 uses `ruff --select F401,F841,F811`; Check 33 normalised bodies, private homonyms and
  families to watch; Check 36 limited to streamtex claims (library code included, third-party versions
  excluded); Check 37 flags `hasattr`/`callable` true by import and duplicated fixtures; Check 38 has a frozen
  AST method with the silent forms enumerated and code in strings ignored; Check 39 adds test-file naming and
  undefined tracking identifiers; Check 9 checks absolute links to untracked files; Check 16 evaluates computed
  paths and detects committed LFS pointers; Check 21 checks that every cited `/stx-x:y` exists.
- `/stx-coherence:audit`: scopes updated (`all` = 1-51 + 1-bis + 28a, new `integrity`, `tests` = 12 + 37 + 51),
  five-repository workspace, N/A reporting. `/stx-coherence:fix`: counts updated, Check 4 example turned into a
  backport (it showed an overwrite of a read-only `.claude/` copy). `/stx-guide`: "19 checks" → 51 + 1-bis + 28a,
  `integrity` scope listed, layer composition points to Check 18.

### Added — streamtex 0.7.35-0.7.40 in the references (streamtex-docs#11)

Every signature and option below was checked against streamtex 0.7.40 (`inspect.signature`, `stx … --help`).

- `streamtex_cheatsheet_en.md`: what `from streamtex import *` exports (`__all__` only, no sub-module,
  `list` no longer shadowed) and the explicit `streamtex.i18n` / `streamtex.facts` imports;
  `st_image(max_vw=, max_vh=, align=)` with the author's decision (`align=` is explicit, the
  `text-align` of a style passed to `st_image` does not place the image); `ScaleConfig.amphi()`;
  `st_book(lang=, scale=)`, `doc_version="auto"`, `[book.defaults]` (the `BOOK_DEFAULT_KEYS`);
  `ProjectBlockRegistry(blocks_dir, shared_dirs=[…])` and `list_shared_blocks()`;
  `BibConfig(strict=True)`, `BibConfig.projection()`; `CollectionConfig(card_border=, card_text_color=)`,
  `next_project()`, `st_next_deck()`; `st_slide`, `SLIDE_CONTAINER`, `set_slide_container`,
  `get_slide_container`; new sections on `load_json` / `load_toml` / `load_text` / `watch_file`,
  `kept_widget` / `kept_value`, `env_flag` / `is_editable` / `is_exportable`, `streamtex.i18n`
  (`T`, `TF`, `current_lang`, `with_lang`, `set_languages`) and `streamtex.facts` (`fact`, `stale_facts`,
  `facts/<source>.toml`); CLI: `stx run --set` with `[[run.documents]]`, `stx validate --build` options and
  `[[validate.rules]]`, `stx deploy diff` / `ci`, `stx claude sync`, `stx claude global status | remove`,
  `stx claude install --dry-run`, `--global-commands`.
- `presentation_cheatsheet_en.md`: `st_slide` (thin: title, marker and zoom stay in the block),
  `ScaleConfig.amphi()`, `stx run --set` to project several documents.
- `coding_standards.md`: the star-import rule, explicit image placement with `st_image(align=)`,
  `uv run stx validate --build` (and `--published`) before publishing, `doc_version="auto"`, `stx run --set`.
- `/stx-guide`: Section 3 gains `stx run` (with `--set`, `--doc`, `--list`, `--kill`, `--fresh`, `--lang`,
  `--ports-offset`, `--open`, `--chrome-profile`, `[[run.documents]]`), `stx validate` (`--build`, `--book`,
  `--timeout`, `--snapshot`, `--against`, `--published`, the limits of the fingerprint, `[[validate.rules]]`),
  `stx claude install --dry-run / --yes`, `stx claude sync [--dry-run/--force/--remove]`, project mode
  (`[claude]`, `.claude/stx.lock` format 1), `stx claude global status / remove`,
  `--global-commands / --no-global-commands`, `stx deploy diff`, `stx deploy ci`, and a section
  "Installation: project mode vs machine mode"; quick-reference rows for the new commands; the `CLAUDE.md`
  propagation row and the global-commands note describe 0.7.35 behaviour.

### Fixed — `/stx-guide` counters measured against the manifests

- §4.2b, `project` profile (measured on `profiles/project/manifest.toml` and an `install.py` run):
  Skills 8 → 15 (9 own + 6 shared), Agents 3 → 8 (6 own + 2 shared), Agents CE 18 → 21, Templates CE
  17 → 19, Import 6 → 7 (`/stx-import:latex`, also in §4f and Section 6).
- `streamtex_cheatsheet_en.md`: `st_book(chrome_banner=)` defaults to `False` (the signature said `True`).

### Fixed — ghost APIs and stale advice in the profiles (board `audit1`)

- Designer templates and `modular-design-philosophy`: `st_book` has no
  `design_system=` parameter (it never had); the design system is created in the
  block and passed to pack components (`design_system=DS`).
- `visual-design-rules`: the legacy `ptn_*` patterns → `streamtex-pack-design`
  components.
- `streamtex_cheatsheet_en.md`: `ptn_cite` → `cite`; `GSheetSource(tab=)`;
  `TOCConfig(sidebar_max_level=)`; `st_image(prompt=)` instead of `st_ai_image()`;
  the `StreamTeX_Styles` section removed (alias removed in streamtex 0.7.14);
  `BibParseError` documented as exported but not raised.
- Six designer/presentation guidelines: `SlideBreakDisplayConfig(space=)` →
  `before=` / `after=`; LaTeX import conventions: `Style(font_color=)` →
  `Style("color: …;", id)`.
- Slash commands that do not exist: `/stx-component:new|list|show|validate` →
  `/stx-component:run <sub>`; `/stx-block:slide-audit|slide-fix|style-audit` →
  `/stx-block:audit`, `/stx-block:fix`, `/stx-block:style-refactor`;
  `/stx-import:pptx|gdocs` marked "no command yet".
- "The star import shadows `list()`" is history since streamtex 0.7.36
  (testing-patterns, documentation CLAUDE.md template, `/stx-guide`).
- `/stx-guide`: `stx claude update` has no `--prune`; `--yes`, `--commit`, `--force`
  described as they are.

## [0.3.5] — 2026-10-03 — Project mode documented, CLAUDE.md templates for multi-module projects

Companion of streamtex 0.7.35 (lot A, boards `claude1` / `lots1`).

### Added

- **README — two ways to install** (#23): project mode (`[claude]` in
  `stx.toml`, `stx claude sync`, `.claude/stx.lock`) next to the classic
  machine mode (`~/.claude/commands` copied by `stx update`), with
  `stx claude global status | remove` and `global_commands = false`.

### Changed

- **`project` and `presentation` CLAUDE.md templates** (#24): describe both
  layouts (single book / one book per module with shared blocks and a
  local pack), served media (`configure_image_path`) instead of "base64",
  and that a block keeps its own explicit settings.
- **`profiles/project/settings.json`** (#25): `git add` and `git commit`
  are no longer granted by default (read-only git commands stay). Existing
  installs keep theirs: settings are merged, never pruned.
- **`install.py`** delegates to the streamtex installer when streamtex
  (≥ 0.7.35) is importable, so both ways of installing give the same
  result (nicolasguelfi/streamtex#65); the standalone path stays for
  environments without streamtex, such as this repository's CI.

## [0.3.4] — 2026-05-25 — /stx-guide: pack-dev + alignment sections + which-stx-command skill

### Added

- **`/stx-guide`**: new §4.12 *Pack development* documenting the
  existing `stx pack add --dev` and `stx dev` link/unlink/status
  workflows for iterating on a pack while a consumer (manual, project)
  consumes the local source.
- **`/stx-guide`**: new §4.13 *Alignment & sync* documenting when to
  use `stx update` vs `stx sync` vs `uv sync` vs their `--upgrade-deps`
  / `--locked` variants, with a robust alignment sequence and
  troubleshooting for `uv.lock` flip-flop.
- **`/stx-guide` Section 6**: new *Decision table — which command for
  my situation?* — one-line answer per common situation, with pointers
  to detailed sections.
- **New skill `which-stx-command`** (shared, auto-loaded as
  `.claude/developer/skills/which-stx-command.md`): lazy-loader that
  routes decision-style questions ("which command should I run for X?",
  "how do I sync/align?") to the relevant section of `/stx-guide`.
  Single source of truth: all content stays in `stx-guide.md`.
- **Two new recognized topics** in `/stx-guide`: `pack-dev` and
  `alignment`.

### Notes

- Requires streamtex >= 0.7.15 for the documented `stx sync` and
  `stx update --upgrade-deps` commands.

## [0.3.3] — 2026-05-21 — Universal authoring trinity (plan + design rules + packs) for all doc types

Closes the GSE-ODOO root cause: `/stx-ce:go` produced 50 slides without ever
invoking the `slide-designer` agent or the design rules (scored 0/20).

### Changed

- **`ce-go`**: new *Step 0ter — Inventory Specialized Artefacts*. The
  orchestrator must enumerate `.claude/<role>/{agents,skills,guidelines,templates}/`
  and delegate to specialists (notably `slide-designer`) — authoring slides
  freehand is now defined as a defect, not a shortcut.
- **`ce-prototype`**: Phase 4 now authors pilot blocks **via the
  `slide-designer` agent**; Phase 5 is a **mandatory automated visual gate** —
  `stx screenshot` → vision review by `visual-reviewer`/`slide-reviewer` →
  self-correct loop — that runs even in autonomous / `/remote-control` mode
  (the agent's vision review replaces the human eye, never bypasses the gate).
  Phase 6 now asks the user to judge only editorial choices, since mechanical
  defects are caught automatically.
- **`ce-produce`**: slide/content authoring delegated to `slide-designer`
  (the "command-driven, no standalone agents" framing that orphaned the agent
  is corrected); global verification adds a rendered visual check; new
  **anti-amplification rule** (capture + review every ~10 blocks; no parallel
  authoring before one rendered batch passes the gate).
- **`ce-assess`**: new requirement **R27 — Design Guideline** selection
  (`maximize-viewport` / `minimalist-visual` / …), persisted to
  `custom/design-guideline.md` for slide projects.
- **`visual-reviewer` / `slide-reviewer` agents**: now review the **rendered
  screenshots** (`docs/_screens/`, via vision) as primary evidence, with an
  auto-detection checklist (unreadable fonts, > ~40% empty viewport, overflow,
  overcrowding, missing TOC entries / part-intros).
- **`ce-conventions`**: new §12 *Always-ask decisions* — output language must
  be asked (never inferred), and deliverable paths announced each phase.
- **`slide-design-rules`**: new *Rule 14* — keep slides telegraphic with
  detail in `st_hover_tooltip` (placement opposite the icon, readable
  content); the image zone must not be systematic (offer a symmetric
  4-bullet variant) to avoid an over-commercial deck.

### Added — universal authoring trinity (plan + design rules + packs) for ALL document types

Generalizes the slide-only design pipeline so every document type (presentation,
manual/report, course, collection) gets the same enforced trinity.

- **`authoring-gate` skill** (`shared/skills/authoring-gate.md`) — the single
  contract every block-authoring path runs before writing: (A) plan present
  (soft-block QCM if absent, with an "ad-hoc assumed" escape), (B) design
  rules + designer specialization resolved by `identity.type`, (C) component
  resolved and recorded in `components.applied`. Wired into `ce-prototype`,
  `ce-produce`, `ce-go`, and the direct `/stx-block:new|slide-new|init` — so the
  trinity holds in CE **and** outside it.
- **`document-designer` umbrella agent** + two new specializations
  **`web-document-designer`** (manual/report/collection hub) and
  **`course-designer`** (course); `slide-designer` is now explicitly the
  `presentation` specialization. Non-slide documents are no longer authored
  freehand.
- **Two new rule overlays**: `web-document-design-rules.md` (reading flow,
  scroll, content idioms) and `course-design-rules.md` (pedagogy, extends the
  web-document overlay).
- **`stx-block:audit`**: new *Reuse & trinity* WARNING checks (block with no
  component and no justification; design project with no resolved guideline).

### Changed — design rules hierarchy

- **`visual-design-rules.md` is now the neutral, format-agnostic base** (was
  titled "for Slides"). Slide geometry stays in `slide-design-rules.md`; the
  documentation/teaching idioms (canonical explain→code→render→detail section,
  "every example has code", WRONG/CORRECT boxes) moved to the web-document
  overlay where they belong. Slide authoring is unaffected (base + slide overlay
  ⊇ the previous content).

### Fixed — deployment (dangling references)

- Registered three files that were **referenced across the profile but absent
  from `manifest.toml`**, so they were never deployed to projects:
  `shared/skills/modular-design-philosophy.md` (read by `slide-designer`,
  `project-architect`, and most design files), `shared/references/grid_layout_guidelines.md`,
  and `shared/references/plotly_guidelines.md`.

## [0.3.2] — 2026-05-20 — Pack naming convention `streamtex-pack-{name}`

### Changed

- All artifacts referencing pack names updated to the new convention:
  - `streamtex-design` (pip / repo name) → `streamtex-pack-design`
  - `streamtex-manuals` (pip / repo name) → `streamtex-pack-manuals`
- Pack references now point to the `streamtex-packs` monorepo:
  `git+https://github.com/nicolasguelfi/streamtex-packs.git@{tag}#subdirectory={pack}`
  with prefixed tags per pack (`pack-design-v0.2.4`, `pack-manuals-v0.1.0`).
- License of packs in the ecosystem: BUSL-1.1 (was MIT for individual packs;
  now aligned with the streamtex library).
- Python module names (`streamtex_design`, `streamtex_manuals`) PRESERVED
  → all `from streamtex_design.components import ...` imports work
  unchanged in user code.

### Migration

For existing projects, update `pyproject.toml`:

```diff
- "streamtex-design @ git+https://github.com/nicolasguelfi/streamtex-design.git@v0.2.3"
- "streamtex-manuals"
+ "streamtex-pack-design  @ git+https://github.com/nicolasguelfi/streamtex-packs.git@pack-design-v0.2.4#subdirectory=streamtex-pack-design"
+ "streamtex-pack-manuals @ git+https://github.com/nicolasguelfi/streamtex-packs.git@pack-manuals-v0.1.0#subdirectory=streamtex-pack-manuals"
```

## [0.3.1] — 2026-05-20 — v2 relative-scale doctrine across all AI artifacts

### Added

- **Authority rule** in `shared/skills/modular-design-philosophy.md`:
  legacy-to-indexed translation table, "never override individual
  paliers" rule, ScaleConfig knob priority order, and audience →
  `base_pt_desktop` recommendation table. Read FIRST by all
  designer/reviewer/pack-designer agents.

### Changed

- 51 AI-control artifacts updated to recommend the v2 indexed scale +
  `ScaleConfig.base_pt_desktop` override as the primary path. Legacy
  tokens (`s.medium`/`s.large`/etc.) remain valid but no longer
  recommended as primary.
- Audience-specific defaults codified across all relevant artifacts:
  - Presentations (auditorium): `base_pt_desktop=24`
  - Screen viewing: `base_pt_desktop=18` (default)
  - Documentation: `base_pt_desktop=18`
  - Dense / data-heavy: `base_pt_desktop=16`
  - Minimalist generous: `base_pt_desktop=20-22`
- Audit/review agents (`slide-reviewer`, `visual-reviewer`,
  `style-consistency-checker`, `presentation-audit`) now express
  font-size criteria in palier-index terms (base-independent), so
  audits remain correct regardless of the project's chosen base.

### Migration

For existing projects, no action required. The `s.large`/`s.huge`/etc.
tokens continue to work. Migration to the indexed scale + base_pt
is recommended for new projects only.

## [Unreleased]

### Added

- New skill: `shared/skills/modular-design-philosophy.md` — codifies
  the pack-first design doctrine + indexed-scale guidance.
- Cheatsheet: new "Indexed responsive font scale" section in
  `shared/references/streamtex_cheatsheet_en.md` mirroring the
  streamtex-docs cheatsheet.

### Changed

- `shared/references/coding_standards.md` extended with a
  "Style storage hierarchy (pack-first)" section and a
  "Font scale: prefer the indexed scale" section.
- `shared/references/presentation_cheatsheet_en.md` gained a
  "Font scale (presentations)" section with indexed-scale ↔ legacy mapping.
- 10+ artifacts (skills, agents, templates, import format) updated to
  recommend the indexed font scale and pack-first storage, with
  legacy tokens kept valid as backward-compatibility fallbacks.
- 3 CLAUDE.md.j2 overlays (library / documentation / presentation)
  cross-reference the new `modular-design-philosophy` skill.

## [0.3.0] — 2026-05-19 — Pack Engineering module

Adds the **Pack Engineering (PE)** module : an orchestrated 7-step
lifecycle (DISCOVERY → DESIGN → IMPLEMENT → ADOPT → RETROFIT → AUDIT
→ PUBLISH) with 4 fundamental validation gates (G1-G4) for extracting,
forking, refining, auditing, adopting, and publishing StreamTeX packs.

### Added

**Single user-facing agent** (`pack-orchestrator`) auto-classifies the
user's prompt into one of six sub-modes :
- `bootstrap` : N projects → brand-new pack from scratch.
- `specialize` : upstream pack + N projects → domain-specific fork.
- `refine` : active pack + new blocks → incremental enrichment.
- `audit` : read-only pack health check.
- `adopt` : install pack in projects without extraction.
- `publish` : mature pack release (semver + tag + optional PyPI).

**Six invisible specialist agents** delegated to by the orchestrator :
`pack-miner`, `pack-designer`, `pack-implementer`, `pack-retrofitter`,
`pack-auditor`, `pack-publisher`. Users never see their names.

**Files added** (28 total) :

- 8 PE skills in `profiles/project/pack-engineering/skills/` :
  `pe-conventions.md`, `pe-go.md`, `pe-bootstrap.md`, `pe-specialize.md`,
  `pe-refine.md`, `pe-audit.md`, `pe-adopt.md`, `pe-publish.md`.
- 7 PE agents in `profiles/project/pack-engineering/agents/` :
  `pack-orchestrator.md`, `pack-miner.md`, `pack-designer.md`,
  `pack-implementer.md`, `pack-retrofitter.md`, `pack-auditor.md`,
  `pack-publisher.md`.
- 6 PE templates in `profiles/project/pack-engineering/templates/` :
  `pack-master-plan.yaml`, `pack-master-plan.md`, `pe-discovery.md`,
  `pe-design.md`, `pe-audit-report.md`, `pe-retrofit-plan.md`.
- 7 PE commands in `profiles/project/commands/stx-pe/` :
  `go.md`, `bootstrap.md`, `specialize.md`, `refine.md`, `audit.md`,
  `adopt.md`, `publish.md`.

### Changed

- `profiles/project/manifest.toml` — adds `pack-engineering` entries
  under `[skills]`, `[agents]`, `[templates]` ; adds `stx-pe` group
  under `[commands]`.
- `install.py` — extends `CATEGORY_PATHS` with `pack-engineering`
  sub-categories so the installer copies the new files.
- `profiles/project/ce/skills/ce-task.md` — adds 5 new archetypes
  (`PACK_BOOTSTRAP`, `PACK_SPECIALIZE`, `PACK_REFINE`, `PACK_AUDIT`,
  `PACK_ADOPT`) that auto-route from `/stx-ce:task` to
  `pack-orchestrator`. `PACK_PUBLISH` is intentionally not routed
  (publish requires explicit `/stx-pe:publish`).
- `profiles/project/ce/skills/ce-go.md` — adds Step 0bis that detects
  PE intent in the prompt and hands off to `pack-orchestrator` before
  the main CE pipeline starts.

### Ecosystem coherence pass

After the initial PE module ship, an ecosystem-wide audit identified
discoverability gaps. The following cross-references were added so PE is
visible from every surface a user naturally consults:

- `cursor/generate_cursor.py` — `pack-engineering/` sub-category added
  to `skill_dirs` and `agent_dirs` (HIGH priority — without it, Cursor
  users would get zero PE artifacts converted to `.mdc` rules even though
  `install.py` copies them).
- `shared/references/pe_cheatsheet_en.md` — new full PE reference
  (commands + agents + gates + decisions-log entry types + semver policy),
  parallel to `ce_cheatsheet_en.md`. Registered in
  `profiles/project/manifest.toml [shared].references`.
- `profiles/project/CLAUDE.md.j2` — new "Workflows — stx-pe Pack
  Engineering" section parallel to the existing CE workflow section,
  so every freshly-installed project surfaces PE in its generated
  `CLAUDE.md`.
- `shared/skills/reuse-architecture.md` — trigger list now includes
  `/stx-pe:*`; new "Orchestrated evolution (Pack Engineering)" subsection
  cross-references PE as the orchestrated counterpart to the static
  reuse mechanics this skill covers.
- `README.md` — tagline updated to "up to 38 slash commands" (15+14+7),
  0.3.0 release callout, profile table updated for `project`, new
  "stx-pe Commands (7)" section, `pack-orchestrator` added to the
  Agents table.
- `.github/workflows/validate.yml` — hardcoded skill/agent path mapping
  updated to include `pack-engineering` (needed by the manifest
  validation step).

### Architectural notes

- **PE lives in the shared project profile**, not `.claude/custom/`,
  because pack engineering is a generic methodological feature of the
  reuse architecture — like CE, import-as-method, or
  deployment-as-method. User-specific bridges (e.g. project-pack
  import mappings) still belong in `.claude/custom/`.
- **Pack-side semver policy** : REMOVED → major, CHANGED → minor,
  ADDED only → patch. Different from the library's "stay on 0.7.X"
  rule — each user pack has its own version trajectory.
- **PUBLISH never auto-runs** : even in autonomous mode, PyPI publish
  requires explicit user QCM approval at Step 7.

## [0.2.0] — 2026-05-19 (Wave 3 Phase 5 — CE workflows refresh)

Builds on the Wave 2 [Unreleased] section (Phase 4 infrastructure, kept
below). Wave 3 completes the migration on the CE side and ships v0.2.0
of the profiles.

### Removed
- `profiles/project/designer/skills/block-blueprints.md` (PLAN §18.1 —
  deferred deletion now safe since Phase 4 + Phase 5 references are
  removed). Manifest entry for `block-blueprints.md` dropped from
  `profiles/project/manifest.toml`.

### Changed (Phase 5 vocabulary refresh)
Mechanical bulk pass (`pattern-library` → `reuse-architecture`,
`/stx-pattern:*` → `/stx-component:*`, `.claude/custom/streamtex-patterns/`
→ primary local pack `./mypack/components/`, etc.) followed by targeted
touch-ups. Total files touched: **27** (24 CE / designer / shared +
3 stx-block/stx-ce commands).

CE skills (6 files):
- `ce-conventions.md` — pattern-catalog table + 3-level promotion table
  rewritten with the streamtex 0.7.x flow (mypack / git pack / pypi).
- `ce-prototype.md` — capture target switched to `mypack/components/`.
- `ce-compound.md` — learnings-researcher mention switched.
- `ce-go.md` — INTEGRATE promotion phrasing updated.
- `ce-integrate.md` — promotion routing table aligned with the 4 Q12
  destinations and the `stx component promote --to=<pack>` command.
- `ce-prototype.md` — capture skeleton clarified.

CE agents (6 files): `prototype-designer`, `structure-architect`,
`learnings-researcher`, `content-strategist`, `format-explorer`,
`audience-advocate` — vocabulary refresh + pre-read pointer to the
central `reuse-architecture` skill.

CE templates: `master-plan.md` — `patterns.applied` → `components.applied`,
catalog location moved to the primary local pack.

Designer skills (5 files): `slide-design-rules`, `visual-design-rules`,
`style-conventions`, `streamtex-quick-reference`, `slide-design-rules` —
catalog references updated to `stx component list` + active packs.

Designer agents (3 files): `slide-designer`, `slide-reviewer`,
`project-architect` — local catalog path updated.

Designer templates: `course.md` — same vocabulary refresh.

Project commands (6 files): `stx-block/{audit,new,slide-new,update,init}.md`
+ `stx-ce/{plan,produce,prototype}.md` — slash-command refs migrated
from `/stx-pattern:*` to `/stx-component:*`.

Shared references (3 files): `coding_standards.md`, `ce_cheatsheet_en.md`,
`streamtex_cheatsheet_en.md` — historical patterns mentions rewired to
the reuse architecture.

`shared/commands/stx-guide.md` — repo table entry for `streamtex-design`
fixed (correct repo URL + label `reuse`); workspace layout block
redrawn around `streamtex-design/`; topic `patterns` renamed to `reuse`
in the help table.

### Acceptance
- `grep -rEn "pattern-library|block-blueprints|ptn_|_pattern_library" profiles/project/ce/` → 0 active references (legacy mentions in `reuse-architecture` skill / overlay CLAUDE.md.j2 explicitly say "removed in 0.7.x").
- Manifests parse cleanly. `block-blueprints.md` no longer registered.

### Added (Wave 2 Phase 4 — non-CE infrastructure for `streamtex 0.7.x` reuse architecture)
- **`shared/skills/reuse-architecture.md`** (~150 lines) — single source of
  truth for the new vocabulary (pack / component / design system / kit),
  discovery, error codes (PR/PV/CV/DV/KV/BV), `stx.toml` schema, and
  `__component_meta__` schema (PLAN §10 Phase 4, Q10 option b).
- **6 new `/shared/commands/` directories**: `stx-pack/`, `stx-component/`,
  `stx-ds/`, `stx-kit/`, `stx-validate/`, `stx-new/`. Each contains a
  `run.md` that pre-reads `reuse-architecture.md` and delegates to the
  new CLI surface (`stx pack/component/ds/kit/validate`, MIG-2).
- Manifests updated (4 profiles: project, library, documentation,
  presentation) — `pattern-library.md` skill replaced by
  `reuse-architecture.md`; `stx-pattern` shared command group replaced
  by `stx-pack/component/ds/kit/validate/new`.
- `CLAUDE.md.j2` rewritten in `profiles/project/`, `library/overlay/`,
  `documentation/overlay/`, `presentation/overlay/` — "StreamTeX
  Patterns" section replaced by "Reuse architecture (packs, components,
  design systems, kits)" with rules pointing at `stx component show` /
  `stx component new`.

### Changed
- `shared/references/coding_standards.md` — pattern-library mechanism
  reference updated to reuse-architecture.
- `shared/commands/stx-coherence/audit.md` — legacy `patterns` scope
  (checks P1-P4 / 46-49) replaced by a `reuse` scope deferring to
  `stx validate` and documenting the new error code families.
- `shared/commands/stx-guide.md` — Section 4h "Patterns graphiques"
  rewritten as Section 4h "Reuse architecture"; the slash-command table
  now lists the six new commands.
- `shared/commands/stx-import/{html,marp}.md` — "Phase 4: Reverse
  pattern mapping" removed (D19 / PLAN §18.9 — imports stay pack-
  agnostic). `html-audit.md` and `marp-analyze.md`: "Pattern coverage
  estimate" sections removed.

### Removed
- `shared/skills/pattern-library.md` (legacy markdown-catalog skill).
- `shared/commands/stx-pattern/` (5 files: list/show/new/reindex/validate).

### Notes (Phase 5 follow-up — Wave 3)
- `shared/references/streamtex_cheatsheet_en.md` and `ce_cheatsheet_en.md`
  still contain historical mentions of `streamtex-patterns` /
  `/stx-pattern:*` inside reference tables. They will be rewritten in
  Phase 5 alongside the CE workflow refresh. The active commands and
  active skills already point at the new architecture.
- `profiles/project/designer/` (11 files) and `profiles/project/ce/`
  (in-scope of Phase 5) are intentionally untouched in this wave.

## [0.1.0] — 2026-05-14

### Added
- **Iterative/incremental CE lifecycle.** Cross-repo refonte aligning the Compound Engineering cycle with the project state. Highlights:
  - **9-phase cycle**: `COLLECT → ASSESS → PLAN → PROTOTYPE → PRODUCE → REVIEW → FIX → COMPOUND → INTEGRATE`. PROTOTYPE is QCM-driven (auto-triggered when a new visual territory appears or no pattern is yet validated; skipped otherwise).
  - **Master plan** as a git-independent living reference: `docs/master-plan.yaml` (orchestration metadata, decisions log, patterns mapping) + `docs/master-plan.md` (content plan with raw drafts) + `docs/master-plan/archive/` (paired snapshots).
  - **3-level pattern catalog promotion**: draft (in PROTOTYPE) → local (in COMPOUND) → shared via INTEGRATE (PR to `streamtex-patterns`).
  - **Unified QCM convention** for every user-facing decision: 1 option `(Recommandé)` + alternatives + `Discutons-en` + auto-injected `Autre`. The `producer-profile.md` field `dialog_level` (`minimal` / `guided` / `exhaustive`) modulates the **frequency** of QCMs, never their format. In `minimal`, only the 4 fundamental gates surface QCMs (post-PLAN, post-REVIEW, post-FIX, post-INTEGRATE).
  - **New skill**: `ce-prototype` (skill file + `/stx-ce:prototype` slash command).
  - **New conventions skill**: `ce-conventions` (canonical reference for QCM format, snapshot policy, master plan paths, decisions log format).
  - **New agents**: `prototype-designer`, `plan-reconciler`, `objective-monitor`.
  - **New templates**: `master-plan.md` (schema reference covering both runtime files, declared as the canonical source for `master-plan.yaml -> <field>` references across the codebase), `prototype-report.md`.

  See the cross-repo entry in `streamtex/CHANGELOG.md` (commit `c5b90de`) and the companion documentation work in `streamtex-docs` branch `feat/ce-lifecycle-incremental`.

### Changed
- `profiles/project/CLAUDE.md.j2` and related references aligned to the 9-phase cycle (8 additional files: `commands/stx-ce/go.md`, `ce/templates/checkpoint.md`, `ce/skills/ce-compound.md`, `designer/templates/project.md`, `shared/commands/stx-guide.md`, `shared/references/streamtex_cheatsheet_en.md`, `profiles/library/overlay/developer/skills/coherence-checks.md`, `profiles/documentation/overlay/developer/skills/coherence-checks.md`).
- `producer-profile.md` template: added the `dialog_level` field (default: `guided`).
- `ce-compound.md`: intro fixed to **4 axes** (Axis 4 is master plan maintenance, including partial purge of snapshots) — previously claimed 3 axes despite documenting 4 in the body.
- `coherence-checks.md` Checks 23-27 (both library/ and documentation/ overlays): reformulated in self-maintaining wording — expected counts and enumerations are now derived from the manifest at audit time, so the checks no longer go stale as the cycle evolves.
- `coherence-checks.md` adds **Check 28a — CE Master Plan Schema Integrity** (both overlays): verifies that every `master-plan.yaml -> <field>` reference across CE skills, agents, templates, and the cheatsheet corresponds to a field defined in the master plan schema. Run via `/stx-coherence:audit ce` and `/stx-coherence:audit all`.
- `shared/commands/stx-coherence/audit.md`: `ce` scope mapping extended to include Check 28a.
- `profiles/project/ce/templates/master-plan.md`: header clarifies the file is a **schema reference**, not a copy source. The orchestrator constructs the runtime files programmatically from this schema.

### Fixed
- `profiles/project/ce/agents/dev-governance.md`: remove two dangling `.claude/developer/skills/{architecture,coherence-checks}.md` references that pointed to files outside the `project` profile (they exist in `library/` and `documentation/` overlays only). The agent remains fully functional (branch check, repo conventions, COMPOUND inventory).

Related commits on `feat/ce-lifecycle-incremental`: `a59931b`, `e6d01f0`, `50f983d`, `af03874` (this file), `277c574`, `e5f4722`.
