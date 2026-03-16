# Claude -> Cursor Converter

Generates a `.cursor/` directory from an installed `.claude/` profile so that Cursor IDE users can reuse StreamTeX Claude components.

## Quick start

```bash
# From a project with .claude/ already installed:
cd my-project/
python path/to/streamtex-claude/cursor/generate_cursor.py
```

## Usage

```
python generate_cursor.py [options]

--source PATH   Source .claude/ directory (default: ./.claude)
--target PATH   Target .cursor/ directory (default: ./.cursor)
--dry-run       Preview without writing
--verbose       Show each file written
--clean         Remove target before generating
```

## What gets converted

| Source (.claude/) | Target (.cursor/) | Type |
|---|---|---|
| `CLAUDE.md` | `rules/00-project-*.mdc` | Always (split by H2) |
| `references/*.md` | `rules/01-ref-*.mdc` | Always |
| `settings.json` permissions | `rules/00-permissions.mdc` | Always |
| `commands/**/*.md` | `commands/**/*.md` | Slash commands |
| `*/skills/*.md` | `rules/skill-*.mdc` | Agent Requested |
| `*/agents/*.md` | `rules/agent-*.mdc` | Agent Requested |
| `*/templates/*.md` | `commands/templates/*.md` | Slash commands |
| `*/tools/*.md` | `commands/tools/*.md` | Slash commands |
| `.claudeignore` | `.cursorignore` | Ignore file |

## Not converted

- **Auto-memory** (`memory/`) -- no Cursor equivalent
- **Subagent isolation** -- agents become context-only rules
- **`$ARGUMENTS`** -- replaced by a note (Cursor commands are static)
- **Tool restrictions** (`allowed-tools`) -- Cursor has no per-command tool control

## Reference

- [claude-cursor-mapping.md](claude-cursor-mapping.md) -- full correspondence table
- [PLAN-generate-cursor.md](PLAN-generate-cursor.md) -- implementation plan
