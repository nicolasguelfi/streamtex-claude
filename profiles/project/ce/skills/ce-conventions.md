# CE Conventions

Shared reference for all CE skills. Read this before invoking any QCM, before writing the master plan, before producing a snapshot, and before deciding the scope of a cycle.

## 1. QCM universel

Every interaction with the user goes through `AskUserQuestion`. The contract:

- **1 to 3 business options**, the first one suffixed `(Recommandé)`.
- **One option `Discutons-en`** that opens a free dialogue on the question.
- **`Autre`** is auto-injected by the QCM tool — never declare it in the options list.

The total of declared options must stay within the tool's limit of 4. In the common case: 1 recommended + 1 alternative + `Discutons-en` = 3 declared options. When relevant, a second alternative replaces or supplements one of these.

### 1.1 Recommendation rule

Every QCM has a recommended default. The LLM that emits the question must, before calling `AskUserQuestion`:

1. Compute its own recommendation using project state, master plan, producer profile, and conversation context.
2. Place that recommendation as option 1, with the `(Recommandé)` suffix and a short description of *why*.
3. Provide at least one alternative when relevant.
4. Always include `Discutons-en` as the last business option.

If no clear recommendation emerges, the LLM does **not** ask a closed QCM — it opens a `Discutons-en`-style dialogue from the start.

### 1.2 Multi-selection

When the question accepts multiple answers, use `multiSelect: true` and:

- Name the recommended subset explicitly in the question text (e.g., *"Recommandé : 1 et 3"*).
- Order options: recommended first, neutral second, risky last.

For lists longer than 4 candidate items, use the **aggregated pattern**:

- Option 1: `Tout` *(Recommandé)*
- Option 2: `Recommandés uniquement` (with the recommended subset described in the question text)
- Option 3: `Sélection à préciser` (the user replies with item numbers via `Discutons-en` or `Autre`)
- Option 4: `Discutons-en`

### 1.3 Dialog level modulation

The producer profile field `dialog_level` controls **frequency**, not format:

| Level | Behavior |
|---|---|
| `minimal` | QCM only at fundamental gates (post-PLAN, post-REVIEW, post-FIX, post-INTEGRATE). Sub-decisions silently apply the recommended default. A synthesis is shown at the end of each phase. |
| `guided` (default) | QCM at all structuring decisions: scope choice, pathway, design choices, PROTOTYPE confirmation, pattern promotion, reconciliation. |
| `exhaustive` | QCM even on minor choices: block naming, blueprint selection, style option tweaks. |

Regardless of level, the QCM format is identical (see 1.1).

## 2. Paths and filenames

| Artifact | Path |
|---|---|
| Master plan — pilotage (YAML) | `docs/master-plan.yaml` |
| Master plan — content (Markdown) | `docs/master-plan.md` |
| Master plan snapshots | `docs/master-plan/archive/YYYY-MM-DD-NNN.yaml` and `.md` |
| Assess reports | `docs/assess/YYYY-MM-DD-<name>-assess-<pathway>.md` |
| Plan increments | `docs/plans/YYYY-MM-DD-NNN-<scope>-<name>-plan.md` |
| Prototype reports | `docs/prototypes/YYYY-MM-DD-NNN-<scope>-prototype.md` |
| Review reports | `docs/reviews/YYYY-MM-DD-<name>-review.md` |
| Solutions | `docs/solutions/<category>/YYYY-MM-DD-<topic>.md` |
| Producer profile | `docs/solutions/producer-profile.md` |
| Pattern catalog (local) | the primary local pack (`./mypack/components/`) (default) or any a git/pypi pack declared in stx.toml in the project |

`YYYY-MM-DD-NNN` increments NNN per day, starting at 001, separately per artifact family.

## 3. Snapshot mechanism

A paired snapshot of the master plan (`<archive>/YYYY-MM-DD-NNN.yaml` + `<archive>/YYYY-MM-DD-NNN.md`) is written when **at least one of the two files differs from the most recent snapshot**. This rule naturally enforces "at most one snapshot per session" without an explicit session id.

Trigger points where snapshot must be considered:

1. At the start of any CE skill that may mutate state — compute diff against last snapshot; if different, snapshot before writing.
2. On user demand — QCM "Snapshot du plan actuel ? (Oui (Recommandé) / Non / Discutons-en)".
3. Before destructive operations (TOC removal, batch reconciliation, etc.) — same QCM, default `Oui`.
4. At session end via "interruption douce" — QCM with default `Oui`.

Retention: all snapshots are kept indefinitely. `ce-compound` proposes partial purge via QCM when the archive grows large.

Snapshots do **not** reference any git commit hash — they are git-independent.

## 4. Decisions log format

Every QCM presented to the user produces an entry in `master-plan.yaml -> decisions_log`:

```yaml
- timestamp: 2026-05-13T14:32:11Z
  question: "Avant de produire les 8 blocs de la section, je propose de produire un bloc pilote pour valider les styles. Procéder ainsi ?"
  options_presented: ["Oui (Recommandé)", "Non, produire directement", "Discutons-en", "Autre"]
  recommendation: "Oui (Recommandé)"
  answer: "Oui (Recommandé)"
  skill: ce-prototype
```

