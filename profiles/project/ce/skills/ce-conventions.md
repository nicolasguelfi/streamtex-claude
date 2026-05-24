# CE Conventions

Shared reference for all CE skills. Read this before invoking any QCM, before writing the master plan, before producing a snapshot, and before deciding the scope of a cycle.

## 1. Universal QCM

Every interaction with the user goes through `AskUserQuestion`. The contract:

- **1 to 3 business options**, the first one suffixed `(Recommended)`.
- **One option `Let's discuss`** that opens a free dialogue on the question.
- **`Other`** is auto-injected by the QCM tool — never declare it in the options list.

The total of declared options must stay within the tool's limit of 4. In the common case: 1 recommended + 1 alternative + `Let's discuss` = 3 declared options. When relevant, a second alternative replaces or supplements one of these.

### 1.1 Recommendation rule

Every QCM has a recommended default. The LLM that emits the question must, before calling `AskUserQuestion`:

1. Compute its own recommendation using project state, master plan, producer profile, and conversation context.
2. Place that recommendation as option 1, with the `(Recommended)` suffix and a short description of *why*.
3. Provide at least one alternative when relevant.
4. Always include `Let's discuss` as the last business option.

If no clear recommendation emerges, the LLM does **not** ask a closed QCM — it opens a `Let's discuss`-style dialogue from the start.

### 1.2 Multi-selection

When the question accepts multiple answers, use `multiSelect: true` and:

- Name the recommended subset explicitly in the question text (e.g., *"Recommended: 1 and 3"*).
- Order options: recommended first, neutral second, risky last.

For lists longer than 4 candidate items, use the **aggregated pattern**:

- Option 1: `All` *(Recommended)*
- Option 2: `Recommended only` (with the recommended subset described in the question text)
- Option 3: `Selection to be specified` (the user replies with item numbers via `Let's discuss` or `Other`)
- Option 4: `Let's discuss`

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
| Master plan — orchestration (YAML) | `docs/master-plan.yaml` |
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

### 2bis. Master plan schema — transverse references

Two `docs/master-plan.yaml` sections are widely consumed but lack a single canonical home in any one skill. Their semantics are summarized here so the master-plan schema definitions in `master-plan.md` always have an operational consumer:

- **`master-plan.yaml -> transverse_decisions`** — captures the cross-cutting design choices that apply to the whole document: palette, presentation_preset, view_modes per profile, bibliography source/format/style, ai_image provider/model/default_size, export asset_mode/mode, spacing strategy, active_guideline. Read by `ce-plan` (when proposing or refining the plan), `ce-prototype` (to apply the chosen palette/preset to pilot blocks), and `ce-produce` (to ensure every produced block honors the chosen styles). Updated whenever the user decides — or revises — a transverse choice. The QCMs that mutate this section follow the universal format defined in §1.
- **`master-plan.yaml -> status_legend`** — embedded self-describing reference for what each status value means for blocks (`planned | prototyped | produced | reviewed | fixed | done`) and objectives (`pending | in_progress | met | unmet | abandoned`). Read by `ce-status` when rendering the dashboard, by `objective-monitor` when judging deviations, and by any agent that surfaces a status to the user. Never edited at runtime — copied verbatim from the schema during initial ASSESS.

When in doubt about the meaning of a status value, dereference `status_legend` instead of inventing a new convention.

## 3. Snapshot mechanism

A paired snapshot of the master plan (`<archive>/YYYY-MM-DD-NNN.yaml` + `<archive>/YYYY-MM-DD-NNN.md`) is written when **at least one of the two files differs from the most recent snapshot**. This rule naturally enforces "at most one snapshot per session" without an explicit session id.

Trigger points where snapshot must be considered:

1. At the start of any CE skill that may mutate state — compute diff against last snapshot; if different, snapshot before writing.
2. On user demand — QCM "Snapshot the current plan? (Yes (Recommended) / No / Let's discuss)".
3. Before destructive operations (TOC removal, batch reconciliation, etc.) — same QCM, default `Yes`.
4. At session end via "soft interruption" — QCM with default `Yes`.

Retention: all snapshots are kept indefinitely. `ce-compound` proposes partial purge via QCM when the archive grows large.

Snapshots do **not** reference any git commit hash — they are git-independent.

## 4. Decisions log format

Every QCM presented to the user produces an entry in `master-plan.yaml -> decisions_log`:

```yaml
- timestamp: 2026-05-13T14:32:11Z
  question: "Before producing the 8 section blocks, I propose producing a pilot block to validate styles. Proceed?"
  options_presented: ["Yes (Recommended)", "No, produce directly", "Let's discuss", "Other"]
  recommendation: "Yes (Recommended)"
  answer: "Yes (Recommended)"
  skill: ce-prototype
```

