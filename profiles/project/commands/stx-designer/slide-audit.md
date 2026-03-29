Audit a StreamTeX slide (block file) for visual design compliance.

Arguments: $ARGUMENTS (file path or block name, e.g. "bck_text_styles" or path to file)

## Steps

1. **Load rules**: Read `.claude/designer/skills/visual-design-rules.md`.
2. **Load guideline**: Read `custom/design-guideline.md` if present. Load the referenced guideline.
   Check for `@guideline` annotations in the block file being audited.
3. **Read the block file** specified in arguments.
4. **Check each rule** and report violations:

### Checklist

- [ ] **Block structure**: Has `BlockStyles` class, `bs` alias, `build()` function
- [ ] **Centered content**: `build()` wraps in `with st_block(s.center_txt):`
- [ ] **Heading**: Main heading uses `tag=t.div, toc_lvl="1"`
- [ ] **Imports**: Includes `helpers`
- [ ] **Line length**: No visible text line exceeds ~45 characters
- [ ] **No string concatenation**: No multi-arg string `st_write()` calls
- [ ] **Code before rendering**: Every live example preceded by `show_code()`
- [ ] **Multi-line strings**: All `show_explanation()`, `show_details()`, `show_code()` use `"""\..."""` (auto-dedented)
- [ ] **Body text size**: Uses `s.large` (32pt) for body, not `s.big`
- [ ] **WRONG explanations**: Every WRONG box explains WHY (uses `st_write` + `st_br`)
- [ ] **Default values**: Details sections document parameter defaults
- [ ] **Spacing**: `st_space("v", 2)` between sections, `st_space("v", 1)` within
- [ ] **Section structure**: subtitle -> explanation -> code -> rendering -> details
- [ ] **Pattern compliance**: If `@pattern:` annotation present, block follows the named pattern
- [ ] **Guideline compliance**: Follows project design guideline principles (if active)
- [ ] **Guideline archetype**: Content correctly handled per the matched archetype
- [ ] **No guideline anti-patterns**: None of the guideline's forbidden patterns present

5. **Report findings**: List all violations with line numbers and suggested fixes.
6. **Severity**: Mark each as ERROR (must fix) or WARNING (should fix).

## Output Format

```
## Audit: [block_name]

### PASS (N rules)
- [x] Rule description

### ERRORS (N)
- Line XX: [violation description] -> [fix suggestion]

### WARNINGS (N)
- Line XX: [violation description] -> [fix suggestion]
```
