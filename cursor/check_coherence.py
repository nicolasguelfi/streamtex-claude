#!/usr/bin/env python3
"""Coherence checks for the Claude -> Cursor conversion toolchain.

Verifies that generate_cursor.py, its documentation, and the CI stay in sync
with the evolving streamtex-claude profile structure.

Usage:
    python cursor/check_coherence.py          # run all checks
    python cursor/check_coherence.py --fix    # show suggested fixes
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent  # streamtex-claude/
CURSOR_DIR = REPO / "cursor"
PROFILES_DIR = REPO / "profiles"
SHARED_DIR = REPO / "shared"

ERRORS: list[str] = []
WARNINGS: list[str] = []
INFO: list[str] = []


def error(check: str, msg: str) -> None:
    ERRORS.append(f"[{check}] {msg}")


def warn(check: str, msg: str) -> None:
    WARNINGS.append(f"[{check}] {msg}")


def info(check: str, msg: str) -> None:
    INFO.append(f"[{check}] {msg}")


# -----------------------------------------------------------------------
# Check 1: CATEGORY_PATHS sync between install.py and generate_cursor.py
# -----------------------------------------------------------------------

def check_category_paths_sync() -> None:
    """Verify that generate_cursor.py scans the same directories as install.py."""
    tag = "C1-PathSync"

    install_py = (REPO / "install.py").read_text(encoding="utf-8")
    gen_py = (CURSOR_DIR / "generate_cursor.py").read_text(encoding="utf-8")

    # Extract all quoted paths from install.py CATEGORY_PATHS block
    # These look like: "designer/skills", "developer/agents", etc.
    install_paths: set[str] = set()
    in_category = False
    for line in install_py.splitlines():
        if "CATEGORY_PATHS" in line:
            in_category = True
        if in_category:
            for m in re.finditer(r'"((?:\w+/)+\w+)"', line):
                install_paths.add(m.group(1))
            if line.strip() == "}":
                in_category = False

    # Extract all path segments constructed via / operator in generate_cursor.py
    # Pattern: source_dir / "a" / "b" / "c" builds path a/b/c
    gen_paths: set[str] = set()
    for m in re.finditer(
        r'source_dir\s*(?:/\s*"(\w+)"\s*){1,4}',
        gen_py,
    ):
        # Re-extract individual segments from the matched region
        segments = re.findall(r'"(\w+)"', m.group(0))
        if segments:
            gen_paths.add("/".join(segments))

    errors_before = len(ERRORS)
    for path in install_paths - gen_paths:
        error(tag, f"install.py CATEGORY_PATHS has '{path}' not scanned by generate_cursor.py "
              f"-> add to the relevant convert_*() function")

    # Paths like "commands" and "references" are top-level dirs handled
    # by dedicated converters (convert_commands, convert_references) that
    # don't correspond to CATEGORY_PATHS entries — not a concern.
    extra_ok = {"commands", "references"}
    for path in gen_paths - install_paths - extra_ok:
        warn(tag, f"generate_cursor.py scans '{path}' not in install.py CATEGORY_PATHS "
             f"-> verify this path is intentional")

    if len(ERRORS) == errors_before:
        info(tag, f"install.py CATEGORY_PATHS ({len(install_paths)} paths) "
             f"and generate_cursor.py ({len(gen_paths)} paths) are in sync")


def _extract_function(source: str, name: str) -> str:
    """Extract the body of a top-level function from Python source."""
    # Match the function definition start (handles multi-line signatures)
    pattern = rf"^def {name}\("
    m = re.search(pattern, source, re.MULTILINE)
    if not m:
        return ""
    start = m.start()
    # Find next top-level def (no indentation) or end of file
    rest = source[start + 1:]  # skip past the 'd' of 'def'
    end_match = re.search(r"\ndef \w+\(", rest)
    if end_match:
        return source[start:start + 1 + end_match.start()]
    return source[start:]


# -----------------------------------------------------------------------
# Check 2: Every manifest category has a converter
# -----------------------------------------------------------------------

def check_manifest_categories_covered() -> None:
    """Verify every manifest.toml category is handled by generate_cursor.py."""
    tag = "C2-CatCoverage"

    gen_py = (CURSOR_DIR / "generate_cursor.py").read_text(encoding="utf-8")

    # Collect all categories used across all manifests
    all_categories: set[str] = set()
    for manifest_path in PROFILES_DIR.rglob("manifest.toml"):
        content = manifest_path.read_text(encoding="utf-8")
        for m in re.finditer(r"^\[(\w+)\]", content, re.MULTILINE):
            cat = m.group(1)
            if cat != "profile":
                all_categories.add(cat)

    # Known converters
    converter_map = {
        "commands": "convert_commands",
        "skills": "convert_skills",
        "agents": "convert_agents",
        "templates": "convert_templates",
        "tools": "convert_tools",
        "shared": "convert_references",  # shared -> references + commands
    }

    for cat in all_categories:
        if cat not in converter_map:
            error(tag, f"Manifest category '{cat}' has no converter in generate_cursor.py "
                  f"-> add convert_{cat}() function")
        elif converter_map[cat] not in gen_py:
            error(tag, f"Converter '{converter_map[cat]}' for category '{cat}' "
                  f"not found in generate_cursor.py")

    if not ERRORS:
        info(tag, f"All {len(all_categories)} manifest categories have converters")


# -----------------------------------------------------------------------
# Check 3: Conversion round-trip completeness
# -----------------------------------------------------------------------

def check_conversion_completeness() -> None:
    """Install each profile and verify generate_cursor.py converts all files."""
    tag = "C3-Completeness"

    # For each non-overlay profile, count declared files vs expected outputs
    for manifest_path in sorted(PROFILES_DIR.rglob("manifest.toml")):
        profile_dir = manifest_path.parent
        profile_name = profile_dir.name
        content = manifest_path.read_text(encoding="utf-8")

        extends = ""
        m = re.search(r'extends\s*=\s*"([^"]*)"', content)
        if m:
            extends = m.group(1)

        # Count declared files
        file_count = 0
        for line in content.splitlines():
            # Count items in arrays like ["a.md", "b.md"]
            arrays = re.findall(r'\[([^\]]+)\]', line)
            for arr in arrays:
                items = re.findall(r'"([^"]+\.md)"', arr)
                file_count += len(items)

        if file_count == 0:
            continue

        # Check that the profile would produce a reasonable output
        has_commands = "commands]" in content
        has_skills = "[skills]" in content
        has_agents = "[agents]" in content

        if has_commands:
            info(tag, f"{profile_name}: {file_count} files declared")
        if extends:
            info(tag, f"{profile_name}: extends '{extends}' -> inherits parent files")


# -----------------------------------------------------------------------
# Check 4: README.md conversion table matches generate_cursor.py
# -----------------------------------------------------------------------

def check_readme_sync() -> None:
    """Verify README.md conversion table lists all converter outputs."""
    tag = "C4-ReadmeSync"

    readme_path = CURSOR_DIR / "README.md"
    if not readme_path.exists():
        error(tag, "cursor/README.md not found")
        return

    readme = readme_path.read_text(encoding="utf-8")
    gen_py = (CURSOR_DIR / "generate_cursor.py").read_text(encoding="utf-8")

    # Extract output patterns from generate_cursor.py
    # Look for write_file calls with filename patterns
    output_patterns = set()
    for m in re.finditer(r'f?"([0-9a-z-]+(?:-\{|\*)[^"]*\.mdc?)"', gen_py):
        output_patterns.add(m.group(1))

    # Check README mentions key output types
    expected_in_readme = [
        "00-project-",     # C1: CLAUDE.md split
        "01-ref-",         # C2: references
        "skill-",          # C4/C5: skills
        "agent-",          # C6: agents
        "commands/",       # C3: commands
        "00-permissions",  # C9: permissions
        ".cursorignore",   # C10: ignore
        "templates/",      # C7: templates
        "tools/",          # C8: tools
    ]

    for pattern in expected_in_readme:
        if pattern not in readme:
            warn(tag, f"README.md missing mention of output pattern '{pattern}'")

    # Check README "Not converted" section mentions key omissions
    not_converted_keywords = ["memory", "agent", "$ARGUMENTS"]
    for kw in not_converted_keywords:
        if kw.lower() not in readme.lower():
            warn(tag, f"README.md 'Not converted' section should mention '{kw}'")

    if not WARNINGS:
        info(tag, "README.md conversion table is in sync")


# -----------------------------------------------------------------------
# Check 5: New profile files not covered by converters
# -----------------------------------------------------------------------

def check_new_uncovered_files() -> None:
    """Detect .md files in profiles that don't match any known converter path."""
    tag = "C5-UncoveredFiles"

    # Known directory patterns handled by generate_cursor.py
    known_patterns = [
        "commands/",
        "designer/skills/",
        "developer/skills/",
        "designer/agents/",
        "developer/agents/",
        "designer/templates/",
        "designer/tools/",
        "designer/presentation/skills/",
        "designer/presentation/agents/",
        "ce/skills/",
        "ce/agents/",
        "ce/templates/",
        "references/",
    ]

    for profile_dir in sorted(PROFILES_DIR.iterdir()):
        if not profile_dir.is_dir():
            continue

        # Check overlay dir for extending profiles, else check profile dir
        base = profile_dir / "overlay" if (profile_dir / "overlay").exists() else profile_dir

        for md_file in base.rglob("*.md"):
            rel = str(md_file.relative_to(base))
            if any(rel.startswith(p) for p in known_patterns):
                continue
            # Skip non-component files
            if md_file.name in ("README.md", "CLAUDE.md.j2"):
                continue
            warn(tag, f"{profile_dir.name}: '{rel}' not covered by any converter "
                 f"-> add handling in generate_cursor.py or document as intentionally skipped")


