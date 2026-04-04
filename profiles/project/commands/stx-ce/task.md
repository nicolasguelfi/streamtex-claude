# /stx-ce:task — Execute an ad-hoc task with lifecycle reconciliation

Arguments: $ARGUMENTS

## Options

- `--from-plan <path>` — Use a specific plan as context (default: auto-detect latest)
- `--help` — Show stx-ce cheatsheet

## Description

Executes a free-form, ad-hoc task outside the standard CE pipeline. The task description is analyzed, classified into one or more archetypes, and executed using existing CE agents. Lifecycle artifacts (plan, review, solutions) are automatically updated so the main cycle can resume coherently.

**6 Task Archetypes** (auto-detected from description):

| Archetype | Triggers | Artifact |
|-----------|----------|----------|
| COMPARE | "compare", "coverage", "gaps", "what's missing" | `docs/reviews/YYYY-MM-DD-coverage-task.md` |
| TARGETED REVIEW | "review", "check", "verify", "audit" + scope | `docs/reviews/YYYY-MM-DD-task-review.md` |
| TARGETED PRODUCTION | "add", "create", "produce", "implement" | New blocks + new plan version |
| PLAN AMENDMENT | "update plan", "reorder", "remove from plan" | New plan version with Change Log |
| TARGETED COMPOUND | "capitalize", "save learning", "extract pattern" | `docs/solutions/<category>/YYYY-MM-DD-<topic>.md` |
| SOURCE ANALYSIS | "analyze source", "extract from", "list topics" | `docs/collect/YYYY-MM-DD-task-analysis.md` |

**Composite tasks**: A single description can combine archetypes — they are decomposed and sequenced automatically.

**Conditional gate**: No confirmation for read-only tasks (COMPARE, SOURCE ANALYSIS). Confirmation before write tasks (PRODUCTION, PLAN AMENDMENT). Configurable via producer profile `task_gate: auto | always | never`.

**Plan versioning**: When a task modifies the plan, the current plan is kept and a new version is created with modifications integrated inline + a Change Log header. Latest by date+sequence = current.

## Examples

- `/stx-ce:task "Compare source lines 524-600 with bck_vibecoding_* blocks"` — Coverage analysis
- `/stx-ce:task "Review danger blocks on citation accuracy"` — Targeted review
- `/stx-ce:task "Add a block on AI ethics based on source lines 402-410"` — Targeted production
- `/stx-ce:task "Move bck_vibeeng_evidence before the spectrum in the plan"` — Plan amendment
- `/stx-ce:task "Capitalize the kitchen metaphor as a pattern"` — Targeted compound
- `/stx-ce:task "Extract all statistics with citations from the source"` — Source analysis
- `/stx-ce:task "Compare source 524-600 with blocks, produce missing, update plan"` — Composite

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-task.md` — Full workflow

## Workflow

Execute the `ce-task` skill. Follow the 6-step flow: PARSE → CONTEXT → GATE → EXECUTE → RECONCILE → REPORT.
