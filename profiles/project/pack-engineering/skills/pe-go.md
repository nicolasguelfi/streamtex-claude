# PE Go

Sequencer skill for the orchestrated Pack Engineering cycle. Read by
`pack-orchestrator` to know how to chain phases for any sub-mode
(bootstrap / specialize / refine).

Read `pe-conventions.md` and `ce-conventions.md` before invoking any QCM.

## Workflow

The cycle is **7 steps** with **4 fundamental gates** (G1, G2, G3, G4).
Sub-mode skills (`pe-bootstrap.md`, `pe-specialize.md`, `pe-refine.md`,
`pe-audit.md`, `pe-adopt.md`, `pe-publish.md`) reuse this sequencer
selectively.

### Step 0 — Detect state and propose scope

Per `pack-orchestrator.md` Methodology Step 0. Loads or initializes
`pack-master-plan.yaml`.

### Step 1 — DISCOVERY

**Sub-mode** : bootstrap, specialize, refine.

**Invoke** : `pack-miner` with the consumer projects and quality thresholds.

**Output** : `docs/pack-engineering/<ts>/discovery.md` + populated
`mining` section in `pack-master-plan.yaml`.

**Duration** : 1-5 min depending on N projects.

### GATE G1 — post-DISCOVERY (fundamental)

Surface QCM with the candidates table summary :

> "L'analyse a trouvé <N> candidats à extraire dans <M> projets.
> Recommandés (≥ 2 projets ET ≥ <threshold> occurrences) : <K>.
> Que faites-vous ?"
>
> - Approuver toute la liste recommandée (Recommandé)
> - Sélection à préciser (drill-down par candidat)
> - Élargir aux candidats single-project (+<X>)
> - Discutons-en

Capture decision : `mining_validated` in `decisions_log`.

### Step 2 — DESIGN

**Sub-mode** : bootstrap, specialize, refine.

**Invoke** : `pack-designer`. Optionally delegate strategy classification
to `prototype-designer`.

**Output** : `docs/pack-engineering/<ts>/design.md` + populated `design`
section in `pack-master-plan.yaml`.

**Duration** : 2-8 min depending on number of candidates.

### GATE G2 — post-DESIGN (fundamental — skippable in minimal dialog_level)

Surface QCM with the conflicts/rejections summary :

> "<N> composants conçus avec contrat complet. <C> conflits résolus.
> <R> composants rejetés (raison: <r>).
> Que faites-vous ?"
>
> - Tout approuver et passer à l'implémentation (Recommandé)
> - Recommandés uniquement (excluant les conflits non-résolus)
> - Sélection à préciser (drill-down par composant)
> - Réviser un composant en particulier
> - Discutons-en

Capture decision : `design_approved`.

### Step 3 — IMPLEMENT

**Sub-mode** : bootstrap, specialize, refine.

**Invoke** : `pack-implementer`. Optionally delegate consistency check to
`style-consistency-checker`.

**Output** : component files in `<target_pack>/<pack>/components/*.py`,
per-component commits, populated `implementation` section.

**Duration** : 3-15 min depending on count.

No gate after IMPLEMENT — the design was the gate. Failures are recorded
in `implementation.failed` but the phase continues.

### Step 4 — ADOPT

**Sub-mode** : bootstrap (auto), specialize (auto), refine (auto, skipped
if the pack is already adopted), adopt-only (explicit).

**Action** : direct CLI on each consumer project (no specialist agent) :

```bash
for proj in <consumer-projects> ; do
  cd "$proj"
  stx pack add <ref>  # the new pack from the implementation step
  stx kit install <pack>:<kit_name>  # default kit if defined
  cd -
done
```

**Output** : updated `stx.toml` in each consumer project, populated
`adoption` section.

**Duration** : < 1 min per project.

### GATE G3 — pre-RETROFIT (fundamental)

After ADOPT but before any block rewrite, surface the dry-run plan :

> "Plan de retrofit prêt : <N> blocs à réécrire sur <M> projets, <K>
> skipped. Mode actuel : dry-run.
> Que faites-vous ?"
>
> - Appliquer tout (Recommandé)
> - Appliquer projet par projet (revue intermédiaire)
> - Lancer un dry-run sur un sous-ensemble pour inspection
> - Discutons-en

Capture decision : intermediate, full apply decision logged at end of
RETROFIT as `retrofit_validated`.

### Step 5 — RETROFIT

**Sub-mode** : bootstrap, specialize, refine.

**Invoke** : `pack-retrofitter` with `--mode dry-run` (default), then
`--mode apply` if G3 approved.

**Output** : block rewrites + commits in consumer projects, populated
`retrofit` section, `retrofit-plan.md` (always) + `retrofit-report.md`
(apply only).

**Duration** : 10-30 min depending on count (smoke render is the bottleneck).

### GATE G4 — post-RETROFIT smoke fail (conditional)

Only triggered if `retrofit.blocks_reverted` is non-empty AND
`--skip-on-smoke-fail` was false.

Surface :

> "<N> blocs ont échoué le smoke render après retrofit. Que faites-vous ?"
>
> - Revert les <N> blocs et continuer sans eux (Recommandé)
> - Inspecter chaque bloc en détail
> - Annuler tout le retrofit
> - Discutons-en

Capture decision in `decisions_log`.

### Step 6 — AUDIT (auto-run after retrofit, optional standalone)

**Sub-mode** : auto-run after RETROFIT (bootstrap, specialize, refine) ;
standalone in audit-only mode.

**Invoke** : `pack-auditor`.

**Output** : `docs/pack-engineering/<ts>/audit-report.md`, populated
`audit` section. No gate (read-only).

**Duration** : 1-3 min.

Follow-up suggestion (not a gate) :

> "L'audit a identifié <N> recommandations (<H> HIGH, <M> MEDIUM, <L> LOW).
> Souhaitez-vous lancer un cycle de refine pour corriger les HIGH ?"
>
> - Oui (Recommandé)
> - Non, conserver le rapport pour plus tard
> - Discutons-en

### Step 7 — PUBLISH (optional, gated)

**Sub-mode** : opt-in only. Triggered by `/stx-pe:publish <pack-path>` or
by an explicit user request at the end of a bootstrap/specialize/refine
cycle.

Surface QCM :

> "Le pack `<name>` est prêt à publier (<count> composants, version
> <new-version> calculée). Que faites-vous ?"
>
> - Publier sur PyPI + git tag (Recommandé)
> - Git tag uniquement (pas de PyPI)
> - Conserver local, ne rien publier
> - Discutons-en

If user authorizes → invoke `pack-publisher`.

Capture decision : `publish_decided` with the chosen targets.

## Termination

A complete bootstrap/specialize cycle terminates at Step 6 (audit
auto-run) or Step 7 (publish, if user opted in). A refine cycle
terminates at Step 5 (no audit by default — invoked separately). An
audit-only cycle terminates at Step 6.

After termination :

- `pack-master-plan.yaml` reflects final state.
- `pack-master-plan.md` has narrative updates.
- No follow-up phase auto-runs.

The orchestrator finally posts a summary message :

> "Cycle PE terminé. <résumé>. Prochaines étapes recommandées : <list>."

## Sub-mode skill references

| If sub-mode | Reads also |
|---|---|
| bootstrap | `pe-bootstrap.md` (entry-specific arg parsing) |
| specialize | `pe-specialize.md` |
| refine | `pe-refine.md` |
| audit | `pe-audit.md` (steps 6 only) |
| adopt-only | `pe-adopt.md` (step 4 only) |
| publish-only | `pe-publish.md` (step 7 only) |
