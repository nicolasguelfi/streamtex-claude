Create a new StreamTeX design pattern interactively.

Arguments: $ARGUMENTS (format: `[<description>]` or `--from <bck_*.py>` or `--help`)

## Argument Parsing

Parse `$ARGUMENTS`:
- `--from <path>` — extract pattern from an existing block file (recommended)
- Free text → treated as a textual description of the pattern
- `--help` → show the help section below and stop

## Workflow

### Step 1 — Source

Determine the source of inspiration:

- If `--from <path>` is given, read the block file in full.
- Otherwise, ask the user: *"Which existing block do you want to inspire
  this pattern from?"* and accept either a `bck_*.py` path or a textual
  description.

### Step 2 — Propose a name

Based on the source, propose a `snake_case` slug. The name should be:
- Short (1–3 words)
- Memorable (evocative of the visual rendering)
- Free of project-specific tokens (avoid `ai4se6d_`, `gensem_`, etc.)

Show 3 candidate names and ask the user to pick or override.

### Step 3 — Extract the pattern content

Read the source block (or use the description) and draft the pattern file.
Fill each required section:

- **Visual**: short description or ASCII mockup of the rendering
- **Structure**: bullet list of the logical structure
- **Styling rules**: extract colors, fonts, paddings, gaps from the source
- **Code skeleton**: parameterize the source code (replace specific values
  with parameters, keep the structure)
- **Extrapolation rules**: identify INVARIANTS (what defines the identity)
  vs PARAMS (what can vary) vs INTERDITS (what would change the identity)
- **When to use** / **When NOT to use**: based on the source context

For each draft section, show it to the user and ask for confirmation or
adjustment before proceeding.

### Step 4 — Locate or create the container

Find an existing `streamtex-patterns/` folder. If none exists, create
`.claude/custom/streamtex-patterns/` and create an empty
`_pattern_library.md` with the auto markers:

```markdown
# Pattern Library

<!-- BEGIN AUTO -->
<!-- END AUTO -->

## Application rules (manual)

- (add project-specific rules here)
```

### Step 5 — Write the pattern file

Write the pattern file as `<container>/<name>.md`. Refuse if it already
exists (suggest a different name or `/stx-pattern:show <name>` to inspect
the existing one).

### Step 6 — Reindex

Trigger `/stx-pattern:reindex` to update the AUTO section of
`_pattern_library.md`.

### Step 7 — Validate

Trigger `/stx-pattern:validate <name>` and report the result.

### Step 8 — Confirm to the user

Show:
- Path of the created file
- Summary of the pattern
- Suggestion: *"Try it on a new block: `/stx-block:new ... using <name>`"*

## Help

```
/stx-pattern:new [<description>]
/stx-pattern:new --from <path/to/bck_*.py>

Create a new StreamTeX design pattern.

Options:
  --from <path>    Extract pattern from an existing block file
  --help           Show this help

The command extracts INVARIANTS, PARAMS and INTERDITS from a reference,
proposes a name, and writes the file in the project's
streamtex-patterns/ folder.
```
