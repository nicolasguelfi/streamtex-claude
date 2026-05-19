# PE Retrofit Plan

> Produced by `pack-retrofitter` at the start of the RETROFIT phase (dry-run mode).
> Lives at `docs/pack-engineering/<timestamp>/retrofit-plan.md`.
> A companion `retrofit-report.md` is written after the actual apply.

**Date** : <YYYY-MM-DD HH:MM:SS>
**Mode** : dry-run | apply
**Target pack** : <name> @ <version>
**Consumer projects** : <list>
**Blocks to rewrite** : <int>
**Blocks to skip** : <int>

## 1. Summary

<One paragraph : N blocks across M projects will be rewritten to import
K components from the target pack. Estimated visual diff : minimal (no
content change, only style hoisting). Estimated effort : automated, ~ X
minutes including smoke renders.>

## 2. Per-project rewrite plan

### proj-a (`<absolute path>`)

| Block file | Cluster matched | Component | Line range | Action |
|---|---|---|---|---|
| `blocks/bck_intro.py` | C-001 (info_callout) | `info_callout` | 23-31 | Replace inline `st_block(bs.callout) > st_write(...)` with `info_callout(design_system=ds, title=..., body=...)` |
| `blocks/bck_intro.py` | C-002 (key_takeaways) | `key_takeaways` | 67-89 | Replace inline 18-line `st_list` structure with `key_takeaways(design_system=ds, items=[...])` |
| `blocks/bck_chapter1.py` | C-003 (comparison_card_grid) | `comparison_card_grid` | 102-145 | Replace inline 2-cell st_grid with `comparison_card_grid(design_system=ds, left=..., right=...)` |
| `blocks/bck_summary.py` | C-001 (info_callout) | `info_callout` | 12-20 | Same as bck_intro:23 |

#### Blocks skipped in proj-a

| Block file | Matched cluster | Reason for skip |
|---|---|---|
| `blocks/bck_appendix.py` | C-005 | Block contains a custom Style override that doesn't match the component's INVARIANTS — keep ad-hoc. |

### proj-b (`<absolute path>`)

(same structure)

### proj-c (`<absolute path>`)

(same structure)

## 3. Pre-retrofit invariants check

For every block to be rewritten, verify :

- [x] The block's `blocks/__init__.py` already imports the target pack (or will after `pe-adopt`).
- [x] The `stx.toml` of the project declares the target pack.
- [x] The active DS provides all `bundles_required` of every component used.
- [x] The block compiles BEFORE the retrofit (`uv run python -c "import blocks.<name>"`).

If any check fails, the orchestrator surfaces a QCM at G3 :

> "Pré-conditions échouées pour <X> blocs (<liste>). Que faites-vous ?"
> - Corriger automatiquement les pré-conditions et continuer (Recommandé)
> - Skipper ces blocs et continuer
> - Discutons-en

## 4. Post-retrofit validation per project

After each block rewrite, the pack-retrofitter triggers `visual-reviewer` :

1. Run `streamlit run book.py --server.headless=true --server.port=<random>` for the project.
2. Wait ≤ 30 s for `/_stcore/health` HTTP 200.
3. Scan the streamlit stdout/stderr for `ERROR|Exception|Traceback`.
4. If KO → revert the block, mark `blocks_reverted` in the YAML, surface G4 QCM.
5. If OK → commit, append to `blocks_rewritten`.

## 5. Git commit policy

Two commits per block per project (NOT one big bulk commit) :

```
chore(retrofit): replace inline pattern with <component> in <block_file>

- Block: <project>/<block_file> lines <range>
- Component: <pack>:<component>
- Pack version: <version>
- Smoke render: OK (HTTP 200, no exceptions)

Refs: pack-master-plan decisions_log retrofit_validated <date>
```

The two-commit policy (before/after pack) means : the previous block state
is reachable via `git revert HEAD` if a deferred regression is discovered.

## 6. Next gate

→ **G3 (pre-RETROFIT)** : `pack-orchestrator` surfaces the QCM :

> "Plan de retrofit prêt : <N> blocs à réécrire sur <M> projets, <K>
> skipped. Mode actuel : dry-run.
> Que faites-vous ?"
>
> - Appliquer tout (Recommandé) — bascule dry-run → apply
> - Appliquer projet par projet (revue intermédiaire)
> - Lancer un dry-run sur un sous-ensemble pour inspection
> - Discutons-en
