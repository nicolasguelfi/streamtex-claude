# /stx-ce:pause — Save session checkpoint before pausing

Arguments: $ARGUMENTS

## Options

- `--message "<text>"` — Add context annotation to the checkpoint
- `--help` — Show stx-ce cheatsheet

## Description

Creates a checkpoint file (`docs/ce-checkpoint.md`) that captures the current session state: in-progress work items, decisions made, pending issues, and context for the next session. This enables effective resumption via `/stx-ce:continue`.

Use this command **before ending a work session** when work is in an intermediate state (partial production, ongoing fixes, ad-hoc tasks in flight). The checkpoint preserves the conversational context that would otherwise be lost between sessions.

**Output structure**:
1. **State inspection**: scans artifacts, blocks, git status
2. **In-progress detection**: identifies partial work, uncommitted changes
3. **Context capture**: extracts decisions and context from the session (with user confirmation)
4. **Checkpoint write**: saves `docs/ce-checkpoint.md`

## Examples

- `/stx-ce:pause` — Capture session state interactively
- `/stx-ce:pause --message "Focus was on LLM section, blocks 6-12. Glossary added out of plan."` — Checkpoint with explicit context

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-pause.md` — Full workflow

## Workflow

Execute the `ce-pause` skill. Inspect state, detect in-progress work, capture context with user confirmation, write checkpoint file.
