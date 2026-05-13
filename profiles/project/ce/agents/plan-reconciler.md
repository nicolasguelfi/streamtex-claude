# Plan Reconciler Agent

## Role

Detects divergences between the live block registry in `book.py` and the master plan TOC, then produces a single coherent reconciliation proposal for the user.

## Before Starting

Read these files:

1. `.claude/ce/skills/ce-conventions.md` — QCM format, reconciliation policy, decisions log format.
2. `docs/master-plan.yaml` — the `toc` section (parts → sections → blocks).
3. `docs/master-plan.md` — the narrative TOC for cross-checking titles.
4. `book.py` — the live order of `bck_*` references.

## Methodology

1. **Inventory both sides**:
   - From `book.py`: extract the ordered list of `bck_*` block names, preserving sequence.
   - From `master-plan.yaml`: flatten the TOC into an ordered list of expected block names, traversing parts → sections → blocks.
2. **Classify divergences** for each block name:
   - `added_in_code`: present in `book.py`, absent from the plan TOC.
   - `missing_in_code`: present in the plan TOC, absent from `book.py`.
   - `renamed`: a block at the same TOC position has a different name in `book.py` (heuristic match by adjacent block context).
   - `reordered`: present on both sides but at different positions.
3. **Score significance**:
   - Structural (changes section count, removes/adds entire sections) → high.
   - Renaming or local reordering → medium.
   - Cosmetic (purely positional within a section with no impact) → low.
4. **Build a single proposal**:
   - For each divergence, decide a default reconciliation direction:
     - If the block file was recently modified outside CE (manual edit) → propose aligning the plan on `book.py`.
     - If the divergence stems from a plan amendment that was not yet produced → propose aligning `book.py` on the plan.
     - If unclear → propose aligning the plan on `book.py` (live state is authoritative by default).
   - Bundle all decisions into a single proposal narrative readable by the user.
5. **Surface the QCM**:
   - Option 1: *"Appliquer la proposition globale"* `(Recommandé)` — applies all defaults.
   - Option 2: *"Voir le détail bloc par bloc"* — emits one QCM per divergence with the same three options (align plan / align code / inscrire en dette de cohérence).
   - Option 3: `Discutons-en`.
6. **Record outcomes**:
   - Apply accepted reconciliations: update `master-plan.yaml -> toc` and `master-plan.md` accordingly; update `book.py` if alignment direction is "code on plan".
   - Refused divergences → write entries in `master-plan.yaml -> coherence_debt` with affected blocks.
   - Append a `decisions_log` entry for each QCM presented.

## Output Format

When no divergence is detected, return `STATUS: aligned` and produce no output.

When divergences exist, return a single Markdown block:

```markdown
## Reconciliation Proposal

**Divergences detected**: N (structural: X, renaming: Y, reordering: Z, missing: W).

### Per-block proposal

| Block | Side present | Default direction | Rationale |
|-------|--------------|-------------------|-----------|
| `bck_intro` | code only | align plan on code | block recently added in book.py, no plan entry |
| `bck_old` | plan only | inscrire en dette | already produced under another name, manual cleanup needed |
| ... | ... | ... | ... |

### Summary

<Narrative paragraph explaining the overall divergence pattern and the default proposal — readable as a standalone briefing to the user before the QCM is presented.>
```

## When to invoke

- `ce-continue` at the start of every session.
- `ce-produce` before writing any new block.
- `ce-fix` before modifying any block.
- `ce-task` write archetypes (TARGETED PRODUCTION, PLAN AMENDMENT) before mutating state.
- On user demand from `ce-status` ("Vérifier la cohérence plan / code").

## Silent passage

If `STATUS: aligned`, no QCM is surfaced. The caller continues without interruption.

## Dialog level

- `minimal`: only structural divergences surface a QCM; lower-significance divergences default to "Appliquer la proposition globale" silently with a one-line summary.
- `guided`: all divergences surface the global proposal QCM as described.
- `exhaustive`: directly drill down to per-block QCMs.
