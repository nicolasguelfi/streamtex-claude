# PE Adopt

Sub-mode skill for the **adopt-only** scenario : install an existing
pack into N consumer projects without running any extraction, design,
or retrofit. This is the "pure adoption" path — for users who already
have a pack ready and just want it wired into their projects.

Read `pe-conventions.md` and `pe-go.md` before invoking.

## When to use

The pack already exists (local or remote). The consumer projects do
not yet declare it in their `stx.toml`. The user wants `stx pack add`
+ `stx kit install` looped over N projects, with optional retrofit
deferred to a later cycle.

Triggers (from `ce-task.md` PACK_ADOPT archetype or `/stx-pe:adopt`) :
- "adopt <pack> in projects A B C"
- "installer <pack> dans mes projets"
- "wire pack into projects"

Note : if the user expects existing blocks to be rewritten to USE the
new pack, recommend `refine` instead (which includes retrofit). Adopt-
only is for fresh adoptions where blocks will be written from scratch
later.

## Inputs

- `<pack>` (mandatory) : pack ref to adopt — `git:url@rev`,
  `pypi:name@spec`, or local path.
- `<projects>` (mandatory) : list of consumer project paths.
- `--kit <name>` (optional ; defaults to the pack's `default` kit if
  declared, else QCM to choose).
- `--retrofit` (optional flag ; if set, escalates to refine sub-mode
  after adopt to rewrite existing blocks).

## Workflow

1. **Validate pack ref** : check the pack resolves (clone-able for git,
   listed on PyPI for pypi, exists on disk for local). Abort with
   actionable error if not.

2. **List available kits** : read pack's `_pack_manifest.toml` →
   `[kits]` section. If `--kit` not provided AND > 1 kit available,
   surface QCM :

   > "Pack `<name>` offers <N> kits: <list-with-counts>. Which one to
   > install in the projects?"
   > - <default-kit-name> (Recommended)
   > - Selection to be specified
   > - No kit (just `stx pack add`)
   > - Let's discuss

3. **Confirm projects** : surface QCM with the list of consumer projects :

   > "Adopt `<pack>` (kit `<kit>`) in <N> projects: <list>.
   > Confirm?"
   > - OK, install (Recommended)
   > - Selection to be specified
   > - Let's discuss

4. **Initialize or extend pack-master-plan** : if a plan exists in
   pilot project, append entry with mode `adopt`. Otherwise create a
   minimal plan with `pack.mode = adopt-only`.

5. **Run `pe-go` Step 4 only** :

   ```bash
   for proj in <consumer-projects> ; do
     cd "$proj"
     stx pack add <pack-ref>
     [ -n "<kit>" ] && stx kit install <pack>:<kit>
     cd -
   done
   ```

   No specialist agent — direct CLI per `pe-go.md` Step 4 §Action.

6. **Optional retrofit escalation** : if `--retrofit` was passed, hand
   off to `pe-refine.md` workflow starting at Step 4 RETROFIT.

7. **No Step 6 AUDIT, no Step 7 PUBLISH** — adopt doesn't change the
   pack itself, only the consumer projects' `stx.toml`.

## Outputs

- Updated `stx.toml` in each consumer project (new `[[packs]]` entry +
  kit installed bundles).
- `pack-master-plan.yaml` populated `adoption` section with per-project
  install results (decisions_log entry : `adoption_completed`).

## Specific QCMs

If installation fails on any project (CLI error, network, etc.) :

> "Installation failed on <N> project(s): <list-with-errors>.
> What do you do?"
> - Retry the failed projects
> - Mark as skipped and continue
> - Cancel everything and restore the `stx.toml` (Recommended if > 50% failing)
> - Let's discuss
