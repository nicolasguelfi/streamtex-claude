# CE Go

Skill for the autonomous workflow of the Compound Engineering cycle. Execute the full cycle sequentially with gates for user validation at critical points.

## Workflow

### Parse Arguments and Flags

Process the following flags before starting:

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

- Run `/stx-ce:plan`.
- If `--from-plan <path>` is set: load the specified plan and skip generation.
- Auto-detect interactive mode: enable `--interactive` if COLLECT found 10 or more sources or the project has 20 or more existing blocks.
- If `--interactive` flag was explicitly set: use interactive mode regardless.
- **GATE**: The user must explicitly validate the plan before proceeding. Present the plan summary and wait for approval. If rejected, allow the user to request modifications and regenerate.

#### Step 4: PRODUCE

- Run `/stx-ce:produce` with the approved plan.
- If `--no-deploy` is set: pass it through to skip deployment.
- If `--review-only` is set: skip this step entirely.
- Track production progress and report completion status.

#### Step 5: REVIEW

- Run `/stx-ce:review`.
- **GATE**: The user must validate the review results. Present the review summary and wait for approval.

#### Step 6: FIX

- Run `/stx-ce:fix` to correct automatable findings from the review.
- If `--review-only` is set: skip this step unless the user explicitly requests fixes.
- **GATE**: The user must validate the fix results. Propose re-review (`/stx-ce:review`) or continue to COMPOUND.
- If the user requests re-review: loop back to Step 5 (REVIEW → FIX can iterate).

#### Step 7: COMPOUND

- Run `/stx-ce:compound` to capitalize learnings.
- This step always runs unless `--review-only` was set and the user declined fixes.

#### Step 8: Final Report

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

### Pipeline Mode

When running from `/stx-ce:go`, individual phases operate in pipeline mode:

- Phases do not ask for user input except at designated GATEs (after PLAN, after REVIEW, and after FIX).
- Phases auto-detect context from previous phase outputs rather than prompting.
- Error handling: if a phase fails, report the error, save progress, and ask the user whether to retry, skip, or abort.
- Progress is saved so the cycle can be resumed if interrupted.

### Related Commands

- `/stx-ce:task "<description>"` — For ad-hoc tasks outside the pipeline (compare, targeted review, plan amendment, etc.). See `ce-task.md`.
- `/stx-ce:continue` — For session resumption after a break (briefing, drift detection, proposals). See `ce-continue.md`.
