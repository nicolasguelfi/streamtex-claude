# StreamTeX PE — Pack Engineering Quick Reference

## Cycle

```
DISCOVERY -> DESIGN -> IMPLEMENT -> ADOPT -> RETROFIT -> AUDIT -> PUBLISH
    |          |                              |           ^         ^
  [G1]       [G2]                           [G3/G4]     (auto)   (opt-in)
```

The same 7-step sequencer runs for every sub-mode (bootstrap / specialize / refine / audit / adopt / publish). Each cycle operates on a **target pack** and one or more **consumer projects**.

## Sub-modes

| Sub-mode | When to use |
|---|---|
| **bootstrap** | N projects with overlapping idioms but no shared pack — extract from scratch |
| **specialize** | Upstream pack almost fits but lacks domain specifics — fork with extensions |
| **refine** | Active pack + new blocks since last cycle — incremental capture |
| **audit** | Read-only health check (unused / duplicates / bundle gaps / drift) |
| **adopt** | Install existing pack into projects (`stx pack add` + `stx kit install`) |
| **publish** | Mature pack release (semver bump + tag + optional PyPI) |

## Master plan

Two paired files in the pilot project, updated by every PE phase:

- `docs/pack-engineering/pack-master-plan.yaml` — state (pack info, phases_completed, mining / design / implementation / adoption / retrofit / audit / publish sections, decisions_log)
- `docs/pack-engineering/pack-master-plan.md` — narrative (decisions log + component justifications)

Phase reports: `docs/pack-engineering/<ts>/{discovery,design,audit-report,retrofit-plan,retrofit-report}.md`.

## QCM convention

All user interactions go through QCMs with: 1 option `(Recommended)` + alternatives + `Let's discuss` + auto-injected `Other`. `dialog_level: minimal` skips G2 and G4 (uses recommended defaults); G1 and G3 always surface.

## Commands (7)

| Command | Description |
|---------|-------------|
| `/stx-pe:go [<projects>]` | Auto-detect sub-mode from prompt + workspace state |
| `/stx-pe:bootstrap <projects>` | Extract a new pack from N projects |
| `/stx-pe:specialize <upstream> <projects>` | Fork an upstream pack with domain extensions |
| `/stx-pe:refine` | Incrementally enrich the active pack with new patterns |
| `/stx-pe:audit <pack> [<projects>]` | Read-only health audit |
| `/stx-pe:adopt <pack> <projects>` | Install pack in N projects without extraction |
| `/stx-pe:publish <pack-path>` | Release a mature pack (semver + tag + optional PyPI) |

## Single user-facing agent

**`pack-orchestrator`** is the only agent that talks to the user. It auto-classifies the prompt into one of the six sub-modes and delegates to invisible specialists. You never need to know the specialists' names or invoke them directly.

## Specialist agents (7 — never user-facing)

| Phase | Specialist | Role |
|-------|-----------|------|
| 0 | `pack-orchestrator` | THE ONLY USER-FACING AGENT — phase detection + gate QCMs + delegation |
| 1. DISCOVERY | `pack-miner` | AST-scan consumer projects, cluster recurring idioms |
| 2. DESIGN | `pack-designer` | Write contracts (Visual / Structure / INVARIANTS / PARAMS / INTERDITS) |
| 3. IMPLEMENT | `pack-implementer` | Scaffold via `stx component new`, write bodies, validate |
| 5. RETROFIT | `pack-retrofitter` | Rewrite consumer blocks + smoke render |
| 6. AUDIT | `pack-auditor` | Unused / duplicates / bundle gaps / drift / coverage |
| 7. PUBLISH | `pack-publisher` | Semver bump + CHANGELOG + tag + optional PyPI |

## Fundamental gates

| Gate | When | Skippable |
|---|---|---|
| **G1** | post-DISCOVERY | Never |
| **G2** | post-DESIGN | Skippable in `dialog_level: minimal` |
| **G3** | pre-RETROFIT | Never |
| **G4** | post-RETROFIT smoke fail | Conditional (only if smoke render fails) |

## /stx-pe:go Flags

| Flag | Effect |
|------|--------|
| `--mode <bootstrap\|specialize\|refine\|audit\|adopt\|publish>` | Force sub-mode (skip auto-detection) |
| `--upstream <ref>` | Required for specialize |
| `--pack <ref>` | Force target pack for audit/adopt/publish |
| `--no-publish` | Forbid Step 7 PUBLISH even on a mature pack |
| `--dialog <minimal\|standard\|verbose>` | Override `dialog_level` |

