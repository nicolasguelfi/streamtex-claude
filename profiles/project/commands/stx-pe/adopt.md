# /stx-pe:adopt — Install a pack in N projects without extraction

Arguments: $ARGUMENTS

## Options

- `<pack>` (mandatory, positional 1) — Pack ref to adopt (git, pypi, or local path).
- `<projects>` (mandatory, positional 2+) — Consumer project paths.
- `--kit <name>` — Kit to install (default : pack's `default` kit ; QCM if multiple).
- `--retrofit` — After adoption, run a refine cycle to rewrite existing blocks.
- `--help` — Show stx-pe cheatsheet.

## Description

Forces the **adopt-only** sub-mode of `/stx-pe:go` : install an existing pack into N consumer projects without running extraction, design, or retrofit. Pure "wire it in" path.

Use adopt-only when :
- The pack already exists (local or remote, you already trust it).
- Consumer projects do not yet declare it in `stx.toml`.
- You will write new blocks against the pack from scratch (no automatic rewrite of existing blocks).

If existing blocks should be rewritten to use the new pack, use `--retrofit` (escalates to refine after adoption) or run `/stx-pe:refine` after.

## Examples

- `/stx-pe:adopt ../streamtex-pack-design projects/manual-a projects/manual-b`
- `/stx-pe:adopt pypi:streamtex-pack-design@^0.2 --kit recommended projects/*`
- `/stx-pe:adopt git:nicolasguelfi/streamtex-packs@pack-design-v0.2.4#subdirectory=streamtex-pack-design --retrofit projects/manual-a`

## Required Readings

Before executing, read :
1. `.claude/pack-engineering/skills/pe-adopt.md` — Adopt-only workflow
2. `.claude/pack-engineering/agents/pack-orchestrator.md`

## Workflow

Invoke the `pack-orchestrator` with the verb forced to `adopt`. The orchestrator validates the pack ref, resolves the kit (QCM if needed), confirms the project list (QCM), then runs Step 4 only (`stx pack add` + `stx kit install` looped over projects). If `--retrofit` was passed, hands off to refine starting at Step 5.
