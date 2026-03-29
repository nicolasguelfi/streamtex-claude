# /stx-ce:fix — Fix findings from the latest review

Arguments: $ARGUMENTS

## Options

- `--target <block>` — Fix a single block instead of all findings
- `--severity <level>` — Minimum severity threshold: CRITICAL (default), MAJOR, MINOR, SUGGESTION
- `--help` — Show stx-ce cheatsheet

## Description

Loads the latest review report from `docs/reviews/` and fixes all automatable findings above the severity threshold. Each fix is verified by a targeted audit. Produces a traceability report.

The REVIEW -> FIX cycle can be iterated: after FIX, run `/stx-ce:review` again to validate corrections.

## Examples

- `/stx-ce:fix` — Fix all CRITICAL findings from the latest review
- `/stx-ce:fix --severity MAJOR` — Fix CRITICAL and MAJOR findings
- `/stx-ce:fix --target bck_intro` — Fix only one block
- `/stx-ce:fix --severity MINOR --target bck_style` — Fix MINOR+ in one block

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-fix.md` — Full workflow
2. `docs/reviews/` — Latest review report
- If project has an active guideline, load it to inform guideline-specific fixes
- Guideline violations from the review report are included in the fix queue

## Workflow

Execute the `ce-fix` skill. GATE: Fix results presented to user — propose re-review or continue to compound.

The traceability report must include:

| Guideline violations | <N> | FIXED / PARTIAL / MANUAL |
