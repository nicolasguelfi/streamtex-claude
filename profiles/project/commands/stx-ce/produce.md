# /stx-ce:produce — Execute the production plan

Arguments: $ARGUMENTS

## Options

- `--from-plan <path>` — Use a specific plan file (default: latest in docs/plans/)
- `--no-deploy` — Skip deployment step
- `--interactive` — Pause after each block/sequence for user validation
- `--granularity <level>` — Validation granularity: block (each block), sequence (group of related blocks), batch (current, with checkpoints)
- `--help` — Show stx-ce cheatsheet

## Description

Executes the production plan item by item. For each item, the appropriate StreamTeX command is invoked:

- **Import items**: `/stx-import:html`, `/stx-import:marp`, or manual conversion
- **Improvement items**: `/stx-designer:update`, `/stx-designer:style-refactor`
- **Creation items**: `/stx-designer:block-new`, `/stx-designer:slide-new`

Each item is audited after production (`/stx-designer:audit --target`) and fixed if needed. A global audit runs at the end.

For each block: classify content, match guideline archetype, and apply directives. Add `# @guideline: <name>` annotation at the top of each produced block file. Validate each block against guideline constraints before moving to the next.

### Interactive Mode (`--interactive`)

When enabled, production pauses at validation points for user review:

- **Per block** (`--granularity block`): Validate each produced block individually. Best for <10 blocks.
- **Per sequence** (`--granularity sequence`): Produce related blocks together, validate the group. Best for 10-25 blocks.
- **Batch with checkpoints** (`--granularity batch`, default): Current behavior with periodic checkpoints. Best for 25+ blocks.

If `--interactive` is used without `--granularity`, the granularity is auto-selected based on plan size.

At each validation point:
1. Show the produced block(s) with guideline archetype and pattern annotations
2. Run targeted audit (`/stx-designer:audit --target`)
3. Present results: Accept / Revise / Skip
4. If Revise: user provides feedback, block is regenerated

## Examples

- `/stx-ce:produce` — Execute latest plan
- `/stx-ce:produce --from-plan docs/plans/2026-03-22-001-import-mycourse-plan.md`
- `/stx-ce:produce --no-deploy` — Produce without deploying

## Required Readings

Before executing, read:
1. `.claude/ce/skills/ce-produce.md` — Full workflow
2. `docs/plans/` — The plan to execute
3. `.claude/references/streamtex_cheatsheet_en.md` — StreamTeX API reference
- **Load design guideline**: If the plan references a guideline, verify the file exists
  in `.claude/designer/guidelines/` and load it. Pass guideline context to all
  designer commands invoked during production.
- **Load design patterns**: Check `custom/design-guideline.md` for `## Patterns` section.
  When producing a block that matches an existing pattern (e.g., a table, a card grid),
  apply the named pattern's recipe instead of designing from scratch.
  Add `# @pattern: <name>` annotation to blocks that use a pattern.

## Workflow

Execute the `ce-produce` skill. Track progress with task list. Run global audit at the end.
