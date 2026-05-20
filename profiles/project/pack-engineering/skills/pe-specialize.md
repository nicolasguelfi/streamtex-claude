# PE Specialize

Sub-mode skill for the **specialize** scenario : take an existing upstream
pack (e.g. `streamtex-pack-design`) and produce a fork-pack that EXTENDS it
with domain-specific components extracted from N projects, while
preserving the upstream as a dependency.

Read `pe-conventions.md` and `pe-go.md` before invoking.

## When to use

The user has an upstream pack that almost fits but lacks domain-specific
patterns visible in their projects. They want a fork that consumes the
upstream and adds what's missing — without overriding the upstream's
existing components.

Triggers (from `ce-task.md` PACK_SPECIALIZE archetype or `/stx-pe:specialize`) :
- "specialize streamtex-pack-design for projects A B C"
- "fork streamtex-pack-design with our extensions"
- "étendre <pack> avec nos composants"

## Inputs

- `<upstream-ref>` (mandatory) : the upstream pack ref (`git:url@rev` or
  `pypi:name@spec`).
- `<projects>` : N consumer project paths.
- `--fork-name <name>` (optional ; orchestrator proposes `<upstream-name>-<workspace-name>`).
- `--fork-target-path <path>` (optional ; defaults to `../<fork-name>/`).

## Workflow

1. **Confirm parameters + clone upstream** :

   > "Fork `<upstream-name>` (rev `<rev>`) en `<fork-name>` à partir de
   > <N> projets : <list>. Chemin cible : `<path>`. Confirmer ?"
   > - OK, cloner + bootstrap fork (Recommandé)
   > - Modifier le nom / chemin
   > - Discutons-en

2. **Initialize fork** : clone upstream into `--fork-target-path`,
   rewrite `pyproject.toml` (new name, dependency on upstream), update
   `_pack_manifest.toml` (new name, upstream listed as parent).

3. **Initialize pack-master-plan** with `pack.type = specialize` and
   `pack.upstream = <upstream-ref>`.

4. **Run `pe-go` Steps 1-6 with filtering** :
   - Step 1 DISCOVERY : `pack-miner` invoked with `--dedup-against-packs true`
     **including the upstream**. Any cluster matching an existing upstream
     component is rejected with reason "already covered upstream".
   - Step 2 DESIGN : `pack-designer` checks each cluster against the
     upstream's components — if name collision, propose `<domain>_<name>`
     disambiguation.
   - Step 3 IMPLEMENT : components written to the fork, NOT to upstream.
   - Step 4 ADOPT : `stx.toml` of each consumer project declares BOTH the
     upstream AND the fork (fork has higher resolution priority).
   - Step 5 RETROFIT : block rewrites preferentially import from the
     fork ; upstream imports preserved if existing.
   - Step 6 AUDIT : focused on the fork's added components.

5. **Optionally Step 7 PUBLISH** — with `--pr-upstream <upstream-repo>`
   prompted in QCM : "Promouvoir N composants matures vers <upstream> ?"

## Outputs

- Fork pack at `<fork-target-path>` with the components added on top of upstream.
- Consumer projects' `stx.toml` declares both packs with `[resolution] prefer`.
- (Optional) PR opened against upstream for mature components.

## Specific QCMs

After implementation :

> "Le fork ajoute <N> composants au-dessus de `<upstream>`. Parmi eux,
> <K> sont matures (≥ 2 projets, contrat stable). Proposer un PR upstream ?"
> - Oui, PR pour les <K> matures (Recommandé)
> - Non, garder fork local
> - Sélection à préciser
> - Discutons-en
