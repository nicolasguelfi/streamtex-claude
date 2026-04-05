# CE Integrate

Skill for the INTEGRATE phase of the Compound Engineering cycle. Routes capitalized solutions from `docs/solutions/` to their operational destinations: library issues, skill updates, documentation improvements, or author custom rules.

## Workflow

### Phase 1: Load Solutions

1. Scan `docs/solutions/` recursively for `.md` files (excluding `producer-profile.md`).
2. For each file, parse the YAML frontmatter.
3. Filter to solutions where:
   - `integrated` is `false`, or
   - `integrated` field is absent (legacy solutions)
4. If `--target <file>` is set, process only that file.
5. If no unintegrated solutions are found, report "Nothing to integrate" and exit.

### Phase 2: Classify Destinations

For each unintegrated solution, determine the routing destination by analyzing its content and category:

| Signal in solution content | Destination | Integration method |
|---------------------------|-------------|-------------------|
| References `st_*` functions, rendering bugs, export issues, `write.py`, `styles/` | **streamtex** (lib) | `/stx-issue:feature` or `/stx-issue:bug` |
| References skills, commands, templates, agents, CE workflow, `ce-*.md`, `CLAUDE.md.j2` | **streamtex-claude** (plugin) | `/stx-issue:feature` or `/stx-issue:bug` |
| References manuals, cheatsheets, documentation gaps, tutorials | **streamtex-docs** (docs) | `/stx-issue:docs` or `/stx-issue:feature` |
| Is a project-specific coding rule, style convention, naming rule | **Author custom** (`.claude/custom/references/`) | Direct file update or creation |
| Is a design pattern or guideline refinement | **Author guideline** (`custom/design-guideline.md`) | Direct file update |

Classification heuristics:
- `scope: generic` solutions are more likely to target repos (lib/claude/docs)
- `scope: specific` solutions are more likely to target author custom rules
- `category: guidelines` → check if it's a generic guideline pattern (→ streamtex-claude) or a project-specific refinement (→ author custom)
- Solutions can have **multiple destinations** (e.g., a rule for the author + an issue for the plugin)

### Phase 3: GATE — Routing Validation

Present the proposed routing to the user:

```
Solutions to integrate:

| # | Solution | Category | Destination | Action |
|---|----------|----------|-------------|--------|
| 1 | factorize-duplicate-styles | style | .claude/custom/ | Update style-rules.md |
| 2 | lib-evolution-over-block-fixes | process | streamtex-claude | Issue: update ce-fix.md |
| 3 | visible-references-pattern | guidelines | .claude/custom/ | Update design guideline |
```

The user can:
- **Accept all** — proceed with all integrations
- **Accept N** — proceed with specific items
- **Skip N** — skip specific items (mark as `integrated: skipped`)
- **Modify N** — change the destination or action
- **Cancel** — abort integration

If `--dry-run` is set, display the routing table and exit without executing.

### Phase 4: Execute Integration

For each validated integration:

#### 4a. GitHub Issues (streamtex / streamtex-claude / streamtex-docs)

1. Determine the issue type:
   - Pattern/technique/feature request → `/stx-issue:feature`
   - Bug/workaround → `/stx-issue:bug`
   - Documentation gap → `/stx-issue:docs`
2. Compose the issue body from the solution content:
   - Title: solution title
   - Body: Context + Problem + Solution sections from the solution file
   - Labels: category tag, `from-compound` tag
3. Execute the issue command on the target repo.
4. Record the issue URL in the solution frontmatter.

#### 4b. Author Custom References (`.claude/custom/references/`)

1. Identify the target file:
   - If a relevant file already exists (e.g., `design-guideline-maximize-viewport.md` for guideline solutions) → **update** it
   - If the solution introduces a new rule domain → **create** a new file (e.g., `style-rules.md`)
2. Extract the operational rule from the solution (the "Solution" section).
3. Present the proposed change (before/after or new content) to the user.
4. Apply the change.

#### 4c. Design Guideline (`custom/design-guideline.md`)

1. If the solution is a new pattern → add to `## Patterns` section
2. If the solution is a guideline refinement → update the relevant section
3. Present the proposed change to the user before applying.

### Phase 5: Mark as Integrated

For each processed solution, update its YAML frontmatter:

```yaml
integrated: true
integrated_date: YYYY-MM-DD
integrated_to: <destination(s)>
```

Where `integrated_to` is one of:
- `streamtex#<issue_number>` — lib issue
- `streamtex-claude#<issue_number>` — plugin issue
- `streamtex-docs#<issue_number>` — docs issue
- `.claude/custom/references/<filename>` — author custom reference
- `custom/design-guideline.md` — design guideline
- `skipped` — user chose to skip

### Phase 6: Report

Present a summary:

```
## Integration Report

| # | Solution | Destination | Status |
|---|----------|-------------|--------|
| 1 | ... | .claude/custom/references/style-rules.md | INTEGRATED |
| 2 | ... | streamtex-claude#42 | ISSUE CREATED |
| 3 | ... | skipped | SKIPPED |

### Summary
- Solutions processed: N
- Integrated to custom rules: N
- Issues created: N (streamtex: N, streamtex-claude: N, streamtex-docs: N)
- Skipped: N

### Remaining unintegrated
- N solutions still pending (run `/stx-ce:integrate` again)
```

Suggest next steps:
- Run `/stx-ce:collect` to start a new cycle.
- Run `/stx-ce:integrate --target <file>` to integrate a specific pending solution.