- `timestamp` is ISO 8601 UTC.
- `question` is the verbatim text shown to the user.
- `options_presented` lists every option, including `Let's discuss` and `Other`, with the `(Recommended)` suffix preserved on the recommended one.
- `recommendation` echoes the option that bore the `(Recommended)` suffix.
- `answer` is either the selected option, the free text for `Other`, or a one-paragraph summary of the dialogue that followed `Let's discuss`.
- `skill` identifies the CE skill that captured this decision.
- `dialog_level` is **not** recorded.

## 5. Reconciliation `book.py` ↔ master plan

At the start of any CE skill that may write blocks (`ce-produce`, `ce-fix`, `ce-task` write archetypes), and at the start of every `ce-continue` session, run reconciliation:

1. Compare the order of `bck_*` in `book.py` against the TOC `blocks` lists in `master-plan.yaml`.
2. Classify divergences: `added_in_code`, `missing_in_code`, `renamed`, `reordered`.
3. Present **a single proposal** built by the LLM covering all divergences. QCM:
   - Option 1: *"Apply the global proposal"* `(Recommended)`
   - Option 2: *"See block-by-block detail"* (drill-down to per-divergence QCM)
   - Option 3: `Let's discuss`
4. Refused divergences become entries in `coherence_debt`.

If no divergence is detected, do not surface the topic — silent passage.

## 6. Reversibility of decisions

Entries in `decisions_log` can be reopened automatically by the orchestrator when new information emerges (new sources collected, divergent observations during REVIEW, contradictory user input). The reopening is itself a new QCM that references the prior decision in its question text:

> *"In iteration 1 we chose <option> for <question>. New elements (<summary>) suggest reconsidering. What do you do?"*

The orchestrator never silently overrides a prior decision — it always asks.

## 7. Objectives monitoring

Objectives in `master-plan.yaml -> objectives` have free-text criteria. The orchestrator (via the `objective-monitor` agent) judges status by reading the current state of the project, the master plan, and the latest review. It does not compute metrics — it produces a textual judgment.

Surface a question only when the judgment identifies a significant deviation. The judgment + proposal pair forms the QCM:

> *"Objective <id> (<title>) appears behind schedule: <judgment>. Proposal:"*
> 1. *"Add a dedicated section in the next increment"* `(Recommended)`
> 2. *"Revise the objective"*
> 3. `Let's discuss`

In `dialog_level: minimal`, this surfacing is deferred to the next fundamental gate.

## 8. Patterns catalog levels

Three levels of pattern maturity:

| Level | Location | Promoted from | Promoted via |
|---|---|---|---|
| `draft` | `docs/solutions/style/patterns/` | extraction in PROTOTYPE or COMPOUND | automatic capture (no QCM at this step) |
| `local` | the primary local pack (`./mypack/components/`) | draft | QCM in PROTOTYPE (immediately) or COMPOUND |
| `shared` | `streamtex-pack-design` pack (PR via `gh`) | local | QCM in INTEGRATE |

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

The QCM question reflects the detected state and proposes the corresponding scope as `(Recommended)`. Alternatives are always available, plus `Let's discuss`.

## 10. Soft interruption

At the end of any CE skill or when the user signals end of session, propose a final snapshot via QCM with default `Yes`. If the master plan has not changed since the last snapshot, skip the QCM silently.

## 11. PROTOTYPE vs PRODUCE boundary

PROTOTYPE is concerned with **visual validation by example** and **pattern capture**. Its output is a small, validated set of pilot blocks plus an enriched local components catalog.

PRODUCE is concerned with **mass production at scale** of the increment's remaining blocks, applying the patterns validated in PROTOTYPE.

Auto-trigger rule for PROTOTYPE (decided in `ce-go` Step 3.5):

| Condition | PROTOTYPE recommendation |
|---|---|
| First iteration of the document, no pattern in catalog yet | `Yes` |
| Increment introduces a new visual territory (new palette, new profile, new layout class) | `Yes` |
| Increment continues a style territory already validated, all patterns already mapped | `No` |
| User explicitly asks for design validation | `Yes` |

In all cases the QCM in `ce-go` Step 3.5 is the user's escape hatch from the auto-decision. In `dialog_level: minimal`, the QCM is skipped only when the recommendation is `No`.

## 12. Always-ask decisions (never infer)

Two decisions must be surfaced explicitly at the start of a cycle and never inferred from context (both were silently wrong in the GSE-ODOO run):

- **Output language.** Do not infer the document's language from the language of the prompt. Surface a QCM (e.g. *"Document language?"* → `English` / `French` / `Let's discuss`) during ASSESS, before producing any content, and record it in `decisions_log`.
- **Deliverable paths.** At the end of each phase, state the absolute paths of the artefacts produced (plan, assess report, master plan, prototype report, screenshots in `docs/_screens/`). The user should never have to ask where things were written.
