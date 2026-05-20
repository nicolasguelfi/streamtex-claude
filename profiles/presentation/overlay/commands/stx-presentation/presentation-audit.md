Audit a StreamTeX presentation block for live projection compliance.

## Before Auditing

Read these files (mandatory):
1. `.claude/designer/presentation/skills/presentation-design-rules.md`
2. `.claude/designer/skills/visual-design-rules.md` (base rules)
3. The target project's `custom/styles.py`

## Target

Audit the block file specified by $ARGUMENTS. If no argument given, ask the user which block to audit.

## Audit Checklist

### CRITICAL (must fix before presenting)

1. **Font size — body text**: Body uses `s.text_4xl` (palier 12 = 32pt @ base 18) or larger, OR uses `base_pt_desktop=24` with `s.text_base` (effective 24pt = 32px). Paliers below 7 (`s.text_xs`/`s.text_sm`) on body = CRITICAL.
2. **Font size — titles**: Section titles use `s.text_7xl` (palier 16) or `s.text_8xl` (palier 17). Titles below palier 13 on main slides = CRITICAL.
2b. **ScaleConfig present**: For projection audiences, `book.py` should set `scale=ScaleConfig(base_pt_desktop=24)`. Missing for stated projection audience = ERROR.
3. **Keywords only**: No bullet exceeds 7 words. No section has more than 3 bullets.
4. **High contrast**: No `muted` or `subtle` color on body text (only on attribution/source).
5. **Image sizing**: No image below 400px width (except logos).
6. **PresentationConfig**: `book.py` must contain `PresentationConfig(aspect_ratio="16/9")`. Missing = CRITICAL.
7. **SlideBreakConfig fullscreen**: `SlideBreakConfig(fullscreen=True)` must be configured. Missing = CRITICAL.
8. **Slide breaks**: `st_slide_break()` must be present between each section/slide. Missing = CRITICAL.
9. **Footer config**: `PresentationConfig(footer=True)` must be set and no manual footer code in blocks. Manual footer = CRITICAL.

### ERROR (should fix)

6. **Generous spacing**: `st_space(size=3)` minimum between sections. Less = ERROR.
7. **One idea per section**: Sections with multiple unrelated concepts = ERROR.
8. **No helper boxes**: `show_explanation()`, `show_details()`, `show_code()` in presentation blocks = ERROR.
9. **Chart readability**: Chart labels/values below 20px font-size = ERROR.
10. **Visual first**: Sections with only text and no visual anchor = ERROR.

### WARNING (consider fixing)

11. **Spacing consistency**: Inconsistent spacing between similar elements = WARNING.
12. **Style reuse**: Repeated inline style compositions instead of `BlockStyles` class = WARNING.
13. **Attribution placement**: Source/footer text larger than palier 7 (`s.text_base`) = WARNING (too prominent).
14. **Density > 60%**: Slide content occupies more than 60% of the viewport surface = WARNING.
15. **Images with px**: Images sized with `px` instead of `%` or `vh` units = WARNING.
16. **Too many bullets**: More than 3 bullets in a fullscreen slide = WARNING.
17. **Numeric block prefixes**: Block filenames like `bck_01_title.py` instead of `bck_title.py` = WARNING.

### Structure checks (base rules)

14. **BlockStyles class**: Missing `BlockStyles` + `bs` alias = ERROR.
15. **build() function**: Missing `build()` function = ERROR.
16. **Imports**: Missing standard imports = WARNING.

## Output Format

```
# Presentation Audit: <filename>

## Summary
- CRITICAL: N issues
- ERROR: N issues
- WARNING: N issues

## CRITICAL Issues
### [C1] <rule name>
- **Line**: <line number>
- **Found**: <what's wrong>
- **Expected**: <what it should be>
- **Fix**: <specific fix instruction>

## ERROR Issues
### [E1] ...

## WARNING Issues
### [W1] ...

## Passed Checks
- [x] <check name>
```
