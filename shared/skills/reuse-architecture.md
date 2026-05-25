# Reuse architecture — packs, components, design systems, kits

This skill is the **single source of truth** for the StreamTeX reuse
architecture: packs, components, design systems, and kits.

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
- Use any `/stx-pe:*` slash command (Pack Engineering operates entirely
  on this architecture — see "Orchestrated evolution" below)

## Orchestrated evolution (Pack Engineering)

This skill covers the **static mechanics** of packs / components / design
systems / kits. The **orchestrated lifecycle** for extracting, forking,
refining, auditing, adopting, and publishing packs across N projects is
the **Pack Engineering (PE)** module — accessed via `/stx-pe:*` slash
commands and the single user-facing `pack-orchestrator` agent.

Use PE when:

- You have N projects with repeated visual idioms but no shared pack
  yet → `/stx-pe:bootstrap`.
- An upstream pack (e.g. `streamtex-pack-design`) almost fits but lacks
  domain-specific patterns → `/stx-pe:specialize`.
- The active pack is in use and new idioms have emerged in recent blocks
  → `/stx-pe:refine`.
- You want a health audit (unused / duplicates / drift / bundle gaps)
  → `/stx-pe:audit`.
- You need to install a pack in projects without extraction
  → `/stx-pe:adopt`.
- The pack is mature enough to release with a semver tag and (optionally)
  PyPI publish → `/stx-pe:publish`.

PE writes its audit trail to `docs/pack-engineering/pack-master-plan.{yaml,md}`
and per-phase reports under `docs/pack-engineering/<ts>/`. PE drives the
deterministic `stx component / pack / kit / validate` CLI commands but
adds the AI-assisted analysis + design + retrofit that those commands
cannot perform deterministically. Full reference: `pe_cheatsheet_en.md`
and `.claude/pack-engineering/skills/pe-conventions.md`.

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
name = "streamtex-pack-design"
ref = "github.com/nicolasguelfi/streamtex-packs"
rev = "pack-design-v0.2.4"
subdirectory = "streamtex-pack-design"

[design_system]
ref = "default"          # name resolved against the active packs

[resolution]
prefer = ["mypack", "streamtex-pack-design"]   # sort order, not a filter

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

## Extended artifacts (manifest 0.2+) — beyond Python

The original pack contract (manifest format 0.1) ships **only Python**
artifacts: components, design systems, kits, CLI templates, project
blueprints. Manifest format **0.2** is **additive** — it unlocks an
optional `[pack.data]` section that lets a pack also ship eight data-first
and documentation categories.

### The 8 extended categories

| Category | Filesystem convention | Canonical format | Used for |
|---|---|---|---|
| **palette** | `<pack>/palettes/<name>.json` | JSON | Color tokens + semantic dimensions ; Python view generated via `streamtex.core.artifacts.palette.load_palette()` |
| **ai_prompt** | `<pack>/ai_prompts/<name>/{prefix,suffix-*}.txt` | TXT | Reusable AI image-generation prompts (PREFIX + scene + SUFFIX-orientation) |
| **archetype** | `<pack>/archetypes/<name>.md` | Markdown + YAML frontmatter | Reusable visual scene compositions (bridge, horizon, balance, …) |
| **guideline** | `<pack>/guidelines/<name>.md` | Markdown + YAML frontmatter | Opposable rules (R1-R13) ; agents and humans must respect |
| **skill** | `<pack>/skills/<name>.md` | Markdown + Claude Code frontmatter | Pack-scoped Claude Code skills, installed to `.claude/custom/skills/<pack>__<name>.md` |
| **agent** | `<pack>/agents/<name>.md` | Markdown + Claude Code frontmatter | Pack-scoped Claude Code agents |
| **asset** | `<pack>/assets/_manifest.toml` + binaries | TOML + bytes | Logos, fonts, images with license tracking |
| **integration** | `<pack>/integrations/<framework>/` | Open contract | Recipe per third-party framework (streamtex, figma, midjourney, …) |

### Declaring extended artifacts

In `_pack_manifest.toml`:

```toml
[manifest]
format = "0.2"

[pack.data]
palettes = ["main"]
ai_prompts = ["scene_generation"]
archetypes = ["bridge", "horizon", "balance"]
guidelines = ["graphic-line"]
skills = ["author-helper"]
agents = ["design-reviewer"]
assets = ["assets"]            # bundle name (matches dir name)
integrations = ["streamtex", "figma"]
```

The list must match the on-disk slugs. An unlisted file on disk is **not**
enumerated by `discover_artifacts`. Format 0.1 packs (no `[pack.data]`)
still work unchanged.

### Generic CLI

```bash
stx artifact list                            # all categories, all packs
stx artifact list --kind palette             # filter by category
stx artifact list --pack streamtex-pack-gse  # filter by pack
stx artifact show <name> --kind <k>          # formatted view
stx artifact validate                        # validate every artifact
stx artifact install <name> --kind skill     # install into .claude/custom/
```

### Lifecycle hooks

Skills and agents are the only categories with a project-side install
step: they're copied to `.claude/custom/skills/` (or `agents/`) so Claude
Code discovers them. Convention:

- Filename in the project: `<pack_slug>__<name>.md` (e.g.
  `gse__gse-author.md`). Avoids cross-pack collisions.
- Confirmation prompt by default at `stx artifact install` ; `--yes` to
  skip.

The other categories (palette, ai_prompt, archetype, guideline, asset,
integration) are consumed **lazily at runtime** from the installed pack —
no copy step.

### When to use which category

| You want to ship … | Category |
|---|---|
| Color tokens for components AND for outside tools (Figma, Midjourney) | palette |
| A reusable prompt template for AI image generation | ai_prompt |
| A reusable visual composition pattern (with "use when / forbidden" guardrails) | archetype |
| Opposable spec rules ("R1: one idea per slide") | guideline |
| Domain expertise Claude Code should pick up automatically | skill |
| A multi-step agent workflow Claude Code should invoke | agent |
| Logos, fonts, images with license tracking | asset |
| Recipe for using the pack from another tool (Figma, Midjourney, …) | integration |

`streamtex-pack-gse v2.0.0` ships all 8 categories — see it as the
reference example of a 0.2-format pack.

## Where to learn more

- `streamtex/documentation/maintenance/reuse-architecture/PLAN.md` —
  authoritative spec (3888 lines).
- `streamtex/documentation/maintenance/design-packs/RFC-extended-artifacts.md`
  — the RFC behind manifest 0.2 + the 8 extended categories (local to
  workspace, not in the public repo).
- `streamtex-pack-design` (in `streamtex-packs` monorepo) — the official
  reference pack for the Python artifacts (manifest 0.1).
- `streamtex-pack-gse v2.0.0` — the reference example for manifest 0.2
  extended artifacts.
- CLI: `stx pack --help`, `stx component --help`, `stx ds --help`,
  `stx kit --help`, `stx artifact --help`, `stx validate --help`.
