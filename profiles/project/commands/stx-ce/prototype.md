# /stx-ce:prototype — Validate styles and patterns by example

Arguments: $ARGUMENTS

## Description

Phase between PLAN and PRODUCE. Produces one (or a small set of) pilot block(s) for the current increment scope, validates the visual decisions with the user, and captures emergent patterns into the local catalog. The pilot block(s) are kept; PRODUCE then completes the increment applying the validated styles and patterns.

The skill auto-detects whether PROTOTYPE is needed for the current iteration based on the master plan state (first iteration, new visual territory, or user request). It is skipped when the increment continues an already-validated style territory and all patterns are already mapped.

## Examples

- `/stx-ce:prototype` — Run PROTOTYPE for the current iteration's scope.

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-prototype.md` — Full workflow
2. `.claude/ce/skills/ce-conventions.md` — QCM format, paths, snapshot, patterns levels
3. `docs/master-plan.yaml` and `docs/master-plan.md` — current scope and patterns mapping
4. The most recent plan in `docs/plans/` — increment objectives
5. `stx component list` — available components from active packs

## Workflow

Execute the `ce-prototype` skill. GATE: the user must validate the pilot before PRODUCE proceeds with the remaining blocks.

## Options

- `--help` — Show stx-ce cheatsheet

(Most behavior is auto-detected by the orchestrator and confirmed via QCM. Flags are reserved for power users.)
