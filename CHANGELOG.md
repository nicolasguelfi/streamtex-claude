# Changelog — StreamTeX Claude Profiles

All notable changes to the StreamTeX Claude Code profiles will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Prior to this Changelog, changes are tracked in the git history of this repository (see `git log` on `main`).

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