# -----------------------------------------------------------------------
# Check 6: Mapping document references valid component types
# -----------------------------------------------------------------------

def check_mapping_doc_freshness() -> None:
    """Verify claude-cursor-mapping.md mentions all component types from manifests."""
    tag = "C6-MappingDoc"

    mapping_path = CURSOR_DIR / "claude-cursor-mapping.md"
    if not mapping_path.exists():
        error(tag, "cursor/claude-cursor-mapping.md not found")
        return

    mapping = mapping_path.read_text(encoding="utf-8").lower()

    # Collect all unique directory names used in profiles
    component_types = set()
    for manifest_path in PROFILES_DIR.rglob("manifest.toml"):
        content = manifest_path.read_text(encoding="utf-8")
        for m in re.finditer(r"^\[(\w+)\]", content, re.MULTILINE):
            cat = m.group(1)
            if cat != "profile":
                component_types.add(cat)

    # "shared" is an internal install.py concept, not a user-facing component type.
    # "templates" appears as "Templates" or "template" in prose.
    internal_types = {"shared"}
    for ctype in component_types - internal_types:
        # Check for the word or its singular/plural forms
        variants = {ctype, ctype.rstrip("s"), ctype + "s"}
        if not any(v in mapping for v in variants):
            warn(tag, f"Mapping document does not mention component type '{ctype}' "
                 f"-> update Partie 1 taxonomy")

    info(tag, f"Checked {len(component_types)} component types against mapping document")


