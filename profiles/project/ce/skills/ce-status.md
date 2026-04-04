# CE Status

Skill for displaying the CE cycle status dashboard. Scans project artifacts to determine which phases are complete, in progress, or pending, and presents a formatted summary.

## Workflow

### Phase 1: Detect Project

1. Verify the current directory is a StreamTeX project:
   - Check for `book.py` or `blocks/` directory at the project root.
   - If neither exists, report an error: "Not a StreamTeX project — no book.py or blocks/ found."
2. Identify the project name from the directory name or from `pyproject.toml` if available.

### Phase 2: Scan Artifacts

Scan the `docs/` directory for CE artifacts from each phase:

| Phase    | Directory          | Pattern                                  |
|----------|--------------------|------------------------------------------|
| COLLECT  | `docs/collect/`    | `YYYY-MM-DD-*-collect.md`                |
| ASSESS   | `docs/assess/`     | `YYYY-MM-DD-*-assess-*.md`               |
| PLAN     | `docs/plans/`      | `YYYY-MM-DD-*-plan.md` or `YYYY-MM-DD-*-*.md` |
| REVIEW   | `docs/reviews/`    | `YYYY-MM-DD-*-review.md`                 |
| COMPOUND | `docs/solutions/`  | Any `.md` files (solution files by category) |

Also check:
- `docs/solutions/producer-profile.md` — Producer profile existence

For each directory, find the most recent file by date prefix (`YYYY-MM-DD`). Record the file path and date.

### Phase 3: Determine Phase Status

For each CE phase, determine its status:

1. **Done**: Artifact exists and contains no lines with `TODO`, `PENDING`, or `[ ]` markers.
2. **In progress**: Artifact exists but contains `TODO`, `PENDING`, or `[ ]` markers indicating incomplete items.
3. **Pending**: No artifact found in the expected directory.

Special cases:
- **PRODUCE**: Determined by examining the latest plan file. If a plan exists, check how many items are marked `[x]` (done) vs `[ ]` (pending). If all done, PRODUCE is Done. If some done, In progress. If none done but plan exists, In progress.
- **FIX**: Check `docs/reviews/` for fix traceability files (`*-fixes.md` or `*-fix-*.md`). If found and complete, Done.
- **COMPOUND**: Check `docs/solutions/` for solution files. If solution files exist (beyond just `producer-profile.md`), Done or In progress based on content.

### Phase 4: Parse Production Progress

If a plan file exists in `docs/plans/`:

1. Read the latest plan file.
2. Count items by status:
   - Done: lines matching `- [x]` or marked as DONE/COMPLETE
   - Pending: lines matching `- [ ]` or marked as TODO/PENDING
3. Break down by type if item lines contain type markers:
   - **IMPORT**: items tagged with import, `[IMPORT]`, or in an import section
   - **IMPROVE**: items tagged with improve, `[IMPROVE]`, or in an improve section
   - **CREATE**: items tagged with create, `[CREATE]`, or in a create section
4. Identify the next item to process (first pending item in the plan).

### Phase 5: Parse Review Findings

If a review file exists in `docs/reviews/`:

1. Read the latest review file.
2. Count findings by severity:
   - **CRITICAL**: lines containing `CRITICAL` severity marker
   - **MAJOR**: lines containing `MAJOR` severity marker
   - **MINOR**: lines containing `MINOR` severity marker
   - **SUGGESTION**: lines containing `SUGGESTION` severity marker
3. Count unfixed findings (items not marked as fixed or resolved).
4. Record the review date from the filename.

### Phase 6: Display Dashboard

Output the following formatted dashboard:

```
CE Cycle Status — {project_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase        Status              Date         Artifact
─────        ──────              ────         ────────
COLLECT      {status_icon}       {date}       {artifact_path}
ASSESS       {status_icon}       {date}       {artifact_path}
PLAN         {status_icon}       {date}       {artifact_path}
PRODUCE      {status_icon}       {date}       {summary}
REVIEW       {status_icon}       {date}       {artifact_path}
FIX          {status_icon}       {date}       {artifact_path}
COMPOUND     {status_icon}       {date}       {artifact_path}
```

Status icons:
- Done: `Done`
- In progress: `In progress`
- Pending: `Pending`

If production progress data is available, append:

```
Production Progress: {done}/{total} ({percent}%)
  IMPORT:  {done}/{total}  {status}
  IMPROVE: {done}/{total}  {status}
  CREATE:  {done}/{total}  {status}
  Next: {next_item_type} {next_item_name}
```

If review data is available, append:

```
Last Review: {date}
  CRITICAL: {count}  MAJOR: {count}  MINOR: {count}  SUGGESTION: {count}
  Unfixed: {count}
```

If producer profile exists, append:

```
Producer Profile: docs/solutions/producer-profile.md
  Solutions: {count} ({category_breakdown})
```

If `--verbose` flag is set, also show:
- Full list of plan items with their status
- Full list of review findings with their severity and fix status
- List of all solution files with their categories

### Session Checkpoint

If `docs/ce-checkpoint.md` exists, include in the dashboard:

```
Session Checkpoint: docs/ce-checkpoint.md
  Saved: <checkpoint_date> (<N days ago>)
  Phase at pause: <current_phase> (<phase_progress>)
  Active items: <N>
  Pending issues: <N>
  Context: <first line of "Context for Next Session">
```

This alerts the user that a previous session was paused with context that should be restored via `/stx-ce:continue`.

### Task Activity

If task-related artifacts exist, include in the dashboard:

| Metric | Value |
|--------|-------|
| Plan versions | N (latest: `<filename>`) |
| Task reviews | N (latest: `<date>`) |
| Last task | `<date>` — `<task description excerpt>` |

Scan for:
- Plan versions: count files in `docs/plans/` matching the project name
- Task reviews: count files in `docs/reviews/` matching `*-task-review.md` or `*-coverage-task.md`
- Last task: parse the most recent task-review or coverage-task file header for the task description
