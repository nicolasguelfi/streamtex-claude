Audit the StreamTeX ecosystem for cross-component coherence issues.

Arguments: $ARGUMENTS (optional scope — default: all)

## Steps

1. **Locate workspace root**: Find the nearest parent directory containing `stx.toml`.
   The workspace root contains: `streamtex/`, `streamtex-docs/`, `streamtex-claude/`, `projects/`.

2. **Load rules**: Read `.claude/developer/skills/coherence-checks.md`.

3. **Determine scope** from arguments:
   - `all` (default) — Run ALL checks (standard + ai + cli = checks 1-45)
   - `standard` — Checks 1-28 (original ecosystem coherence checks)
   - `ai` — Checks 29-41 (AI-generated code quality: ghost API, dead code, explanation drift, cross-block contradictions, unused exports, version claims, test quality, silent failures, naming coherence, secret leaks, hardcoded URLs)
   - `cli` — Checks 42-45 (CLI coherence: help↔code, stx-guide↔CLI, deploy scripts↔Docker, optional deps↔imports)
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
