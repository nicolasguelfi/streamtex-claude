Check that pattern files comply with the StreamTeX patterns spec.

Arguments: $ARGUMENTS (format: `[<name>|--all]` or `--help`)

## Argument Parsing

Parse `$ARGUMENTS`:
- `<name>` — validate a single pattern by name
- `--all` — validate every pattern in the project
- (no argument) → validate every pattern in the project (same as `--all`)
- `--help` → show the help section below and stop

## Workflow

### Step 1 — Resolve target files

```bash
find . -type d -name 'streamtex-patterns' -not -path '*/.git/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*'
```

- `--all` (or no argument): every `.md` at the root of every container, except those starting with `_`.
- `<name>`: search for `<name>.md` in every container. Refuse if found in two containers.

### Step 2 — For each pattern file, run checks

#### Frontmatter

- [ ] YAML block present at the top, delimited by `---`
- [ ] Required fields: `name`, `type`, `description`, `extrapolable`, `since`
- [ ] `type` equals `pattern`
- [ ] `name` matches the filename (without `.md`)
- [ ] `name` is `snake_case` (lowercase, alphanumeric + underscores)
- [ ] `description` is a string with length < 100
- [ ] `tags` (if present) is a list of strings
- [ ] `extrapolable` is a boolean
- [ ] `since` is a date `YYYY-MM-DD`

#### Required sections

- [ ] `## Visual`
- [ ] `## Structure`
- [ ] `## Styling rules`
- [ ] `## Code skeleton` (with at least one fenced `python` code block)
- [ ] `## When to use`
- [ ] `## When NOT to use`

#### Conditional sections

- [ ] If `extrapolable: true`, the `## Extrapolation rules` section exists
      and contains the three sub-sections: `### INVARIANTS`, `### PARAMS`,
      `### INTERDITS`

#### Code skeleton

- [ ] The Python code block parses as valid Python (use `ast.parse`).
- [ ] References to undefined imports are tolerated (the snippet is a
      starting point, not a runnable module).

#### References to other patterns (advisory, not blocking)

- For each `snake_case` token in the file that matches the name of a
  pattern referenced in `_pattern_library.md`, no action.
- For each `snake_case` token that looks like a pattern name but doesn't
  exist in the catalog, emit an advisory note.

### Step 3 — Report

For each file, output:
- ✅ if all checks pass
- ❌ + list of failures otherwise
- ⚠️ + list of advisories (broken references, missing optional sections)

Summary:
- Total files checked
- Files passing
- Files failing
- Files with advisories

If invoked with `--all` and any file fails, exit with a non-zero indicator
in the summary so it can be wired into a pre-commit hook later.

## Help

```
/stx-pattern:validate [<name>|--all]

Check that pattern files comply with the StreamTeX patterns spec.

Arguments:
  <name>      Validate a single pattern
  --all       Validate every pattern (default if no argument)
  --help      Show this help

Checks: frontmatter, required sections, code skeleton parses, references.
Run after /stx-pattern:new or before committing pattern changes.
```
