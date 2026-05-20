# Template: course

StreamTeX pedagogical course with structured chapters.

## Defaults

| Setting | Value |
|---------|-------|
| Type | presentation |
| Audience | screen (upgrade to auditorium if user specifies projection) |
| Theme | dark |
| Pagination | yes |
| TOC | `NumberingMode.SIDEBAR_ONLY`, `sidebar_max_level=2`, `search=True` |
| Sidebar | `initial_sidebar_state="expanded"` |
| Banner | `BannerConfig.full()` |
| Marker | `MarkerConfig(auto_marker_on_toc=1, show_nav_ui=True)` |
| Body font | `s.text_lg` (palier 5, ≈14pt desktop responsive) |
| Title font | `s.text_7xl` (palier 16, ≈60pt desktop responsive) |
| Hero font | `s.text_9xl` (palier 19, ≈128pt desktop responsive) |
| Max blocks | 15 (otherwise suggest splitting into collection) |

### Design System Pack (recommended for any non-trivial project)

For any project beyond a single block, scaffold a project-specific
design system pack at init:

```bash
stx project new <name> --kit streamtex_design:project-default
# Creates ./mypack/ as the primary local pack

stx ds new default --pack mypack
# Creates ./mypack/design_systems/default.py

# Edit ./mypack/design_systems/default.py to declare the project's
# visual identity (colors, callouts, titles, body)
```

Then in `book.py`:

```python
from mypack.design_systems.default import DesignSystem as ProjectDS
from streamtex import st_book

st_book([...], design_system=ProjectDS())
```

This puts reusable styles in the pack (versionable, scope-able,
testable). Per-block specifics go in `BlockStyles` inside each block
file. See the `modular-design-philosophy` skill for the decision tree.

### Design Guideline (Optional)

Projects can adopt a design guideline for consistent visual design across all slides.
Recommended for courses: `academic-structured` or `maximize-viewport`.

- Available guidelines: `.claude/designer/guidelines/_index.md`
- Project config: Create `custom/design-guideline.md` referencing the chosen guideline
- Per-block override: Add `# @guideline: <name>` at top of block files

## Pedagogical structure

A course follows a strict pedagogical progression:

### Phase 1: Context (1-2 blocks)
- **Title block** — use `title_slide` component: course name, instructor, date
- **Objectives block** — use `takeaways` or `composite_block`: learning objectives as bullet points

### Phase 2: Core content (N blocks)
Each chapter follows the pattern:
- **Section header** — use `manual_section` or `slide_heading`: chapter title and overview
- **Concept explanation** — use `composite_block` + `narrative_transition`: key concepts with bullets
- **Illustration** — use `feature_walkthrough` or `composite_block`: diagram or AI-generated visual
- **Practical demo** — use `composite_block` with `st_code`: code examples with output
- **Exercise / quiz** — use `exercise_flow`: practice questions or key points

### Phase 3: Synthesis (1-2 blocks)
- **Summary** — use `takeaways`: key takeaways from all chapters
- **Next steps** — use `composite_block`: references, further reading, assignments

## Component mapping (default streamtex-design pack)

| Chapter element | Component | Notes |
|----------------|-----------|-------|
| Course title | `title_slide` | First slide |
| Learning objectives | `takeaways` or `composite_block` | Bullet list |
| Chapter header | `manual_section` / `slide_heading` | "Chapter N: Title" |
| Concept explanation | `composite_block` | Mix text + lists |
| Visual illustration | `feature_walkthrough` | Diagram + caption |
| Code demonstration | `composite_block` + `st_code` | Live code example |
| Comparison | `comparison_table` | "Approach A vs B" |
| Process/workflow | `exercise_flow` or `transition_gse` | Step-by-step |
| Key takeaway | `cite` or `evidence_insight` | Important message |
| Chapter summary | `takeaways` | End-of-chapter recap |
| Course conclusion | `takeaways` | Final takeaways |

If your installed pack does not expose one of these names, run
`stx component list` to discover what is available, or scaffold a
project-local component with `stx component new <name> --granularity composition`.

## Typical course structure (6 chapters)

```
 1.  bck_title              title_slide       Course title
 2.  bck_objectives         takeaways         Learning objectives
 3.  bck_ch1_header         manual_section    Chapter 1: Introduction
 4.  bck_ch1_content        composite_block   Chapter 1 content
 5.  bck_ch1_demo           composite_block   Chapter 1 demo (code)
 6.  bck_ch2_header         manual_section    Chapter 2: ...
 7.  bck_ch2_content        composite_block   Chapter 2 content
 8.  bck_ch2_comparison     comparison_table  Chapter 2 comparison
 ...
13.  bck_ch6_content        composite_block   Chapter 6 content
14.  bck_summary            takeaways         Course summary
15.  bck_next_steps         composite_block   References & assignments
```

## Reference files

- `.claude/designer/agents/project-architect.md` — architecture agent for planning
- `.claude/shared/skills/reuse-architecture.md` — pack/component catalog
- `stx component list` — browse every component installed in the project
- `stx component show <name>` — read a component's contract before using it
