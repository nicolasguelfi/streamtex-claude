#!/usr/bin/env python3
"""Install a StreamTeX Claude AI profile into a project directory.

Usage:
    python install.py <profile> [target_dir]
    python install.py project ./my-project
    python install.py presentation ./my-presentation
    python install.py library ./streamtex
    python install.py documentation ./streamtex-docs
    python install.py --list
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        # Minimal TOML parser for manifest files (Python <3.11 without tomli)
        import json
        import re

        class _MinimalTOML:
            """Parse simple TOML manifests (enough for manifest.toml files)."""

            @staticmethod
            def load(f):  # noqa: ANN001, ANN205
                return _MinimalTOML.loads(f.read().decode("utf-8"))

            @staticmethod
            def loads(s: str) -> dict:
                result: dict = {}
                current_section: dict = result
                for line in s.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Section header [section] or [section.subsection]
                    m = re.match(r"^\[([^\]]+)\]$", line)
                    if m:
                        keys = m.group(1).split(".")
                        current_section = result
                        for key in keys:
                            current_section = current_section.setdefault(key, {})
                        continue
                    # Key = value
                    m = re.match(r'^(\w+)\s*=\s*(.+)$', line)
                    if m:
                        key, value = m.group(1), m.group(2).strip()
                        if value.startswith('"') and value.endswith('"'):
                            current_section[key] = value[1:-1]
                        elif value.startswith("["):
                            # Collect multi-line array
                            arr_str = value
                            current_section[key] = json.loads(arr_str.replace("'", '"'))
                        else:
                            current_section[key] = value
                return result

        tomllib = _MinimalTOML  # type: ignore[assignment, misc]

PROFILES_DIR = Path(__file__).parent / "profiles"
SHARED_DIR = Path(__file__).parent / "shared"

# Mapping from shared/ subdirectory to target .claude/ subdirectory.
# e.g. shared/skills/foo.md → .claude/developer/skills/foo.md
SHARED_DEST_PATHS: dict[str, str] = {
    "references": "references",
    "commands": "commands",
    "skills": "developer/skills",
    "agents": "developer/agents",
    "import-formats": "import-formats",
}

# Mapping from manifest category to filesystem paths
CATEGORY_PATHS = {
    "commands": "commands",
    "skills": {
        "designer": "designer/skills",
        "developer": "developer/skills",
        "presentation": "designer/presentation/skills",
        "ce": "ce/skills",
    },
    "agents": {
        "designer": "designer/agents",
        "developer": "developer/agents",
        "presentation": "designer/presentation/agents",
        "ce": "ce/agents",
    },
    "templates": {
        "designer": "designer/templates",
        "ce": "ce/templates",
    },
    "tools": {
        "designer": "designer/tools",
    },
    "guidelines": {
        "designer": "designer/guidelines",
        "presentation": "designer/presentation/guidelines",
    },
    "import-formats": "import-formats",
}


def _resolve_path(category: str, subdir: str) -> str:
    """Resolve a manifest category+subdir to a filesystem path."""
    mapping = CATEGORY_PATHS.get(category)
    if isinstance(mapping, dict):
        return mapping.get(subdir, f"{category}/{subdir}")
    return f"{mapping}/{subdir}"


def _copy_tree(src: Path, dst: Path) -> int:
    """Recursively copy src into dst, return count of files copied."""
    count = 0
    for item in src.rglob("*"):
        if item.is_file():
            rel = item.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            count += 1
    return count


def _render_template(template_path: Path, output_path: Path,
                     project_name: str, profile_name: str) -> None:
    """Render a Jinja2 template to produce CLAUDE.md."""
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError:
        # Fallback: simple string replacement if jinja2 not installed
        content = template_path.read_text(encoding="utf-8")
        content = content.replace("{{ project_name }}", project_name)
        content = content.replace("{{ profile }}", profile_name)
        # Handle simple conditionals by keeping everything (no stripping)
        output_path.write_text(content, encoding="utf-8")
        return

    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        keep_trailing_newline=True,
    )
    template = env.get_template(template_path.name)
    claude_md = template.render(
        project_name=project_name,
        profile=profile_name,
    )
    output_path.write_text(claude_md, encoding="utf-8")


def install_profile(profile_name: str, target_dir: Path,
                    project_name: str = "") -> bool:
    """Install a Claude AI profile into the target directory.

    Args:
        profile_name: Name of the profile (project, presentation, library, documentation)
        target_dir: Target project directory
        project_name: Project name for CLAUDE.md template (defaults to target_dir.name)

    Returns:
        True if installation succeeded
    """
    profile_dir = PROFILES_DIR / profile_name
    manifest_path = profile_dir / "manifest.toml"

    if not manifest_path.exists():
        print(f"Error: Profile '{profile_name}' not found at {profile_dir}")
        available = [p.name for p in PROFILES_DIR.iterdir() if p.is_dir()]
        print(f"Available profiles: {', '.join(sorted(available))}")
        return False

    with open(manifest_path, "rb") as f:
        manifest = tomllib.load(f)

    project_name = project_name or target_dir.name
    target_claude = target_dir / ".claude"
    target_claude.mkdir(parents=True, exist_ok=True)

    total_files = 0
    extends = manifest.get("profile", {}).get("extends", "")

    if extends:
        # Install parent profile first
        print(f"  Installing parent profile '{extends}'...")
        install_profile(extends, target_dir, project_name)

        # Then overlay additional files
        overlay_dir = profile_dir / "overlay"
        if overlay_dir.exists():
            count = _copy_tree(overlay_dir, target_claude)
            total_files += count
            print(f"  Overlaid {count} files from '{profile_name}'")
    else:
        # Copy files from manifest categories
        for category in ["commands", "skills", "agents", "templates", "tools",
                         "guidelines", "import-formats"]:
            if category not in manifest:
                continue
            for subdir, files in manifest[category].items():
                fs_path = _resolve_path(category, subdir)
                src_dir = profile_dir / fs_path
                dst_dir = target_claude / fs_path
                dst_dir.mkdir(parents=True, exist_ok=True)
                for filename in files:
                    src_entry = src_dir / filename
                    if not src_entry.exists():
                        print(f"  Warning: {src_entry} not found, skipping")
                        continue
                    if src_entry.is_dir():
                        count = _copy_tree(src_entry, dst_dir / filename)
                        total_files += count
                    else:
                        shutil.copy2(src_entry, dst_dir / filename)
                        total_files += 1

    # Copy shared resources (read-only copies)
    if "shared" in manifest:
        for subdir, files in manifest["shared"].items():
            src_dir = SHARED_DIR / subdir
            dest_subdir = SHARED_DEST_PATHS.get(subdir, subdir)
            dst_dir = target_claude / dest_subdir
            dst_dir.mkdir(parents=True, exist_ok=True)
            for entry_name in files:
                src_entry = src_dir / entry_name
                if not src_entry.exists():
                    print(f"  Warning: shared/{subdir}/{entry_name} not found, skipping")
                    continue
                if src_entry.is_dir():
                    dst_entry_dir = dst_dir / entry_name
                    dst_entry_dir.mkdir(parents=True, exist_ok=True)
                    count = _copy_tree(src_entry, dst_entry_dir)
                    for item in dst_entry_dir.rglob("*"):
                        if item.is_file():
                            item.chmod(0o444)
                    total_files += count
                else:
                    dst_file = dst_dir / entry_name
                    shutil.copy2(src_entry, dst_file)
                    dst_file.chmod(0o444)
                    total_files += 1

    # Clean up legacy command directories (renamed in v2: stx-designer/stx-project/stx-developer → stx-block)
    for legacy_dir in ["commands/stx-designer", "commands/stx-project", "commands/stx-developer"]:
        legacy_path = target_claude / legacy_dir
        if legacy_path.exists():
            shutil.rmtree(legacy_path)
            print(f"  Removed legacy directory: {legacy_dir}")

    # Copy settings.json
    settings_src = profile_dir / "settings.json"
    if settings_src.exists():
        shutil.copy2(settings_src, target_claude / "settings.json")
        total_files += 1

    # Generate CLAUDE.md from template
    template_path = profile_dir / "CLAUDE.md.j2"
    if not template_path.exists() and extends:
        template_path = PROFILES_DIR / extends / "CLAUDE.md.j2"

    if template_path.exists():
        _render_template(template_path, target_dir / "CLAUDE.md",
                         project_name, profile_name)
        total_files += 1

    # Write profile marker
    (target_claude / ".stx-profile").write_text(profile_name, encoding="utf-8")

    print(f"Installed profile '{profile_name}' -> {target_dir}")
    print(f"  {total_files} files installed")
    return True


def list_profiles() -> None:
    """List all available profiles with their descriptions."""
    print("Available Claude AI Profiles")
    print("=" * 58)
    for profile_dir in sorted(PROFILES_DIR.iterdir()):
        if not profile_dir.is_dir():
            continue
        manifest_path = profile_dir / "manifest.toml"
        if not manifest_path.exists():
            continue
        with open(manifest_path, "rb") as f:
            manifest = tomllib.load(f)
        info = manifest.get("profile", {})
        name = info.get("name", profile_dir.name)
        desc = info.get("description", "")
        extends = info.get("extends", "")

        print(f"\n  {name:<18} {desc}")
        if extends:
            print(f"  {'':18} (extends: {extends})")

        # Show command counts
        commands = manifest.get("commands", {})
        if commands:
            parts = [f"{k}({len(v)})" for k, v in commands.items()]
            print(f"  {'':18} Commands: {', '.join(parts)}")

        skills = manifest.get("skills", {})
        if skills:
            parts = [f"{k}({len(v)})" for k, v in skills.items()]
            print(f"  {'':18} Skills: {', '.join(parts)}")

        agents = manifest.get("agents", {})
        if agents:
            parts = [f"{k}({len(v)})" for k, v in agents.items()]
            print(f"  {'':18} Agents: {', '.join(parts)}")

    print("\n" + "=" * 58)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Install a StreamTeX Claude AI profile into a project directory.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install.py project ./my-project
  python install.py presentation ./my-presentation
  python install.py library ./streamtex
  python install.py documentation ./streamtex-docs
  python install.py --list
        """,
    )
    parser.add_argument(
        "profile",
        nargs="?",
        help="Profile name: project, presentation, library, documentation",
    )
    parser.add_argument(
        "target_dir",
        nargs="?",
        default=".",
        help="Target project directory (default: current directory)",
    )
    parser.add_argument(
        "--name",
        help="Project name for CLAUDE.md (default: directory name)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available profiles",
    )

    args = parser.parse_args()

    if args.list:
        list_profiles()
        return

    if not args.profile:
        parser.error("profile is required (or use --list)")

    target = Path(args.target_dir).resolve()
    if not target.exists():
        target.mkdir(parents=True)
        print(f"Created target directory: {target}")

    success = install_profile(args.profile, target, args.name or "")
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
