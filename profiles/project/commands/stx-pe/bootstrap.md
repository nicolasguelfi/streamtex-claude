# /stx-pe:bootstrap — Extract a new shared pack from N projects

Arguments: $ARGUMENTS

## Options

- `<projects>` (mandatory) — Positional list of consumer project paths.
- `--pack-name <name>` — Name of the new pack (default : derived from workspace).
- `--target-path <path>` — Where to write the new pack (default : `../<pack-name>/`).
- `--active-ds <ref>` — Design system reference (default : minimal scaffold).
- `--min-occurrences <N>` — Minimum repetition count (default : 2).
- `--min-projects <N>` — Minimum project coverage (default : 2).
- `--dialog <minimal|standard|verbose>` — Override `dialog_level`.
- `--help` — Show stx-pe cheatsheet.

## Description

Forces the **bootstrap** sub-mode of `/stx-pe:go` : analyze N existing StreamTeX projects, extract recurring visual idioms, and produce a brand-new shared pack containing them. All consumer projects are then updated to declare the new pack (`stx pack add`), the recommended kit is installed, and existing blocks are rewritten to use the pack's components.

Use bootstrap when :
- You have ≥ 2 existing projects with overlapping visual patterns.
- There is no upstream pack to fork.
- You want to start a shared library from scratch.

The cycle runs through Steps 1-6 (DISCOVERY → AUDIT). Step 7 (PUBLISH) is offered as opt-in at the end.

## Examples

- `/stx-pe:bootstrap projects/manual-a projects/manual-b projects/manual-c`
- `/stx-pe:bootstrap --pack-name design-corporate projects/*`
- `/stx-pe:bootstrap --target-path ../shared-design --min-projects 3 projects/*`

## Required Readings

Before executing, read :
1. `.claude/pack-engineering/skills/pe-bootstrap.md` — Bootstrap workflow
2. `.claude/pack-engineering/skills/pe-go.md` — Step-by-step sequencer
3. `.claude/pack-engineering/agents/pack-orchestrator.md`

## Workflow

Invoke the `pack-orchestrator` with the verb forced to `bootstrap`. The orchestrator surfaces the parameter-confirmation QCM (per `pe-bootstrap.md` Step 1), then chains Steps 1-6 with gates G1, G2, G3 (and G4 conditional).
