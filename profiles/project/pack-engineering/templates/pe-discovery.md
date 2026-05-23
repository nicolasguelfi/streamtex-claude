# PE Discovery Report

> Produced by `pack-miner` at the end of the DISCOVERY phase.
> Lives at `docs/pack-engineering/<timestamp>/discovery.md` in the pilot project.

**Date** : <YYYY-MM-DD HH:MM:SS>
**Mode** : bootstrap | specialize | refine
**Pilot project** : <path>
**Consumer projects scanned** : <N>
**Total blocks read** : <int>
**AST clusters found** : <int>
**Candidates after quality filter** : <int>

## 1. Summary

<One paragraph human-readable summary : how many candidates, granularity distribution, cross-project coverage statistics.>

Example : "Found 18 visual idiom clusters across 91 blocks of 3 projects.
After excluding triviality (single `st_write`, no structural elements) and
already-covered (matched against installed packs), 12 candidates remain :
4 primitive, 6 composition, 2 block. 9 of 12 appear in ≥ 2 distinct
consumer projects ; 3 in a single project but with high reuse density
(≥ 5 occurrences in that project)."

## 2. Candidates table

| # | Proposed name | Granularity | Occurrences | Projects | Source signatures |
|---|---|---|---|---|---|
| 1 | `info_callout` | primitive | 14 | proj-a (8), proj-b (6) | `st_block(bs.callout) > st_write(bs.title) > st_write(bs.body)` |
| 2 | `key_takeaways` | composition | 9 | proj-a (4), proj-c (5) | `st_block(bs.takeaways) > st_list(ul) > [st_write × N]` |
| 3 | `comparison_card_grid` | composition | 7 | proj-a (3), proj-b (4) | `st_grid(2cols) > [st_block × 2 with bs.compare_left / bs.compare_right]` |
| … | | | | | |

## 3. Rejected candidates (and reasons)

<Transparency on what was filtered out, so the user can re-include if needed.>

| Signature | Reason |
|---|---|
| `st_write × 1` | Triviality threshold (no structural elements) |
| `st_block(bs.warning_proj_a)` | Project-specific token in style name |
| `st_block(bs.callout)` matching streamtex-pack-design:callout | Duplicate of already-installed pack |

## 4. Already-covered (deduplicated against installed packs)

<Patterns that the `learnings-researcher` agent matched against an existing
component in any installed pack. NOT a recommendation to skip — the user
may want to OVERRIDE the existing one. But the orchestrator surfaces this
explicitly at the G1 gate.>

| Candidate | Already in pack | Component | Action recommended |
|---|---|---|---|
| (signature X) | streamtex-pack-design | callout | Skip — reuse upstream. Add `[resolution] prefer = ["streamtex-pack-design"]` if not already set. |

## 5. Naming suggestions per candidate

<For each retained candidate, the `pack-miner` agent proposes a name based
on : dominant style tag, dominant tag attribute, structural primitive.>

- **`info_callout`** : derived from `bs.callout` + `kind="info"` parameter detected.
- **`key_takeaways`** : derived from `bs.takeaways` + `st_list(ul)` structural marker.
- **`comparison_card_grid`** : derived from `st_grid(2cols)` + 2-cell symmetric structure.

## 6. Next gate

→ **G1 (post-DISCOVERY)** : `pack-orchestrator` surfaces the QCM to the user :

> "Found <N> candidates to extract across <M> projects (<dist>).
> Recommended: <K> (≥ 2 projects AND ≥ <threshold> occurrences).
> What do you do?"
>
> - Approve the full recommended list (Recommended)
> - Selection to be specified (drill-down per candidate)
> - Widen to include single-project candidates (3 additional candidates)
> - Let's discuss
