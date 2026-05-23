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

> "Analysis found <N> candidates to extract across <M> projects.
> Recommended (≥ 2 projects AND ≥ <threshold> occurrences): <K>.
> What do you do?"
>
> - Approve the full recommended list (Recommended)
> - Selection to be specified (drill-down per candidate)
> - Widen to include single-project candidates (+<X>)
> - Let's discuss

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

> "<N> components designed with full contract. <C> conflicts resolved.
> <R> components rejected (reason: <r>).
> What do you do?"
>
> - Approve all and proceed to implementation (Recommended)
> - Recommended only (excluding unresolved conflicts)
> - Selection to be specified (drill-down per component)
> - Revise a specific component
> - Let's discuss

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

> "Retrofit plan ready: <N> blocks to rewrite across <M> projects, <K>
> skipped. Current mode: dry-run.
> What do you do?"
>
> - Apply all (Recommended)
> - Apply project by project (intermediate review)
> - Run a dry-run on a subset for inspection
> - Let's discuss

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

> "<N> blocks failed the smoke render after retrofit. What do you do?"
>
> - Revert the <N> blocks and continue without them (Recommended)
> - Inspect each block in detail
> - Cancel the entire retrofit
> - Let's discuss

Capture decision in `decisions_log`.

### Step 6 — AUDIT (auto-run after retrofit, optional standalone)

**Sub-mode** : auto-run after RETROFIT (bootstrap, specialize, refine) ;
standalone in audit-only mode.

**Invoke** : `pack-auditor`.

**Output** : `docs/pack-engineering/<ts>/audit-report.md`, populated
`audit` section. No gate (read-only).

**Duration** : 1-3 min.

Follow-up suggestion (not a gate) :

> "The audit identified <N> recommendations (<H> HIGH, <M> MEDIUM, <L> LOW).
> Do you want to launch a refine cycle to fix the HIGH items?"
>
> - Yes (Recommended)
> - No, keep the report for later
> - Let's discuss

### Step 7 — PUBLISH (optional, gated)

**Sub-mode** : opt-in only. Triggered by `/stx-pe:publish <pack-path>` or
by an explicit user request at the end of a bootstrap/specialize/refine
cycle.

Surface QCM :

> "The pack `<name>` is ready to publish (<count> components, version
> <new-version> computed). What do you do?"
>
> - Publish on PyPI + git tag (Recommended)
> - Git tag only (no PyPI)
> - Keep local, do not publish
> - Let's discuss

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

> "PE cycle complete. <summary>. Recommended next steps: <list>."

## Sub-mode skill references

| If sub-mode | Reads also |
|---|---|
| bootstrap | `pe-bootstrap.md` (entry-specific arg parsing) |
| specialize | `pe-specialize.md` |
| refine | `pe-refine.md` |
| audit | `pe-audit.md` (steps 6 only) |
| adopt-only | `pe-adopt.md` (step 4 only) |
| publish-only | `pe-publish.md` (step 7 only) |
