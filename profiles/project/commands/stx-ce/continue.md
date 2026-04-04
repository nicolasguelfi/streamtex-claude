# /stx-ce:continue — Resume work with context briefing and proposals

Arguments: $ARGUMENTS

## Options

- `--verbose` — Show detailed drift analysis and full artifact contents
- `--help` — Show stx-ce cheatsheet

## Description

Inspects the current project state after a session break, detects drift (source changes, manual edits, stale artifacts), and proposes prioritized next steps. The user can select a proposal or describe their own task.

This command is designed for **session resumption** — when the user returns after hours, days, or weeks and needs to understand where the project stands and what to do next.

**Output structure**:
1. **Briefing**: Project name, last CE activity date, current plan version, block count, production progress
2. **Drift detection**: Source changes, manual block edits, plan drift, stale artifacts, unresolved findings
3. **Proposals**: Prioritized list of recommended actions with executable commands
4. **Interactive dispatch**: User selects a proposal or describes a custom task

## Examples

- `/stx-ce:continue` — Resume with briefing and proposals
- `/stx-ce:continue --verbose` — Detailed drift analysis

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-continue.md` — Full workflow

## Workflow

Execute the `ce-continue` skill. Display briefing, detect drift, propose actions, dispatch user choice.
