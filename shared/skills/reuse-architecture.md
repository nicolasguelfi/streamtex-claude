# Reuse architecture — packs, components, design systems, kits

This skill is the **single source of truth** for the StreamTeX reuse
architecture (introduced in `streamtex 0.7.x`). It replaces the legacy
`pattern-library` and `block-blueprints` skills.

A **component** is a Python module that exposes a callable + a docstring
following PLAN §4.1 (Visual / Structure / Styling rules / Extrapolation
rules / When to use / When NOT to use / Design system bundles required)
and a `__component_meta__` dict. Components live in **packs** distributed
as ordinary Python packages, declared via the `streamtex.packs` PEP 621
entry point.

## When this skill activates

Read this skill whenever you:

- Generate, edit, or audit a StreamTeX block
- See a component referenced by name (e.g. *"use the `callout`"*)
- Need to know which packs / components / kits the project ships with
- Use any `/stx-pack:*`, `/stx-component:*`, `/stx-ds:*`, `/stx-kit:*`,
  `/stx-validate` slash command
- Capture a new component in PROTOTYPE or promote one in INTEGRATE

## 1 — Vocabulary

| Term | Definition |
|---|---|
| **Pack** | A Python package that ships components, design systems, CLI templates, project blueprints, and kits. Declares an entry point under `streamtex.packs`. Local (project-internal) or external (git / pypi). |
| **Component** | A Python module with a structured docstring + `__component_meta__`. Granularity is a tag: `primitive`, `composition`, or `block`. |
| **Design system** | A Python class implementing `DesignSystemProtocol` — a bag of `Style` bundles (colors, titles, callouts, body, …). |
| **CLI template** | A scaffold (book.py, blocks/, custom/) packaged inside a pack and copied into new projects. |
| **Project blueprint** | A markdown file (instructions for the AI) that lives inside a pack — the only non-Python artifact. |
| **Kit** | A TOML manifest gluing 1 design system + a curated component list + (optionally) a CLI template + samples. Installed by `stx kit install <pack>:<kit_name>`. |
| **Primary local pack** | The single `[[packs]] type="local" primary=true` entry — the **default destination** for capture flows. Created by `stx project new` as `./mypack/`. |
| **stx.toml** | The project-level configuration declaring its packs, design system, resolution preferences, and active kit. Schema in PLAN §6.1. |

## 2 — Discovery (runtime)

`streamtex.core.discovery.discover_packs()` returns a list of
`DiscoveredPack` objects derived from:

1. **Python entry points** (`importlib.metadata.entry_points(group="streamtex.packs")`)
2. **stx.toml `[[packs]]`** declarations in the current project

The five lifecycle states (PLAN §5.6bis) — Nominal, Drift install,
Indirect, Manifest cassé, Collision — surface via the `state` attribute
on each `DiscoveredPack` and via the documented error codes:

- **PR001** — promote to `pypi` refused
- **PR002** — declared pack not installed
- **PR003** — manifest unreadable
- **PR004** — entry-point collision
- **PV001-PV010** — manifest format failures (`_pack_manifest.toml`)
- **DV001-DV006** — design system contract failures
- **CV001-CV011** — component docstring / meta failures
- **KV001-KV005** — kit failures
- **BV001-BV002** — bundle access failures

## 3 — Catalog levels (granularity tag)

A component declares one of three `granularity` values in its
`__component_meta__`:

- **`primitive`** — atomic visual element (callout, slide heading,
  inline emphasis). 1 bundle row, < 50 lines.
- **`composition`** — combines 2-N primitives in a small reusable
  arrangement (card grid, comparison table, takeaways list).
- **`block`** — a full self-contained block (title slide, manual section,
  evidence-insight). Composes compositions + primitives + free Python.

Granularity is a **tag**, not a constraint of use. A block can call
another block; resolution is purely by name.

## 4 — `stx.toml` schema (§6.1)

```toml
[project]
name = "my-project"
version = "0.1.0"

[[packs]]
type = "local"           # local | git | pypi
name = "mypack"
path = "./mypack"
primary = true

[[packs]]
type = "git"
name = "streamtex-design"
ref = "github.com/nicolasguelfi/streamtex-design"
rev = "v0.1.0"

[design_system]
ref = "default"          # name resolved against the active packs

[resolution]
prefer = ["mypack", "streamtex-design"]   # sort order, not a filter

[kit]
ref = "streamtex_design:project-default"
```

## 5 — `__component_meta__` schema (§5.2)

```python
__component_meta__: ComponentMeta = {
    "name": "callout",
    "description": "Boxed inline notice with a kind (info | warn | error | success).",
    "tags": ["primitive", "callout"],
    "extrapolable": True,
    "since": "2026-05-19",
    "bundles_required": [
        "callouts.info", "callouts.warn", "callouts.error",
        "callouts.success", "callouts.title", "callouts.body",
    ],
    "granularity": "primitive",
    "uses_components": [],   # optional, only for compositions/blocks (Q5)
}
```

## 6 — Capture and promote (CE workflow links)

PROTOTYPE Phase 7 captures a new component into the **primary local pack**
(`mypack/components/`) by default. The full schema (§8.1):

1. Sketch the component in a block.
2. Extract into `mypack/components/<name>.py` with the §4.1 docstring.
3. Add `__component_meta__`.
4. `stx component validate <name>` (CV001-CV011).
5. Test render.

INTEGRATE promotion (§8.3) has four destinations (Q12):

1. **Primary local pack** → copy only, no separate commit.
2. **Secondary local pack with `.git`** → copy + interactive QCM commit.
3. **Git remote pack** → branch `feat/promote-<comp>-from-<project>` +
   push + `gh pr create`.
4. **PyPI pack** → refused (PR001).

## Where to learn more

- `streamtex/documentation/maintenance/reuse-architecture/PLAN.md` —
  authoritative spec (3888 lines).
- `streamtex-design` repo — the official reference pack.
- CLI: `stx pack --help`, `stx component --help`, `stx ds --help`,
  `stx kit --help`, `stx validate --help`.