## Sub-mode Flags

| Sub-mode | Key flags |
|----------|-----------|
| bootstrap | `--pack-name <name>`, `--target-path <path>`, `--active-ds <ref>`, `--min-occurrences <N>`, `--min-projects <N>` |
| specialize | `--fork-name <name>`, `--fork-target-path <path>`, `--pr-upstream <repo>` |
| refine | `--target-pack <ref>`, `--since <date\|tag>`, `--full-scan`, `--no-retrofit` |
| audit | `--minimal`, `--no-followup` |
| adopt | `--kit <name>`, `--retrofit` |
| publish | `--bump <patch\|minor\|major>`, `--target <pypi\|tag\|both>`, `--pr-upstream <repo>`, `--dry-run` |

## Auto-routing via /stx-ce:task

You don't need to type `/stx-pe:*`. The free-text `/stx-ce:task` command auto-classifies into 5 PACK_* archetypes:

| Archetype | Triggers | Routes to |
|-----------|----------|-----------|
| PACK_BOOTSTRAP | "extract pack", "from scratch", "bootstrap pack" | `/stx-pe:bootstrap` |
| PACK_SPECIALIZE | "specialize pack", "fork pack", "extend pack" | `/stx-pe:specialize` |
| PACK_REFINE | "refine pack", "enrichir pack", "capture emerged" | `/stx-pe:refine` |
| PACK_AUDIT | "audit pack", "pack health", "unused components" | `/stx-pe:audit` |
| PACK_ADOPT | "adopt pack", "install pack in projects" | `/stx-pe:adopt` |

**PACK_PUBLISH is intentionally NOT auto-routed** — release requires explicit `/stx-pe:publish` for safety.

## Pack-side semver policy

| Change | Bump |
|--------|------|
| Component REMOVED | major |
| Component CHANGED (signature, output, INVARIANTS) | minor |
| Component ADDED only (or doc fixes) | patch |

Independent from streamtex library's stay-on-patches rule — each user pack has its own version trajectory.

## CLI commands orchestrated by PE

PE drives existing `stx` commands deterministically:

| Phase | CLI commands used |
|-------|-----------------|
| 3. IMPLEMENT | `stx component new`, `stx component validate`, `stx component promote`, `stx pack new` |
| 4. ADOPT | `stx pack add <ref>`, `stx kit install <pack>:<kit>` |
| 5. RETROFIT | (smoke render via headless browser) |
| 6. AUDIT | `stx component validate` (read-only) |
| 7. PUBLISH | `stx pack validate --strict`, `git tag`, `uv publish` |

## Decisions log entry types

Captured in `pack-master-plan.yaml.decisions_log`:

| Entry type | Captured after |
|------------|---------------|
| `mining_validated` | G1 |
| `design_approved` | G2 |
| `implementation_completed` | Step 3 |
| `adoption_completed` | Step 4 |
| `retrofit_validated` | G3 + RETROFIT apply |
| `smoke_fail_resolved` | G4 (if triggered) |
| `audit_completed` | Step 6 |
| `publish_decided` | Step 7 |

## Project Directory Structure (PE artifacts)

```
pilot-project/
  docs/
    pack-engineering/
      pack-master-plan.yaml   # state — read/written every phase
      pack-master-plan.md     # narrative
      <ts>/                    # per-cycle reports
        discovery.md
        design.md
        retrofit-plan.md
        retrofit-report.md
        audit-report.md
```

## Hard rules (anti-patterns)

- NEVER invoke a specialist agent directly — always go through `pack-orchestrator`.
- NEVER skip G1 or G3 (G2/G4 may be skipped in minimal dialog).
- NEVER auto-publish to PyPI — Step 7 always requires explicit QCM approval.
- NEVER modify a consumer project without `pack-retrofitter` (smoke render safety).
- NEVER overwrite `pack-master-plan.yaml` blindly — read, mutate, write atomically.

## Related references

- `streamtex_cheatsheet_en.md` — full `stx` CLI reference (commands PE orchestrates).
- `ce_cheatsheet_en.md` — Compound Engineering (PE's conceptual sibling for project-scope authoring).
- `reuse-architecture.md` skill — packs / components / DS / kits mechanics.
