# CE Go

Skill for the orchestrated workflow of the Compound Engineering cycle. The cycle may cover the full document or an increment (part, section, single block) — the scope is determined by dialogue with the user at the start, not by flags.

Read `.claude/ce/skills/ce-conventions.md` before invoking any user-facing question. All interactions follow the universal QCM format with `(Recommended)` + `Let's discuss` + auto-injected `Other`.

## Workflow

### Step 0: Detect State and Propose Scope

Before executing any phase, the orchestrator builds a contextual proposal by reading the master plan (if present) and the project state. Internal flags exist for advanced use but are **not** exposed by default — the user is guided through QCMs.

1. **Read master plan** (`docs/master-plan.yaml` + `docs/master-plan.md`). If absent, this is the first iteration on a new document.
2. **Load producer profile** (read `dialog_level`).
3. **Determine current state**:
   - Master plan absent → first iteration, scope = full document, pathway TBD by ASSESS auto-detection.
   - TOC defined, 0 block produced → recommend starting with first section (PROTOTYPE expected).
   - TOC defined, partial production → recommend continuing current incomplete section or moving to next planned section.
   - All sections produced, no review yet → recommend full review.
   - Document complete → propose new objectives or end of project.
4. **Surface scope QCM** (skipped only if first iteration on empty project — then ASSESS handles initialization directly):

   Question (adapted to current state): *"The plan defines X parts / Y sections, Z blocks produced out of N planned. How do you want to proceed in this cycle?"*

   Options:
   - *"Continue the current increment"* `(Recommended)` — when partial work exists
   - *"Start the next section / part"* — when current is complete
   - *"Let's discuss"* — opens dialogue
   - (Other — auto-injected, captures custom scope description)

   Other state-specific phrasings:
   - First iteration on new document: *"No plan detected. What scope for this first cycle?"* → `Full document (Recommended)` / `A first pilot section` / `Let's discuss`.
   - Document complete: *"All blocks are produced and reviewed. What do you do?"* → `New improvement increment (Recommended)` / `Close the project` / `Let's discuss`.

5. **Capture decision** in `decisions_log` and set the internal `scope` for downstream phases.

### Step 0bis: Detect Pack Engineering Intent (route to PE)

Before launching the main CE pipeline, analyze the prompt for Pack Engineering intent. If detected, **suspend ce-go and hand off to `pack-orchestrator`** — PE is its own lifecycle and must not interleave with CE phases.

Trigger keywords (case-insensitive, English):

| Sub-mode | Triggers |
|---|---|
| `bootstrap` | "extract pack", "from scratch", "bootstrap pack", "new pack from projects", "factor components from" |
| `specialize` | "specialize pack", "fork pack", "extend pack", "upstream pack" |
| `refine` | "refine pack", "enrich pack", "capture emerged patterns", "add to pack" |
| `audit` | "audit pack", "pack health", "unused components" |
| `adopt` | "adopt pack in projects", "install pack in N projects", "wire pack" |
| `publish` | NEVER auto-routed (requires explicit `/stx-pe:publish`) |

Routing :
1. If a single PE trigger is detected with high confidence → confirm with QCM :

   > "Detected intent concerns pack engineering (sub-mode `<mode>`). Launch the PE cycle instead of CE?"
   > - Yes, launch `/stx-pe:<mode>` (Recommended)
   > - No, continue with CE
   > - Let's discuss

2. If confirmed → invoke `pack-orchestrator` with the chosen verb and stop ce-go. The orchestrator handles its own lifecycle (gates G1-G4) and writes outputs to `docs/pack-engineering/`.

3. If declined or no PE intent → continue with CE Step 1 (COLLECT) as normal.

Read `.claude/pack-engineering/skills/pe-conventions.md` + `.claude/pack-engineering/agents/pack-orchestrator.md` before delegating.

### Step 0ter: Inventory Specialized Artefacts (mandatory)

`/stx-ce:go` is an **orchestrator, not a monolithic executor**. Before producing any content, take stock of the specialized artefacts shipped in `.claude/` and delegate to them — do **not** execute design/production work freehand (the GSE-ODOO failure: 50 slides authored without ever opening `slide-designer`, scored 0/20).

