# StreamTeX Claude AI Profiles

Claude AI configuration profiles for [StreamTeX](https://github.com/nicolasguelfi/streamtex) projects. Install a profile to get slash commands, designer skills, coding standards, and project-specific CLAUDE.md — all tailored to your use case.

## Profiles

| Profile | Audience | Description |
|---------|----------|-------------|
| **project** | Project developers | Full development profile: designer commands, migration tools, coding standards |
| **presentation** | Presentation authors | Extends `project` with live projection design rules (48pt+ fonts, 10-20m distance) |
| **library** | Library developers | Focused on library development: tests, linting, deployment, architecture |
| **documentation** | Documentation authors | Manual authoring: designer commands, course generation, coding standards |

## Quick Start

```bash
# Clone this repo
git clone https://github.com/nicolasguelfi/streamtex-claude.git

# Install a profile into your project
python streamtex-claude/install.py project ./my-streamtex-project

# List available profiles
python streamtex-claude/install.py --list
```

## Installation

### For project developers (Bob)

```bash
# Install the standard project profile
python install.py project ./my-project

# Or the presentation profile (includes project + presentation design rules)
python install.py presentation ./my-presentation
```

### For library development (Nicolas)

```bash
python install.py library ./streamtex
```

### For documentation authoring (Nicolas)

```bash
python install.py documentation ./streamtex-docs
```

## What Gets Installed

The installer copies into your project:

```
your-project/
├── CLAUDE.md                  # Generated from profile template
└── .claude/
    ├── settings.json          # Claude Code permissions
    ├── .stx-profile           # Installed profile marker
    ├── commands/              # Slash commands (/designer:*, /developer:*, etc.)
    ├── designer/              # Design skills and agents
    ├── developer/             # Developer skills
    └── references/            # Coding standards + cheatsheet
```

## Profile Details

### `project` (28 commands/skills/agents)

- **Commands**: designer (7), migration (5), project (5), developer (2)
- **Skills**: designer (4), developer (1)
- **Agents**: designer (3)
- **Shared**: coding_standards.md, streamtex_cheatsheet_en.md

New in v2 (2026-03-02):
- `/project:project-init` — Initialize a complete project interactively from a natural language description
- `/project:project-customize` — Customize an existing project (theme, typography, navigation, features)
- `block-blueprints.md` skill — Catalog of 10 block templates (title, comparison, timeline, etc.)
- `project-architect.md` agent — Designs project structure before generation

### `presentation` (extends project + 6 overlay files)

Inherits everything from `project`, plus:
- **Commands**: presentation-audit, presentation-fix, survey-convert
- **Skills**: presentation-design-rules, survey-chart-conversion
- **Agents**: presentation-designer

### `library` (5 commands/skills)

- **Commands**: developer (3: test-run, lint, deploy)
- **Skills**: architecture, testing-patterns
- **Shared**: coding_standards.md, streamtex_cheatsheet_en.md

### `documentation` (15 commands/skills/agents)

- **Commands**: designer (7), project (1: course-generate), developer (2)
- **Skills**: designer (3)
- **Agents**: designer (2)
- **Shared**: coding_standards.md, streamtex_cheatsheet_en.md

## Updating

To update an already-installed profile, simply re-run the install command:

```bash
python install.py project ./my-project
```

The installer will overwrite existing files with the latest versions.

## Dependencies

- Python 3.11+ (uses `tomllib`)
- Optional: `jinja2` for template rendering (falls back to simple string replacement)

## Repository Structure

```
streamtex-claude/
├── install.py              # Installation script
├── profiles/
│   ├── project/            # Standard project profile
│   ├── presentation/       # Live projection profile (extends project)
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
