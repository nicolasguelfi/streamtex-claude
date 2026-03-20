<p align="center">
  <img src="https://media.githubusercontent.com/media/nicolasguelfi/streamtex/main/documentation/images/logos/logo-stx-full.png" alt="StreamTeX" width="200">
</p>

<h1 align="center">StreamTeX Claude AI Profiles</h1>

<p align="center">
  <a href="https://github.com/sponsors/nicolasguelfi">
    <img src="https://img.shields.io/badge/%E2%9D%A4%EF%B8%8F_Support_us!-Sponsor-ea4aaa?style=for-the-badge&logo=githubsponsors" alt="Support us!">
  </a>
</p>

[![Works with Claude Code](https://img.shields.io/badge/Works%20with-Claude%20Code-blueviolet)](https://claude.ai/claude-code)
[![Works with Cursor](https://img.shields.io/badge/Works%20with-Cursor-blue)](https://cursor.com)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-pink)](https://github.com/sponsors/nicolasguelfi)
[![Best on Chrome](https://img.shields.io/badge/Best%20on-Chrome-4285F4?logo=googlechrome&logoColor=white)](https://www.google.com/chrome/)

**AI profiles for [StreamTeX](https://github.com/nicolasguelfi/streamtex)** — build presentations, courses, and web-books with slash commands and agents, no coding required.

> Install a profile to get **up to 31 slash commands**, **3 specialized agents**, **8 blueprints**,
> coding standards, and a project-specific CLAUDE.md — all tailored to your use case.

## Quick Start for End-Users

```bash
# 1. Install the StreamTeX CLI
uv tool install streamtex[cli]

# 2. Create a workspace with Claude profiles
mkdir streamtex-dev && cd streamtex-dev
stx install                              # standard preset (docs + claude)
stx update                               # clones repos, syncs deps, installs /stx-guide globally

# 3. Create a project and install a Claude profile
stx project new my-project
cd projects/stx-my-project
stx claude install project .

# 4. Open in Claude Code or Cursor
claude          # or: cursor .
```

Lighter setup (Claude profiles only, no docs):

```bash
stx install --preset user
stx update                               # clones repos, syncs deps, installs /stx-guide globally
stx project new my-project
cd projects/stx-my-project
stx claude install project .
```

Then use slash commands to build your project:

```
/stx-designer:init Docker introduction course, 10 slides, dark theme, with table of contents
```

The AI agent proposes a structure, you approve, and all files are generated.
Run `stx run` to preview.

See the **[AI Guide](https://github.com/nicolasguelfi/streamtex/blob/main/AI_GUIDE.md)** for all workflows and examples.

## Workspace Presets

The `stx install` command supports 5 presets that control which repos and extras are set up:

| Preset | Repos | Extras | Use case |
|--------|-------|--------|----------|
| `basic` | — | pdf | Workspace only, upgrade later |
| `user` | streamtex-claude | pdf | + Claude AI profiles |
| `standard` *(default)* | streamtex-docs, streamtex-claude | pdf, ai | + rich templates, local docs |
| `power` | streamtex-docs, streamtex-claude | pdf, ai, inspector | + all extras |
| `developer` | all 3 repos | pdf, ai, inspector | + library source, editable install |

```bash
stx install --preset user       # Claude profiles only
stx install                     # standard (default)
stx install --preset power --project my-project  # all extras
stx install --preset developer  # full developer setup
```

Upgrade an existing workspace to a higher preset:

```bash
stx install --preset developer
stx update
```

## Profiles

| Profile | Audience | Commands | Agents | Skills | Key Use Cases |
|---------|----------|:--------:|:------:|:------:|---------------|
| **project** | Content creators, teachers | 24 | 3 | 8 | Create projects, design slides, migrate HTML, audit design |
| **presentation** | Live presenters | +3 | +1 | +3 | All of `project` + live projection rules (48pt+ fonts, 10-20m) |
| **library** | Library contributors | 4 | — | 3 | Test, lint, deploy the StreamTeX library |
| **documentation** | Manual authors | 11 | 2 | 5 | Multi-manual coordination, course generation |

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
    ├── commands/
    │   ├── stx-guide.md       # Shared: ecosystem navigation guide
    │   ├── stx-designer/      # Design commands (/stx-designer:init, update, audit, fix, tool, slide-*, style-*, block-*)
    │   ├── stx-developer/     # Dev commands (/stx-developer:test-run, lint, deploy)
    │   └── stx-project/       # Project commands (/stx-project:issue)
    ├── references/            # Shared: coding standards + cheatsheet
    ├── designer/              # Design skills, agents, templates, tools
    └── developer/             # Developer skills
```

## Command Overview

### stx-designer Commands (12) — Project lifecycle

| Command | What it does |
|---------|-------------|
| `/stx-designer:init [--template] <desc>` | Create a complete project from natural language. Templates: `project` (default), `presentation`, `collection`, `course` |
| `/stx-designer:update [--upgrade\|--migrate\|--export] <desc>` | Add blocks, change styles, migrate HTML, export, upgrade structure |
| `/stx-designer:audit [--all\|--target <name>] <desc>` | Check project quality: structure, styles, design rules, presentation compliance |
| `/stx-designer:fix [--all\|--target <name>] <desc>` | Auto-fix issues found by audit |
| `/stx-designer:tool <tool-name> <desc>` | Run specialized tools (e.g. `survey-convert`) |

**Lifecycle**: `init` → `update` → `audit` → `fix` → `update` → ...

All commands accept `--help` to show the full cheatsheet.

### Developer Commands (2-3)

| Command | What it does |
|---------|-------------|
| `/stx-developer:test-run` | Run test suite |
| `/stx-developer:lint` | Run linter with auto-fix |
| `/stx-developer:deploy` | Deploy to Docker/HF/GCP (library profile only) |

### Workspace & Project Management

| Command | What it does |
|---------|-------------|
| `stx status` | Show workspace status: preset, repos, installed profiles, project list |
| `stx project upgrade` | Upgrade a project's dependencies and extras to match the current preset |

### Presentation overlay

The `presentation` profile extends `project` with additional **skills and agents** (not commands):
- `presentation-design-rules.md` — Live projection rules (48pt min, keywords only)
- `survey-chart-conversion.md` — Survey screenshot conversion schema
- `presentation-designer.md` — Agent for projection-optimized slides

The stx-designer commands **auto-detect** presentation profile and apply projection rules.

## Agents

| Agent | Profile | Role |
|-------|---------|------|
| **Project Architect** | project | Designs project structure from natural language descriptions |
| **Slide Designer** | project | Creates pedagogically structured, visually polished slides |
| **Slide Reviewer** | project | Reviews and validates completed slides |
| **Presentation Designer** | presentation | Specialist for live projection (10-20m distance) |

## Updating

After a new StreamTeX release:

```bash
# 1. Update the CLI
uv tool install "streamtex[cli]" -U

# 2. Update everything (repos + deps + profiles + global commands)
cd streamtex-dev/
stx update

# 3. Verify
stx claude check
```

Fine-grained control:
```bash
stx update --skip-sync      # skip uv sync
stx update --skip-profiles  # skip Claude profile update
```

> Use `/stx-guide update` inside Claude Code for guided assistance.

Fine-grained control for a single project:

```bash
stx claude diff .           # Compare installed vs source
stx claude update .         # Update (preserves local CLAUDE.md)
stx claude update . --force # Override everything including CLAUDE.md
```

### What gets updated

| Source in `streamtex-claude/` | Destination in each project |
|---|---|
| `shared/references/*.md` | `.claude/references/` |
| `shared/commands/*.md` | `.claude/commands/` (per-project) |
| `shared/commands/*.md` | `~/.claude/commands/` (global, via `stx update`) |
| `profiles/<profile>/commands/` | `.claude/commands/` |
| `profiles/<profile>/*/skills/` | `.claude/*/skills/` |
| `profiles/<profile>/*/agents/` | `.claude/*/agents/` |
| `profiles/<profile>/CLAUDE.md` | `CLAUDE.md` (preserved unless `--force`) |

Shared files (references and commands) are set read-only (0o444) to signal they are managed automatically.

> **Global commands**: `stx update` also copies `shared/commands/` to `~/.claude/commands/`,
> making commands like `/stx-guide` available globally — even outside any project directory.

### How projects are discovered

`stx claude update --all` and `stx claude check` scan:
- Top-level workspace directories (e.g., `streamtex/`, `streamtex-docs/`)
- Subdirectories of `projects/` (e.g., `projects/stx-ai4se/`)

Projects are identified by the `.claude/.stx-profile` marker file.

## Related

- **[StreamTeX](https://github.com/nicolasguelfi/streamtex)** — Core library (Python API)
- **[AI Guide](https://github.com/nicolasguelfi/streamtex/blob/main/AI_GUIDE.md)** — Complete zero-code workflow guide
- **[StreamTeX Docs](https://github.com/nicolasguelfi/streamtex-docs)** — Interactive manuals and examples
- **[Online Manuals](https://docs.streamtex.ros.lu)** — Live documentation

## Dependencies

- Python 3.11+ (uses `tomllib`)
- Optional: `jinja2` for template rendering (falls back to simple string replacement)

## Repository Structure

```
streamtex-claude/
├── install.py              # Installation script
├── profiles/
│   ├── project/            # Standard project profile (24 commands, 3 agents)
│   ├── presentation/       # Live projection overlay (extends project)
│   ├── library/            # Library development profile
│   └── documentation/      # Documentation authoring profile
├── shared/
│   ├── references/         # Shared coding standards + cheatsheet
│   └── commands/           # Shared commands (stx-guide, etc.)
└── .github/
    └── workflows/
        └── validate.yml    # CI: validate profile completeness
```

## Support the Project

If StreamTeX is useful to you, consider [sponsoring the project](https://github.com/sponsors/nicolasguelfi) to help maintain and improve it.

## License

MIT