1. Run `find .claude -type f -name '*.md'` (or read the role directories) and note what exists under `.claude/<role>/{agents,skills,guidelines,templates}/` and `.claude/references/`.
2. Map the work of this cycle to the available specialists:
   - **`authoring-gate`** (`.claude/shared/skills/authoring-gate.md`) is the single entry point for writing **any** block: it enforces the trinity (plan + design rules/agent + component) and delegates to the designer specialization for the document's `identity.type` — **`slide-designer`** (presentation), **`web-document-designer`** (manual/report/collection hub), or **`course-designer`** (course). All extend the **`document-designer`** umbrella contract. This holds for every document type, not just slides.
   - **`visual-reviewer` / `slide-reviewer`** (agents) run the screenshot + vision gate (all document types).
   - **`prototype-designer`** (agent) selects pilots and the pattern strategy in PROTOTYPE.
   - A **design guideline** (`maximize-viewport`, `minimalist-visual`, `dense-informative`, `academic-structured`) is selected at ASSESS and persisted to `custom/design-guideline.md`.
   - CE **templates** (`master-plan`, `prototype-report`, `review-report`, …) are used verbatim, not reinvented.
3. If a specialist exists for a task, invoke it. Authoring a block yourself instead of through `authoring-gate` / the designer specialization is a defect, not a shortcut — for any document type.

### Internal Flags (not exposed in default flow)

The following flags remain implemented but are inferred from dialogue rather than typed by the user. Power users may still pass them directly:

- `--quick`: Skip COLLECT and ASSESS phases. Go directly to PLAN.
- `--from-plan <path>`: Resume from an existing plan file. Skip COLLECT, ASSESS, and PLAN.
- `--interactive`: Force interactive planning mode (4-step dialogue in PLAN phase).
- `--review-only`: Only run REVIEW on the existing project. Skip all other phases.
- `--no-deploy`: Skip deployment during the PRODUCE phase.
- `--import <path>`: Force pathway A (Import) and use the specified path as the source.
- `--improve`: Force pathway B (Improvement) on the current project.

### Execute Sequentially

#### Step 1: COLLECT

- Run `/stx-ce:collect` with any relevant flags.
- If `--quick` or `--from-plan` is set: skip this step.
- If `--import <path>` is set: pass the path to collect.
- Record the number of sources found and the recommended pathway.

#### Step 2: ASSESS

- Run `/stx-ce:assess` with the pathway detected or forced.
- If `--quick` or `--from-plan` is set: skip this step.
- If `--improve` is set: force pathway B.
- Record the requirements and assessment results.

#### Step 3: PLAN

- Run `/stx-ce:plan` with the scope determined in Step 0.
- First iteration produces the global master plan TOC plus the first increment's detailed plan.
- Subsequent iterations produce only the detailed plan for the current increment, in coherence with the master plan TOC.
- If `--from-plan <path>` is set: load the specified plan and skip generation.
- Auto-detect interactive mode: enable `--interactive` if COLLECT found 10 or more sources or the project has 20 or more existing blocks.
- If `--interactive` flag was explicitly set: use interactive mode regardless.
- **GATE (fundamental)**: surface QCM to validate the plan. Options: `Approve (Recommended)` / `Revise` / `Let's discuss`.

#### Step 3.5: PROTOTYPE

- Determine whether PROTOTYPE is needed for this increment:
  - Auto-recommended (`Yes`) when at least one of: no patterns validated yet for the current visual territory; design choices in PLAN differ significantly from prior iterations; user has not yet seen a produced block in this style.
  - Auto-recommended (`No`) when the increment continues a style territory already validated.
- Surface QCM (skipped only in `dialog_level: minimal` if recommendation is `No`):

  *"Before producing the N planned blocks, I propose producing a pilot block to validate styles and patterns. Proceed?"*

  Options: `Yes (Recommended / not recommended depending on context)` / `No, produce directly` / `Several pilot blocks (cover archetypes)` / `Let's discuss`.
- If accepted: run `/stx-ce:prototype` for the increment.

#### Step 4: PRODUCE

- Run `/stx-ce:produce` with the approved plan and the validated patterns from PROTOTYPE (if any).
- If `--no-deploy` is set: pass it through to skip deployment.
- If `--review-only` is set: skip this step entirely.
- Track production progress and report completion status.

