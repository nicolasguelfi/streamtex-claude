# /stx-ce:review — Multi-perspective document review

Arguments: $ARGUMENTS

## Options

- `--perspective <name>` — Run only one perspective (audience|pedagogy|visual|style|editorial)
- `--help` — Show stx-ce cheatsheet

## Description

Reviews the document from 5 complementary perspectives using specialized agents:

| Perspective | Agent | What it evaluates |
|-------------|-------|-------------------|
| Reader/Learner | audience-advocate | Clarity, progression, prerequisites, engagement |
| Pedagogical | pedagogy-analyst | Objectives, alignment, assessment, rhythm |
| Visual | visual-reviewer | Visual coherence, readability, accessibility |
| Technical | style-consistency-checker | CSS styles, StreamTeX conventions, book.py |
| Editorial | content-editor | Writing quality, tone, terminology, references |

Findings are classified: CRITICAL / MAJOR / MINOR / SUGGESTION.

## Examples

- `/stx-ce:review` — Full 5-perspective review
- `/stx-ce:review --perspective visual` — Visual review only

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-review.md` — Full workflow
2. `.claude/designer/skills/visual-design-rules.md` — Visual rules
3. `.claude/designer/skills/style-conventions.md` — Style rules
- Load project design guideline (`custom/design-guideline.md`) if present
- Pass guideline context to visual-reviewer and style-consistency-checker agents

## Workflow

Execute the `ce-review` skill. GATE: Review results presented to user for validation. Suggest `/stx-ce:fix` as next step.

The review report must include a **Guideline Compliance** section:

### Guideline Compliance
- Status: COMPLIANT / PARTIAL / NON-COMPLIANT
- Guideline: <name>
- Violations: [list of violations with block references]

### Pattern Opportunities
- Identify recurring visual components across blocks that could be extracted as named patterns
- Propose pattern names and descriptions for `custom/design-guideline.md ## Patterns`