# -----------------------------------------------------------------------
# Check 7: CI validates cursor conversion
# -----------------------------------------------------------------------

def check_ci_integration() -> None:
    """Verify the CI workflow includes cursor conversion validation."""
    tag = "C7-CI"

    ci_path = REPO / ".github" / "workflows" / "validate.yml"
    if not ci_path.exists():
        error(tag, ".github/workflows/validate.yml not found")
        return

    ci = ci_path.read_text(encoding="utf-8")

    if "generate_cursor" not in ci and "check_coherence" not in ci:
        warn(tag, "CI workflow does not run cursor conversion or coherence checks "
             "-> add a step: python cursor/check_coherence.py")
    else:
        info(tag, "CI includes cursor validation")


# -----------------------------------------------------------------------
# Check 8: Converter count matches between generate_cursor.py main() and definitions
# -----------------------------------------------------------------------

def check_converter_wiring() -> None:
    """Verify all defined convert_* functions are called in main()."""
    tag = "C8-Wiring"

    gen_py = (CURSOR_DIR / "generate_cursor.py").read_text(encoding="utf-8")

    # Find all convert_* function definitions
    defined = set(re.findall(r"^def (convert_\w+)\(", gen_py, re.MULTILINE))
    # Find all convert_* calls in main()
    main_body = _extract_function(gen_py, "main")
    called = set(re.findall(r"(convert_\w+)\(", main_body))

    for fn in defined - called:
        error(tag, f"Converter '{fn}' is defined but not called in main()")
    for fn in called - defined:
        error(tag, f"main() calls '{fn}' but it is not defined")

    if defined == called:
        info(tag, f"All {len(defined)} converters are wired in main()")


# -----------------------------------------------------------------------
# Check 9: MDC frontmatter validity
# -----------------------------------------------------------------------