#### Step 5: REVIEW

- Run `/stx-ce:review` with the current scope.
- **GATE (fundamental)**: surface QCM to validate the review results. Options: `Launch FIX (Recommended)` / `Examine findings first` / `Let's discuss`.

#### Step 6: FIX

- Run `/stx-ce:fix` to correct automatable findings from the review.
- If new patterns were introduced in PROTOTYPE, propose re-application to prior blocks via QCM (inter-iteration coherence).
- If `--review-only` is set: skip this step unless the user explicitly requests fixes.
- **GATE (fundamental)**: surface QCM to validate the fix results. Options: `Continue to COMPOUND (Recommended)` / `Re-review` / `Let's discuss`.
- If user chooses re-review: loop back to Step 5.

#### Step 7: COMPOUND

- Run `/stx-ce:compound` to capitalize learnings.
- This step always runs unless `--review-only` was set and the user declined fixes.

#### Step 8: INTEGRATE

- Run `/stx-ce:integrate` to route solutions to their operational destinations, including pattern promotion to the shared catalog (`streamtex-pack-design` pack) for patterns judged generic enough.
- Present the routing plan to the user.
- **GATE (fundamental)**: surface QCM to validate which integrations to execute. Options: `Execute all (Recommended)` / `Selection to be specified` / `None` / `Let's discuss`.
- This step runs after COMPOUND if solutions or local patterns were produced. Skip if no new solutions and no new patterns.

#### Step 9: Final Report

Produce a comprehensive summary covering:

1. **Production results**: what was created, imported, or improved (number of blocks, document structure).
2. **Review results**: overall quality score, number of findings by severity, fixes applied.
3. **Capitalized learnings**: what was stored in docs/solutions/, categories covered.
4. **Cycle statistics**: total time, phases completed, gates passed.
5. **Recommendations**: suggested next actions (new cycle, further improvements, deployment).

### Development Governance

At cycle start (before Step 1), record the current git commit hash of each ecosystem repo (streamtex, streamtex-claude, streamtex-docs) if they exist in the workspace. This baseline is used by COMPOUND Axis 3 to compute diffs.

At any point during the cycle, if Claude is asked to modify an ecosystem repo:
1. Consult the **dev-governance** agent for branch check and convention guidance.
2. Apply the soft-block pattern: warn if on main, propose branch creation, accept user choice.
3. This applies to both `/stx-ce:*` commands and direct user requests.

For the user's document project (in `projects/`), if `branch_suggestions: true` in the producer profile:
- Before PRODUCE: propose creating a branch `ce/<plan-name>`.
- Before FIX: propose creating a branch `ce/fix/<review-name>`.
- The user can decline without blocking.

### Pipeline Mode and Dialog Levels

When running from `/stx-ce:go`, individual phases operate in pipeline mode, modulated by `dialog_level`:

- `minimal`: phases do not surface QCMs except at fundamental GATEs (post-PLAN, post-REVIEW, post-FIX, post-INTEGRATE). Sub-decisions silently apply recommended defaults. Phase synthesis is shown at the end of each phase.
- `guided` (default): phases surface QCMs at all structuring decisions (scope, pathway, design choices, PROTOTYPE confirmation, pattern promotion, reconciliation).
- `exhaustive`: phases surface QCMs even on minor choices.
- Phases auto-detect context from the master plan and previous phase outputs rather than prompting unnecessarily.
- Error handling: if a phase fails, report the error, save progress (master plan snapshot if state changed), and surface a QCM: `Retry (Recommended)` / `Skip` / `Abort` / `Let's discuss`.

### End-of-Cycle Soft Interruption

After Step 9, surface a QCM: *"Final snapshot of the plan?"* with default `Yes` (per `ce-conventions.md`). Skip silently if the master plan has not changed since the last snapshot.

### Related Commands

- `/stx-ce:task "<description>"` — For ad-hoc tasks outside the pipeline (compare, targeted review, plan amendment, etc.). See `ce-task.md`.
- `/stx-ce:continue` — For session resumption after a break (briefing, drift detection, proposals). See `ce-continue.md`.
