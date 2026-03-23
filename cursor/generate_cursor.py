#!/usr/bin/env python3
"""Generate a .cursor/ directory from an installed Claude .claude/ profile.

Converts Claude Code components (CLAUDE.md, commands, skills, agents,
templates, tools, settings, references) into their Cursor IDE equivalents
(.cursor/rules/*.mdc, .cursor/commands/*.md, .cursorignore).

Usage:
    python generate_cursor.py                          # .claude/ -> .cursor/
    python generate_cursor.py --source ./my/.claude    # custom source
    python generate_cursor.py --dry-run --verbose      # preview only
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ConversionReport:
    """Tracks conversion statistics and warnings."""
    rules_always: int = 0
    rules_agent_requested: int = 0
    commands: int = 0
    ignore: int = 0
    warnings: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    files_written: list[str] = field(default_factory=list)

    @property
    def total_rules(self) -> int:
        return self.rules_always + self.rules_agent_requested

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def skip(self, msg: str) -> None:
        self.skipped.append(msg)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def wrap_mdc(content: str, *, description: str, always_apply: bool,
             globs: str = "") -> str:
    """Wrap markdown content in Cursor MDC format with YAML frontmatter."""
    lines = ["---"]
    lines.append(f"description: \"{_escape_yaml(description)}\"")
    if globs:
        lines.append(f"globs: \"{globs}\"")
    lines.append(f"alwaysApply: {'true' if always_apply else 'false'}")
    lines.append("---")
    lines.append("")
    lines.append(content.rstrip())
    lines.append("")
    return "\n".join(lines)


def _escape_yaml(text: str) -> str:
    """Escape characters that would break YAML double-quoted strings."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def extract_description(content: str) -> str:
    """Extract a short description from a markdown file.

    Priority:
    1. Blockquote with **Scope**: ... -> text after "Scope:"
    2. H1 title -> title text
    3. First non-empty paragraph -> truncated to 200 chars
    """
    for line in content.splitlines():
        line = line.strip()
        # Priority 1: blockquote with Scope
        m = re.match(r">\s*\*\*Scope\*\*\s*:\s*(.+)", line)
        if m:
            return m.group(1).strip()[:200]

    for line in content.splitlines():
        line = line.strip()
        # Priority 2: H1 title
        m = re.match(r"^#\s+(.+)", line)
        if m:
            title = m.group(1).strip()
            # Remove trailing " — description" format, keep description part
            if " — " in title:
                return title.split(" — ", 1)[1].strip()[:200]
            return title[:200]

    # Priority 3: first non-empty paragraph
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith(">"):
            return line[:200]

    return "Converted from Claude Code profile"


def split_by_h2(content: str) -> list[tuple[str, str, str]]:
    """Split markdown content by H2 sections.

    Returns:
        List of (slug, title, section_content) tuples.
    """
    sections: list[tuple[str, str, str]] = []
    current_title = ""
    current_slug = ""
    current_lines: list[str] = []
    preamble_lines: list[str] = []

    for line in content.splitlines():
        m = re.match(r"^##\s+(.+)", line)
        if m:
            # Save previous section
            if current_slug:
                sections.append((current_slug, current_title,
                                 "\n".join(current_lines).strip()))
            elif current_lines:
                # Content before first H2 = preamble
                preamble_lines = current_lines[:]

            current_title = m.group(1).strip()
            current_slug = _slugify(current_title)
            current_lines = []
        else:
            current_lines.append(line)

    # Save last section
    if current_slug:
        sections.append((current_slug, current_title,
                         "\n".join(current_lines).strip()))

    # If there's a preamble (content before first H2), prepend it
    if preamble_lines and sections:
        preamble = "\n".join(preamble_lines).strip()
        if preamble:
            sections.insert(0, ("preamble", "Project Identity",
                                preamble))
    elif preamble_lines and not sections:
        # No H2 sections at all — treat entire content as one section
        sections.append(("main", "Project Rules",
                         "\n".join(preamble_lines).strip()))

    return sections


def _slugify(title: str) -> str:
    """Convert a section title to a filesystem-safe slug.

    'Environment (MANDATORY)' -> 'environment'
    'Coding Standards' -> 'coding-standards'
    'Workflows — stx-designer Commands' -> 'workflows'
    """
    # Take text before — or ( if present
    text = re.split(r"[—(]", title)[0].strip()
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text or "section"


