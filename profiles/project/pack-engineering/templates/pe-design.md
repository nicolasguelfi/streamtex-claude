# PE Design Report

> Produced by `pack-designer` (augmented by `prototype-designer` for strategy
> classification) at the end of the DESIGN phase.
> Lives at `docs/pack-engineering/<timestamp>/design.md` in the pilot project.

**Date** : <YYYY-MM-DD HH:MM:SS>
**Mode** : bootstrap | specialize | refine
**Target pack** : <name>
**Components designed** : <int>
**Components rejected** : <int>
**Naming conflicts resolved** : <int>

## 1. Summary

<One paragraph : N components designed with full contract, decomposed by
granularity (P/C/B), totaling X required bundles across Y design system
bundle namespaces.>

## 2. Per-component contract

<One subsection per approved component. The pack-implementer reads each
subsection verbatim and pastes the docstring into the scaffolded file.>

### 2.1 — `<component_name>`

**Granularity** : <primitive | composition | block>
**Strategy** : <reuse_as_is | reuse_adapted | create_new | ad_hoc>
**Source clusters** (from `pe-discovery.md`) : <list of cluster IDs>

#### Docstring contract (paste verbatim into `<component_name>.py`)

```python
"""
## Visual

<1-2 sentence visual description : what does the user see ?>

## Structure

<the structural intent — which primitives compose this component.>

## Styling rules

<which Style bundles / which palette colors / what spacing.>

### INVARIANTS

- <Non-negotiable property #1. E.g. "Title is always exactly 1 line, never wrapped.">
- <Non-negotiable property #2.>
- <Non-negotiable property #3.>

### PARAMS

- `<param>: <type> = <default>` — <what it controls>
- `<param>: <type> = <default>` — <what it controls>

### INTERDITS

- <Anti-pattern #1. E.g. "Never use this for a >3-bullets list — use `takeaways` instead.">
- <Anti-pattern #2.>

## When to use

<2-4 bullets describing the situations where this component fits.>

## When NOT to use

<At least 2 bullets describing situations where another component or ad-hoc code fits better.>

## Design system bundles required

- `<bundle>.<attr>` — <how it's used>
- `<bundle>.<attr>` — <how it's used>
"""
```

#### `__component_meta__` (paste verbatim)

```python
__component_meta__: ComponentMeta = {
    "name": "<component_name>",
    "description": "<one-liner from Visual section>",
    "tags": ["<granularity>", "<dominant tag>"],
    "extrapolable": <True | False>,
    "since": "<YYYY-MM-DD>",
    "bundles_required": [
        "<bundle>.<attr>",
        ...
    ],
    "granularity": "<primitive | composition | block>",
    "uses_components": [],  # optional ; list for compositions/blocks
}
```

#### Function signature

```python
def <component_name>(*, design_system, <param1>, <param2>=<default>, ...): ...
```

#### Implementation sketch (non-binding ; pack-implementer may refine)

```python
def <component_name>(*, design_system, title, body, kind="info"):
    ds = design_system
    with st_block(ds.callouts[kind]):
        st_write(ds.callouts.title, title)
        st_write(ds.callouts.body, body)
```

#### Source occurrences extracted (for traceability)

- `<project>/<block_file>:<line_range>` — original snippet.
- `<project>/<block_file>:<line_range>`

---

### 2.2 — `<next_component_name>`

(same structure)

## 3. Naming conflicts resolved

| Original cluster name | Conflict with | Final name | Rationale |
|---|---|---|---|
| `callout` | `streamtex-design:callout` | `domain_callout` | The fork's variant uses a different palette and adds a `severity` PARAM not present upstream. |

## 4. Rejected designs

<Components considered during DESIGN but discarded — e.g. semantic
duplicate, contract too narrow to be reusable, INVARIANT impossible to
satisfy with available DS bundles.>

| Candidate | Reason |
|---|---|
| `proj_a_hero` | Too project-specific (depended on `bs.proj_a_accent` — should be a project style override). |
| `tiny_note` | Indistinguishable from existing `streamtex-design:cite` after contract analysis. |

## 5. Bundle coverage matrix

<Cross-check that every `bundles_required` declared is provided by the
target DS. If gaps exist, document them in §4 of `pack-master-plan.md`.>

| Bundle | Provided by `<active_DS>` | Required by components |
|---|---|---|
| `callouts.info` | ✓ | info_callout, warning_callout |
| `callouts.body` | ✓ | info_callout, key_takeaways |
| `compare.left_palette` | ✗ MISSING | comparison_card_grid |

## 6. Next gate

→ **G2 (post-DESIGN)** : `pack-orchestrator` surfaces the QCM :

> "<N> composants conçus avec contrat complet. Recommandé : approuver
> tous, sauf <K> qui ont des conflits non résolus.
> Que faites-vous ?"
>
> - Tout approuver et passer à l'implémentation (Recommandé)
> - Recommandés uniquement (excluant les conflits)
> - Sélection à préciser (drill-down par composant)
> - Réviser un composant en particulier
> - Discutons-en
