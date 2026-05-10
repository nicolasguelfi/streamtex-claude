List every StreamTeX design pattern available in the current project.

Arguments: $ARGUMENTS (format: `[--tag <tag>]` or `--help`)

## Argument Parsing

Parse `$ARGUMENTS`:
- `--tag <tag>` — filter by frontmatter tag (optional)
- `--help` → show the help section below and stop

## Workflow

### Step 1 — Locate pattern containers

Find every folder named `streamtex-patterns/` in the current project:

```bash
find . -type d -name 'streamtex-patterns' -not -path '*/.git/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*'
```

The conventional default is `.claude/custom/streamtex-patterns/`. Other
locations (e.g. `docs/streamtex-patterns/`) are also accepted and merged.

If no container is found, tell the user how to create one:

> No `streamtex-patterns/` folder found.
> Create one at `.claude/custom/streamtex-patterns/` and add patterns with
> `/stx-pattern:new`.

### Step 2 — Read each container's index

For each container, read `_pattern_library.md` and extract the AUTO table.

### Step 3 — Display the merged catalog

Display a single combined table across all containers. If `--tag` is set,
filter rows whose `Tags` column contains the given tag (case-insensitive).

Output format:

```
## Pattern catalog (<N> patterns from <M> container(s))

| Name | Description | Tags | Extrapolable | Source |
|---|---|---|---|---|
| grid_boston | 2-row grid, yellow header / green body | grid, comparison | ✓ | .claude/custom/... |
| ...
```

If no patterns are found, display a friendly empty-state message and suggest
`/stx-pattern:new` to create the first one.

### Step 4 — Detect drift

If the AUTO section of any `_pattern_library.md` looks out of sync with the
files actually present (e.g. a `.md` file with no entry), warn the user and
suggest `/stx-pattern:reindex`.

## Help

```
/stx-pattern:list [--tag <tag>]

List every StreamTeX design pattern available in the current project.

Options:
  --tag <tag>    Filter by tag (case-insensitive)
  --help         Show this help

The command scans every folder named `streamtex-patterns/` in the project
(default: .claude/custom/streamtex-patterns/) and merges their indexes.
```
