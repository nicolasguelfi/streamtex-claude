# Modular Design Philosophy

## When this skill activates

Read this whenever you:

- Generate or edit a StreamTeX block
- Scaffold a new project (`stx-block:init`, `stx-designer:init`)
- Audit or refactor an existing project (`stx-coherence:audit`,
  `stx-block:audit`)
- Design a new component, kit, or design system

## Font scale (authority — overrides legacy guidance encountered elsewhere)

For ALL new font-size decisions, the indexed responsive scale is the
single source of truth. If you read older guidance recommending
`s.medium` / `s.large` / `s.huge` / `s.Huge` / `s.LARGE` / `s.GIANT`
for new code, translate it through this table:

| Legacy token | Indexed equivalent | Palier index | Default pt @ base 18 |
|---|---|---|---|
| `s.tiny` (4pt) | `s.text_xs` | idx_5 | 14pt (floor) |
| `s.small` (6pt) | `s.text_xs` | idx_5 | 14pt (floor) |
| `s.little` (8pt) | `s.text_xs` | idx_5 | 14pt (floor) |
| `s.medium` (12pt) | `s.text_xs` | idx_5 | 14pt (floor) |
| `s.big` (16pt) | `s.text_base` | idx_7 | 18pt (BASE) |
| `s.large` (24pt) | `s.text_2xl` | idx_10 | 24pt |
| `s.Large` (32pt) | `s.text_4xl` | idx_12 | 32pt |
| `s.LARGE` (48pt) | `s.text_6xl` | idx_15 | 48pt |
| `s.huge` (64pt) | `s.text_7xl` | idx_16 | 60pt |
| `s.Huge` (80pt) | `s.text_8xl` | idx_17 | 72pt |
| `s.HUGE` (96pt) | `s.scale[18]` | idx_18 | 96pt |
| `s.giant` (128pt) | `s.text_9xl` | idx_19 | 128pt |
| `s.Giant` (160pt) | `s.scale[20]` | idx_20 | 156pt |
| `s.GIANT` (196pt) | `s.scale[27]` | idx_27 | 196pt |

### NEVER override individual paliers

If a document needs larger or smaller type overall, change the **base**
in one place, not 29 paliers:

```python
# RECOMMENDED — one-line override, every palier follows proportionally
st_book([...], scale=ScaleConfig(base_pt_desktop=24))   # generous

# WRONG — per-palier hand-tuning
st_book([...], scale=ScaleConfig(custom_desktop=[10, 12, 14, ...]))
```

### `ScaleConfig` knobs (use them in this order of preference)

1. `base_pt_desktop` — scale everything proportionally (most common)
2. `tablet_scale` / `mobile_scale` — adjust per-breakpoint shrink
3. `curve` — switch silhouette (WORD_PROCESSOR / GEOMETRIC / BODY_CENTRIC / BELL)
4. `count` — change the number of paliers in the active scale
5. `custom_desktop` / `custom_tablet` / `custom_mobile` — last resort

### Recommended `base_pt_desktop` per audience

| Audience | base_pt_desktop |
|----------|----------------|
| Screen viewing (default) | 18 |
| Documentation / reading | 18 |
| Auditorium projection | 24 |
| Workshop interactive | 20-22 |
| Dense / data-heavy | 16 |
| Minimalist generous | 20-22 |

## The decomposition principle

Visual artefacts in StreamTeX live in one of **three layers**, picked
according to **scope of reuse**:

| Scope | Layer | Where it lives | Example |
|---|---|---|---|
| Cross-project, universal | Upstream pack | `streamtex-pack-design` or a domain pack | `callout`, `comparison_table` |
| Project-wide identity | Project pack | `./mypack/design_systems/default.py` + `./mypack/components/` | Project's color palette, custom CTA card |
| Single-block, one-off | Block-local | `BlockStyles` class inside the block file | A specific spacing variant for this block only |

## Decision tree

When you find yourself writing a style or component, ask:

```
            Will it be used by more than one block?
                            │
                  ┌─────────┴─────────┐
                  │                   │
                 NO                  YES
                  │                   │
        BlockStyles class      Will it be used by more than one project?
        inside the block file          │
                                ┌──────┴──────┐
                                │             │
                               NO            YES
                                │             │
                       Project design pack   Upstream pack
                       (./mypack/design_systems/)  (streamtex-pack-design or domain)
```

## Font scale: modular vocabulary

The indexed responsive scale (`s.text_xs` … `s.text_9xl`, `s.scale[N]`)
is the **default** font sizing vocabulary for new code. It:

- Spans 29 paliers from ~6pt to ~200pt depending on viewport.
- Responds to breakpoints (1024px tablet, 480px mobile).
- Can be overridden per-document via `st_book(scale=…)`.
- Coexists with the legacy `s.medium`/`s.large`/etc. — those remain
  valid but should not be preferred for new code.

Inside a pack's design system bundle, **always** use a CSS variable
reference, not a hardcoded `Npx`:

```python
# Good — responsive, integrated with the scale system
body = Style("font-size: var(--stx-scale-5, 14pt); line-height: 1.5;", "body")

# Bad — fixed px, breaks responsiveness for all consumers
body = Style("font-size: 15px; line-height: 1.5;", "body")
```

## Anti-patterns to avoid

- **Centralizing every style in `custom/styles.py`**: this was the
  legacy pattern. For new projects, use a design pack — keep
  `custom/styles.py` only for one-off overrides.
- **Hardcoding `font-size: Npx` in design system bundles**: breaks
  responsive sizing for every consumer of the bundle.
- **Putting block-specific variants in the pack**: clutters the pack
  with single-use styles. Block-specific → `BlockStyles`.
- **Using `s.medium`/`s.large` in new block code**: prefer `s.text_base`
  / `s.text_lg`. The legacy tokens remain valid for backward
  compatibility but the indexed scale is the new default.

## Scaffolding workflow

When initializing a new project:

```bash
# Default — creates ./mypack/ as the primary local pack
stx project new my-doc --kit streamtex_design:project-default

# Then scaffold the project's design system in the pack
stx ds new default --pack mypack

# Edit ./mypack/design_systems/default.py to declare the project's
# visual identity (colors, callouts, titles, body)
```

In `book.py`, consume the project's pack:

```python
from mypack.design_systems.default import DesignSystem as ProjectDS
from streamtex import st_book

st_book(
    [...blocks...],
    design_system=ProjectDS(),  # the project's identity
)
```

## Cross-references

- `reuse-architecture` skill — pack/component vocabulary, lifecycle
- `streamtex_cheatsheet_en.md` — full API reference
- `coding_standards.md` — style storage hierarchy (mirrors this skill)
- `stx_manual_advanced/blocks/bck_indexed_font_scale.py` — visual reference
- `stx_manual_reuse/blocks/bck_pack_font_scale_integration.py` —
  pack-author angle
