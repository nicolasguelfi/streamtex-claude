# StreamTeX CE — Compound Document Engineering Quick Reference

## Cycle

```
COLLECT -> ASSESS -> PLAN -> PRODUCE -> REVIEW -> FIX -> COMPOUND -> INTEGRATE
   ^                  |                    |        |        |           |
   |               [GATE]              [GATE]    [GATE]   [GATE]        |
   +--------------------------------------------------------------------+
```

## Commands (13)

| Command | Description |
|---------|-------------|
| `/stx-ce:collect <path>` | Inventory and classify existing material |
| `/stx-ce:assess` | Evaluate material and define document objectives |
| `/stx-ce:plan [--interactive]` | Plan production (auto or collaborative 4-step) |
| `/stx-ce:produce` | Execute the plan (import/create/improve) |
| `/stx-ce:review` | Multi-perspective review (5 agents) — read-only evaluation |
| `/stx-ce:fix [--severity LEVEL]` | Fix findings from the latest review (interactive by default) |
| `/stx-ce:compound` | Capitalize learnings (3 axes: production, feedback, governance) |
| `/stx-ce:integrate` | Route solutions to operational destinations (lib issues, custom rules) |
| `/stx-ce:go [flags]` | Full autonomous cycle with 4 gates |
| `/stx-ce:status` | Show CE cycle status for current project |
| `/stx-ce:task "<desc>"` | Execute ad-hoc task with lifecycle reconciliation |
| `/stx-ce:pause [--message]` | Save session checkpoint before pausing work |
| `/stx-ce:continue` | Resume work: briefing, drift detection, checkpoint restore |

## Pathways

| Pathway | Starting point | Description |
|---------|---------------|-------------|
| **A (Import)** | External material (Word, PPT, PDF, LaTeX, HTML...) | Progressive import into StreamTeX |
| **B (Improve)** | Existing StreamTeX project | Correct, enrich, restructure |
| **C (Create)** | Context (other projects, collection) | New document in existing context |

## /stx-ce:go Flags

| Flag | Effect |
|------|--------|
| `--quick` | Skip COLLECT + ASSESS, go to PLAN |
| `--from-plan <path>` | Resume from existing plan |
| `--interactive` | Force 4-step collaborative planning |
| `--review-only` | Only REVIEW (+ optional FIX) existing project |
| `--no-deploy` | Skip deployment |
| `--import <path>` | Force pathway A |
| `--improve` | Force pathway B |

## Planning Modes

| Mode | Trigger | Steps |
|------|---------|-------|
| **Auto** | Default (or `--quick`) | Single-pass plan generation |
| **Interactive** | `--interactive` or auto (>= 10 sources / >= 20 blocks) | 1. Skeleton -> 2. Objectives -> 3. Design -> 4. Final plan |

## /stx-ce:task — Ad-Hoc Tasks

**Syntax**: `/stx-ce:task "<free-text description>"`

| Archetype | Triggers | Artifact |
|-----------|----------|----------|
| COMPARE | "compare", "coverage", "gaps" | `docs/reviews/YYYY-MM-DD-coverage-task.md` |
| TARGETED REVIEW | "review", "check" + scope/criteria | `docs/reviews/YYYY-MM-DD-task-review.md` |
| TARGETED PRODUCTION | "add", "create", "produce" | New blocks + new plan version |
| PLAN AMENDMENT | "update plan", "reorder" | New plan version with Change Log |
| TARGETED COMPOUND | "capitalize", "extract pattern" | `docs/solutions/<cat>/YYYY-MM-DD-<topic>.md` |
| SOURCE ANALYSIS | "analyze source", "extract from" | `docs/collect/YYYY-MM-DD-task-analysis.md` |

**Gate**: No gate for read-only (COMPARE, ANALYSIS), confirmation for write tasks. Configurable: `task_gate` in producer profile.
**Plan versioning**: New plan version created (not appended). Latest by date+sequence = current.
**Composite**: Multiple archetypes in one description → decomposed and sequenced automatically.

## /stx-ce:pause — Session Checkpoint

**Syntax**: `/stx-ce:pause [--message "<text>"]`

**Purpose**: Save a checkpoint before ending a work session. Captures in-progress work, decisions, pending issues, and context that would be lost between sessions.

**Output**: `docs/ce-checkpoint.md` (overwritten each time)

**Checkpoint contains**:
- Active work items (blocks in progress, incomplete, out-of-plan)
- Decisions log (design choices, scope decisions, plan deviations)
- Pending issues (blockers, missing assets, partial fixes)
- Uncommitted changes summary
- Free-text context for next session