- `timestamp` is ISO 8601 UTC.
- `question` is the verbatim text shown to the user.
- `options_presented` lists every option, including `Discutons-en` and `Autre`, with the `(Recommandé)` suffix preserved on the recommended one.
- `recommendation` echoes the option that bore the `(Recommandé)` suffix.
- `answer` is either the selected option, the free text for `Autre`, or a one-paragraph summary of the dialogue that followed `Discutons-en`.
- `skill` identifies the CE skill that captured this decision.
- `dialog_level` is **not** recorded.

## 5. Reconciliation `book.py` ↔ master plan

At the start of any CE skill that may write blocks (`ce-produce`, `ce-fix`, `ce-task` write archetypes), and at the start of every `ce-continue` session, run reconciliation:

1. Compare the order of `bck_*` in `book.py` against the TOC `blocks` lists in `master-plan.yaml`.
2. Classify divergences: `added_in_code`, `missing_in_code`, `renamed`, `reordered`.
3. Present **a single proposal** built by the LLM covering all divergences. QCM:
   - Option 1: *"Appliquer la proposition globale"* `(Recommandé)`
   - Option 2: *"Voir le détail bloc par bloc"* (drill-down to per-divergence QCM)
   - Option 3: `Discutons-en`
4. Refused divergences become entries in `coherence_debt`.

If no divergence is detected, do not surface the topic — silent passage.

## 6. Reversibility of decisions

Entries in `decisions_log` can be reopened automatically by the orchestrator when new information emerges (new sources collected, divergent observations during REVIEW, contradictory user input). The reopening is itself a new QCM that references the prior decision in its question text:

> *"En itération 1 nous avions choisi <option> pour <question>. Les nouveaux éléments (<résumé>) suggèrent de reconsidérer. Que faites-vous ?"*

The orchestrator never silently overrides a prior decision — it always asks.

## 7. Objectives monitoring

Objectives in `master-plan.yaml -> objectives` have free-text criteria. The orchestrator (via the `objective-monitor` agent) judges status by reading the current state of the project, the master plan, and the latest review. It does not compute metrics — it produces a textual judgment.

Surface a question only when the judgment identifies a significant deviation. The judgment + proposal pair forms the QCM:

> *"L'objectif <id> (<title>) semble en retard : <judgment>. Proposition :"*
> 1. *"Ajouter une section dédiée au prochain incrément"* `(Recommandé)`
> 2. *"Réviser l'objectif"*
> 3. `Discutons-en`

In `dialog_level: minimal`, this surfacing is deferred to the next fundamental gate.

## 8. Patterns catalog levels

Three levels of pattern maturity:

| Level | Location | Promoted from | Promoted via |
|---|---|---|---|
| `draft` | `docs/solutions/style/patterns/` | extraction in PROTOTYPE or COMPOUND | automatic capture (no QCM at this step) |
| `local` | the primary local pack (`./mypack/components/`) | draft | QCM in PROTOTYPE (immediately) or COMPOUND |
| `shared` | `streamtex-design` pack (PR via `gh`) | local | QCM in INTEGRATE |

The orchestrator never auto-promotes to `local` or `shared`. The user decides via QCM.

## 9. Scope detection

The orchestrator (`ce-go`, `ce-continue`) detects the appropriate scope by reading the master plan:

| Master plan state | Default scope (recommended in QCM) |
|---|---|
| Absent or empty | Full document, first iteration (creates master plan in ASSESS) |
| TOC defined, 0 block produced | First section (PROTOTYPE expected) |
| TOC defined, partial production | Continue current section, or next planned section |
| All sections produced, review pending | Global review then fix |
| Document complete | New iteration on improvement, or end of project |

The QCM question reflects the detected state and proposes the corresponding scope as `(Recommandé)`. Alternatives are always available, plus `Discutons-en`.

## 10. Soft interruption

At the end of any CE skill or when the user signals end of session, propose a final snapshot via QCM with default `Oui`. If the master plan has not changed since the last snapshot, skip the QCM silently.

## 11. PROTOTYPE vs PRODUCE boundary

PROTOTYPE is concerned with **visual validation by example** and **pattern capture**. Its output is a small, validated set of pilot blocks plus an enriched local components catalog.

PRODUCE is concerned with **mass production at scale** of the increment's remaining blocks, applying the patterns validated in PROTOTYPE.

Auto-trigger rule for PROTOTYPE (decided in `ce-go` Step 3.5):

| Condition | PROTOTYPE recommendation |
|---|---|
| First iteration of the document, no pattern in catalog yet | `Oui` |
| Increment introduces a new visual territory (new palette, new profile, new layout class) | `Oui` |
| Increment continues a style territory already validated, all patterns already mapped | `Non` |
| User explicitly asks for design validation | `Oui` |

In all cases the QCM in `ce-go` Step 3.5 is the user's escape hatch from the auto-decision. In `dialog_level: minimal`, the QCM is skipped only when the recommendation is `Non`.
