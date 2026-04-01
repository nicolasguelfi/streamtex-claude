# Template: collection

StreamTeX collection hub — a multi-project aggregator.

## Defaults

| Setting | Value |
|---------|-------|
| Type | collection |
| Audience | screen |
| Theme | dark |
| Pagination | no |
| TOC | `NumberingMode.SIDEBAR_ONLY`, `sidebar_max_level=2` |
| Sidebar | `initial_sidebar_state="expanded"` |
| Banner | no |
| Marker | no |
| Body font | `s.large` (32pt) |
| Title font | `s.huge` (80pt) |

### Design Guideline (Optional)

Projects can adopt a design guideline for consistent visual design across all blocks.
Recommended for collections: `minimalist-visual` or `maximize-viewport`.

- Available guidelines: `.claude/designer/guidelines/_index.md`
- Project config: Create `custom/design-guideline.md` referencing the chosen guideline
- Per-block override: Add `# @guideline: <name>` at top of block files

## Structure

A collection is different from a standard project:
- Uses `st_collection()` instead of `st_book()`
- Has a `collection.toml` configuration file
- Has a home page block (`bck_home.py`) with project cards
- Sub-projects run on separate ports

## Required files

```
[collection_name]/
  book.py                 # st_collection() entry point
  collection.toml         # Collection configuration
  blocks/
    __init__.py            # ProjectBlockRegistry
    helpers.py             # Block helper config
    bck_home.py            # Home page with project cards
  custom/
    styles.py              # Collection styles
    themes.py              # Theme overrides
  static/
    images/
      covers/              # Project cover images
  .streamlit/
    config.toml            # Streamlit config
```

## Solutions convention

Collections use a two-level solutions hierarchy:

- **`<root>/docs/solutions/`** — Cross-module solutions applicable to all projects in the collection
- **`modules/<name>/docs/solutions/`** — Module-specific solutions

When `/stx-ce:compound` writes a solution, it should:
1. Check if the learning applies to a single module or the whole collection
2. Place it at the appropriate level
3. Check both levels for duplicates before writing

## book.py pattern

```python
from streamtex import st_collection, CollectionConfig

config = CollectionConfig.from_toml("collection.toml")
st_collection(config=config, home_styles=s)
```

## collection.toml pattern

```toml
[collection]
title = "My Collection"
description = "Collection of StreamTeX projects"

[[projects]]
name = "Project 1"
description = "Description of project 1"
port = 8502
path = "../project-1"
cover = "static/images/covers/project1.png"
```

## Compound Engineering (optional)

Use `/stx-ce:go "description"` to produce this collection with the full CE cycle.
See `.claude/references/ce_cheatsheet_en.md`.

## Reference files

- `streamtex-docs/templates/template_collection/` — canonical template
- `streamtex-docs/manuals/stx_manuals_collection/` — working example
