# Template: Master Plan

> **Nature of this file** — schema reference, not a copy source. CE skills (`ce-assess`, `ce-continue`, `ce-plan`, etc.) read this template to know the structure of the runtime files, then **construct** `docs/master-plan.yaml` and `docs/master-plan.md` programmatically from user input and contextual inference. The orchestrator never copies this file directly to `docs/`.
>
> When the schema evolves, edit this single file — both runtime files derive from it. This document is also the canonical source for fields referenced as `master-plan.yaml -> <field>` across all skills, agents, and other templates (see check 26 of the coherence audit).

The **master plan** is the living reference for the document being produced. It is stored as **two paired files** in the project's `docs/` directory:

- `docs/master-plan.yaml` — orchestration and automation metadata (machine-readable)
- `docs/master-plan.md` — detailed content plan (human-readable, may contain raw content drafts)

Snapshots are taken as paired files in `docs/master-plan/archive/YYYY-MM-DD-NNN.yaml` and `docs/master-plan/archive/YYYY-MM-DD-NNN.md` with identical timestamp prefix.

## When to read

Read both files at the start of every CE skill invocation. The YAML drives orchestration decisions (status, statuses, scope detection, objectives monitoring, decisions log). The MD drives content production (titles, content briefs, raw drafts, design notes).

## When to write

Update the relevant file(s) at the end of any CE skill that mutates state. If at least one of the two files differs from the most recent snapshot when a skill begins writing, take a new paired snapshot first (see Snapshot policy below).

## File 1 — `docs/master-plan.yaml`

```yaml
# Master plan — orchestration and automation
# Single source of truth for orchestration decisions

identity:
  title: <document title>
  type: <manual | presentation | course | report | collection>
  audience: <free text description of target audience>
  language: <fr | en | other>
  created: <YYYY-MM-DD>
  last_updated: <YYYY-MM-DD>

objectives:
  # Free-text criteria, consolidated by the LLM from user input and context.
  # No quantitative/structural/qualitative schema imposed.
  - id: O1
    title: <short title>
    description: <one-line description>
    criteria: |
      <free text consolidating success criteria from user dialogue and context>
    status: <pending | in_progress | met | unmet | abandoned>
    last_review: <YYYY-MM-DD or null>
  - id: O2
    # ...

toc:
  # Hierarchical TOC with per-node status. The MD file holds the narrative content;
  # this section holds the operational status only.
  - id: P1
    title: <Part 1 title>
    status: <planned | in_progress | done>
    sections:
      - id: S1.1
        title: <Section 1.1 title>
        status: <planned | prototyped | produced | reviewed | fixed | done>
        blocks:
          - name: bck_intro
            status: <planned | prototyped | produced | reviewed | fixed | done>
            components: [<component_name>, ...]  # components applied to this block
      # ...

transverse_decisions:
  palette: <name or description, or null>
  presentation_preset: <responsive | presentation | desktop_mobile | custom | null>
  view_modes: {desktop: <PAGINATED|CONTINUOUS>, presenter: <...>, ...}
  bibliography: {source: <path or null>, format: <APA|...>, style: <NUMBERED|AUTHOR_YEAR>}
  ai_image: {provider: <openai|google|fal|null>, model: <...>, default_size: <...>}
  export: {asset_mode: <EMBEDDED|EXTERNAL>, mode: <ALWAYS|MANUAL|NEVER>}
  spacing: <free text or structured config reference>
  active_guideline: <name or null>

components:
  # Mapping: component_name -> blocks using it. Source of truth for inter-iteration consistency.
  catalog_location: <the primary local pack (./mypack/components/) | other>
  applied:
    - name: <component_name>
      level: <draft | local | shared>  # draft=docs/solutions, local=primary local pack, shared=git/pypi pack
      blocks: [bck_..., bck_...]
      promoted_at: <YYYY-MM-DD or null>

iterations:
  # One entry per CE cycle executed.
  - sequence: 1
    started: <YYYY-MM-DD>
    completed: <YYYY-MM-DD or null>
    scope: <document | part:P1 | section:S1.1 | blocks:[...]>
    pathway: <A | B | C | A+B | mixed>
    summary: <one-line summary of what was produced or improved>
    artifacts:
      assess: <docs/assess/...>
      plan: <docs/plans/...>
      prototype: <docs/prototypes/... or null>
      review: <docs/reviews/...>
      solutions: [<docs/solutions/...>, ...]

decisions_log:
  # Append-only. One entry per user QCM answer captured by the orchestrator.
  - timestamp: <YYYY-MM-DDTHH:MM:SSZ>
    question: <verbatim question text>
    options_presented: [<option1>, <option2>, "Let's discuss", "Other"]
    recommendation: <option that carried the (Recommended) suffix>
    answer: <option selected, or free text if "Other", or summary of dialogue if "Let's discuss">
    skill: <which CE skill captured this decision>
  # ...

coherence_debt:
  # Entries created when the user refuses a reconciliation or pattern re-application.
  # The orchestrator surfaces these periodically.
  - id: <unique id>
    created: <YYYY-MM-DD>
    description: <what was refused and what divergence remains>
    affected_blocks: [bck_..., ...]
    resolution: <null | resolved on YYYY-MM-DD with description>

pointers:
  # Convenience references to other CE artifacts of this project.
  collect: [<docs/collect/...>, ...]
  assess: [<docs/assess/...>, ...]
  plans: [<docs/plans/...>, ...]
  prototypes: [<docs/prototypes/...>, ...]
  reviews: [<docs/reviews/...>, ...]
  solutions: [<docs/solutions/...>, ...]
  producer_profile: <docs/solutions/producer-profile.md or null>

status_legend:
  # Stable reference for what each status means. Embedded so the file is self-describing.
  block:
    planned: "Listed in TOC, not yet produced."
    prototyped: "Validated as a pilot block in PROTOTYPE phase."
    produced: "Content written and audited."
    reviewed: "Reviewed by the multi-agent review phase."
    fixed: "Findings from review applied."
    done: "Ready for delivery."
  objective:
    pending: "Stated but not yet acted upon."
    in_progress: "Partially addressed by produced content."
    met: "Verified as fully addressed."
    unmet: "Identified as not addressed; surfaced to user with proposals."
    abandoned: "Explicitly dropped by user with justification in decisions_log."
```

