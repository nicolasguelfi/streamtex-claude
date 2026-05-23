# PE Publish

Sub-mode skill for the **publish-only** scenario : release a mature
pack. Computes the next semver, generates a CHANGELOG entry, creates a
git tag, and (optionally) publishes to PyPI. Optionally opens an
upstream PR for fork-packs.

Read `pe-conventions.md` and `pe-go.md` before invoking.

## When to use

The pack is local-stable and the user wants to make it a versioned
release. This is typically run AFTER a bootstrap/specialize/refine
cycle that added new components, but can also be run standalone on a
pack edited manually.

Triggers (from `/stx-pe:publish` only — no automatic archetype routing,
publish requires explicit user intent) :
- "publish my pack"
- "publier <pack> version <X.Y.Z>"
- "release <pack>"

Note : `pack-publisher` NEVER auto-publishes to PyPI without explicit
QCM approval, even in autonomous mode (cf. `pack-orchestrator.md`
Hard rules).

## Inputs

- `<pack-path>` (mandatory) : path to the pack on disk (must be a
  local checkout, not a remote ref — publish writes files).
- `--bump <patch|minor|major>` (optional ; defaults to auto-computed
  from `decisions_log` since last release).
- `--target <pypi|tag|both>` (optional ; defaults to QCM at Step 7).
- `--pr-upstream <upstream-repo>` (optional ; only meaningful for
  fork-packs ; opens a PR for the components flagged "mature" in the
  master plan).

## Workflow

1. **Validate pack state** :
   - Working tree clean (no uncommitted changes ; otherwise abort with
     actionable error).
   - `_pack_manifest.toml` exists and is valid.
   - All components pass `stx component validate` (delegate to
     `pack-auditor` with `--minimal` if desired ; otherwise just run
     the CLI).

2. **Compute next version** : read `pack-master-plan.yaml` →
   `decisions_log` since last `publish_decided` entry. Per
   `pe-conventions.md` §7 :
   - Any REMOVED component → major bump.
   - Any CHANGED component (signature, output, INVARIANTS) → minor bump.
   - Otherwise (only ADDED components, doc fixes, etc.) → patch bump.

   If `--bump` provided, use it (with confirmation if it disagrees with
   computed bump).

3. **Initialize or extend pack-master-plan** : append `publish` entry.

4. **Run `pe-go` Step 7** : delegate to `pack-publisher` agent. The
   publisher :
   - Writes the CHANGELOG entry from `decisions_log` since last release.
   - Bumps version in `pyproject.toml` and `_pack_manifest.toml`.
   - Creates commit + signed git tag `v<X.Y.Z>`.
   - Surfaces QCM for PyPI publish (cf. `pe-go.md` Step 7 QCM).
   - If `--pr-upstream` provided AND fork-pack with mature components,
     surfaces additional QCM to open PR.

5. **Final QCM** if user opted for tag-only :

   > "Tag `v<version>` created locally. Push to `origin` now?"
   > - Yes (Recommended)
   > - Later, manually
   > - Let's discuss

## Outputs

- `CHANGELOG.md` updated in pack repo with a new section for `<version>`.
- `pyproject.toml` and `_pack_manifest.toml` version bumped.
- Commit + signed git tag `v<X.Y.Z>`.
- (Optional) PyPI release if user approved at Step 7 QCM.
- (Optional) PR opened against upstream if `--pr-upstream` + matures exist.
- `pack-master-plan.yaml` `publish` section populated (decisions_log
  entry : `publish_decided` with chosen targets).

## Specific QCMs

If the working tree is dirty :

> "The pack has uncommitted changes: <files>. What do you do?"
> - Cancel the publish — commit manually first (Recommended)
> - Make an auto commit "chore: pre-release housekeeping"
> - Let's discuss

If computed bump disagrees with `--bump` user override :

> "The bump computed from `decisions_log` is `<computed>` (reason:
> <reason>). The user requests `<override>`. Confirm the override?"
> - OK, force `<override>` (Recommended if justified)
> - Use the computed bump `<computed>`
> - Let's discuss
