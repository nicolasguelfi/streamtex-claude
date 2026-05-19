# /stx-pe:refine — Capture emergent patterns into the active pack

Arguments: $ARGUMENTS

## Options

- `--target-pack <ref>` — Which pack to enrich (default : primary local pack from `stx.toml`).
- `--since <date|tag>` — Cutoff for new-blocks scan (default : date of last `mining_validated` in pack-master-plan).
- `--full-scan` — Ignore `--since` and analyze all blocks in cwd.
- `--no-retrofit` — Skip Step 5 RETROFIT (just add components to the pack).
- `--dialog <minimal|standard|verbose>` — Override `dialog_level`.
- `--help` — Show stx-pe cheatsheet.

## Description

Forces the **refine** sub-mode of `/stx-pe:go` : the current project's `stx.toml` already declares a pack. New blocks have been authored since the last PE cycle and contain idioms not yet captured. Refine extracts those NEW patterns and adds them to the existing pack — without re-doing the bootstrap analysis.

Use refine when :
- A pack is already active in the current project.
- Production has continued ; new visual idioms have emerged.
- You want incremental enrichment, not a full re-analysis.

Refine operates on **a single project** (the cwd's). The cycle dedup-filters against the active pack itself — only NEW clusters survive. After implementation, the current project's blocks are rewritten to use the new components.

No Step 6 AUDIT by default (refine is incremental — full audit is a separate cycle).

## Examples

- `/stx-pe:refine` — Refine the primary pack with patterns since the last cycle
- `/stx-pe:refine --since 2026-04-01` — Custom cutoff date
- `/stx-pe:refine --full-scan --no-retrofit` — Full scan, but only add to pack

## Required Readings

Before executing, read :
1. `.claude/pack-engineering/skills/pe-refine.md` — Refine workflow
2. `.claude/pack-engineering/skills/pe-go.md` — Step-by-step sequencer
3. `.claude/pack-engineering/agents/pack-orchestrator.md`

## Workflow

Invoke the `pack-orchestrator` with the verb forced to `refine`. The orchestrator detects the active pack from `stx.toml`, applies the `--since` cutoff, then chains Steps 1, 2, 3, 5 (RETROFIT current project only). Gates G1, G2, G3 apply ; G4 conditional.
