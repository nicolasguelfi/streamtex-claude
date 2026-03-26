# /stx-ce:status — Show CE cycle status for current project

Arguments: $ARGUMENTS

## Options

- `--verbose` — Show detailed artifact contents and item-level breakdown
- `--help` — Show stx-ce cheatsheet

## Description

Displays a dashboard of the CE cycle state for the current project. Scans all CE phase artifacts in `docs/` and reports which phases are done, in progress, or pending. Includes production progress breakdown and review findings summary when applicable.

No arguments required — operates on the current project directory.

## Examples

- `/stx-ce:status` — Show cycle status for current project
- `/stx-ce:status --verbose` — Show detailed status with item-level breakdown

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-status.md` — Full workflow

## Workflow

Execute the `ce-status` skill. Display the dashboard to the user.