## File 2 — `docs/master-plan.md`

```markdown
# Master Plan — <document title>

> Detailed content plan. Source of truth for block production.
> References `docs/master-plan.yaml` for orchestration and statuses.

## Overview

<Free paragraph describing the document, its audience, its pedagogical or
editorial intent. Should reflect what was captured in ASSESS and refined
across iterations.>

## Objectives

<Numbered list of objectives in prose. For each: a readable formulation of
what must be achieved, followed in italics by the current status.>

1. **<Objective 1>** — <prose description>. *(in progress / met / unmet / abandoned)*
2. **<Objective 2>** — <description>. *(...)* 

## Transverse decisions

<Narrative section consolidating palette, presentation profiles, bibliography,
AI images, export, spacing, active guideline choices. Directly readable by
the user. The structured form lives in the YAML.>

- **Palette**: <prose description>
- **Presentation profiles**: <prose description>
- **Bibliography**: <prose description or "none">
- **AI images**: <prose description or "none">
- **Export**: <prose description>
- **Active guideline**: <name or "none">

## Detailed table of contents

> For each TOC node: title, intent, sources, design notes, draft content
> proposals. Subsections may descend to any depth (section / subsection /
> sub-subsection).

### Part 1 — <Title>

**Intent**: <what this part should produce in the reader>.

#### Section 1.1 — <Title>

**Intent**: <what this section should produce>.

**Sources**:
- <reference to collected material, page, chapter, URL>
- ...

**Design notes**:
- <applicable components, visual constraints>

**Draft content proposals**:

> <Content draft — may be written text, bullet points, examples, callout
> sketches. This content will be refined in PRODUCE then transposed into
> StreamTeX blocks.>

##### Subsection 1.1.1 — <Title>

<Same structure as above, recursive to the depth of the document.>

#### Section 1.2 — <Title>
<...>

### Part 2 — <Title>
<...>

## Visual components used

<Prose list of catalog components used, with their level (draft / local /
shared) and the blocks that consume them.>

- `<component_name>` (local) — used in <block(s)>. <Optional notes on the
  applied extrapolation>.

## Coherence debt

<This section exists only if at least one divergence is documented. Each
entry results from a refused reconciliation or refused component
re-application, captured in a QCM.>

- **<id>** (created on <date>) — <divergence description>. Affected blocks:
  <list>. Resolution: <pending / resolved on <date>>.

## Risks and watch points

<Optional section, useful when objectives are `unmet` or production hits
structural obstacles.>

## Iteration history

<Brief prose summary of executed CE cycles. Technical details live in the YAML.>

- **Iteration 1** (<date>) — scope: <document/part/section>. <One or two
  sentences on what was produced or improved>.
- **Iteration 2** — ...
```

## Snapshot policy

A new paired snapshot is written to `docs/master-plan/archive/YYYY-MM-DD-NNN.{yaml,md}` (incrementing NNN per day starting at 001) **only if at least one of the two files differs from the most recent snapshot**. This naturally enforces "at most one snapshot per session" while allowing context-justified additional snapshots.

The user may explicitly request a snapshot at any time. The orchestrator may propose one (QCM, default "Yes") before destructive operations (TOC removals, large refactors, batch reconciliations) or at session end ("soft interruption").

## Reconciliation policy

When the orchestrator detects divergence between `book.py` (the live `bck_*` registry order) and the master plan TOC, it produces a single proposal with the full reconciliation reasoning, presented as a QCM:

- **Apply the global proposal** *(Recommended)*
- **See block-by-block detail** (drills down to per-divergence QCM)
- **Let's discuss**
- (Other — auto-injected)

If the user refuses individual divergences, those become entries in `coherence_debt`.

## Decisions log format

Every QCM presented to the user (in any CE skill) is appended to `decisions_log` with the structure shown above. The `dialog_level` of the producer profile is **not** recorded — the decision is what matters, not the conversational mode active at the time.

## Multi-project policy

Out of scope. The master plan assumes a single document per session.

## Independence from git

Snapshots do not reference git commit hashes. The master plan archive is a self-contained history independent from `git log`.
