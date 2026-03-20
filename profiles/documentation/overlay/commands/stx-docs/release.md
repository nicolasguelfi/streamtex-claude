Prepare a documentation release: bump version, update changelog, and commit.

Arguments: $ARGUMENTS (optional: "patch", "minor", or "major" — defaults to "patch")

## Workflow

### Step 1 — Determine the bump type

Parse `$ARGUMENTS` for the bump type. Default to `patch` if not specified.

### Step 2 — Read current state

1. Read `pyproject.toml` to get the current version (field `project.version`).
2. Read `CHANGELOG.md` to understand the existing entries.
3. Run `git log --oneline $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD` to get commits since the last tag (or all commits if no tag exists).

### Step 3 — Compute the new version

Apply semantic versioning bump to the current version:
- `patch`: 0.4.0 -> 0.4.1
- `minor`: 0.4.0 -> 0.5.0
- `major`: 0.4.0 -> 1.0.0

Display: `Current: X.Y.Z -> New: A.B.C (bump type)`

### Step 4 — Generate changelog entry

From the git log, draft a changelog entry following [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
## [A.B.C] — YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...
```

Rules:
- Use **em-dash with spaces** (`—`) as separator, not a hyphen.
- Use bold lead-in phrases: `- **Feature name**: explanation`.
- Group by Added/Changed/Fixed/Removed — omit empty sections.
- Summarize commits meaningfully — don't just copy commit messages verbatim.
- Use today's date.

Present the draft to the user and ask for confirmation or edits.

### Step 5 — Apply changes

After user confirmation:

1. **Update `pyproject.toml`**: change `version = "X.Y.Z"` to `version = "A.B.C"`.
2. **Update `CHANGELOG.md`**: insert the new entry at the top (after the header lines, before the first `## [` entry).
3. **Run `uv lock`** to update the lockfile with the new version.

### Step 6 — Verify

1. Run `uv run ruff check manuals/` — must pass.
2. Verify all 6 `book.py` files parse correctly:
   ```bash
   uv run python -c "import ast, glob; [ast.parse(open(f).read()) for f in glob.glob('manuals/**/book.py', recursive=True)]"
   ```

### Step 7 — Commit

Stage and commit with message:
```
docs: release vA.B.C

<one-line summary of key changes>
```

Do NOT push. Inform the user:
- "Release vA.B.C committed. Run `git push` when ready to deploy."
- Remind that the library must be published on PyPI first if this release depends on new library features.

## Error handling

- If ruff or syntax checks fail, fix the issues and re-run the checks before committing.
- If `CHANGELOG.md` does not exist, create it with the standard header.
- If `pyproject.toml` has no `project.version` field, abort with an error message.
