Audit the StreamTeX ecosystem for cross-component coherence issues.

Arguments: $ARGUMENTS (optional scope — default: all)

## Steps

1. **Locate workspace root**: Find the nearest parent directory containing `stx.toml`.
   The workspace root contains: `streamtex/`, `streamtex-docs/`, `streamtex-claude/`, `projects/`.

2. **Load rules**: Read `.claude/developer/skills/coherence-checks.md`.

3. **Determine scope** from arguments:
   - `all` (default) — Run ALL checks (standard + ai + cli + patterns = checks 1-49)
   - `standard` — Checks 1-28 (original ecosystem coherence checks)
   - `ai` — Checks 29-41 (AI-generated code quality: ghost API, dead code, explanation drift, cross-block contradictions, unused exports, version claims, test quality, silent failures, naming coherence, secret leaks, hardcoded URLs)
   - `cli` — Checks 42-45 (CLI coherence: help↔code, stx-guide↔CLI, deploy scripts↔Docker, optional deps↔imports)
   - `patterns` — Checks P1-P4 / 46-49 (streamtex-patterns mechanism: catalog drift, annotations consistency, format A2 compliance, naming conventions — see `pattern-library` skill for the underlying mechanism)
   - `library` — Checks 1 + 2 + 5 + 9 + 10 + 12 + 17 + 22 (API coverage, cheatsheet sync, version alignment, README links, language, test coverage sync, CHANGELOG freshness, release pipeline)
   - `docs` — Checks 3 + 6 + 7 + 10 + 13 + 14 + 15 + 16 (cross-manual consistency, block structure, template freshness, language, blocks→library API, example signatures, enum coherence, static files)
   - `profiles` — Checks 4 + 8 + 10 + 11 + 18 + 19 + 20 + 21 (profile file sync, stx-guide sync, language, artifact API validation, manifest file existence, CLI template registry sync, issue template sync, command namespace prefix)
   - `blocks` — Checks 3 + 6 + 7 + 10 + 13 + 14 + 15 + 16 (block patterns, structure, template freshness, language, blocks→library API, example signatures, enum coherence, static files)
   - `artifacts` — Check 11 only (Claude artifact API validation)
   - `tests` — Check 12 only (test coverage sync)
   - `language` — Check 10 only (language consistency)
   - `ce` — Checks 23-28 (CE agent sync, CE template sync, CE docs structure, CE cheatsheet sync, CE command registration, CE plan-solution coherence)

4. **Execute checks** for the selected scope. For each check:
   - Read the specified source files
   - Compare against the expected state defined in coherence-checks.md
   - Record findings with severity (ERROR / WARNING / INFO)

5. **Profile File Sync (Check 4) — Special Handling**:

   For files distributed from `streamtex-claude` to project `.claude/` directories (read-only copies):

   **NEVER modify local copies directly.** Instead, analyze the divergence direction:

   a. **Source newer than local** (source has content that local doesn't):
      - Report as INFO: "Local copy out of date — run `stx claude update` to sync"

   b. **Local has modifications not in source** (local diverges from source):
      - Compare the diff to determine if the local changes are **relevant improvements**
      - If relevant: report as WARNING with a backport task description:
        ```
        [BACKPORT] <source_file> — local copy in <project> has changes not in source:
          <brief diff summary>
          → Backport to: streamtex-claude/<source_path>
          → Then run: stx claude update --all
        ```
      - If not relevant (stale local edits superseded by source): report as INFO suggesting `stx claude update`

   c. **Bidirectional divergence** (both changed differently):
      - Report as WARNING with detailed diff and explicit decision needed

   The audit **MUST NOT**:
   - Overwrite local `.claude/` files
   - `chmod` any files
   - Copy files from source to local or vice versa

   The audit **MUST**:
   - Report divergences with enough context to decide the action
   - Generate backport task descriptions for relevant local improvements
   - Remind that `stx claude update` handles source→local sync

6. **Report findings** in the output format below.

## Output Format

```
## Coherence Audit — [scope]

### Ecosystem Health Dashboard
| Metric                    | Value         |
|--------------------------|---------------|
| API exports              | N             |
| Documented exports       | X/N (Y%)      |
| Tested exports           | X/N (Y%)      |
| Ghost API calls found    | N             |
| Stale explanations       | N             |
| Test quality issues      | N             |
| Secret leaks             | N             |
| CLI coherence issues     | N             |

### Summary
| Category | Status | Issues |
|----------|--------|--------|
| API Coverage | ⚠ 3 warnings | |
| Cheatsheet Sync | ✓ OK | |
| ... | | |

### ERRORS (N) — must fix
- [Category] File:Line — Description → Suggested fix

### WARNINGS (N) — should fix
- [Category] File:Line — Description → Suggested fix

### INFO (N) — for awareness
- [Category] Description

### BACKPORT TASKS (N) — local improvements to propagate upstream
- [File] <source_path> — <brief description of local improvement>
  Local: <project>/.claude/<path>
  Target: streamtex-claude/<source_path>
  Diff summary: <what changed>
  Action: Copy relevant changes to source, then run `stx claude update --all`

### SYNC REMINDERS (N) — local copies out of date
- [File] <path> — run `stx claude update` to sync from source
```

## Patterns Checks (46-49)

The following checks verify the coherence of the **streamtex-patterns**
mechanism in a project. The mechanism itself is described in the
`pattern-library` skill — these checks only verify its integrity, they do
not redefine it.

**Check P1: Pattern catalog drift**

If `.claude/custom/streamtex-patterns/` exists, run
`stx patterns status` and check that no pattern has uncommitted local
modifications relative to `.patterns-meta.json` (Strat U2 detection).

- Severity: warning
- Failure example: "callout.md modified locally vs source SHA"
- Fix suggestion: "Run `stx patterns diff callout` to inspect; promote
  with `stx patterns promote` or revert with `stx patterns update --force`."

**Check P2: Pattern annotations consistency**

Scan all `bck_*.py` files in `blocks/` (and atomic sub-blocks) for
annotations like `# @pattern: <name>`. For each annotation:

- Verify `<name>` is in snake_case (not kebab-case).
- Verify `<name>` matches a pattern in
  `.claude/custom/streamtex-patterns/_pattern_library.md`.
- Verify the file ACTUALLY uses that pattern (light heuristic on
  imports / function calls / styles).

- Severity: error for mismatched names, warning for missing pattern usage
- Failure example: "bck_evidence.py declares `# @pattern: stat-hero`
  (kebab-case); should be `stat_hero`"
- Fix: provide a sed/migration command.

**Check P3: Pattern format A2 compliance**

If `.claude/custom/streamtex-patterns/` exists, run
`stx patterns validate --all` (or simulate via the spec).

- Severity: error
- Failure example: "callout.md missing required section `## Visual`"
- Fix: refer to SPEC.md (in streamtex-patterns repo) for the full A2
  rules.

**Check P4: Pattern naming conventions**

Verify that:

- Each pattern filename matches its frontmatter `name`.
- Each pattern filename is snake_case (regex `^[a-z][a-z0-9_]*\.md$`).
- No filename starts with `_` except `_pattern_library.md`.
- The `# @pattern:` annotations in blocks use snake_case
  (canonicalized from any historical kebab-case).

- Severity: error
- Fix: rename + sed migration.
