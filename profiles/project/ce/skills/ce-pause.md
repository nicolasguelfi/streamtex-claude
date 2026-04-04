# CE Pause

Skill for creating a session checkpoint before pausing work. Captures the current state of in-progress work, decisions made, and context needed to resume effectively in a future session.

## Workflow

### Parse Arguments

If `--message "<text>"` is set, use it as context annotation in the checkpoint.
If `--help` is set, display the CE cheatsheet.

### Step 1: INSPECT — Capture Current State

1. **Detect project**: Check for `book.py` or `blocks/` directory. If not found, report "No StreamTeX project detected" and exit.

2. **Scan CE artifacts** (same as `ce-continue` Step 1):
   - `docs/collect/`, `docs/assess/`, `docs/plans/`, `docs/reviews/`, `docs/solutions/`
   - Determine current plan (latest by date+sequence)
   - Count blocks in book.py vs blocks/ directory
   - Parse production progress from plan ([x] vs [ ] markers)
   - Parse review findings if review exists

3. **Determine current phase**: Based on which artifacts exist and their completeness:
   - Latest completed phase (artifact exists, no TODO/PENDING/[ ] markers)
   - Current in-progress phase (artifact exists with incomplete markers)
   - Next pending phase

4. **Design guideline**: Check `custom/design-guideline.md` for active guideline name.

### Step 2: DETECT IN-PROGRESS WORK

#### 2.1 Uncommitted Changes

Run `git status --short` and `git diff --stat` to identify:
- Modified block files (blocks/bck_*.py)
- Modified CE artifacts (docs/)
- Modified configuration files (book.py, custom/)
- New untracked files

#### 2.2 Partial Production

If a plan exists, identify blocks that are:
- **In progress**: Block file exists but plan marks it as `[ ]` (pending), AND the file has been modified since the plan was created (detected via git log or mtime)
- **Incomplete**: Block file exists but contains `TODO`, `FIXME`, or `HACK` markers
- **Out-of-plan**: Block file exists in blocks/ but is not in the current plan

#### 2.3 Partial Review/Fix

If a review exists:
- Count findings by status: FIXED, PARTIAL, UNFIXED
- Identify which blocks have been modified since the review (potential partial fixes)

#### 2.4 Recent Task Activity

Check for recent task artifacts (task-review, coverage-task, task-analysis) created during this session:
- List tasks and their outcomes
- Note any plan amendments caused by tasks

### Step 3: CAPTURE CONTEXT — Build Checkpoint

Generate a checkpoint file using the `checkpoint` template. The checkpoint captures:

1. **Session metadata**: project name, checkpoint date, current plan path, current phase
2. **Active work items**: blocks being worked on, their state, what remains to do
3. **Decisions log**: prompt the user to confirm or add decisions made during this session
4. **Pending issues**: known problems, missing assets, blocked items
5. **Context for next session**: free-text summary of where things stand and what to focus on next

#### Context Gathering

To populate the "Decisions log" and "Context for next session" sections:

1. **Analyze the conversation history**: Review all CE commands executed in the current session, task descriptions, and user instructions to extract:
   - Design choices (e.g., "chose 2-column grid for the comparison slide")
   - Scope decisions (e.g., "decided to skip the bibliography for now")
   - Plan deviations (e.g., "added glossary block not in original plan")
   - Quality trade-offs (e.g., "accepted MINOR findings, will fix in next pass")

2. **Present draft to user**: Show the extracted decisions and ask:
   ```
   I've captured these decisions from our session. 
   Please confirm, modify, or add anything I missed:
   
   1. [decision 1]
   2. [decision 2]
   ...
   
   Additional context for next session (optional):
   ```

3. **If `--message` was provided**: Include it as the primary context annotation, still present the rest for confirmation.

### Step 4: WRITE CHECKPOINT

1. Write the checkpoint to `docs/ce-checkpoint.md` (overwrites any previous checkpoint).
2. Display a summary:

```
Checkpoint saved: docs/ce-checkpoint.md

   Project: <name>
   Phase: <current_phase> (<progress>)
   Active items: <N blocks in progress>
   Decisions: <N captured>
   Pending issues: <N>

   Next session: run /stx-ce:continue to restore context.
```

3. If there are uncommitted changes, suggest:
```
   Uncommitted changes detected. Consider committing before pausing:
   git add docs/ce-checkpoint.md && git commit -m "chore(ce): checkpoint — <summary>"
```

### Output Format

#### Checkpoint File

Written to `docs/ce-checkpoint.md` using the `checkpoint` template. See `.claude/ce/templates/checkpoint.md` for the full structure.

#### Terminal Output

```
Checkpoint saved: docs/ce-checkpoint.md

   Project: <project_name>
   Phase: <current_phase> (<progress_summary>)
   Active items: <N blocks in progress>
   Decisions: <N captured>
   Pending issues: <N>

   Next session: run /stx-ce:continue to restore context.
```
