# /stx-pe:go — Run a Pack Engineering cycle (auto-detect sub-mode)

Arguments: $ARGUMENTS

## Options

- `<projects>` — Optional positional list of consumer projects.
- `--mode <bootstrap|specialize|refine|audit|adopt|publish>` — Force a sub-mode (skips auto-detection).
- `--upstream <ref>` — Required for specialize sub-mode.
- `--pack <ref>` — Force the target pack for audit/adopt/publish sub-modes.
- `--no-publish` — Forbid Step 7 PUBLISH even if a mature pack is detected.
- `--dialog <minimal|standard|verbose>` — Override the producer profile's `dialog_level`.
- `--help` — Show stx-pe cheatsheet.

## Description

Executes a complete Pack Engineering cycle through 7 steps (DISCOVERY → DESIGN → IMPLEMENT → ADOPT → RETROFIT → AUDIT → PUBLISH) with 4 fundamental gates (G1, G2, G3, G4).

Sub-mode is auto-detected from the prompt + workspace state :
- pack-master-plan absent + N projects + no upstream → **bootstrap**
- pack-master-plan absent + N projects + `--upstream` → **specialize**
- pack-master-plan present + new blocks since last cycle → **refine**
- prompt matches "audit / unused / duplicates" → **audit**
- prompt matches "adopt / install / wire" → **adopt-only**
- prompt matches "publish / release / version" → **publish-only**

The sole user-facing agent is `pack-orchestrator` — it delegates each phase to a specialist (`pack-miner`, `pack-designer`, `pack-implementer`, `pack-retrofitter`, `pack-auditor`, `pack-publisher`) but never exposes them.

## Gates (mandatory user validation)

| Gate | When | Skippable ? |
|---|---|---|
| **G1** | post-DISCOVERY | Never |
| **G2** | post-DESIGN | Skippable in `dialog_level: minimal` |
| **G3** | pre-RETROFIT | Never |
| **G4** | post-RETROFIT smoke fail | Conditional (only if smoke render failures) |

## Examples

- `/stx-pe:go projects/manual-a projects/manual-b` — Bootstrap from 2 projects
- `/stx-pe:go --mode specialize --upstream git:streamtex-design@v0.4 projects/*` — Fork upstream
- `/stx-pe:go` (inside a project with active pack) — Refine
- `/stx-pe:go --mode audit --pack ../streamtex-design` — Standalone audit
- `/stx-pe:go --mode publish ../streamtex-design` — Release a mature pack

## Required Readings

Before executing, read :
1. `.claude/pack-engineering/skills/pe-go.md` — Full workflow
2. `.claude/pack-engineering/agents/pack-orchestrator.md` — The user-facing agent

## Workflow

Invoke the `pack-orchestrator` agent with the parsed `$ARGUMENTS`. The orchestrator runs Step 0 (state detection + sub-mode classification), then chains Steps 1-7 per `pe-go.md`, surfacing gates G1-G4 to the user as configured.
