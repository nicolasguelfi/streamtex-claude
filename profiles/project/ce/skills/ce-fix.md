# CE Fix

Skill for the FIX phase of the Compound Engineering cycle. Load the latest review report, apply automated corrections, verify each fix, and produce a traceability report.

## Workflow

### Phase 1: Load Review Report

1. Scan `docs/reviews/` for the most recent review report.
2. If no report is found, inform the user and suggest running `/stx-ce:review` first. Do not proceed.
3. Parse the report to extract all findings with their severity, block, and description.
4. Filter findings by the `--severity` threshold (default: CRITICAL). Include all findings at or above the threshold.
5. If `--target <block>` is set, further filter to only that block.
6. Classify each finding as **automatable** or **manual**:
   - Automatable: style issues, convention violations, spacing, CSS problems, missing attributes, section spacing inconsistencies
   - Manual: content rewrites, structural reorganization, pedagogical changes, factual corrections

### Phase 2: Apply Fixes

Process findings from most severe to least severe.

For each automatable finding:

1. Run `/stx-block:fix --target <block>` with the specific fix instruction from the finding.
2. For presentation projects, use `/stx-block:slide-fix` when appropriate.
3. For spacing findings, apply these specific fixes:
   - **Inconsistent spacing**: apply a uniform `SpacingConfig` via `set_spacing()` at book or profile level
   - **Unnecessary block-level overrides**: remove `set_block_spacing()` calls that duplicate the global/profile spacing; use `reset_block_spacing()` to clear them
   - **Double-spacing**: fix adjacent bottom+top margins by adjusting one side (prefer setting `bottom=0` on the preceding block or `top=0` on the following block)
   - **Horizontal margin mismatch**: adjust `set_section_horizontal()` or per-block left/right values to match the target profile
4. Run `/stx-block:audit --target <block>` to verify the fix resolved the finding.
4. Record the result:
   - **FIXED**: the finding is fully resolved (audit confirms)
   - **PARTIAL**: the finding is improved but not fully resolved
   - **FAILED**: the fix attempt did not resolve the finding or introduced a regression

### Phase 3: Global Verification

1. Run `/stx-block:audit --all` to perform a full re-audit.
2. Compare the number of findings before and after fixes.
3. Detect regressions: new findings that did not exist in the original review.
4. If regressions are found, attempt to fix them. If they persist, flag them clearly.

### Phase 4: Traceability Report

1. Update the review report in `docs/reviews/` by appending a "Fix Applied" section:

```markdown
## Fix applied on YYYY-MM-DD

| # | Severity | Block | Finding | Status |
|---|----------|-------|---------|--------|
| 1 | CRITICAL | bck_xxx | <description> | FIXED |
| 2 | MAJOR | bck_yyy | <description> | PARTIAL |
| 3 | MAJOR | bck_zzz | <description> | MANUAL |
...

### Summary
- Findings processed: <N>
- Fixed: <N>
- Partial: <N>
- Failed: <N>
- Manual (not attempted): <N>
- Regressions detected: <N>
```

2. Present the summary to the user:

| Severity | Total | Fixed | Partial | Failed | Manual |
|----------|-------|-------|---------|--------|--------|
| CRITICAL | ... | ... | ... | ... | ... |
| MAJOR | ... | ... | ... | ... | ... |
| MINOR | ... | ... | ... | ... | ... |

3. List remaining findings (manual + failed), grouped by severity.

### Phase 5: GATE

Present the results to the user and propose next steps:

1. **Re-review**: Run `/stx-ce:review` to validate that corrections meet quality standards.
2. **Continue**: Proceed to `/stx-ce:compound` to capitalize learnings.
3. **Fix more**: Run `/stx-ce:fix --severity MINOR` to lower the threshold and fix more findings.

The user must explicitly choose before proceeding.
