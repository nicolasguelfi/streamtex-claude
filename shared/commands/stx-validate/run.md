Aggregate `stx validate` — run every reuse-architecture validation.

Arguments: $ARGUMENTS

## Pre-read

Read `shared/skills/reuse-architecture.md`.

## What it covers

```
stx validate            # default: stx.toml + packs + design system + components
stx validate --strict   # warnings become errors
```

Exit codes: `0` = OK, `1` = warnings, `2` = errors.

Run all of:

- `stx pack validate --all` (PV001-PV010, PR002-PR004)
- `stx component validate --all` (CV001-CV011)
- `stx ds validate` (DV001-DV006)
- `stx kit validate --all` (KV001-KV005)
- `validate_bundles_required` (BV001-BV002)
- `stx project validate .` (14 checks — base 1-10 + reuse 11-14)

## Workflow

1. Delegate to `uv run stx validate` (or `--strict` if requested).
2. Read the aggregated report.
3. Group findings by **family** (PV / CV / DV / KV / BV / PR) and explain
   each error code by name. Mention which file the issue points at.
