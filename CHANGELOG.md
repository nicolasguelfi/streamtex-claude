# Changelog — StreamTeX Claude Profiles

All notable changes to the StreamTeX Claude Code profiles will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Prior to this Changelog, changes are tracked in the git history of this repository (see `git log` on `main`).

## [Unreleased]

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
