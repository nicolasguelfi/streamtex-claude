# PE Audit Report

> Produced by `pack-auditor` at the end of the AUDIT phase (which can be
> invoked standalone via `/stx-pe:audit` or auto-run after RETROFIT).
> Lives at `docs/pack-engineering/<timestamp>/audit-report.md`.

**Date** : <YYYY-MM-DD HH:MM:SS>
**Audited pack** : <pack-name> @ <version>
**Consumer projects** : <list>

## 1. Summary

<One paragraph : N components declared, M used cross-projects, K unused,
D duplicate suspects, B bundle gaps, C naming conflicts. Overall verdict :
HEALTHY / NEEDS ATTENTION / CRITICAL.>

## 2. Unused components

<Components declared in the pack but not imported by any consumer project.
Candidates for deprecation or removal.>

| Component | Declared since | Reason for non-usage (if known) | Recommended action |
|---|---|---|---|
| `legacy_card` | v0.1.0 | Replaced by `card_grid` in v0.2.0 | Mark deprecated in v0.3.0, remove in v0.4.0 |

## 3. Duplicate suspects

<Pairs of components with ≥ 80 % overlap on docstring keywords.>

| Component A | Component B | Overlap | Recommended action |
|---|---|---|---|
| `info_callout` | `note_callout` | 85% | Merge into `callout(kind=info|note)` with PARAM ; deprecate one. |
| `key_takeaways` | `summary_list` | 82% | Both ship `bullet_list + heading` pattern. Keep `takeaways` (semantic), deprecate `summary_list`. |

## 4. Bundle gaps

<Each component declares `bundles_required` ; verify the active DS provides
them all.>

| Component | Missing bundle | Active DS | Fix |
|---|---|---|---|
| `comparison_card_grid` | `compare.left_palette` | `default` | Add `compare.left_palette` to `default` DS, or change component to use `colors.accent_left`. |

## 5. Naming conflicts (cross-pack)

<Components with the same name across installed packs in any consumer project.>

| Name | Packs colliding | Resolution recommended |
|---|---|---|
| `callout` | `streamtex-pack-design`, `our-fork` | Document `[resolution] prefer = ["our-fork", "streamtex-pack-design"]` in each consumer project's `stx.toml`. |

## 6. Per-component usage map

<For each component declared : count of imports across all consumer projects.>

| Component | proj-a | proj-b | proj-c | Total |
|---|---|---|---|---|
| `info_callout` | 8 | 6 | 0 | 14 |
| `key_takeaways` | 4 | 0 | 5 | 9 |
| `legacy_card` | 0 | 0 | 0 | 0 ← UNUSED |

## 7. Contract drift

<Components whose source has changed since the last `stx component validate`
(e.g. someone edited the function but didn't update the docstring).>

| Component | Drift detected | Action |
|---|---|---|
| `key_takeaways` | Added a `subtitle` param without updating PARAMS section | Re-run `stx component validate <name>` after fixing docstring. |

## 8. Recommendations (ordered by priority)

1. **HIGH** : add bundle `compare.left_palette` to `default` DS (blocks `comparison_card_grid`).
2. **MEDIUM** : merge `info_callout` + `note_callout` → `callout(kind=...)` — semver minor bump.
3. **LOW** : deprecate `legacy_card` with a CHANGELOG note + removal target in next major.
4. **LOW** : add `[resolution] prefer` to consumer projects to silence the `callout` collision warning.

## 9. Next steps

<No gate — audit is read-only. The orchestrator surfaces a follow-up QCM
asking what the user wants to act on, but doesn't gate.>

> "L'audit a identifié <N> recommandations (<H> HIGH, <M> MEDIUM, <L> LOW).
> Souhaitez-vous lancer un cycle de refine pour corriger les HIGH ?"
>
> - Oui, lancer `/stx-pe:refine` ciblé sur les HIGH (Recommandé)
> - Non, conserver le rapport pour plus tard
> - Discutons-en
