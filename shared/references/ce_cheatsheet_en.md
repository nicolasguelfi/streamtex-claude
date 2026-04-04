# StreamTeX CE — Compound Document Engineering Quick Reference

## Cycle

```
COLLECT -> ASSESS -> PLAN -> PRODUCE -> REVIEW -> FIX -> COMPOUND
   ^                  |                    |        |        |
   |               [GATE]              [GATE]    [GATE]      |
   +----------------------------------------------------------+
```

## Commands (11)

| Command | Description |
|---------|-------------|
| `/stx-ce:collect <path>` | Inventory and classify existing material |
| `/stx-ce:assess` | Evaluate material and define document objectives |
| `/stx-ce:plan [--interactive]` | Plan production (auto or collaborative 4-step) |
| `/stx-ce:produce` | Execute the plan (import/create/improve) |
| `/stx-ce:review` | Multi-perspective review (5 agents) — read-only evaluation |
| `/stx-ce:fix [--severity LEVEL]` | Fix findings from the latest review with verification |
| `/stx-ce:compound` | Capitalize learnings (3 axes: production, feedback, governance) |
| `/stx-ce:go [flags]` | Full autonomous cycle with 3 gates |
| `/stx-ce:status` | Show CE cycle status for current project |
| `/stx-ce:task "<desc>"` | Execute ad-hoc task with lifecycle reconciliation |
| `/stx-ce:continue` | Resume work: briefing, drift detection, proposals |

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

## /stx-ce:continue — Session Resumption

**Syntax**: `/stx-ce:continue [--verbose]`

**Output**:
1. **Briefing**: project name, last activity, plan version, block count, progress
2. **Drift**: source changes, manual edits, plan mismatch, stale artifacts, unresolved findings
3. **Proposals**: prioritized next steps with executable commands
4. **Dispatch**: select proposal by number, describe custom task, or skip

**Priority levels**: CRITICAL (unresolved critical findings) > HIGH (source drift, remaining production) > MEDIUM (stale reviews, source updates) > LOW (missing phases) > INFO (up to date)

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

## Templates (16)

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

## COMPOUND — 3 Axes of Capitalization

| Axis | What it does | Output |
|------|-------------|--------|
| **1. Document production** | Extract learnings (specific + generic), update producer profile | `docs/solutions/<category>/`, `producer-profile.md` |
| **2. Ecosystem feedback** | Detect bugs/features, propose tickets via `/stx-issue:*` (with GATE) | GitHub issues, `feedback-summary.md` |
| **3. Dev governance** | Inventory ecosystem repo changes, verify workflows, propose PRs | `docs/solutions/governance/dev-report.md` |

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

## Orchestrated StreamTeX Commands

### During PRODUCE
| Action | Commands used |
|--------|-------------|
| Import | `/stx-import:html`, `:html-block`, `:html-batch`, `:marp` |
| Create | `/stx-designer:init`, `:block-new`, `:slide-new` |
| Improve | `/stx-designer:update`, `:style-refactor` |
| Verify | `/stx-designer:audit --target`, `/stx-designer:fix --target` |
| Deliver | `/stx-export:html`, `/stx-deploy:deploy` |

### During FIX
| Action | Commands used |
|--------|-------------|
| Fix | `/stx-designer:fix --target <block>` |
| Verify | `/stx-designer:audit --target <block>`, `--all` |

### During COMPOUND (Axis 2)
| Action | Commands used |
|--------|-------------|
| Submit tickets | `/stx-issue:bug`, `:feature`, `:docs`, `:question` |
