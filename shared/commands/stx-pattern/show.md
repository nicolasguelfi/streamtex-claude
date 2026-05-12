Display the full content of a StreamTeX design pattern.

Arguments: $ARGUMENTS (format: `<name>` or `--help`)

## Argument Parsing

Parse `$ARGUMENTS`:
- First token = **name** (snake_case slug of the pattern)
- `--help` → show the help section below and stop

If name is missing, ask the user which pattern to show, and offer to run
`/stx-pattern:list` first.

## Workflow

### Step 1 — Locate the pattern file

Find every `streamtex-patterns/` folder in the project. Search for
`<name>.md` at the root of each container.

```bash
find . -type d -name 'streamtex-patterns' -not -path '*/.git/*' -not -path '*/__pycache__/*' -not -path '*/.venv/*'
```

If multiple containers contain the same `<name>.md`, refuse to show and ask
the user to resolve the collision (rename one of them).

If no file is found, list the closest matches by name (Levenshtein-style)
and suggest `/stx-pattern:list`.

### Step 2 — Display the file

Read the full file and display its contents to the user, preserving the
markdown structure. Do not re-format.

### Step 3 — Optional: lint feedback

After displaying, check for spec violations:
- Frontmatter missing or malformed
- `name` mismatched with filename
- Required sections missing (Visual, Structure, Styling rules, Code
  skeleton, When to use, When NOT to use)
- If `extrapolable: true`, no Extrapolation rules section

If any violation is found, append a brief note suggesting
`/stx-pattern:validate <name>` for full details.

## Help

```
/stx-pattern:show <name>

Display the full content of a pattern.

Arguments:
  name           snake_case slug of the pattern
  --help         Show this help
```
