# Template: Master Plan

The **master plan** is the living reference for the document being produced. It is stored as **two paired files** in the project's `docs/` directory:

- `docs/master-plan.yaml` — pilotage and automation metadata (machine-readable)
- `docs/master-plan.md` — detailed content plan (human-readable, may contain raw content drafts)

Snapshots are taken as paired files in `docs/master-plan/archive/YYYY-MM-DD-NNN.yaml` and `docs/master-plan/archive/YYYY-MM-DD-NNN.md` with identical timestamp prefix.

## When to read

Read both files at the start of every CE skill invocation. The YAML drives orchestration decisions (status, statuses, scope detection, objectives monitoring, decisions log). The MD drives content production (titles, content briefs, raw drafts, design notes).

## When to write

Update the relevant file(s) at the end of any CE skill that mutates state. If at least one of the two files differs from the most recent snapshot when a skill begins writing, take a new paired snapshot first (see Snapshot policy below).

## File 1 — `docs/master-plan.yaml`

```yaml
# Master plan — pilotage et automatisation
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
            patterns: [<pattern_name>, ...]  # patterns applied to this block
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

patterns:
  # Mapping: pattern_name -> blocks using it. Source of truth for inter-iteration consistency.
  catalog_location: <.claude/custom/streamtex-patterns/ | other>
  applied:
    - name: <pattern_name>
      level: <draft | local | shared>  # draft=docs/solutions, local=catalog, shared=streamtex-patterns repo
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
    options_presented: [<option1>, <option2>, "Discutons-en", "Autre"]
    recommendation: <option that carried the (Recommandé) suffix>
    answer: <option selected, or free text if "Autre", or summary of dialogue if "Discutons-en">
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

> Plan détaillé du contenu. Source de vérité pour la production des blocs.
> Référence le fichier `docs/master-plan.yaml` pour le pilotage et les statuts.

## Vue d'ensemble

<Paragraphe libre décrivant le document, son public, son intention pédagogique
ou éditoriale. Doit refléter ce qui a été capté en ASSESS et raffiné au fil
des itérations.>

## Objectifs

<Liste numérotée des objectifs en prose. Pour chacun, une formulation lisible
de ce qui doit être atteint, suivie en italique de l'état actuel.>

1. **<Objectif 1>** — <description en prose>. *(en cours / atteint / non atteint / abandonné)*
2. **<Objectif 2>** — <description>. *(...)* 

## Décisions transverses

<Section narrative consolidant les choix de palette, profils, bibliographie,
images IA, export, spacing, guideline active. Lisible directement par
l'utilisateur. La forme structurée est dans le YAML.>

- **Palette** : <description en prose>
- **Profils de présentation** : <description en prose>
- **Bibliographie** : <description en prose ou "aucune">
- **Images IA** : <description en prose ou "aucune">
- **Export** : <description en prose>
- **Guideline active** : <nom ou "aucune">

## Table des matières détaillée

> Pour chaque nœud du TOC : titre, intention, sources, notes de conception,
> propositions brutes de contenu. Les sous-sections peuvent descendre à
> n'importe quel niveau (section / sous-section / sous-sous-section).

### Partie 1 — <Titre>

**Intention** : <ce que cette partie doit produire chez le lecteur>.

#### Section 1.1 — <Titre>

**Intention** : <ce que cette section doit produire>.

**Sources** :
- <référence au matériel collecté, page, chapitre, URL>
- ...

**Notes de conception** :
- <choix de blueprint, patterns applicables, contraintes visuelles>

**Propositions brutes de contenu** :

> <Brouillon de contenu — peut être du texte rédigé, des bullet points,
> des exemples, des esquisses de callouts. Ce contenu sera affiné en
> PRODUCE puis transposé en blocs StreamTeX.>

##### Sous-section 1.1.1 — <Titre>

<Même structure que ci-dessus, récursive selon la profondeur du document.>

#### Section 1.2 — <Titre>
<...>

### Partie 2 — <Titre>
<...>

## Patterns visuels mobilisés

<Liste en prose des patterns du catalogue utilisés, avec mention de leur
niveau (brouillon / local / partagé) et des blocs qui les consomment.>

- `<pattern_name>` (local) — utilisé dans <bloc(s)>. <Notes éventuelles sur
  l'extrapolation appliquée>.

## Dette de cohérence

<Cette section n'existe que si au moins une divergence est documentée.
Chaque entrée résulte d'un refus de réconciliation ou de ré-application
de pattern, capturé en QCM.>

- **<id>** (créée le <date>) — <description de la divergence>. Blocs
  concernés : <liste>. Résolution : <pendante / résolue le <date>>.

## Risques et points d'attention

<Section facultative, utile quand des objectifs sont en `unmet`
ou que la production rencontre des obstacles structurants.>

## Historique des itérations

<Bref résumé en prose des cycles CE exécutés. Détails techniques dans le YAML.>

- **Itération 1** (<date>) — scope : <document/part/section>. <Une à deux
  phrases sur ce qui a été produit ou amélioré>.
- **Itération 2** — ...
```

## Snapshot policy

A new paired snapshot is written to `docs/master-plan/archive/YYYY-MM-DD-NNN.{yaml,md}` (incrementing NNN per day starting at 001) **only if at least one of the two files differs from the most recent snapshot**. This naturally enforces "at most one snapshot per session" while allowing context-justified additional snapshots.

The user may explicitly request a snapshot at any time. The orchestrator may propose one (QCM, default "Oui") before destructive operations (TOC removals, large refactors, batch reconciliations) or at session end ("interruption douce").

## Reconciliation policy

When the orchestrator detects divergence between `book.py` (the live `bck_*` registry order) and the master plan TOC, it produces a single proposal with the full reconciliation reasoning, presented as a QCM:

- **Appliquer la proposition globale** *(Recommandé)*
- **Voir le détail bloc par bloc** (drills down to per-divergence QCM)
- **Discutons-en**
- (Autre — auto-injected)

If the user refuses individual divergences, those become entries in `coherence_debt`.

## Decisions log format

Every QCM presented to the user (in any CE skill) is appended to `decisions_log` with the structure shown above. The `dialog_level` of the producer profile is **not** recorded — the decision is what matters, not the conversational mode active at the time.

## Multi-project policy

Out of scope. The master plan assumes a single document per session.

## Independence from git

Snapshots do not reference git commit hashes. The master plan archive is a self-contained history independent from `git log`.
