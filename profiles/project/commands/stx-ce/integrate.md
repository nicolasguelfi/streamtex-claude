# /stx-ce:integrate — Integrate capitalized solutions into operational rules

Arguments: $ARGUMENTS

## Options

- `--target <file>` — Integrate a single solution file instead of all pending
- `--dry-run` — Show routing plan without applying changes
- `--help` — Show stx-ce cheatsheet

## Description

Routes solutions from `docs/solutions/` to their operational destinations after the COMPOUND phase. Solutions are classified and sent to one of 4 targets:

| Destination | Target | Method |
|-------------|--------|--------|
| **streamtex** (lib) | Library bugs or features | `/stx-issue:feature` or `/stx-issue:bug` |
| **streamtex-claude** (plugin) | Skill, command, or template changes | `/stx-issue:feature` or `/stx-issue:bug` |
| **streamtex-docs** (docs) | Documentation improvements | `/stx-issue:docs` |
| **Author custom rules** | `.claude/custom/references/` or `custom/design-guideline.md` | Direct file update |

Solutions are marked as `integrated: true` in their frontmatter after processing.

## Examples

- `/stx-ce:integrate` — Integrate all pending solutions
- `/stx-ce:integrate --dry-run` — Preview routing without applying
- `/stx-ce:integrate --target docs/solutions/style/2026-04-05-factorize-duplicate-styles.md` — Integrate one solution

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-integrate.md` — Full workflow
2. `docs/solutions/` — Solutions to integrate
3. `.claude/custom/README.md` — Custom references structure

## Workflow

Execute the `ce-integrate` skill. GATE: routing validation before execution.
