# CE Task

Skill for ad-hoc task execution within the Compound Engineering lifecycle. Executes free-form tasks outside the standard pipeline while maintaining lifecycle artifact coherence.

## Workflow

### Parse Arguments

The task description is provided as the argument string. If `--from-plan <path>` is present, extract and use as plan context. If `--help` is present, display the CE cheatsheet.

### Step 1: PARSE — Understand the Task

Analyze the free-text task description using AI understanding with keyword hints:

1. **Extract intent**: What does the user want to achieve?
2. **Extract scope**: Which blocks, sources, or sections are targeted?
3. **Extract sources**: Any file paths, line ranges, or URLs mentioned?
4. **Classify into archetype(s)**:
   - **COMPARE**: keywords "compare", "coverage", "gaps", "missing", "covered"
   - **TARGETED REVIEW**: keywords "review", "check", "verify", "audit" + block name or custom criteria
   - **TARGETED PRODUCTION**: keywords "add", "create", "produce", "write", "implement"
   - **PLAN AMENDMENT**: keywords "update plan", "add to plan", "reorder", "remove from plan", "amend"
   - **TARGETED COMPOUND**: keywords "capitalize", "save learning", "extract pattern", "document pattern"
   - **SOURCE ANALYSIS**: keywords "analyze source", "extract from", "list topics", "what does the source say"
5. **Detect composite tasks**: If multiple archetypes are detected, decompose and sequence them (each step feeds the next).
6. **Ambiguity handling**: If the classification is not confident, present interpretation and ask user to confirm before proceeding.

### Step 2: CONTEXT — Load Relevant Artifacts

1. **Plan**: Auto-detect current plan by scanning `docs/plans/` for the latest file by date+sequence number. If `--from-plan` is set, use that path instead.
2. **Review**: Load the latest review file from `docs/reviews/` (if exists).
3. **Producer profile**: Load `docs/solutions/producer-profile.md` (if exists). Read `task_gate` preference.
4. **Design guideline**: Load `custom/design-guideline.md` (if exists).
5. **Source files**: If the task references a source path or line range, read the relevant file/section.
6. **Target blocks**: If the task references block names or glob patterns (e.g., `bck_danger_*`), locate and read matching block files in `blocks/`.
7. **book.py**: Read to understand current block order and configuration.

### Step 3: GATE — Conditional Confirmation

Check the `task_gate` field in the producer profile (default: `auto`).

| task_gate | Read-only tasks | Write tasks |
|-----------|-----------------|-------------|
| `auto` | Skip gate | Present execution plan, ask "Proceed?" |
| `always` | Present execution plan | Present execution plan |
| `never` | Skip gate | Skip gate |

**Read-only archetypes**: COMPARE, SOURCE ANALYSIS, TARGETED REVIEW (when no fixes implied).
**Write archetypes**: TARGETED PRODUCTION, PLAN AMENDMENT.
**Mixed**: TARGETED COMPOUND (writes solution files — treat as write).

If gate is active, present:
```
I will execute the following:
1. [Archetype]: [Brief description of what will be done]
2. [Archetype]: [Brief description]
Artifacts that will be created/modified:
- [path 1]
- [path 2]
Proceed? (yes/no)
```

### Step 4: EXECUTE — Run the Task

Execute each archetype in sequence (for composite tasks, each step receives the output of the previous).

#### Archetype: COMPARE

1. Read the source document (file path + optional line range).
2. Extract themes, concepts, statistics, and key facts from the source.
3. Read all target blocks (from scope, or all `blocks/bck_*.py` if no scope specified).
4. For each source theme, search block content for semantic matches.
5. Classify each theme:
   - **COVERED**: Theme is present and faithful to source
   - **PARTIAL**: Theme is present but incomplete or simplified
   - **REPLACED**: Theme is present but deliberately adapted (e.g., metaphor change)
   - **MISSING**: Theme is not present in any block
6. Generate coverage matrix using the **coverage-matrix** template.
7. Generate gap recommendations: for each MISSING theme, suggest a block to create.

#### Archetype: TARGETED REVIEW

1. **Determine scope**: Parse block names or glob patterns from the task description. If none specified, apply to all blocks.
2. **Determine criteria**:
   - If the task mentions a built-in perspective name (audience, pedagogy, visual, style, editorial), use the corresponding review agent.
   - If the task describes custom criteria, use the **ad-hoc-reviewer** agent with the user's criteria as its mandate.
