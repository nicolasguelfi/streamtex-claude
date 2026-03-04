# StreamTeX Claude AI Profiles

[![Works with Claude Code](https://img.shields.io/badge/Works%20with-Claude%20Code-blueviolet)](https://claude.ai/claude-code)
[![Works with Cursor](https://img.shields.io/badge/Works%20with-Cursor-blue)](https://cursor.com)

**AI profiles for [StreamTeX](https://github.com/nicolasguelfi/streamtex)** — build presentations, courses, and web-books with slash commands and agents, no coding required.

> Install a profile to get 22 slash commands, 4 specialized agents, 10 block templates,
> coding standards, and a project-specific CLAUDE.md — all tailored to your use case.

## Quick Start for End-Users

```bash
# 1. Install the StreamTeX CLI
uv tool install streamtex[cli]

# 2. Create a workspace with Claude profiles
mkdir streamtex-dev && cd streamtex-dev
stx workspace init .                     # standard preset (docs + claude)
stx workspace clone

# 3. Create a project and install a Claude profile
stx project new mon-projet
cd projects/stx-mon-projet
stx claude install project .

# 4. Open in Claude Code or Cursor
claude          # or: cursor .
```

Lighter setup (Claude profiles only, no docs):

```bash
stx workspace init . --preset user
stx workspace clone
stx project new mon-projet
cd projects/stx-mon-projet
stx claude install project .
```

Then use slash commands to build your project:

```
/project:project-init
> "Docker introduction course, 10 slides, dark theme, with table of contents"
```

The AI agent proposes a structure, you approve, and all files are generated.
Run `uv run streamlit run book.py` to preview.

See the **[AI Guide](https://github.com/nicolasguelfi/streamtex/blob/main/AI_GUIDE.md)** for all workflows and examples.

## Profiles

| Profile | Audience | Commands | Agents | Skills | Key Use Cases |
|---------|----------|:--------:|:------:|:------:|---------------|
| **project** | Content creators, teachers | 19 | 3 | 5 | Create projects, design slides, migrate HTML, audit design |
| **presentation** | Live presenters | +3 | +1 | +2 | All of `project` + live projection rules (48pt+ fonts, 10-20m) |
| **library** | Library contributors | 3 | — | 2 | Test, lint, deploy the StreamTeX library |
| **documentation** | Manual authors | 10 | 2 | 3 | Multi-manual coordination, course generation |

## Installation

### For content creators

```bash
# Standard project profile (recommended)
stx claude install project ./my-project

# Or presentation profile (includes project + large-font projection rules)
stx claude install presentation ./my-presentation
```

### For library development

```bash
stx claude install library ./streamtex
```

### For documentation authoring

```bash
stx claude install documentation ./streamtex-docs
```

### List available profiles

```bash
stx claude list
```

## What Gets Installed

The installer copies into your project:

```
your-project/
├── CLAUDE.md                  # Generated AI assistant instructions
└── .claude/
    ├── settings.json          # Claude Code permissions
    ├── .stx-profile           # Installed profile marker
    ├── commands/              # Slash commands (/designer:*, /project:*, etc.)
    ├── designer/              # Design skills and agents
    ├── developer/             # Developer skills
    └── references/            # Coding standards + cheatsheet
```

## Command Overview

### Project Commands (5)

| Command | What it does |
|---------|-------------|
| `/project:project-init` | Create a complete project from natural language |
| `/project:project-customize` | Modify theme, colors, typography, navigation |
| `/project:course-generate` | Generate `book.py` from a CSV block list |
| `/project:collection-new` | Create a multi-project collection hub |
| `/project:project-upgrade` | Upgrade project to latest template |

### Designer Commands (7)

| Command | What it does |
|---------|-------------|
| `/designer:slide-new` | Create a slide from a description |
| `/designer:block-new` | Create a block with blueprint matching |
| `/designer:slide-audit` | Validate design rules |
| `/designer:slide-fix` | Auto-fix design violations |
| `/designer:style-audit` | Check styles for consistency |
| `/designer:style-refactor` | Extract and optimize styles |
| `/designer:block-preview` | Validate structure and assets |

### Migration Commands (5)

| Command | What it does |
|---------|-------------|
| `/migration:html-migrate` | Convert HTML to StreamTeX |
| `/migration:html-convert-batch` | Batch convert HTML files |
| `/migration:html-convert-block` | Convert a single HTML block |
| `/migration:html-export` | Configure HTML export |
| `/migration:conversion-audit` | Audit conversion quality |

### Developer Commands (3)

| Command | What it does |
|---------|-------------|
| `/developer:test-run` | Run test suite |
| `/developer:lint` | Run linter with auto-fix |
| `/developer:deploy` | Deploy to Docker/HF/GCP |

### Presentation Commands (3, overlay)

| Command | What it does |
|---------|-------------|
| `/designer:presentation-audit` | Check live projection compliance |
| `/designer:presentation-fix` | Fix projection design issues |
| `/designer:survey-convert` | Convert survey screenshots to blocks |

## Agents

| Agent | Profile | Role |
|-------|---------|------|
| **Project Architect** | project | Designs project structure from natural language descriptions |
| **Slide Designer** | project | Creates pedagogically structured, visually polished slides |
| **Slide Reviewer** | project | Reviews and validates completed slides |
| **Presentation Designer** | presentation | Specialist for live projection (10-20m distance) |

## Updating

Use the StreamTeX CLI for fine-grained control:

```bash
stx claude diff .           # Compare installed vs source
stx claude update .         # Update (preserves local CLAUDE.md)
stx claude update . --force # Override everything including CLAUDE.md
```

Or re-run the install command to overwrite:

```bash
stx claude install project ./my-project
```

## Related

- **[StreamTeX](https://github.com/nicolasguelfi/streamtex)** — Core library (Python API)
- **[AI Guide](https://github.com/nicolasguelfi/streamtex/blob/main/AI_GUIDE.md)** — Complete zero-code workflow guide
- **[StreamTeX Docs](https://github.com/nicolasguelfi/streamtex-docs)** — Interactive manuals and examples
- **[Online Manuals](https://streamtex.onrender.com)** — Live documentation

## Dependencies

- Python 3.11+ (uses `tomllib`)
- Optional: `jinja2` for template rendering (falls back to simple string replacement)

## Repository Structure

```
streamtex-claude/
├── install.py              # Installation script
├── profiles/
│   ├── project/            # Standard project profile (19 commands, 3 agents)
│   ├── presentation/       # Live projection overlay (extends project)
│   ├── library/            # Library development profile
│   └── documentation/      # Documentation authoring profile
├── shared/
│   └── references/         # Shared coding standards + cheatsheet
└── .github/
    └── workflows/
        └── validate.yml    # CI: validate profile completeness
```

## License

MIT
