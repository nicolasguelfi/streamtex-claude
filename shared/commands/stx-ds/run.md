Manage StreamTeX design systems.

Arguments: $ARGUMENTS

## Pre-read

Read `shared/skills/reuse-architecture.md`.

## Sub-commands

```
stx ds list                                    # all DSs from active packs
stx ds show <name>                              # bundles + tokens
stx ds switch <name>                            # update [design_system].ref
stx ds new <name> [--to <pack>]                 # scaffold a DS class
stx ds validate [<name>]                        # DV001-DV006
```

## Workflow

1. Parse `$ARGUMENTS`.
2. Delegate to `uv run stx ds <sub> <args>`.
3. After `stx ds switch`, remind the user that components whose
   `bundles_required` are not covered by the new DS will surface BV001
   errors at install or runtime. Run `stx validate` to confirm.

## What a design system is

A Python class implementing `DesignSystemProtocol`. It exposes the
required bundles (colors, titles, callouts, body) as `Style` ClassVars.
Optional bundles (card_grid, stat_hero, comparison_table, takeaways,
citation, inline_emphasis, lists) extend coverage.