**Workflow**: INSPECT state → DETECT in-progress work → CAPTURE context (with user confirmation) → WRITE checkpoint

**Best practice**: Run `/stx-ce:pause` before ending any session where work is in an intermediate state. Commit the checkpoint to git for reliable restoration.

## /stx-ce:continue — Session Resumption

**Syntax**: `/stx-ce:continue [--verbose]`

**Output**:
0. **Checkpoint restore**: if `docs/ce-checkpoint.md` exists, restore context and archive it
1. **Briefing**: project name, last activity, plan version, block count, progress
2. **Drift**: source changes, manual edits, plan mismatch, stale artifacts, unresolved findings
3. **Proposals**: prioritized next steps with executable commands (checkpoint items integrated)
4. **Dispatch**: select proposal by number, describe custom task, or skip

**Priority levels**: CRITICAL (unresolved critical findings) > HIGH (source drift, remaining production, checkpoint active items) > MEDIUM (stale reviews, source updates) > LOW (missing phases) > INFO (up to date)

## Agents (18)

### COLLECT (2)
| Agent | Role |
|-------|------|
| `source-scanner` | Scan files, detect types, extract metadata |
| `import-assessor` | Evaluate import complexity, recommend method |

### ASSESS (5)
| Agent | Role | Pathway |
|-------|------|---------|
| `audience-analyst` | Profile target audience | All |
| `content-strategist` | Analyze themes, coverage, gaps | All |
| `gap-analyst` | Compare current vs target state | A, B |
| `format-explorer` | Propose document formats | C |
| `angle-generator` | Propose narrative angles | C |

- **R27b**: Design guideline selection (builtin / custom / none)

### PLAN (3)
| Agent | Role |
|-------|------|
| `structure-architect` | Design document skeleton and block mapping |
| `domain-researcher` | Research external best practices and references |
| `learnings-researcher` | Search docs/solutions/ for past patterns |

### REVIEW (5 perspectives)
| Perspective | Agent | Evaluates |
|-------------|-------|-----------|
| Reader/Learner | `audience-advocate` | Clarity, progression, engagement |
| Pedagogical | `pedagogy-analyst` | Objectives, alignment, rhythm |
| Visual | `visual-reviewer` | Coherence, readability, accessibility |
| Technical | `style-consistency-checker` | CSS, conventions, book.py |
| Editorial | `content-editor` | Writing quality, tone, terminology |

### COMPOUND (2)
| Agent | Role |
|-------|------|
| `feedback-detector` | Detect ecosystem bugs and missing features from cycle artifacts |
| `dev-governance` | Verify dev conventions, propose branches and PRs |

### TASK (1)
| Agent | Role |
|-------|------|
| `ad-hoc-reviewer` | Custom-criteria review of scoped blocks |

## Templates (17)

### COLLECT (1)
| Template | Purpose |
|----------|---------|
| `collect-report` | Source inventory and classification report |

### ASSESS (3)
| Template | Purpose | Pathway |
|----------|---------|---------|
| `assess-import` | Assessment for importing external material | A |
| `assess-improve` | Assessment for improving existing project | B |
| `assess-create` | Assessment for creating new document | C |

### PLAN (3)
| Template | Purpose | Pathway |
|----------|---------|---------|
| `plan-import` | Production plan for import pathway | A |
| `plan-improve` | Production plan for improve pathway | B |
| `plan-create` | Production plan for create pathway | C |

### REVIEW (1)
| Template | Purpose |
|----------|---------|
| `review-report` | Multi-perspective review report |

### PRODUCE (1)
| Template | Purpose |
|----------|---------|
| `solution` | Capitalized learning / reusable pattern |

### COMPOUND (3)
| Template | Purpose |
|----------|---------|
| `producer-profile` | Persistent producer preferences and learnings |
| `feedback-summary` | Ecosystem feedback summary (bugs, features) |
| `dev-report` | Dev governance report (repo changes, PRs) |

### TASK (4)
| Template | Purpose |
|----------|---------|
| `task-review` | Targeted review findings |
| `coverage-matrix` | Source vs production coverage analysis |
| `task-analysis` | Source document structured analysis |
| `task-report` | Task execution summary |
| `checkpoint` | Session checkpoint for pause/resume |

## COMPOUND — 3 Axes of Capitalization

