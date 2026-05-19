# CE Go

Skill for the orchestrated workflow of the Compound Engineering cycle. The cycle may cover the full document or an increment (part, section, single block) — the scope is determined by dialogue with the user at the start, not by flags.

Read `.claude/ce/skills/ce-conventions.md` before invoking any user-facing question. All interactions follow the universal QCM format with `(Recommandé)` + `Discutons-en` + auto-injected `Autre`.

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

   Question (adapted to current state): *"Le plan définit X parties / Y sections, Z blocs produits sur N prévus. Comment voulez-vous procéder dans ce cycle ?"*

   Options:
   - *"Continuer l'incrément courant"* `(Recommandé)` — when partial work exists
   - *"Démarrer la prochaine section / partie"* — when current is complete
   - *"Discutons-en"* — opens dialogue
   - (Autre — auto-injected, captures custom scope description)

   Other state-specific phrasings:
   - First iteration on new document: *"Aucun plan détecté. Quelle ampleur pour ce premier cycle ?"* → `Document complet (Recommandé)` / `Une première section pilote` / `Discutons-en`.
   - Document complete: *"Tous les blocs sont produits et revus. Que faites-vous ?"* → `Nouvel incrément sur amélioration (Recommandé)` / `Clore le projet` / `Discutons-en`.

5. **Capture decision** in `decisions_log` and set the internal `scope` for downstream phases.

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
- **GATE (fundamental)**: surface QCM to validate the plan. Options: `Approuver (Recommandé)` / `Réviser` / `Discutons-en`.

#### Step 3.5: PROTOTYPE

- Determine whether PROTOTYPE is needed for this increment:
  - Auto-recommended (`Oui`) when at least one of: no patterns validated yet for the current visual territory; design choices in PLAN differ significantly from prior iterations; user has not yet seen a produced block in this style.
  - Auto-recommended (`Non`) when the increment continues a style territory already validated.
- Surface QCM (skipped only in `dialog_level: minimal` if recommendation is `Non`):

  *"Avant de produire les N blocs prévus, je propose de produire un bloc pilote pour valider styles et patterns. Procéder ainsi ?"*

  Options: `Oui (Recommandé / non recommandé selon contexte)` / `Non, produire directement` / `Plusieurs blocs pilotes (couvrir les archétypes)` / `Discutons-en`.
- If accepted: run `/stx-ce:prototype` for the increment.

#### Step 4: PRODUCE

- Run `/stx-ce:produce` with the approved plan and the validated patterns from PROTOTYPE (if any).
- If `--no-deploy` is set: pass it through to skip deployment.
- If `--review-only` is set: skip this step entirely.
- Track production progress and report completion status.

#### Step 5: REVIEW

- Run `/stx-ce:review` with the current scope.
- **GATE (fundamental)**: surface QCM to validate the review results. Options: `Lancer FIX (Recommandé)` / `Examiner les findings d'abord` / `Discutons-en`.

#### Step 6: FIX

- Run `/stx-ce:fix` to correct automatable findings from the review.
- If new patterns were introduced in PROTOTYPE, propose ré-application to prior blocks via QCM (cohérence inter-itérations).
- If `--review-only` is set: skip this step unless the user explicitly requests fixes.
- **GATE (fundamental)**: surface QCM to validate the fix results. Options: `Continuer vers COMPOUND (Recommandé)` / `Re-revue` / `Discutons-en`.
- If user chooses re-revue: loop back to Step 5.

#### Step 7: COMPOUND

- Run `/stx-ce:compound` to capitalize learnings.
- This step always runs unless `--review-only` was set and the user declined fixes.

#### Step 8: INTEGRATE

- Run `/stx-ce:integrate` to route solutions to their operational destinations, including pattern promotion to the shared catalog (`streamtex-design` pack) for patterns judged generic enough.
- Present the routing plan to the user.
- **GATE (fundamental)**: surface QCM to validate which integrations to execute. Options: `Tout exécuter (Recommandé)` / `Sélection à préciser` / `Aucun` / `Discutons-en`.
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
- Error handling: if a phase fails, report the error, save progress (master plan snapshot if state changed), and surface a QCM: `Retenter (Recommandé)` / `Passer` / `Abandonner` / `Discutons-en`.

### End-of-Cycle Soft Interruption

After Step 9, surface a QCM: *"Snapshot final du plan ?"* with default `Oui` (per `ce-conventions.md`). Skip silently if the master plan has not changed since the last snapshot.

### Related Commands

- `/stx-ce:task "<description>"` — For ad-hoc tasks outside the pipeline (compare, targeted review, plan amendment, etc.). See `ce-task.md`.
- `/stx-ce:continue` — For session resumption after a break (briefing, drift detection, proposals). See `ce-continue.md`.
