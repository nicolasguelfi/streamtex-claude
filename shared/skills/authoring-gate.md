# Authoring Gate

The **single contract** every block-authoring path runs **before writing any
block**, regardless of entry point — the CE pipeline (`/stx-ce:prototype`,
`/stx-ce:produce`) **and** the direct commands (`/stx-block:new`,
`/stx-block:slide-new`, `/stx-block:init`). It guarantees that the three
fundamental elements of StreamTeX document construction are always in place:

1. **The plan** — what to build, in coherence with the document.
2. **The design rules** — how the content is represented graphically, per the
   document type.
3. **The packs/components** — the technical building blocks and how to implement
   them for the intended representation.

Skipping the gate is a defect: it is exactly how the GSE-ODOO document was
produced (50 blocks, no plan discipline, no design agent, no component reuse →
0/20). The gate makes the trinity systematic, not optional.

## The gate (run in order, before writing)

### Step A — Plan (precondition)

1. Load `docs/master-plan.yaml` (+ the current increment plan in `docs/plans/`).
2. **If absent**, soft-block with a QCM (never silently proceed):
   - `Créer un plan minimal (1 incrément) (Recommandé)` — bootstrap a minimal master plan + a one-item increment, then continue.
   - `Continuer en ad-hoc assumé` — proceed without a plan **for this single block only**; record the override in `decisions_log`. Use for genuine one-off touch-ups, not for building a document.
   - `Lancer /stx-ce:plan` — go plan properly first.
3. Confirm the target block is in (or added to) the plan before authoring.

### Step B — Design rules + agent (by document type)

1. Read `docs/master-plan.yaml -> identity.type` (`presentation | manual | report | course | collection`).
2. Resolve the design layers: neutral base `visual-design-rules.md` **+** the format overlay:
   - `presentation` → `slide-design-rules.md`
   - `manual` / `report` / `collection` (hub) → `web-document-design-rules.md`
   - `course` → `web-document-design-rules.md` + `course-design-rules.md`
3. Resolve the **active guideline** (`# @guideline:` > `custom/design-guideline.md` > project default). If a slide/document project has **no** guideline, surface the design-guideline QCM (see `ce-assess` R27) and persist the choice to `custom/design-guideline.md`.
4. Select the **designer specialization** for the type (`slide-designer` /
   `web-document-designer` / `course-designer`) — authoring is delegated to it
   in Step D, never done freehand.

### Step C — Component resolution (packs)

1. Run `stx component list` (read `reuse-architecture` + `modular-design-philosophy`).
2. For the block, decide and **record the decision**:
   - **reuse** an existing component, or
   - **adapt** one with parameters, or
   - **create** a local component (`./mypack/`), or
   - **one-off justified** — bespoke structure, with a written justification.
3. Write the decision into `master-plan.yaml -> components.applied` (which block,
   which component, `level: shared|local|none`). Authoring a block "from scratch"
   without a component requires the explicit one-off justification.

### Step D — Author, then visual gate

1. Invoke the selected **designer specialization** to author the block (it applies
   base + overlay + guideline + the resolved component + project palette).
2. Run `/stx-block:audit --target <block>` (structural correctness).
3. Run the **visual gate**: `stx screenshot` → vision review by `visual-reviewer`
   (or `slide-reviewer` for slides) → self-correct loop for any auto-detected
   defect (unreadable fonts, > ~40% empty viewport, overflow, overcrowding,
   missing TOC entries / part-intros). This runs even in autonomous /
   `/remote-control` mode.

## Dialog level

- `minimal`: Steps A-C apply recommended defaults silently **except** the
  plan-absent soft-block (Step A.2) and a missing guideline (Step B.3), which
  always surface — both were silently wrong in GSE-ODOO.
- `guided` / `exhaustive`: each decision surfaces its QCM.

## Notes

- The gate is **doc-type-agnostic**: it works identically for a pitch deck, a
  manual, a course, or a collection hub — only the resolved overlay/agent differ.
- Callers invoke the gate, they do not re-implement it — this is the single
  source of truth so CE and the direct commands never drift apart.
