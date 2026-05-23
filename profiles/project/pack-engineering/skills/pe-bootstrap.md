# PE Bootstrap

Sub-mode skill for the **bootstrap** scenario : start from N existing
StreamTeX projects and produce a brand-new shared pack containing the
recurring visual idioms extracted from those projects.

Read `pe-conventions.md` and `pe-go.md` before invoking.

## When to use

The user has ≥ 2 existing projects with overlapping visual idioms but no
shared pack. They want to factorize. No upstream pack to fork.

Triggers (from `ce-task.md` PACK_BOOTSTRAP archetype or `/stx-pe:bootstrap`) :
- "extract a shared pack from projects A B C"
- "bootstrap pack from these documents"
- "factoriser composants depuis mes projets"

## Inputs

- `<projects>` : list of paths (relative or absolute) — the N consumer projects.
- `--pack-name <name>` (optional ; orchestrator proposes a default).
- `--target-path <path>` (optional ; defaults to `../<pack-name>/`).
- `--active-ds <ref>` (optional ; defaults to `default` — orchestrator scaffolds a minimal DS).

## Workflow

1. **Confirm parameters** — orchestrator surfaces a parameter-confirmation QCM :

   > "Bootstrap a new pack `<proposed-name>` from <N> projects:
   > <list>. Target path: `<target-path>`. Initial DS: `<ds>`. Confirm?"
   > - OK, launch (Recommended)
   > - Modify the name / path / DS
   > - Let's discuss

2. **Initialize pack-master-plan** — write `docs/pack-engineering/pack-master-plan.{yaml,md}`
   in the pilot project (= the directory where the orchestrator is invoked,
   defaults to the parent of the consumer projects).

3. **Run `pe-go` Steps 1-6** :
   - Step 1 DISCOVERY → G1
   - Step 2 DESIGN → G2
   - Step 3 IMPLEMENT (creates pack via `stx pack new`)
   - Step 4 ADOPT
   - Step 5 RETROFIT → G3
   - Step 6 AUDIT (auto-run)

4. **Optionally Step 7 PUBLISH** — surface QCM "Publish?".

## Outputs

- New pack repo at `<target-path>` with components/DS/kit + per-component commits.
- All N consumer projects updated : `stx.toml` declares pack, blocks rewritten.
- Pilot project `docs/pack-engineering/` populated with full audit trail.

## Specific QCMs (sub-mode flavor)

The QCM phrasing in Step 0 is adapted :

> "No existing pack-master-plan — initializing a bootstrap cycle.
> <N> projects will be analyzed. <proposed-name> is the suggested name
> for the new pack (based on the workspace name). Confirm the name?"
> - Keep <proposed-name> (Recommended)
> - Rename
> - Let's discuss

## Defaults

- `--min-occurrences 2` (passed to pack-miner).
- `--min-projects 2`.
- `--dedup-against-packs true` (pack-miner skips clusters already covered
  by `streamtex-pack-design` if installed).
- DS scaffolded with 5 minimal bundles : `colors`, `titles`, `body`,
  `callouts`, `card_grid` (enough for the most common components).
- Initial kit `recommended` containing the top-5 components by usage count.