3. Execute the review agent(s) on the scoped blocks.
4. Produce findings with standard severity levels (CRITICAL, MAJOR, MINOR, SUGGESTION).
5. Generate task-review file using the **task-review** template.

#### Archetype: TARGETED PRODUCTION

1. Load the current plan.
2. Determine what to produce from the task description (new block, modification, split).
3. If creating a new block:
   - Use `/stx-block:new` or `/stx-block:slide-new` with content from the task description and source references.
   - Apply design guideline if active (add `# @guideline: <name>` annotation).
   - Run `/stx-block:audit --target <block>` to verify.
   - Fix any findings with `/stx-block:fix --target <block>`.
4. If modifying an existing block:
   - Use `/stx-block:update` with the change description.
   - Audit and fix.
5. Update `book.py` to include the new/modified block at the correct position.

#### Archetype: PLAN AMENDMENT

1. Load the current plan (latest by date+sequence in `docs/plans/`).
2. Read the full plan content.
3. Apply the requested modification inline:
   - **Add**: Insert new block/section at the specified position
   - **Remove**: Delete the block/section (with user confirmation for destructive change)
   - **Reorder**: Move block/section to new position
   - **Modify**: Update block description, content, or metadata
4. Create a new plan file with incremented sequence number.
5. Add **Change Log** header to the new plan:

```markdown
## Metadata
| Field | Value |
|-------|-------|
| Previous version | `<previous-plan-filename>` |
| Change trigger | `/stx-ce:task "<task description>"` |

## Change Log (vs previous version)
- **Added/Removed/Moved/Modified**: <description of change>
- **Impact**: <block count change, slide count change>
```

6. The rest of the plan is the complete, self-contained document with modifications integrated.

#### Archetype: TARGETED COMPOUND

1. Identify the learning/pattern to capitalize from the task description.
2. Search `docs/solutions/` for existing similar entries (using the **learnings-researcher** agent in targeted mode).
3. If duplicate found: update existing solution file.
4. If new: write solution file using the **solution** template to `docs/solutions/<category>/YYYY-MM-DD-<topic>.md`.
5. If the learning is a visual pattern: update `custom/design-guideline.md ## Patterns` section.
6. If relevant: update `docs/solutions/producer-profile.md` with new preference or anti-pattern.

#### Archetype: SOURCE ANALYSIS

1. Read the source document (path + optional line range).
2. Extract and structure:
   - **Themes/sections**: hierarchical outline of topics covered
   - **Statistics**: all numerical data points with their context
   - **Citations**: all references and attributions
   - **Key concepts**: definitions and terminology
   - **Structure**: document organization and flow
3. Generate analysis report using the **task-analysis** template.

### Step 5: RECONCILE — Update Lifecycle Artifacts

Apply reconciliation rules based on what the task produced:

| Task output | Reconciliation action |
|-------------|----------------------|
| New/modified blocks | Create new plan version (PLAN AMENDMENT archetype auto-triggered) + update book.py |
| Review findings | Write `docs/reviews/YYYY-MM-DD-task-review.md` |
| Plan changes | New plan version with Change Log (already done in PLAN AMENDMENT) |
| Solutions/patterns | Write to `docs/solutions/`; update design-guideline if pattern |
| Source analysis | Write to `docs/collect/YYYY-MM-DD-task-analysis.md` |
| Read-only analysis | No reconciliation needed |

**Destructive changes** (removing blocks from plan, deleting files) require explicit user confirmation regardless of `task_gate` setting.

### Step 6: REPORT — Summarize

Generate a task report using the **task-report** template:

```markdown
## Task Report

**Task**: "<original task description>"
**Date**: YYYY-MM-DD
**Archetypes**: [list of archetypes executed]

### Actions Taken
1. [Action 1 — what was done]
2. [Action 2 — what was done]

### Artifacts Created
- `path/to/new/file.md` — [description]

### Artifacts Modified
- `path/to/modified/file.md` — [what changed]

### Cycle State Impact
- Plan version: v2 → v3
- Blocks: 41 → 42 (+1 new)
- Open review findings: 0

### Suggested Next Steps
1. [Suggested action with command]
2. [Suggested action with command]
```

Display the report to the user.
