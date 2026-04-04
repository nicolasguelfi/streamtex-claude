# CE Continue

Skill for session resumption within the Compound Engineering lifecycle. Inspects project state, detects drift since last activity, and proposes prioritized next steps.

## Workflow

### Parse Arguments

If `--verbose` is set, include detailed artifact contents and full git diffs in the output.
If `--help` is set, display the CE cheatsheet.

### Step 1: INSPECT — Build Project State Snapshot

1. **Detect project**: Check for `book.py` or `blocks/` directory. If not found, report "No StreamTeX project detected" and exit.

2. **Scan CE artifacts**:
   - `docs/collect/` — collect reports (sorted by date)
   - `docs/assess/` — assessment documents
   - `docs/plans/` — plan files (identify current = latest by date+sequence)
   - `docs/reviews/` — review files (including task-review files)
   - `docs/solutions/` — solution files by category
   - `docs/solutions/producer-profile.md` — producer profile

3. **Determine last CE activity date**: The most recent timestamp from any CE artifact filename (YYYY-MM-DD prefix).

4. **Count blocks**:
   - In `book.py`: count `blocks.bck_*` references
   - In `blocks/`: count `bck_*.py` files
   - Mismatch = blocks exist but not referenced (or vice versa)

5. **Production progress** (if plan exists):
   - Parse plan for total planned blocks
   - Compare with existing block files
   - Calculate: N produced / M planned

6. **Review status** (if review exists):
   - Parse latest review for findings by severity
   - Check if fixes were applied (look for "Fix Applied" section or task-review fix status)
   - Count unresolved CRITICAL and MAJOR findings

7. **Design guideline**: Check `custom/design-guideline.md` for active guideline name.

### Step 2: DETECT DRIFT — What Changed Since Last Activity

Use the last CE activity date as the baseline.

#### 2.1 Source Document Drift

If the plan or assessment references a source document path:
1. Check the source file's modification date (filesystem mtime).
2. If modified after last CE activity:
   - Run `git diff` or compare mtime to identify changed sections.
   - If `--verbose`: show the changed line ranges and brief content summary.
   - Classify as: **new content added**, **existing content modified**, or **content removed**.

#### 2.2 Manual Block Drift

1. For each block file in `blocks/bck_*.py`:
   - Check if the file was modified after the last CE activity date.
   - Use `git log --since="<last_activity_date>" -- blocks/bck_*.py` to detect changes.
2. List blocks modified outside the CE cycle (manual edits by the user).

#### 2.3 Plan Drift

1. Compare the block list in `book.py` with the block list in the current plan.
2. Detect:
   - **Added**: blocks in book.py but not in plan
   - **Removed**: blocks in plan but not in book.py
   - **Reordered**: blocks in different order

#### 2.4 Stale Artifact Detection

1. **Stale review**: Review date is older than source modifications or manual block edits → findings may no longer be valid.
2. **Stale plan**: Plan date is older than significant manual changes to book.py or block structure.
3. **Stale collect**: Collect date is older than source document modifications.

#### 2.5 Unresolved Findings

Parse the latest review file for findings with status != FIXED:
- Count by severity (CRITICAL, MAJOR, MINOR, SUGGESTION)
- Highlight CRITICAL as blocking

### Step 3: PROPOSE — Prioritized Next Steps

Generate a prioritized list of recommendations based on the inspection and drift results.

**Priority logic** (highest to lowest):

| Priority | Condition | Recommendation |
|----------|-----------|----------------|
| CRITICAL | Unresolved CRITICAL review findings | `/stx-ce:fix --severity CRITICAL` |
| HIGH | Source document has new content in areas already produced | `/stx-ce:task "Compare source changes with produced blocks"` |
| HIGH | Blocks remaining in plan (production incomplete) | `/stx-ce:go --from-plan <current-plan>` or `/stx-ce:produce` |
| HIGH | Plan drift detected (book.py ≠ plan) | `/stx-ce:task "Update plan to match current book.py"` |
| MEDIUM | Source has new content in areas not yet produced | `/stx-ce:task "Analyze new source content for plan integration"` |
| MEDIUM | Stale review (source changed since review) | `/stx-ce:review` (re-run review) |
| MEDIUM | Unresolved MAJOR review findings | `/stx-ce:fix --severity MAJOR` |
| LOW | No review executed yet | `/stx-ce:review` |
| LOW | No compound executed yet | `/stx-ce:compound` |
| INFO | All phases complete, no drift | "Project is up to date. No action needed." |

**Fresh project** (no artifacts at all):
- Recommend `/stx-ce:go` to start the full cycle
- Or `/stx-ce:go --quick` if the user wants to skip collect/assess

### Step 4: INTERACT — Dispatch User Choice

Present the briefing + drift + proposals to the user, then prompt:

```
Enter a number to execute a proposal,
describe your own task (dispatches to /stx-ce:task),
or type 'skip' to exit.
```

**Dispatch logic**:
- **Number selected**: Execute the corresponding command from the proposals list.
- **Free text**: Dispatch to `/stx-ce:task "<user text>"`.
- **"skip"** or empty: Exit without action.

### Output Format

#### Briefing Section

```
📋 Project: <project_name>
   Last CE activity: <date> (<N days ago>)
   Current plan: <filename> (version <N>)
   Blocks: <N in book.py> / <M in plan> (<P produced, Q remaining>)
   Review: <status — none / date with N findings / N unresolved>
   Source: <filename> (last modified: <date>)
   Guideline: <name or "none">
```

#### Drift Section (only shown if drift detected)

```
⚠️  Changes detected since last CE activity (<date>):

   Source document: <N lines modified> (<date>)
     → Lines <range>: <brief description>
     → Lines <range>: <brief description>

   Manual changes: <N blocks modified>
     → <block_name> (<date>)
     → <block_name> (<date>)

   Plan drift: <description or "none">
   Stale artifacts: <list or "none">
   Unresolved findings: <N CRITICAL, M MAJOR or "none">
```

#### Proposals Section

```
📌 Recommended next steps:

   1. [<PRIORITY>] <Description>
      → <command>

   2. [<PRIORITY>] <Description>
      → <command>

   ...

Enter a number, describe your own task, or 'skip':
```
