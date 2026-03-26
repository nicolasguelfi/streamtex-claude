# Template: Plan Improve

Improvement production plan — detailed execution plan for enhancing an existing StreamTeX document.

## Structure

```markdown
# Production Plan — Pathway B: IMPROVEMENT

## Metadata

| Field | Value |
|-------|-------|
| Project | <project name> |
| Pathway | IMPROVEMENT |
| Planning mode | <auto / interactive> |
| Current state | <number of blocks, parts> |
| Audit findings | <CRITICAL: n, MAJOR: n, MINOR: n> |
| Assess report ref | <assess report file or date> |
| Estimated effort | <low / medium / high> |

## Improvements

| # | Block | Action | Type | Reason | Effort |
|---|-------|--------|------|--------|--------|
| 1 | <block_name> | <revise / rewrite / split / merge / add / remove / restyle> | <content / style / structure> | <gap or issue reference> | <low / medium / high> |
| 2 | <...> | <...> | <...> | <...> | <...> |

## Document Structure

### Skeleton (validated)

| Part | Section | Objective | Changes | Blocks |
|------|---------|-----------|---------|--------|
| <Part 1: Title> | <Section 1.1> | <what this section achieves> | <new / revised / unchanged> | <block_name_1, block_name_2> |
| | <Section 1.2> | <...> | <...> | <...> |
| <Part 2: Title> | <Section 2.1> | <...> | <...> | <...> |

### Skeleton Validation

- [ ] All improvements are mapped to specific blocks
- [ ] No structural regressions introduced
- [ ] Part progression remains logical
- [ ] Block count after improvements: <number>

## Design Choices

| Aspect | Current | Revised | Rationale |
|--------|---------|---------|-----------|
| Theme | <current> | <revised or "unchanged"> | <why> |
| Color palette | <current> | <revised or "unchanged"> | <why> |
| Layouts | <current> | <revised or "unchanged"> | <why> |
| Typography | <current> | <revised or "unchanged"> | <why> |
| Asset types | <current> | <revised or "unchanged"> | <why> |

### Presentation Profiles

| Aspect | Current | Revised | Rationale |
|--------|---------|---------|-----------|
| Preset | <current preset or "none"> | <revised or "unchanged"> | <why> |

| Profile Name | ViewMode | Width% | Zoom% | SlideBreak Enabled | SlideBreak Mode | Change |
|-------------|----------|--------|-------|-------------------|-----------------|--------|
| <profile name> | <PAGINATED / CONTINUOUS> | <width%> | <zoom%> | <yes / no> | <PAGINATED / CONTINUOUS / HIDDEN> | <new / revised / unchanged> |
| <...> | <...> | <...> | <...> | <...> | <...> | <...> |

**book.py config**: `ProfileConfig` setup with `save()`/`load()` and selected profiles.

### Section Spacing

| Level | Current | Revised | Rationale |
|-------|---------|---------|-----------|
| Global (`set_spacing()`) | <current Spacing values> | <revised or "unchanged"> | <why> |
| Per-profile overrides | <current overrides> | <revised or "unchanged"> | <why> |
| Per-block overrides | <blocks with `set_block_spacing()`> | <revised or "unchanged"> | <why> |

**Override hierarchy**: built-in < book < profile < block < call-site

### Bibliography Setup

| Aspect | Current | Revised | Rationale |
|--------|---------|---------|-----------|
| Source | <current path or `none`> | <revised or "unchanged"> | <why> |
| Format | <current BibFormat or `none`> | <revised or "unchanged"> | <why> |
| Citation style | <current CitationStyle or `none`> | <revised or "unchanged"> | <why> |
| Placement | <current block or `none`> | <revised or "unchanged"> | <why> |

**book.py config**: `set_bib_config(BibConfig(format=BibFormat.APA, style=CitationStyle.AUTHOR_YEAR))`

<If no bibliography: "No bibliography — `none`.">

### AI Image Configuration

| Aspect | Current | Revised | Rationale |
|--------|---------|---------|-----------|
| Provider | <current provider or `none`> | <revised or "unchanged"> | <why> |
| Model | <current model or `none`> | <revised or "unchanged"> | <why> |
| Default size | <current size> | <revised or "unchanged"> | <why> |
| Default quality | <current quality> | <revised or "unchanged"> | <why> |
| Generation mode | <manual / auto> | <revised or "unchanged"> | <why> |
| Seed strategy | <current strategy> | <revised or "unchanged"> | <why> |

#### Prompt Guidelines

- Visual style: <realistic / illustration / diagram / abstract>
- Color temperature: <warm / cool / neutral — aligned with document palette>
- Consistency rules: <shared style terms to use across all prompts>

**book.py config**: `set_ai_image_config(AIImageConfig(provider="openai", model="gpt-image-1", size="1024x1024", quality="standard"))`

<If no AI images: "No AI images — `none`.">

### Export Configuration

| Aspect | Current | Revised | Rationale |
|--------|---------|---------|-----------|
| Asset mode | <current AssetMode or "default (EXTERNAL)"> | <revised or "unchanged"> | <why> |
| Export mode | <current ExportMode or "default (MANUAL)"> | <revised or "unchanged"> | <why> |
| PDF export | <yes / no> | <revised or "unchanged"> | <why> |
| PDF config | <current PdfConfig or `none`> | <revised or "unchanged"> | <why> |

**book.py config**: `ExportConfig(asset_mode=AssetMode.EXTERNAL, mode=ExportMode.MANUAL)`

<If no export changes: "Export configuration unchanged.">

## External Sources to Integrate

<If pathway A+B:>

| Source | Purpose | Import Method | Target Block(s) |
|--------|---------|--------------|-----------------|
| <source name> | <what it adds> | <pandoc / manual / partial> | <block name(s)> |

<If pure B: "No external sources — improvement only.">

## Execution Order

| Step | Action | Blocks Affected | Dependencies |
|------|--------|----------------|-------------|
| 1 | <action description> | <block name(s)> | <none / step #> |
| 2 | <...> | <...> | <...> |
| 3 | <...> | <...> | <...> |

## Pre-Production Checklist

- [ ] Current document backed up or committed
- [ ] Audit report reviewed and findings confirmed
- [ ] Design changes validated against profile
- [ ] book.py skeleton updated to reflect structural changes
- [ ] New assets prepared (if any)
- [ ] External sources accessible (if pathway A+B)
- [ ] No conflicting edits in progress
- [ ] AI image provider API key available (if AI images configured)

## Next Step

Proceed with `/stx-ce:produce` to execute this plan.
```
