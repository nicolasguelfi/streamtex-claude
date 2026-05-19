# PE Conventions

Single source of truth for the **Pack Engineering** (PE) galaxy of skills,
agents, templates, and slash commands. Parallel to `ce-conventions.md`
(Compound Engineering for documents) but dedicated to the lifecycle of a
StreamTeX **pack** (components / design systems / kits).

Read this file **before** invoking any `/stx-pe:*` command or any
`pack-*` agent. The unique user-facing agent is `pack-orchestrator`.

## 1. Vocabulary

| Term | Definition |
|---|---|
| **Pilot project** | The project where the orchestrator runs and where the `pack-master-plan.{yaml,md}` lives — typically the same workspace root as the consumer projects but conceptually distinct. |
| **Consumer projects** | The N input projects whose blocks are mined for recurring visual idioms. They become the first consumers of the produced pack at the ADOPT phase. |
| **Target pack** | The pack written to by PE. May be brand-new (`bootstrap`), a fork of an existing one (`specialize`), or an already-active pack being enriched (`refine`). |
| **Upstream pack** | (Specialize mode only) the parent pack the target forks. Promotion-eligible candidates can later flow back upstream via `pack-publisher --pr-upstream`. |
| **Pack master plan** | `docs/pack-engineering/pack-master-plan.{yaml,md}` in the pilot project — the living orchestration artifact. The YAML carries structured state (phases, discovered components, decisions log) ; the MD carries narrative justifications. |

## 2. QCM format

PE strictly reuses the **universal QCM format** defined in
`.claude/ce/skills/ce-conventions.md` §1 :

```
"<question scope-aware en français>"

- Option 1 suffixed `(Recommandé)` + justification one-liner
- 0-2 business alternatives
- `Discutons-en`
- (`Autre` — auto-injected by the harness)
```

Read `ce-conventions.md` once per orchestrator invocation ; do not duplicate
its rules here. PE-specific QCM phrasings live in each `pe-*.md` skill.

## 3. Fundamental gates (4)

Like CE has 4 fundamental gates (post-PLAN / post-REVIEW / post-FIX /
post-INTEGRATE), PE has 4 :

| # | Gate | When | QCM |
|---|---|---|---|
| **G1** | post-DISCOVERY | After `pack-miner` produces `pe-discovery.md` | Validate / refine the candidate list before paying for design tokens. |
| **G2** | post-DESIGN | After `pack-designer` produces `pe-design.md` | Validate the contracts (INVARIANTS / PARAMS / INTERDITS / bundles_required) before scaffolding & implementing. |
| **G3** | pre-RETROFIT | After ADOPT but before any block rewrite | Confirm dry-run results — diff per block, expected smoke-render outcomes. |
| **G4** | post-RETROFIT (smoke fails) | If smoke render headless KO on at least one block after retrofit | Decide : revert the failing block / accept-as-is / discuss. |

In `dialog_level: minimal` (per producer-profile), only G1 and G3 are
surfaced ; G2 and G4 auto-apply the recommended default.

## 4. Decisions log entries

The `pack-master-plan.yaml -> decisions_log` is append-only. PE writes the
following entry types (one per QCM decision) :

- `bootstrap_started` — PE invoked in bootstrap mode with N consumer projects
- `mining_validated` — G1 passed, list of candidates accepted
- `design_approved` — G2 passed, list of components to implement
- `implementation_done` — every component scaffolded + filled + validated
- `adoption_validated` — `stx pack add` + `stx kit install` succeeded on all consumer projects
- `retrofit_validated` — G3 passed, retrofit applied (or dry-run only)
- `audit_completed` — `pack-auditor` produced `pe-audit-report.md`
- `publish_decided` — semver bump + tag + (optional) PyPI publish + (optional) upstream PR

Format :
```yaml
- date: 2026-05-19T14:30:00Z
  entry: design_approved
  scope: bootstrap
  decision: "Approved 12 components ; rejected 3 (too project-specific)"
  rationale: "G2 QCM — option 'Tout valider' selected"
```

## 5. Pack master plan schema

The YAML twin (`pack-master-plan.yaml`) is the structured single source of
truth. See `templates/pack-master-plan.yaml` for the full schema. Required
top-level keys :

- `plan_id` : `<pack-name>-<YYYY-MM-DD>`
- `pack` : `{ name, type, upstream, target_path }`
- `consumer_projects` : list of `{ path, blocks_count }`
- `phases_completed` : append-only list of phase IDs
- `mining` / `design` / `implementation` / `adoption` / `retrofit` / `audit` : per-phase state
- `decisions_log` : append-only list of decision entries

The MD twin (`pack-master-plan.md`) is the narrative. Required sections :
Objectives, Constraints (semver policy, naming policy, upstream PR policy),
Per-component justification, Open questions.

## 6. Relation to CE

PE and CE are **parallel and independent** :

- A pilot project can run **both** PE and CE cycles (different master plans,
  different `docs/` subdirectories — `docs/pack-engineering/` vs `docs/`).
- PE never touches CE's `master-plan.yaml` and vice versa.
- PE **reuses** these CE agents without modification, called with explicit scope
  arguments :
  - `learnings-researcher` — duplicate detection across installed packs.
  - `prototype-designer` — design strategy classification (reuse_as_is /
    reuse_adapted / create_new / ad_hoc) for each candidate.
  - `style-consistency-checker` — naming + palette coherence audit.
  - `visual-reviewer` — headless smoke render after retrofit.
- PE **does not reuse** : `audience-advocate`, `pedagogy-analyst`,
  `content-strategist`, `format-explorer`, `objective-monitor`,
  `feedback-detector`, `domain-researcher` — these are document-centric
  and have no analog in pack engineering.

## 7. Pack-side semver policy

The stay-on-patches rule (memory `feedback_no_minor_bump`) applies to
**streamtex** the library, NOT to **packs**. Each pack has its own
semver life-cycle :

- patch bump : ADDED components only, no contract change.
- minor bump : CHANGED contract on existing components OR added DS / kit.
- major bump : REMOVED components OR breaking contract change.

`pack-publisher` enforces this — it computes the bump from the
implementation diff vs. the previous tag.

## 8. Vocabulary cross-references

- Component / pack / design system / kit / bundle → `shared/skills/reuse-architecture.md`.
- Contract docstring (Visual / Structure / Styling rules / INVARIANTS /
  PARAMS / INTERDITS / When to use / When NOT to use / bundles_required) →
  `shared/skills/reuse-architecture.md` §4.1.
- `__component_meta__` schema → `shared/skills/reuse-architecture.md` §5.
- Q12 promotion routing (primary_local / secondary_local_with_git /
  git_remote / pypi-refused) → `shared/skills/reuse-architecture.md` §6.
- Error codes (PR / CV / DV / KV / BV / PV) → `shared/skills/reuse-architecture.md` §2.

## 9. Outputs on disk

PE writes exclusively under `docs/pack-engineering/` of the pilot project :

```
docs/pack-engineering/
├── pack-master-plan.yaml          # structured state
├── pack-master-plan.md            # narrative
└── <timestamp>/                   # per-run snapshots
    ├── discovery.md
    ├── design.md
    ├── adoption-log.md
    ├── retrofit-plan.md
    ├── retrofit-report.md
    └── audit-report.md
```

Snapshots are kept until `pack-publisher` runs (which prunes to the last 3
runs by default — equivalent to the CE master-plan archive partial purge).
