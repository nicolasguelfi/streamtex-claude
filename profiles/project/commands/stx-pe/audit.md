# /stx-pe:audit — Standalone health audit of an existing pack

Arguments: $ARGUMENTS

## Options

- `<pack>` (mandatory, positional 1) — Pack ref or local path.
- `<projects>` (optional, positional 2+) — Consumer projects to widen the scope. Auto-detected if omitted.
- `--minimal` — Skip the detailed contract-drift section.
- `--no-followup` — Don't propose a refine cycle for HIGH issues at the end.
- `--help` — Show stx-pe cheatsheet.

## Description

Forces the **audit-only** sub-mode of `/stx-pe:go` : run a read-only health audit of an existing pack. The audit checks :
- **Unused components** (declared in pack but not used by any consumer).
- **Duplicates** (components with overlapping signatures or outputs).
- **Bundle gaps** (DS bundles required by contracts but not declared).
- **Naming conflicts** (with upstream packs in the consumer chain).
- **Contract-implementation drift** (docstring claims vs actual behavior).
- **Test coverage** (component tests in the pack repo).

The audit is **read-only** — it produces a report at `docs/pack-engineering/<ts>/audit-report.md` but modifies no source files. At the end, a follow-up QCM proposes a refine cycle if HIGH-severity issues are found.

This sub-mode is also auto-run by bootstrap and specialize at Step 6 ; the standalone command is for invoking the audit outside an extraction cycle.

## Examples

- `/stx-pe:audit ../streamtex-pack-design` — Audit local pack, auto-detect consumers
- `/stx-pe:audit git:streamtex-pack-design@pack-design-v0.2.4 projects/*` — Audit remote pack against projects
- `/stx-pe:audit --minimal ../my-pack` — Quick audit, no drift section
- `/stx-pe:audit --no-followup ../my-pack` — Audit report only, no QCM at the end

## Required Readings

Before executing, read :
1. `.claude/pack-engineering/skills/pe-audit.md` — Audit workflow
2. `.claude/pack-engineering/agents/pack-orchestrator.md`
3. `.claude/pack-engineering/agents/pack-auditor.md` — The specialist (loaded by orchestrator)

## Workflow

Invoke the `pack-orchestrator` with the verb forced to `audit`. The orchestrator resolves the pack location, detects consumer projects (with QCM if ambiguous), then runs Step 6 only. No gates (audit is read-only). At the end, the recommendation QCM is surfaced unless `--no-followup`.
