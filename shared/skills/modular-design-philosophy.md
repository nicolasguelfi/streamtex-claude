# Modular Design Philosophy

## When this skill activates

Read this whenever you:

- Generate or edit a StreamTeX block
- Scaffold a new project (`stx-block:init`, `stx-designer:init`)
- Audit or refactor an existing project (`stx-coherence:audit`,
  `stx-block:audit`)
- Design a new component, kit, or design system

## The decomposition principle

Visual artefacts in StreamTeX live in one of **three layers**, picked
according to **scope of reuse**:

| Scope | Layer | Where it lives | Example |
|---|---|---|---|
| Cross-project, universal | Upstream pack | `streamtex-design` or a domain pack | `callout`, `comparison_table` |
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
                       (./mypack/design_systems/)  (streamtex-design or domain)
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
