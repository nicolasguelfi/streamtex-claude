# Template: Dev Governance Report

Report documenting ecosystem repo modifications made during a CE cycle, their verification status, and any PRs created.

## Structure

```markdown
---
title: Dev Governance Report — <project name>
date: <YYYY-MM-DD>
cycle: <COLLECT date> to <COMPOUND date>
repos_modified: [<repo1>, <repo2>]
branch_used: <true/false>
---

# Development Governance Report — <Project Name>

## Cycle Context

| Field | Value |
|-------|-------|
| Project | <project name> |
| Cycle dates | <start> to <end> |
| Pathway | <A / B / C> |

## Repo Modifications

### streamtex (library)

| File | Change type | Description |
|------|------------|-------------|
| `streamtex/xxx.py` | bug fix | <description> |
| `CHANGELOG.md` | documentation | Added entry for fix |

**Branch**: `ce/<project>/<description>` | main
**Verification**:
- [x] ruff check passed
- [x] pytest passed (1300/1300)
- [x] CHANGELOG.md updated
**PR**: #<number> | not created | not applicable

### streamtex-claude (profiles)

| File | Change type | Description |
|------|------------|-------------|
| `profiles/project/ce/skills/xxx.md` | feature | <description> |

**Branch**: main
**Verification**:
- [x] manifest.toml coherent
- [x] install.py up to date
**PR**: not applicable

### streamtex-docs (documentation)

No modifications during this cycle.

## Summary

| Repo | Files modified | Branch | Conventions | PR |
|------|---------------|--------|-------------|-----|
| streamtex | 2 | ce/fix-bib | OK | #45 |
| streamtex-claude | 1 | main | OK | — |
| streamtex-docs | 0 | — | — | — |
```

## Usage

Stored in `docs/solutions/governance/YYYY-MM-DD-dev-report.md`. One report per CE cycle that involved ecosystem modifications.
