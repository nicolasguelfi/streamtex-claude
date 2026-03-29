# CE Compound

Skill for the COMPOUND phase of the Compound Engineering cycle. Capitalize learnings across 3 axes: document production, ecosystem feedback, and development governance.

## Workflow

The COMPOUND phase executes 3 axes sequentially.

---

### Axis 1: Document Production Capitalization

#### Phase 1.0: Scan Context

1. Review auto-memory for any notes from the current project cycle.
2. Scan recent project history: review report (and fix report if any), plan, assessment, and collect report.
3. Build a timeline of what happened during this cycle.
4. Load the producer profile from `docs/solutions/producer-profile.md` if it exists.

#### Phase 1.1: Extract Learnings

Run 5 analysis perspectives sequentially to extract knowledge from the cycle.

1. **Context Analyzer**:
   - What was the document type (course, presentation, report, manual)?
   - Who was the target audience?
   - What was the primary objective?
   - Which pathway was used (A/B/C/mixed)?

2. **Solution Extractor**:
   - What patterns or techniques worked particularly well?
   - Which StreamTeX features were key to success?
   - What reusable code snippets or block patterns emerged?
   - What content structures proved effective?
   - What AI image prompts produced effective results? Save effective prompts as patterns in `docs/solutions/assets/`
   - What provider/model/seed combinations produced good results? Record for reuse
   - What prompt anti-patterns were discovered (vague descriptions, inconsistent style terms, poor reproducibility)?

3. **Related Finder**:
   - What other documents in the workspace are related to this one?
   - What cross-references or shared patterns exist?
   - Could any learnings apply to those related projects?

4. **Prevention Strategist**:
   - What problems were encountered during the cycle?
   - What went wrong and how was it resolved?
   - What should be avoided next time?
   - What warnings or precautions should be documented?

5. **Category Classifier**:
   - Assign each learning to one or more categories:
     - `structure`: document organization, navigation, skeleton patterns
     - `style`: visual design, CSS, theming, layout
     - `content`: writing, pedagogy, examples, exercises
     - `process`: workflow, tooling, automation, efficiency
     - `pedagogy`: learning design, assessment, progression
     - `assets`: images, diagrams, code samples, media
     - `ai-images`: AI image generation prompts, provider configs, seed strategies, style patterns
     - `deployment`: hosting, CI/CD, export, delivery
     - `import`: conversion, migration, format handling
     - `style/patterns`: Named design patterns extracted from produced blocks — reusable component recipes
   - Classify each learning by **scope**:
     - `specific`: applicable only to this document
     - `generic`: applicable to all documents of this type (course, presentation, etc.)

#### Phase 1.2: Check for Duplicates

1. Use the **learnings-researcher** agent to search `docs/solutions/` for similar existing entries.
2. For each candidate learning:
   - If a duplicate is found: update the existing solution file with new insights rather than creating a new one.
   - If a partial match is found: extend the existing solution with the new perspective.
   - If no match: prepare for creation as a new entry.

#### Phase 1.3: Assemble and Write

1. For each new or updated learning:
   - Write to `docs/solutions/<category>/YYYY-MM-DD-<topic>.md` using the **solution** template from `.claude/ce/templates/`.
   - Include the `scope` field in the frontmatter (`specific` or `generic`).
   - Include:
     - Context (when this applies)
     - Problem or opportunity
     - Solution or pattern
     - StreamTeX code examples where applicable
     - Related learnings (cross-references)
     - Tags for searchability
2. Create the category subdirectory if it does not exist.

#### Phase 1.4: Update Producer Profile

1. If `docs/solutions/producer-profile.md` exists:
   - Enrich with new style preferences, content preferences, and patterns discovered during the cycle.
   - Add any new anti-patterns identified.
   - Increment `projects_count`.
   - Update `last_updated` date.
2. If it does not exist:
   - Ask the user if they want to create one based on this cycle's learnings.
   - If yes: create using the **producer-profile** template, pre-filled from this cycle.
