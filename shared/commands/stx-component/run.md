Manage StreamTeX components (reuse architecture).

Arguments: $ARGUMENTS

## Pre-read

Read `shared/skills/reuse-architecture.md` before executing.

## Sub-commands

```
stx component list [--granularity <g>] [--pack <p>]
stx component show <name>                              # docstring + signature
stx component new <name>                               # scaffold (kwargs + docstring)
stx component validate [<name> | --all]                # CV001-CV011
stx component find <description>                       # fuzzy search by tag/description
stx component promote <name> [--to=<pack>] [--message] [--no-commit]
```

## Workflow

1. Parse `$ARGUMENTS` for sub-command + options.
2. Delegate to `uv run stx component <sub> <args>`.
3. For `promote` with no `--to`: present an interactive QCM listing every
   pack declared in `stx.toml` — the new architecture's 4-branch routing
   (Q12) dispatches automatically based on the destination's type:
   - primary local: copy only.
   - secondary local with .git: copy + commit prompt.
   - git remote: clone → branch → push → `gh pr create`.
   - pypi: refused (PR001).
4. For `new`: ensure the generated docstring contains the 7 sections from
   PLAN §4.1.1 (Visual / Structure / Styling rules / Extrapolation rules
   with INVARIANTS+PARAMS+INTERDITS / When to use / When NOT to use /
   Design system bundles required) and a valid `__component_meta__`.

## Diff between two versions

Use **git diff** directly (D18 — no dedicated `stx component diff`):

```bash
git diff <sha1> <sha2> -- <pack>/components/<name>.py
diff <(stx component show A) <(cd ../other-pack && stx component show A)
```