def transform_arguments(content: str) -> tuple[str, bool]:
    """Replace Claude argument placeholders with Cursor-compatible notes.

    Returns:
        (transformed_content, had_arguments)
    """
    had_args = "$ARGUMENTS" in content or re.search(r"\$\d+", content)

    if not had_args:
        return content, False

    # Replace $ARGUMENTS
    content = content.replace("$ARGUMENTS", "{{USER_INPUT}}")

    # Replace $1, $2, etc.
    content = re.sub(r"\$(\d+)", r"{{ARG_\1}}", content)

    # Add note at top (after first H1 if present)
    note = (
        "\n> **Note (Cursor)**: This command was converted from Claude Code. "
        "Argument placeholders (`{{USER_INPUT}}`) are not dynamically substituted "
        "in Cursor — provide your arguments directly in the chat input after "
        "invoking the command.\n"
    )
    # Insert after first H1 line
    lines = content.splitlines()
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_idx = i + 1
            break

    lines.insert(insert_idx, note)
    return "\n".join(lines), True


def resolve_imports(content: str, source_dir: Path) -> str:
    """Resolve @path/to/file references in CLAUDE.md content.

    If the referenced file exists, inline its content.
    Otherwise, add an HTML comment noting the unresolved reference.
    """
    def replace_import(m: re.Match) -> str:
        ref_path = m.group(1)
        # Try relative to source_dir (which is .claude/)
        full_path = source_dir / ref_path.lstrip("./")
        if full_path.exists() and full_path.is_file():
            return full_path.read_text(encoding="utf-8").rstrip()
        # Also try from project root (parent of .claude/)
        project_root = source_dir.parent
        full_path = project_root / ref_path.lstrip("./")
        if full_path.exists() and full_path.is_file():
            return full_path.read_text(encoding="utf-8").rstrip()
        return f"<!-- Claude ref: @{ref_path} (not resolved) -->"

    # Match lines like: @.claude/references/coding_standards.md
    # or inline references like: See @path/to/file for details
    # Only match standalone @path patterns (not email-like @user patterns)
    return re.sub(r"(?<!\w)@(\.?[a-zA-Z0-9_/.:-]+\.md\b)", replace_import, content)


def write_file(path: Path, content: str, *, dry_run: bool = False,
               verbose: bool = False, report: ConversionReport | None = None
               ) -> None:
    """Write content to a file, creating parent directories as needed."""
    if verbose:
        print(f"  {'[DRY] ' if dry_run else ''}Write: {path}")

    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    if report is not None:
        report.files_written.append(str(path))


# ---------------------------------------------------------------------------
# Converters (C1-C11)
# ---------------------------------------------------------------------------

def convert_claude_md(source_dir: Path, target_dir: Path,
                      *, dry_run: bool, verbose: bool,
                      report: ConversionReport) -> None:
    """C1: CLAUDE.md -> split into .cursor/rules/00-project-*.mdc"""
    # CLAUDE.md is at the project root (parent of .claude/)
    claude_md = source_dir.parent / "CLAUDE.md"
    if not claude_md.exists():
        report.skip("CLAUDE.md not found")
        return

    content = claude_md.read_text(encoding="utf-8")

    # Resolve @imports before splitting
    content = resolve_imports(content, source_dir)

    # Remove Jinja2 artifacts if template wasn't fully rendered
    content = re.sub(r"\{%.*?%\}\n?", "", content)
    content = re.sub(r"\{\{.*?\}\}", "", content)

    sections = split_by_h2(content)

    rules_dir = target_dir / "rules"
    for slug, title, section_content in sections:
        if not section_content.strip():
            continue
        filename = f"00-project-{slug}.mdc"
        mdc = wrap_mdc(
            section_content,
            description=f"Project rules — {title}",
            always_apply=True,
        )
        write_file(rules_dir / filename, mdc,
                    dry_run=dry_run, verbose=verbose, report=report)
        report.rules_always += 1


