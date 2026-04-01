# /stx-ce:plan — Plan document production

Arguments: $ARGUMENTS

## Options

- `--interactive` — Enable 4-step collaborative planning (skeleton > objectives > design > plan)
- `--deep` — Run all agents in parallel for comprehensive research before planning
- `--gap-analysis` — Run source gap analysis after initial plan (mandatory for Pathway C sources >500 lines)
- `--help` — Show stx-ce cheatsheet

## Description

Creates a structured production plan from the assessment. Supports two modes:

- **Auto** (default): Generates the plan in a single pass. Best for small documents or simple improvements.
- **Interactive** (`--interactive`): 4-step collaborative planning where the user validates each layer:
  1. **Structure pass**: Propose sequence/block list (titles only). User validates, reorders, adds, removes.
  2. **Content pass**: For each validated block, propose detailed content objectives. User validates block by block.
  3. **Design pass**: Propose design choices (guideline, archetypes, patterns). User adjusts.
  4. **Consolidation pass**: Assemble final plan for overall review.
  Best for complex documents or when the author has strong opinions on structure.

The plan varies by pathway (import/improve/create) and includes: document skeleton, per-section objectives, design choices, execution order, pre-production checklist, and **design guideline** (name, reference path, and how it affects block production).

### Source Gap Analysis

For Pathway C (create from source), a **source gap analysis** phase runs after the initial plan to counter confirmation bias. This phase is mandatory when source documents exceed 500 lines, and optional otherwise. Use `--gap-analysis` to force it.

**Steps**:
1. **Extract plan themes** — List all topics covered by the initial plan
2. **Inverse search** — Scan the source document for sections/paragraphs NOT matching any plan theme
3. **Relevance filter** — Evaluate each unmatched section against the document objectives from the assessment
4. **Enrich** — Add high-relevance discoveries to the plan as new items or enrichments to existing items
5. **Document** — Record what was found, what was added, and what was deliberately excluded (with reasons)

The gap analysis output is appended to the plan document under a `## Source Gap Analysis` heading.

If a guideline is active, the structure proposals must respect its principles. Each planned block is mapped to its expected guideline archetype (text-dominant, image-dominant, etc.), and the guideline's recommended PresentationProfile values are included.

## Examples

- `/stx-ce:plan` — Auto mode from latest assessment
- `/stx-ce:plan --interactive` — Collaborative 4-step planning
- `/stx-ce:plan --interactive --deep` — Deep research + interactive planning

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-plan.md` — Full workflow
2. `docs/assess/` — Latest assessment document
3. `.claude/designer/skills/block-blueprints.md` — Block catalog for structure planning
4. `.claude/designer/templates/` — Available project templates
5. If Pathway C with sources >500 lines: source gap analysis is mandatory (see above)
- If assess report references a design guideline, load it from `.claude/designer/guidelines/<name>.md`
- **Pattern mapping**: For each planned block, check if an existing named pattern
  from `custom/design-guideline.md ## Patterns` applies. If so, reference it in the plan.
  This avoids redesigning components that already have a proven recipe.

## Workflow

Execute the `ce-plan` skill. GATE: The plan must be validated by the user before proceeding to production.
