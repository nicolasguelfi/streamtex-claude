# CE Prototype

Skill for the PROTOTYPE phase of the Compound Engineering cycle. Sits between PLAN and PRODUCE. Validates visual styles and identifies / reuses graphic patterns **by example** — by producing one (or a small set of) pilot block(s), extracting reusable patterns, and validating the design with the user before mass production.

Read `.claude/ce/skills/ce-conventions.md` before invoking any user-facing question. All interactions follow the universal QCM format with `(Recommandé)` + `Discutons-en` + auto-injected `Autre`.

## When this phase runs

PROTOTYPE runs when at least one of the following is true:

- The current iteration is the first iteration of the document (no patterns validated yet for the visual territory).
- The current increment introduces new transverse design decisions that differ from previous iterations (new palette, new profile, new layout pattern).
- The user explicitly requested validation of styles before production.

It is skipped when the increment continues an already-validated visual territory and all patterns are already in the catalog. In `dialog_level: minimal`, the skip decision is silent; in `guided` or `exhaustive`, a QCM confirms the recommendation.

## Workflow

### Phase 1: Load Context

1. Load `docs/master-plan.yaml` and `docs/master-plan.md`.
2. Load the current plan increment from `docs/plans/` (most recent).
3. Load the producer profile (`dialog_level`, favorite patterns, anti-patterns).
4. Read the components catalog (``stx component list` output` and individual `<component>.py` files for any pattern listed in the plan).
5. Determine the increment scope from the master plan iterations entry.

### Phase 2: Select Pilot Block(s)

Use the `prototype-designer` agent to select the pilot block(s):

- **Default**: one representative block (typically the first block of the increment scope that exercises the chosen palette + at least one structural pattern).
- **Set mode** (user opts in via QCM): one block per distinct archetype in the increment (title, content, code-demo, callout-heavy, etc.).

Surface QCM:

*"Produire un seul bloc pilote ou un jeu couvrant les archétypes du scope ?"*

Options:
- `Un seul bloc pilote (Recommandé)`
- `Un jeu couvrant les archétypes`
- `Discutons-en`

### Phase 3: Plan Patterns for the Pilot

For the chosen pilot block(s), the `prototype-designer` agent proposes a pattern strategy:

- For each visual component expected in the pilot (heading, callouts, grids, code box, etc.), decide: **reuse existing pattern**, **adapt an existing pattern with parameters**, or **create a new pattern from scratch**.
- For each decision, justify in prose (the recommendation rationale).

Surface QCM (multi-select if several patterns are proposed):

*"Patterns proposés pour le bloc pilote. Recommandé : <liste explicite>. Que faites-vous ?"*

Options:
- `Tout (Recommandé)` — applies the full proposal
- `Recommandés uniquement` — applies the subset marked recommended
- `Sélection à préciser` — drill down to a per-pattern dialog
- `Discutons-en`

### Phase 4: Produce the Pilot Block(s)

For each pilot block:

1. Scaffold the block with `/stx-block:new` (or `/stx-block:slide-new` for presentations).
2. **Author the block through the `authoring-gate` skill** (`.claude/shared/skills/authoring-gate.md`) — never freehand. The gate resolves the plan, the design rules + designer specialization **for this document's `identity.type`** (slide-designer / web-document-designer / course-designer), and the component to apply, then delegates authoring to that specialization with the patterns validated in Phase 3. This is identical for every document type — only the resolved overlay/agent differ.
3. Use the `Propositions brutes` from `master-plan.md` for the pilot's section as initial content.
4. Run `/stx-block:audit --target <block>` to verify structural correctness.
5. Update `master-plan.yaml -> toc[*].sections[*].blocks[*].status` to `prototyped`.

### Phase 5: Automated Visual Gate (capture + vision review) — MANDATORY

A `ruff`/import smoke-test is **not** a visual validation. Before involving the user, validate what actually renders:

1. **Capture** — run `stx screenshot` to render the pilot block(s) to PNGs in `docs/_screens/` (full-page + per-`.stx-block`). If Chromium is missing, run `uv run playwright install chromium` (auto-installed by `stx install`).
2. **Vision review** — invoke the `visual-reviewer` (or `slide-reviewer` for slide projects) agent. It opens the PNGs and auto-detects, per slide, the defects that must never reach the user: unreadable fonts (projection floor), > ~40% empty viewport, content overflow/clipping, overcrowding (> ~6 dense cells), missing TOC entries, missing part-intros.
3. **Self-correct loop** — for every auto-detected defect, fix it (re-invoke `slide-designer`) and **re-capture**. Iterate until the rendered pilots are clean. Only auto-detectable defects are gated here; subjective/editorial calls go to the user in Phase 6.

This phase is never skipped — not even in `dialog_level: minimal` and not in autonomous / `/remote-control` runs (there the agent's vision review *replaces* the human eye, it does not bypass the gate).

### Phase 6: User Validation

The pilot has already passed the automated visual gate (Phase 5). Present the captured screenshots (`docs/_screens/`) and the vision-review summary, then surface QCM — the user now judges only the *subjective/editorial* choices (tone, palette, message density), not the mechanical defects already caught:

*"Bloc pilote produit et validé visuellement (auto-revue : <n défauts corrigés>). Voici le rendu (docs/_screens/). Confirmez les choix éditoriaux."*

Options:
- `Valider et continuer (Recommandé)`
- `Ajuster les styles avant production`
- `Repartir d'une autre piste`
- `Discutons-en`

If `Ajuster` or `Repartir`: loop back to Phase 3 with the user's input. If `Valider`: proceed to Phase 7.

### Phase 7: Pattern Capture (draft → local)

For each new composition that emerged from the pilot and is not yet in the catalog, surface a QCM:

*"Composition visuelle candidate à devenir un pattern nommé : <description>. La capturer dans le catalogue local ?"*

Options:
- `Oui, capturer dans le catalogue local (Recommandé)` — runs `stx component new <name>` (extracting the visual idiom from `<pilot_block>` into the new component scaffold), writing to the primary local pack (`./mypack/components/`)
- `Non, garder en code ad-hoc`
- `Renommer / ajuster avant de capturer`
- `Discutons-en`

For each component captured, update `master-plan.yaml -> components.applied` with `level: local` and the pilot block in `blocks: [...]`.

Multi-select aggregated component capture is used when several candidates are proposed at once (see `ce-conventions.md`).

### Phase 8: Write Prototype Report

Write the report to `docs/prototypes/YYYY-MM-DD-NNN-<scope>-prototype.md` using the `prototype-report` template.

Update `master-plan.yaml`:
- Append the report to `pointers.prototypes`.
- Set the iteration's `artifacts.prototype` field.

### Phase 9: GATE — Continue to PRODUCE

Surface QCM:

*"Le prototypage est validé. Continuer la production des blocs restants du scope ?"*

Options:
- `Oui, lancer PRODUCE (Recommandé)`
- `Non, je veux ajuster le plan d'abord`
- `Discutons-en`

If `Oui`: suggest `/stx-ce:produce`. If `Non`: suggest `/stx-ce:task "amend plan"` or `/stx-ce:plan` (re-planning).

Append a `decisions_log` entry for every QCM in this phase.

## Dialog level

- `minimal`: only Phase 6 (validation) and Phase 9 (continue gate) surface QCMs. Other phases apply recommendations silently. A synthesis is shown at the end.
- `guided` (default): all phases surface their QCMs.
- `exhaustive`: in Phase 4, also surface per-block style QCMs; in Phase 7, drill down to per-pattern dialog.

## Output

Phase 8 writes the prototype report. The pilot block(s) remain in `blocks/` with status `prototyped` in the YAML; they will be picked up by PRODUCE (which sees their status and either leaves them as-is or refines them).