def convert_references(source_dir: Path, target_dir: Path,
                       *, dry_run: bool, verbose: bool,
                       report: ConversionReport) -> None:
    """C2: .claude/references/*.md -> .cursor/rules/01-ref-*.mdc"""
    refs_dir = source_dir / "references"
    if not refs_dir.exists():
        return

    rules_dir = target_dir / "rules"
    for md_file in sorted(refs_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        stem = md_file.stem  # e.g. "coding_standards"
        slug = stem.replace("_", "-")
        desc = extract_description(content)

        mdc = wrap_mdc(content, description=desc, always_apply=True)
        write_file(rules_dir / f"01-ref-{slug}.mdc", mdc,
                    dry_run=dry_run, verbose=verbose, report=report)
        report.rules_always += 1


def convert_commands(source_dir: Path, target_dir: Path,
                     *, dry_run: bool, verbose: bool,
                     report: ConversionReport) -> None:
    """C3: .claude/commands/ -> .cursor/commands/ (with $ARGUMENTS transform)"""
    cmds_dir = source_dir / "commands"
    if not cmds_dir.exists():
        return

    out_dir = target_dir / "commands"
    args_count = 0

    for md_file in sorted(cmds_dir.rglob("*.md")):
        rel = md_file.relative_to(cmds_dir)
        content = md_file.read_text(encoding="utf-8")
        content, had_args = transform_arguments(content)
        if had_args:
            args_count += 1

        write_file(out_dir / rel, content,
                    dry_run=dry_run, verbose=verbose, report=report)
        report.commands += 1

    if args_count:
        report.warn(f"$ARGUMENTS in {args_count} command(s) replaced by note")


def convert_skills(source_dir: Path, target_dir: Path,
                   *, dry_run: bool, verbose: bool,
                   report: ConversionReport) -> None:
    """C4/C5/C10: skills/ -> .cursor/rules/skill-*.mdc (Agent Requested)"""
    rules_dir = target_dir / "rules"

    # Scan all skill directories
    skill_dirs = [
        ("", source_dir / "designer" / "skills"),
        ("", source_dir / "developer" / "skills"),
        ("pres-", source_dir / "designer" / "presentation" / "skills"),
        ("ce-", source_dir / "ce" / "skills"),
    ]

    for prefix, skill_dir in skill_dirs:
        if not skill_dir.exists():
            continue
        for md_file in sorted(skill_dir.glob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            slug = md_file.stem.replace("_", "-")
            desc = extract_description(content)

            mdc = wrap_mdc(content, description=desc, always_apply=False)
            write_file(rules_dir / f"skill-{prefix}{slug}.mdc", mdc,
                        dry_run=dry_run, verbose=verbose, report=report)
            report.rules_agent_requested += 1


def convert_agents(source_dir: Path, target_dir: Path,
                   *, dry_run: bool, verbose: bool,
                   report: ConversionReport) -> None:
    """C6/C11: agents/ -> .cursor/rules/agent-*.mdc (Agent Requested)"""
    rules_dir = target_dir / "rules"
    agent_count = 0

    agent_dirs = [
        ("", source_dir / "designer" / "agents"),
        ("", source_dir / "developer" / "agents"),
        ("pres-", source_dir / "designer" / "presentation" / "agents"),
        ("ce-", source_dir / "ce" / "agents"),
    ]

    warning = (
        "<!-- Converted from Claude Code agent. Original features lost: "
        "subagent isolation, dedicated model, tool restrictions, "
        "persistent memory. This rule provides the agent's knowledge "
        "as context only. -->\n\n"
    )

    for prefix, agent_dir in agent_dirs:
        if not agent_dir.exists():
            continue
        for md_file in sorted(agent_dir.glob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            slug = md_file.stem.replace("_", "-")
            desc = extract_description(content)
            desc += " (originally a Claude subagent)"

            mdc = wrap_mdc(
                warning + content,
                description=desc,
                always_apply=False,
            )
            write_file(rules_dir / f"agent-{prefix}{slug}.mdc", mdc,
                        dry_run=dry_run, verbose=verbose, report=report)
            report.rules_agent_requested += 1
            agent_count += 1

    if agent_count:
        report.warn(
            f"{agent_count} agent(s) converted to rules (lost: isolation, "
            "dedicated model, memory)"
        )


def convert_templates(source_dir: Path, target_dir: Path,
                      *, dry_run: bool, verbose: bool,
                      report: ConversionReport) -> None:
    """C7: templates/ -> .cursor/commands/templates/*.md"""
    tpl_dirs = [
        source_dir / "designer" / "templates",
        source_dir / "ce" / "templates",
    ]

    out_dir = target_dir / "commands" / "templates"
    header = (
        "> **Template**: Use this command to scaffold a new project "
        "using this template.\n"
        "> Provide your project description after the slash command.\n\n"
    )

    for tpl_dir in tpl_dirs:
        if not tpl_dir.exists():
            continue
        for md_file in sorted(tpl_dir.glob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            # Insert header after H1
            lines = content.splitlines()
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("# "):
                    insert_idx = i + 1
                    break
            lines.insert(insert_idx, "\n" + header)

            write_file(out_dir / md_file.name, "\n".join(lines),
                        dry_run=dry_run, verbose=verbose, report=report)
            report.commands += 1


def convert_tools(source_dir: Path, target_dir: Path,
                  *, dry_run: bool, verbose: bool,
                  report: ConversionReport) -> None:
    """C8: tools/ -> .cursor/commands/tools/*.md"""
    tools_dir = source_dir / "designer" / "tools"
    if not tools_dir.exists():
        return

    out_dir = target_dir / "commands" / "tools"
    header = (
        "> **Tool**: This command runs a specialized conversion/analysis tool.\n"
        "> Provide your arguments after the slash command.\n\n"
    )

    for md_file in sorted(tools_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        content, _ = transform_arguments(content)

        lines = content.splitlines()
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith("# "):
                insert_idx = i + 1
                break
        lines.insert(insert_idx, "\n" + header)

        write_file(out_dir / md_file.name, "\n".join(lines),
                    dry_run=dry_run, verbose=verbose, report=report)
        report.commands += 1


def convert_permissions(source_dir: Path, target_dir: Path,
                        *, dry_run: bool, verbose: bool,
                        report: ConversionReport) -> None:
    """C9: .claude/settings.json permissions -> .cursor/rules/00-permissions.mdc"""
    settings_path = source_dir / "settings.json"
    if not settings_path.exists():
        return

    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        report.warn("settings.json could not be parsed")
        return

    permissions = settings.get("permissions", {})
    allow_list = permissions.get("allow", [])

    if not allow_list:
        return

    # Build human-readable content
    lines = ["# Allowed Commands\n"]
    lines.append("The following terminal commands are pre-approved "
                 "and can be run without user confirmation:\n")

    for rule in allow_list:
        # Parse "Bash(pattern)" format
        m = re.match(r"Bash\((.+)\)", rule)
        if m:
            pattern = m.group(1)
            lines.append(f"- `{pattern}`")
        else:
            lines.append(f"- `{rule}`")

    content = "\n".join(lines)
    mdc = wrap_mdc(
        content,
        description="Allowed terminal commands — reference for agent",
        always_apply=True,
    )

    rules_dir = target_dir / "rules"
    write_file(rules_dir / "00-permissions.mdc", mdc,
                dry_run=dry_run, verbose=verbose, report=report)
    report.rules_always += 1


def convert_ignore(source_dir: Path, target_dir: Path,
                   *, dry_run: bool, verbose: bool,
                   report: ConversionReport) -> None:
    """Convert .claudeignore -> .cursorignore"""
    # .claudeignore is at project root (parent of .claude/)
    project_root = source_dir.parent
    claudeignore = project_root / ".claudeignore"

    if not claudeignore.exists():
        return

    content = claudeignore.read_text(encoding="utf-8")
    # .cursorignore goes at project root, not inside .cursor/
    cursorignore = project_root / ".cursorignore"

    write_file(cursorignore, content,
                dry_run=dry_run, verbose=verbose, report=report)
    report.ignore += 1


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def generate_report(report: ConversionReport, source: Path,
                    target: Path) -> str:
    """Generate a human-readable conversion report."""
    # Detect profile from .stx-profile marker
    profile_marker = source / ".stx-profile"
    profile = "unknown"
    if profile_marker.exists():
        profile = profile_marker.read_text(encoding="utf-8").strip()

    w = 50
    lines = [
        "+" + "-" * w + "+",
        f"|{'Conversion Claude -> Cursor':^{w}}|",
        "+" + "-" * w + "+",
        f"|  {'Source':12}: {str(source):<{w - 17}}|",
        f"|  {'Target':12}: {str(target):<{w - 17}}|",
        f"|  {'Profile':12}: {profile:<{w - 17}}|",
        "|" + " " * w + "|",
        f"|  {'Rules (.mdc)':20}: {report.total_rules:<{w - 25}}|",
        f"|    {'Always':18}: {report.rules_always:<{w - 27}}|",
        f"|    {'Agent Requested':18}: {report.rules_agent_requested:<{w - 27}}|",
        f"|  {'Commands (.md)':20}: {report.commands:<{w - 25}}|",
        f"|  {'Ignore files':20}: {report.ignore:<{w - 25}}|",
    ]

    if report.warnings:
        lines.append("|" + " " * w + "|")
        lines.append(f"|  {'Warnings:':48}|")
        for warning in report.warnings:
            # Wrap long warnings
            text = f"  - {warning}"
            while len(text) > w - 2:
                lines.append(f"|{text[:w]}|")
                text = "    " + text[w:]
            lines.append(f"|{text:<{w}}|")

    if report.skipped:
        lines.append("|" + " " * w + "|")
        lines.append(f"|  {'Not converted:':48}|")
        for skip in report.skipped:
            lines.append(f"|  - {skip:<{w - 4}}|")

    # Always note non-convertible items
    lines.append("|" + " " * w + "|")
    lines.append(f"|  {'Non-convertible (by design):':48}|")
    lines.append(f"|  - {'Auto-memory (memory/)':<{w - 4}}|")
    lines.append(f"|  - {'Profile marker (.stx-profile)':<{w - 4}}|")
    lines.append(f"|  - {'Manifest (manifest.toml)':<{w - 4}}|")

    lines.append("+" + "-" * w + "+")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a .cursor/ directory from an installed "
                    "Claude .claude/ profile.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python generate_cursor.py                        # .claude/ -> .cursor/
  python generate_cursor.py --source .claude       # explicit source
  python generate_cursor.py --dry-run --verbose    # preview only
  python generate_cursor.py --clean                # remove .cursor/ first
""",
    )
    parser.add_argument(
        "--source", default=".claude",
        help="Path to the .claude/ source directory (default: ./.claude)",
    )
    parser.add_argument(
        "--target", default=".cursor",
        help="Path to the .cursor/ target directory (default: ./.cursor)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be generated without writing files",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Show details of each conversion",
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Remove target .cursor/ directory before generating",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    source = Path(args.source).resolve()
    target = Path(args.target).resolve()

    if not source.exists():
        print(f"Error: Source directory not found: {source}")
        print("Make sure a Claude profile is installed (.claude/ directory).")
        sys.exit(1)

    if args.clean and target.exists() and not args.dry_run:
        shutil.rmtree(target)
        if args.verbose:
            print(f"  Cleaned: {target}")

    report = ConversionReport()
    opts = dict(dry_run=args.dry_run, verbose=args.verbose, report=report)

    if args.verbose:
        mode = "[DRY RUN] " if args.dry_run else ""
        print(f"{mode}Converting {source} -> {target}\n")

    # Run all converters in dependency order
    convert_claude_md(source, target, **opts)      # C1
    convert_references(source, target, **opts)      # C2
    convert_commands(source, target, **opts)         # C3
    convert_skills(source, target, **opts)           # C4/C5/C10
    convert_agents(source, target, **opts)           # C6/C11
    convert_templates(source, target, **opts)        # C7
    convert_tools(source, target, **opts)            # C8
    convert_permissions(source, target, **opts)      # C9
    convert_ignore(source, target, **opts)           # C10

    # Print report
    print()
    print(generate_report(report, source, target))

    total = report.total_rules + report.commands + report.ignore
    if total == 0:
        print("\nNo files generated. Is the source a valid .claude/ directory?")
        sys.exit(1)

    if args.dry_run:
        print(f"\n[DRY RUN] {total} files would be generated.")
    else:
        print(f"\n{total} files generated successfully.")


if __name__ == "__main__":
    main()