| Axis | What it does | Output |
|------|-------------|--------|
| **1. Document production** | Extract learnings (specific + generic), update producer profile | `docs/solutions/<category>/`, `producer-profile.md` |
| **2. Ecosystem feedback** | Detect bugs/features, propose tickets via `/stx-issue:*` (with GATE) | GitHub issues, `feedback-summary.md` |
| **3. Dev governance** | Inventory ecosystem repo changes, verify workflows, propose PRs | `docs/solutions/governance/dev-report.md` |

## INTEGRATE — Route Solutions to Operational Destinations

| Destination | Target | Method |
|-------------|--------|--------|
| **streamtex** (lib) | Library bugs or features | `/stx-issue:feature` or `/stx-issue:bug` |
| **streamtex-claude** (plugin) | Skill, command, template changes | `/stx-issue:feature` or `/stx-issue:bug` |
| **streamtex-docs** (docs) | Documentation improvements | `/stx-issue:docs` |
| **Author custom** | `.claude/custom/references/` or `custom/design-guideline.md` | Direct file update |

Options: `--target <file>` (single solution), `--dry-run` (preview only)

Solutions are marked `integrated: true` in frontmatter after processing.

## Producer Profile

Stored in `docs/solutions/producer-profile.md`. Loaded at COLLECT, used by ASSESS (pre-fill R9-R12) and PLAN (inform design proposals). Updated at COMPOUND.

## Severity Levels (Review / Fix)

| Level | Meaning |
|-------|---------|
| **CRITICAL** | Blocks work or comprehension |
| **MAJOR** | Significantly degrades quality |
| **MINOR** | Minor polish needed |
| **SUGGESTION** | Nice to have improvement |

## Project Directory Structure

```
my-project/
  docs/
    ce-checkpoint.md  # Session checkpoint (created by /stx-ce:pause)
    collect/        # Source inventory reports
    assess/         # Requirements and objectives
    plans/          # Production plans
    reviews/        # Review reports (+ fix traceability)
    solutions/      # Capitalized learnings
      structure/    # Document structure patterns
      style/        # CSS/theme patterns
      content/      # Content writing patterns
      process/      # Workflow patterns
      pedagogy/     # Pedagogical patterns
      assets/       # Asset management patterns
      deployment/   # Deploy/export patterns
      import/       # Import conversion patterns
      governance/   # Dev governance reports
      producer-profile.md  # Producer preferences (persistent)
```

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Collect | `YYYY-MM-DD-<name>-collect.md` | `2026-03-22-info101-collect.md` |
| Assess | `YYYY-MM-DD-<name>-assess-<pathway>.md` | `2026-03-22-info101-assess-import.md` |
| Plan | `YYYY-MM-DD-NNN-<pathway>-<name>-plan.md` | `2026-03-22-001-import-info101-plan.md` |
| Review | `YYYY-MM-DD-<name>-review.md` | `2026-03-22-info101-review.md` |
| Solution | `YYYY-MM-DD-<topic>.md` | `2026-03-22-grid-layout-pattern.md` |
| Feedback | `YYYY-MM-DD-<name>-feedback.md` | `2026-03-23-info101-feedback.md` |
| Dev report | `YYYY-MM-DD-dev-report.md` | `2026-03-23-dev-report.md` |
| Checkpoint | `ce-checkpoint.md` (active) / `ce-checkpoint-YYYY-MM-DD.md` (archived) | `ce-checkpoint.md` |

## Orchestrated StreamTeX Commands

### During PRODUCE
| Action | Commands used |
|--------|-------------|
| Import | `/stx-import:html`, `:html-block`, `:html-batch`, `:marp` |
| Create | `/stx-block:init`, `:new`, `:slide-new` |
| Improve | `/stx-block:update`, `:style-refactor` |
| Verify | `/stx-block:audit --target`, `/stx-block:fix --target` |
| Deliver | `/stx-export:html`, `/stx-deploy:deploy` |

### During FIX
| Action | Commands used |
|--------|-------------|
| Fix | `/stx-block:fix --target <block>` |
| Verify | `/stx-block:audit --target <block>`, `--all` |

### During COMPOUND (Axis 2)
| Action | Commands used |
|--------|-------------|
| Submit tickets | `/stx-issue:bug`, `:feature`, `:docs`, `:question` |

### During INTEGRATE
| Action | Commands used |
|--------|-------------|
| Route to repos | `/stx-issue:feature`, `:bug`, `:docs` |
| Route to author | Direct edit of `.claude/custom/references/` or `custom/design-guideline.md` |
| Mark integrated | Update solution frontmatter (`integrated: true`) |
