Manage StreamTeX packs (reuse architecture — PLAN §6.2 / 0.7.x).

Arguments: $ARGUMENTS

## Pre-read

Before executing, read the central skill `shared/skills/reuse-architecture.md`
(single source of truth for vocabulary, discovery, and `stx.toml` schema).

## Sub-commands

```
stx pack add <ref> [--rev <tag>] [--dev <path-or-url>]   # add a pack
stx pack remove <name>                                    # remove a pack
stx pack list [--trace]                                   # discovery
stx pack sync                                             # install packs from stx.toml
stx pack info <name>                                      # detail
stx pack validate <name>                                  # PV001-PV010
stx pack new <name>                                       # scaffold a new local pack
stx pack set-primary <name>                               # change primary local pack
```

## Workflow

1. Parse `$ARGUMENTS` to extract the sub-command and its options.
2. If the user is asking for help (`--help` or unknown sub-command), print
   the synopsis above.
3. Otherwise, call the corresponding CLI invocation directly:
   `uv run stx pack <sub> <args>` from the project root.
4. Read the JSON / text output and explain it in plain English to the user,
   especially error codes (`PR001-PR004`, `PV001-PV010`).

## Notes

- `--dev` accepts a local path OR a git URL (auto-clone into
  `~/.local/share/stx/dev-packs/`). Implies `editable=true` in stx.toml.
- The 5 lifecycle states (Nominal / Drift install / Indirect / Manifest
  cassé / Collision) are reported by `stx pack list --trace`.
- Promotion to a `pypi`-type pack is refused with code PR001 — use a
  local or git pack instead.