3. **Multi-project consolidation**: If the user works on multiple projects, check if other projects in the workspace have their own `producer-profile.md`. If so, propose consolidating them into a unified profile. The user chooses which projects to consolidate and which preferences to keep in case of conflicts.

---

### Axis 2: Ecosystem Feedback

#### Phase 2.1: Detect Issues

Use the **feedback-detector** agent to scan cycle artifacts:

1. **Review findings**: For each CRITICAL/MAJOR finding, determine if it is caused by a StreamTeX limitation (not user content).
2. **Solutions**: Identify `workaround` solutions (likely bugs) and `technique` solutions mentioning missing features.
3. **Conversation history**: Look for Python tracebacks, error messages, or unresolved questions.

#### Phase 2.2: Route to Repos

For each detected issue, determine the target repo and ticket type:

| Problem | Repo | Command |
|---------|------|---------|
| Bug in `st_*` functions, rendering, export, PDF | `streamtex` | `/stx-issue:bug` |
| Missing library feature | `streamtex` | `/stx-issue:feature` |
| Bug in agent, skill, template, or command | `streamtex-claude` | `/stx-issue:bug` |
| Missing agent or inadequate behavior | `streamtex-claude` | `/stx-issue:feature` |
| Incorrect or missing documentation | `streamtex-docs` | `/stx-issue:docs` |
| Unresolved usage question | `streamtex` | `/stx-issue:question` |

#### Phase 2.3: GATE — Ticket Validation

Present the proposed tickets to the user:

```
| # | Type | Repo | Title | Source |
|---|------|------|-------|--------|
```

The user can:
- Validate a ticket as-is
- Modify the title or description
- Delete a ticket from the list
- Add a ticket manually
- Validate all at once
- Cancel all

#### Phase 2.4: Submit Tickets

For each validated ticket:
1. Execute the corresponding `/stx-issue:*` command.
2. Record the created issue number.
3. Write the feedback summary to `docs/solutions/YYYY-MM-DD-<name>-feedback.md` using the **feedback-summary** template.

---

### Axis 3: Development Governance

#### Phase 3.1: Inventory Ecosystem Modifications

For each ecosystem repo (streamtex, streamtex-claude, streamtex-docs):

1. If a baseline commit hash was recorded at cycle start (by ce-go), compute `git diff --name-only <baseline>..HEAD`.
2. If no baseline exists, check `git log` for commits made during the cycle timeframe.
3. Classify each modification: bug fix, feature, refactoring, documentation.
4. Check if modifications are on a branch or on main.

If no ecosystem repos were modified during the cycle, skip to the Summary.

#### Phase 3.2: Verify Workflows

For each modified repo, verify conventions were followed:

- **streamtex**: ruff check passed? pytest passed? CHANGELOG.md updated?
- **streamtex-claude**: manifest.toml coherent? install.py up to date?
- **streamtex-docs**: block structure compliant? CI checks passed?

Use the **dev-governance** agent for verification.

#### Phase 3.3: Propose PRs

- If modifications are on a branch: propose creating a PR with a summary.
- If modifications are on main: warn and propose creating a retroactive branch.
- The user chooses: create PR, defer, or ignore.

#### Phase 3.4: Write Governance Report

Write to `docs/solutions/governance/YYYY-MM-DD-dev-report.md` using the **dev-report** template.

---

### Summary

Report what was capitalized across all 3 axes:

1. **Axis 1 — Document production**:
   - Number of new learnings created / updated
   - Categories covered
   - Producer profile status (created / updated / unchanged)
   - File paths of all written solutions

2. **Axis 2 — Ecosystem feedback**:
   - Number of tickets proposed / submitted / skipped
   - Repos targeted

3. **Axis 3 — Development governance**:
   - Repos modified
   - Branch status
   - PRs created or pending

Suggest next cycle:
- Run `/stx-ce:collect` to start a new cycle with new material.
- Run `/stx-ce:assess` to reassess and improve the current project.
