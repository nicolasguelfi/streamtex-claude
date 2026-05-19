# /stx-pe:specialize — Fork an upstream pack with domain extensions

Arguments: $ARGUMENTS

## Options

- `<upstream-ref>` (mandatory, positional 1) — Upstream pack ref (`git:url@rev`, `pypi:name@spec`).
- `<projects>` (mandatory, positional 2+) — Consumer project paths.
- `--fork-name <name>` — Name of the fork pack (default : `<upstream-name>-<workspace>`).
- `--fork-target-path <path>` — Where to write the fork (default : `../<fork-name>/`).
- `--pr-upstream <repo>` — At Step 7, propose a PR upstream for mature components.
- `--dialog <minimal|standard|verbose>` — Override `dialog_level`.
- `--help` — Show stx-pe cheatsheet.

## Description

Forces the **specialize** sub-mode of `/stx-pe:go` : take an existing upstream pack that almost fits but lacks domain-specific patterns, and produce a fork-pack that EXTENDS it without overriding upstream components.

Use specialize when :
- You have an upstream pack as a starting point (e.g. `streamtex-design`).
- Your N projects share patterns NOT covered by upstream.
- You want to preserve upstream as a dependency (not vendoring it).

The cycle clones the upstream, rewrites `pyproject.toml` / `_pack_manifest.toml` with the new name + upstream as dep, then runs Steps 1-6. Mining and design are **dedup-filtered** against upstream — clusters already covered upstream are rejected with reason "already covered upstream".

## Examples

- `/stx-pe:specialize git:github.com/streamtex/streamtex-design@v0.4 projects/manual-a projects/manual-b`
- `/stx-pe:specialize pypi:streamtex-design@^0.4 --fork-name design-edu projects/*`
- `/stx-pe:specialize ../streamtex-design --pr-upstream streamtex/streamtex-design projects/*`

## Required Readings

Before executing, read :
1. `.claude/pack-engineering/skills/pe-specialize.md` — Specialize workflow
2. `.claude/pack-engineering/skills/pe-go.md` — Step-by-step sequencer
3. `.claude/pack-engineering/agents/pack-orchestrator.md`

## Workflow

Invoke the `pack-orchestrator` with the verb forced to `specialize`. The orchestrator surfaces the upstream-fork-confirmation QCM, clones the upstream, then chains Steps 1-6 with gates. At Step 7 (opt-in), the `--pr-upstream` QCM is surfaced if mature components exist.
