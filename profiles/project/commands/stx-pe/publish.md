# /stx-pe:publish — Release a mature pack (semver + tag + optional PyPI)

Arguments: $ARGUMENTS

## Options

- `<pack-path>` (mandatory) — Local checkout of the pack (must be on disk, not a remote ref).
- `--bump <patch|minor|major>` — Override computed semver bump.
- `--target <pypi|tag|both>` — Skip the Step 7 QCM and force a specific target.
- `--pr-upstream <upstream-repo>` — For fork-packs, propose an upstream PR for mature components.
- `--dry-run` — Compute bump + write CHANGELOG entry locally, but don't commit, tag, or publish.
- `--help` — Show stx-pe cheatsheet.

## Description

Forces the **publish-only** sub-mode of `/stx-pe:go` : release a mature pack.

Steps :
1. Validate working tree clean + all components pass `stx component validate`.
2. Compute next semver from `decisions_log` since last release (REMOVED → major, CHANGED → minor, ADDED only → patch).
3. Write CHANGELOG entry, bump `pyproject.toml` + `_pack_manifest.toml` versions.
4. Surface QCM for PyPI publish (NEVER auto-published, even in autonomous mode).
5. Create signed git tag `v<X.Y.Z>`.
6. Optionally open upstream PR if `--pr-upstream` provided and matures exist.

## Examples

- `/stx-pe:publish ../streamtex-pack-design` — Auto-computed bump, QCM for target
- `/stx-pe:publish --bump minor ../streamtex-pack-design` — Force minor bump
- `/stx-pe:publish --target tag ../streamtex-pack-design` — Tag only, skip PyPI
- `/stx-pe:publish --pr-upstream streamtex/streamtex-packs ../design-edu`
- `/stx-pe:publish --dry-run ../streamtex-pack-design` — Preview the bump + changelog

## Required Readings

Before executing, read :
1. `.claude/pack-engineering/skills/pe-publish.md` — Publish workflow
2. `.claude/pack-engineering/agents/pack-orchestrator.md`
3. `.claude/pack-engineering/agents/pack-publisher.md` — The specialist

## Workflow

Invoke the `pack-orchestrator` with the verb forced to `publish`. The orchestrator validates the pack, computes the bump (surfacing a disagreement QCM if `--bump` overrides the computed value), then delegates to `pack-publisher` for write operations. Publishing to PyPI ALWAYS requires explicit user QCM approval at Step 7.
