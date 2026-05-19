Create a new StreamTeX project (alias of `stx project new`).

Arguments: $ARGUMENTS

## Pre-read

Read `shared/skills/reuse-architecture.md` and PLAN §7.1.

## Synopsis

```
stx project new <name>                                # minimal scaffold
stx project new <name> --kit <pack>:<kit_name>        # kit-based scaffold
stx project new <name> --pack <ref>                   # extra pack(s)
stx project new <name> --pack-name <pack>             # rename mypack
stx project new <name> --no-mypack                    # consumer-only project
stx project new <name> --collection                   # collection hub
stx project new <name> --no-git | --no-sync | --no-claude
```

## Workflow

1. Parse `$ARGUMENTS`.
2. Delegate to `uv run stx project new <args>`.
3. After completion, the project has:
   - `stx.toml` (PLAN §6.1)
   - `mypack/` (or `<pack_name>/`) with `_pack_manifest.toml` and 4
     subdirectories — installed in editable mode after `uv sync`.
   - Optional kit: design system injected in `custom/styles.py`.
4. Suggest the user run `stx run` once the project is created.
