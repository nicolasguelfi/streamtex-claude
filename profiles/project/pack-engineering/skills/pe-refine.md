# PE Refine

Sub-mode skill for the **refine** scenario : the user has been producing
blocks in the current project (often after a previous PE bootstrap), new
visual idioms have emerged, and they want to capture those NEW patterns
into the existing pack — without re-doing the full bootstrap analysis.

Read `pe-conventions.md` and `pe-go.md` before invoking.

## When to use

A pack is already active in the current project (`stx.toml` declares it).
Production has continued ; new blocks contain idioms not yet in the pack.
The user wants to enrich the pack incrementally.

Triggers (from `ce-task.md` PACK_REFINE archetype or `/stx-pe:refine`) :
- "refine pack, capture emerged patterns"
- "enrichir mon pack avec les nouveaux patterns"
- "add to pack what's new in the latest blocks"

Note : `refine` operates on **a single project at a time** (the current
project). To capture cross-project patterns, use bootstrap or specialize.

## Inputs

- (No project argument — operates on cwd's project.)
- `--target-pack <ref>` (optional ; defaults to the primary local pack
  declared in current project's `stx.toml`).
- `--since <date|tag>` (optional ; defaults to the date of the last
  `decisions_log` entry of type `mining_validated` in the pack-master-plan).

## Workflow

1. **Detect active pack** : read `stx.toml` ; find the `[[packs]]` entry
   marked primary (or fall back to the only declared pack).

2. **Determine scan window** : `--since <date>` defines the cutoff.
   Blocks modified or added before that date are skipped (their idioms
   are already covered by previous PE cycles).

3. **Initialize / extend pack-master-plan** : if a `pack-master-plan.yaml`
   exists in `docs/pack-engineering/`, append a new iteration entry under
   `phases_completed` with mode `refine`. Otherwise create a fresh plan
   (rare case : refine without prior bootstrap).

4. **Run `pe-go` Steps 1-5** with reduced scope :

   - Step 1 DISCOVERY : `pack-miner` invoked with `--consumer-projects <cwd>`
     ONLY (single project) and `--dedup-against-packs true` including the
     active pack. Only NEW clusters survive.
   - Step 2 DESIGN → G2.
   - Step 3 IMPLEMENT : new components added to the existing pack (no
     `stx pack new` — pack already exists).
   - Step 4 ADOPT : not needed (pack already in stx.toml ; kit may need
     to be updated to include new components — QCM proposed).
   - Step 5 RETROFIT → G3 : rewrites only the blocks in cwd that match
     the new clusters.

5. **No Step 6 AUDIT by default** (refine is incremental — full audit is
   a separate cycle). The orchestrator suggests :

   > "<N> new components added to the pack. Launch a health audit to
   > verify global coherence?"
   > - No, keep for later (Recommended in refine)
   > - Yes, launch `/stx-pe:audit <pack>`
   > - Let's discuss

6. **Step 7 PUBLISH** : if the pack has its own semver lifecycle, propose
   a patch bump (refine usually adds, doesn't change). Otherwise leave the
   pack at its current version pending a later release.

## Outputs

- Updated pack with new components added.
- Current project's blocks rewritten to use the new components.
- `pack-master-plan.yaml` has a new entry in `phases_completed` like
  `refine-<date>`.

## Specific QCMs

After detection of new clusters :

> "<N> new visual idioms detected in blocks modified since
> `<since>`. None is already covered by the current pack. Continue?"
> - Yes (Recommended)
> - Widen the scan to the full duration (ignore --since)
> - Let's discuss
