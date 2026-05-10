Regenerate the AUTO section of `_pattern_library.md` from pattern files.

Arguments: $ARGUMENTS (format: `[--container <path>]` or `--help`)

## Argument Parsing

Parse `$ARGUMENTS`:
- `--container <path>` — reindex only the given container (optional, default: all)
- `--help` → show the help section below and stop

## Workflow

### Step 1 — Locate containers

```bash
find . -type d -name 'streamtex-patterns' -not -path '*/.git/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*'
```

If `--container <path>` is set, restrict to that path. Refuse if it doesn't
exist or isn't named `streamtex-patterns/`.

### Step 2 — For each container, scan pattern files

List every `.md` at the root of the container that does not start with `_`.
For each, parse the YAML frontmatter and extract:
- `name`
- `description`
- `tags`
- `extrapolable`

If the frontmatter is missing or malformed, skip the file and log a warning
(don't fail the whole reindex).

### Step 3 — Build the table

Construct a markdown table:

```markdown
| Name | Description | Tags | Extrapolable |
|---|---|---|---|
| <name> | <description> | <tag1, tag2> | ✓ or ✗ |
```

Sort rows alphabetically by `name`.

### Step 4 — Update `_pattern_library.md`

Read the existing `_pattern_library.md`. Replace the content between
`<!-- BEGIN AUTO -->` and `<!-- END AUTO -->` with the new table,
preserving everything outside those markers.

If the markers are missing, prepend the auto section to the file (with the
markers) and warn the user that the file was malformed.

If the file doesn't exist, create it with the standard skeleton:

```markdown
# Pattern Library

<!-- BEGIN AUTO -->
<table>
<!-- END AUTO -->

## Application rules (manual)

- (add project-specific rules here)
```

### Step 5 — Report

Display a summary:
- Containers processed
- Patterns indexed (total)
- Skipped files (with reasons)
- Drift detected (entries removed because the file is gone, or files added)

## Help

```
/stx-pattern:reindex [--container <path>]

Regenerate the AUTO section of `_pattern_library.md` from pattern files.

Options:
  --container <path>   Reindex only the given container
  --help               Show this help

Run this after manually adding or removing pattern files. Automatically
triggered by /stx-pattern:new.
```