def check_mdc_output_validity() -> None:
    """Spot-check that wrap_mdc() produces valid MDC frontmatter."""
    tag = "C9-MDCFormat"

    gen_py = (CURSOR_DIR / "generate_cursor.py").read_text(encoding="utf-8")

    # Check wrap_mdc function exists
    if "def wrap_mdc(" not in gen_py:
        error(tag, "wrap_mdc() function not found in generate_cursor.py")
        return

    wrap_body = _extract_function(gen_py, "wrap_mdc")

    # Check required MDC fields are generated (may be inside f-strings)
    required_fields = ["description", "alwaysApply"]
    for fld in required_fields:
        if fld not in wrap_body:
            error(tag, f"wrap_mdc() does not reference MDC field '{fld}'")

    # Check it produces YAML delimiters (literal '---' strings)
    if '"---"' not in wrap_body and "'---'" not in wrap_body:
        error(tag, "wrap_mdc() should produce YAML frontmatter with --- delimiters")

    # Verify alwaysApply uses lowercase true/false (YAML boolean, in f-string)
    if "true" in wrap_body and "false" in wrap_body:
        info(tag, "wrap_mdc() produces valid MDC frontmatter")
    else:
        warn(tag, "wrap_mdc() may not produce correct YAML booleans (true/false)")


# -----------------------------------------------------------------------
# Check 10: New manifest subcategories
# -----------------------------------------------------------------------

def check_new_subcategories() -> None:
    """Detect new manifest subcategories not in generate_cursor.py."""
    tag = "C10-SubCats"

    gen_py = (CURSOR_DIR / "generate_cursor.py").read_text(encoding="utf-8")

    # Collect all subcategory keys from manifests
    # e.g. [skills] designer = [...] -> subcategory "designer" under "skills"
    subcats: dict[str, set[str]] = {}
    for manifest_path in PROFILES_DIR.rglob("manifest.toml"):
        content = manifest_path.read_text(encoding="utf-8")
        current_section = ""
        for line in content.splitlines():
            section_m = re.match(r"^\[(\w+)\]", line)
            if section_m:
                current_section = section_m.group(1)
                continue
            key_m = re.match(r"^(\w+)\s*=", line)
            if key_m and current_section not in ("profile", ""):
                subcats.setdefault(current_section, set()).add(key_m.group(1))

    # Check generate_cursor.py mentions each subcategory's path
    for category, subs in subcats.items():
        if category == "shared":
            continue  # shared is handled differently
        for sub in subs:
            # The converter should reference this subdirectory
            if sub not in gen_py:
                warn(tag, f"Manifest subcategory '{category}.{sub}' not referenced "
                     f"in generate_cursor.py -> may not be converted")

    info(tag, f"Checked {sum(len(v) for v in subcats.values())} subcategories")


# -----------------------------------------------------------------------
# Report
# -----------------------------------------------------------------------

def print_report() -> None:
    print("=" * 60)
    print("  Cursor Toolchain Coherence Audit")
    print("=" * 60)
    print()

    if ERRORS:
        print(f"ERRORS ({len(ERRORS)}) — must fix")
        for e in ERRORS:
            print(f"  ✗ {e}")
        print()

    if WARNINGS:
        print(f"WARNINGS ({len(WARNINGS)}) — should fix")
        for w in WARNINGS:
            print(f"  ⚠ {w}")
        print()

    if INFO:
        print(f"INFO ({len(INFO)})")
        for i in INFO:
            print(f"  ✓ {i}")
        print()

    total = len(ERRORS) + len(WARNINGS)
    if total == 0:
        print("All checks passed!")
    else:
        print(f"{len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Coherence checks for the Claude -> Cursor conversion toolchain.",
    )
    parser.add_argument("--fix", action="store_true",
                        help="Show suggested fixes for each issue")
    parser.parse_args()

    checks = [
        check_category_paths_sync,       # C1: install.py <-> generate_cursor.py paths
        check_manifest_categories_covered,  # C2: every manifest category has a converter
        check_conversion_completeness,     # C3: file count sanity
        check_readme_sync,                 # C4: README matches script output
        check_new_uncovered_files,         # C5: new .md files not handled
        check_mapping_doc_freshness,       # C6: mapping doc covers all types
        check_ci_integration,              # C7: CI runs cursor checks
        check_converter_wiring,            # C8: all converters called in main()
        check_mdc_output_validity,         # C9: MDC format correct
        check_new_subcategories,           # C10: new manifest subcategories
    ]

    for check_fn in checks:
        check_fn()

    print_report()
    sys.exit(1 if ERRORS else 0)


if __name__ == "__main__":
    main()
