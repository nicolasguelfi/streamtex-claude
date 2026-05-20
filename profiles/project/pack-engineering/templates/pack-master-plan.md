# Pack Master Plan — <pack-name>

> Narrative companion to `pack-master-plan.yaml`. Lives at
> `docs/pack-engineering/pack-master-plan.md` in the pilot project.
> The YAML carries structured state ; this file carries the *why*.

**Date** : <YYYY-MM-DD>
**Mode** : bootstrap | specialize | refine | audit
**Pilot project** : <path>
**Consumer projects** : <proj-a, proj-b, …>
**Target pack** : <name> at `<target_path>`
**Upstream pack** (specialize only) : <ref>

---

## 1. Objectives

<Why are we doing this PE cycle ? What pain point are we addressing ?>

- Decrease duplication across blocks of <consumer-projects>.
- Stabilize a shared visual vocabulary for future documents.
- (Specialize) extend `<upstream>` with the project-domain idioms it
  doesn't cover.
- (Refine) capture the patterns that emerged in the latest production
  iteration without going through a full bootstrap.

## 2. Constraints

### Semver policy (target pack)

<Patch / minor / major rules — see `pe-conventions.md` §7.>

### Naming policy

- snake_case, English-only, descriptive.
- No project-specific tokens (e.g. `ai4se_callout` forbidden, `info_callout` allowed).
- Granularity tag must match actual size : `primitive` < 30 lines, `composition` 30-100, `block` > 100.

### Upstream PR policy (specialize only)

- Components mature enough (used in ≥ 2 consumer projects, no project-specific tokens, contract stable for ≥ 1 month) are eligible for upstream promotion.
- The PR title format : `feat: add <component> from <fork-pack-name>`.

## 3. Per-component justification

<Filled by pack-designer ; one subsection per approved component.>

### <component-name>

- **Granularity** : <primitive | composition | block>
- **Discovered in** : <list of (project, block) sources>
- **Justification** : <why is this worth extracting ? what would happen without ?>
- **Bundles required** : <list>
- **INVARIANTS** : <short summary of the contract's non-negotiable elements>
- **PARAMS** : <what varies>
- **INTERDITS** : <what should never be used for>

## 4. Open questions

<Things that need user decision but not via QCM gate.>

- [ ] Should `<comp-X>` and `<comp-Y>` be merged ? They overlap on `<aspect>`.
- [ ] DS bundle `<bundle>` is required by N components but not yet in `streamtex-pack-design.default` — propose to upstream ?

## 5. Decisions log (narrative)

<Mirrored from pack-master-plan.yaml.decisions_log but with surrounding context.>

### 2026-05-19 — G1 mining_validated

Accepted 12 candidates out of 18 discovered. Rejected 6 :
- 2 were 1-occurrence singletons (below threshold).
- 3 were project-specific (used proj-a's accent color directly — should be a project style override, not a pack component).
- 1 was indistinguishable from `streamtex-pack-design:callout` (the system flagged duplicate ; no need to re-create).
