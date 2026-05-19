Manage StreamTeX kits.

Arguments: $ARGUMENTS

## Pre-read

Read `shared/skills/reuse-architecture.md`.

## Sub-commands

```
stx kit list                                    # kits available from active packs
stx kit show <name>                              # composition (DS + components + template)
stx kit install <pack>:<kit_name>                # apply a kit to the current project
stx kit new <name> [--to <pack>]                 # scaffold a new kit manifest
stx kit validate [<name>]                        # KV001-KV005
```

## Workflow

1. Parse `$ARGUMENTS`.
2. Delegate to `uv run stx kit <sub> <args>`.
3. After `stx kit install`, the design system referenced by the kit is
   injected into `custom/styles.py` and `[kit] ref = …` is set in stx.toml.

## What a kit is

A TOML manifest gluing **1 design system** + **a curated component list**
(+ optionally a CLI template + samples). Provided by a pack so a fresh
project can pick a coherent starter (e.g. `slides-modern-dark`,
`project-default`, `manual-default`).
