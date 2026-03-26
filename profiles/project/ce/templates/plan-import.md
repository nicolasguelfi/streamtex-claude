# Template: Plan Import

Import production plan — detailed execution plan for importing external sources into a StreamTeX project.

## Structure

```markdown
# Production Plan — Pathway A: IMPORT

## Metadata

| Field | Value |
|-------|-------|
| Project | <project name> |
| Profile | <design profile name> |
| Pathway | IMPORT |
| Planning mode | <auto / interactive> |
| Sources to import | <number> |
| Assess report ref | <assess report file or date> |
| Estimated effort | <low / medium / high> |

## Sources to Import

| # | Source | Import Method | Target Block(s) | Effort |
|---|--------|--------------|-----------------|--------|
| 1 | <source name> | <pandoc / manual / partial> | <block_name_1, block_name_2> | <low / medium / high> |
| 2 | <...> | <...> | <...> | <...> |

## Document Structure

### Skeleton

| Part | Section | Objective | Sources | Content Type | Detail Level | Blocks |
|------|---------|-----------|---------|-------------|-------------|--------|
| <Part 1: Title> | <Section 1.1> | <what this section achieves> | <source #s> | <text / code / mixed / visual> | <overview / detailed / reference> | <block_name_1, block_name_2> |
| | <Section 1.2> | <...> | <...> | <...> | <...> | <...> |
| <Part 2: Title> | <Section 2.1> | <...> | <...> | <...> | <...> | <...> |

### Skeleton Validation

- [ ] All sources are assigned to at least one section
- [ ] No orphan sections (every section has at least one block)
- [ ] Part progression is logical
- [ ] Estimated block count: <number>

## Design Choices

| Aspect | Choice |
|--------|--------|
| Theme | <StreamTeX theme name> |
| Color palette | <palette description or name> |
| Layouts | <single column / two column / tabs / mixed> |
| Typography | <default / custom font choices> |
| Asset types | <diagrams / screenshots / icons / code snippets / tables> |
| Conventions | <naming, styling, or structural conventions> |

### Presentation Profiles

| Aspect | Value |
|--------|-------|
| Preset | <responsive_preset() / presentation_preset() / desktop_mobile_preset() / custom> |

| Profile Name | ViewMode | Width% | Zoom% | SlideBreak Enabled | SlideBreak Mode |
|-------------|----------|--------|-------|-------------------|-----------------|
| <profile name> | <PAGINATED / CONTINUOUS> | <width%> | <zoom%> | <yes / no> | <PAGINATED / CONTINUOUS / HIDDEN> |
| <...> | <...> | <...> | <...> | <...> | <...> |

**book.py config**: `ProfileConfig` setup with `save()`/`load()` and selected profiles.

### Section Spacing

| Level | Config | Value |
|-------|--------|-------|
| Global | `set_spacing(SpacingConfig(...))` | `Spacing(top=<>, bottom=<>, left=<>, right=<>)` |
| Per-profile | `PresentationProfile.spacing` | <override or "inherit global"> |
| Per-block overrides | `set_block_spacing()` on specific blocks | <block name: Spacing values, with justification> |

**Override hierarchy**: built-in < book < profile < block < call-site

### Bibliography Setup

| Aspect | Value |
|--------|-------|
| Source | <path to .bib / .ris / .json file, URL, or `none`> |
| Format | <BibFormat: HARVARD / APA / CHICAGO / IEEE / CUSTOM> |
| Citation style | <CitationStyle: NUMBERED / AUTHOR_YEAR> |
| Placement | <block name where `st_bibliography()` will be rendered> |

**book.py config**: `set_bib_config(BibConfig(format=BibFormat.APA, style=CitationStyle.AUTHOR_YEAR))`

<If no bibliography: "No bibliography — `none`.">

### AI Image Configuration

| Aspect | Value |
|--------|-------|
| Provider | <openai / google / fal or `none`> |
| Model | <provider-specific model name> |
| Default size | <size preset (e.g., 1024x1024)> |
| Default quality | <quality preset (e.g., standard / hd)> |
| Generation mode | <manual / auto> |
| Seed strategy | <fixed seed value / random> |
| Estimated image count | <number> |

#### Prompt Guidelines

- Visual style: <realistic / illustration / diagram / abstract>
- Color temperature: <warm / cool / neutral — aligned with document palette>
- Consistency rules: <shared style terms to use across all prompts>

**book.py config**: `set_ai_image_config(AIImageConfig(provider="openai", model="gpt-image-1", size="1024x1024", quality="standard"))`

<If no AI images: "No AI images — `none`.">

### Export Configuration

| Aspect | Value |
|--------|-------|
| Asset mode | <AssetMode: EMBEDDED / EXTERNAL (default)> |
| Asset mode rationale | <why this mode — e.g., single-file delivery vs media-rich with deduplication> |
| Export mode | <ExportMode: ALWAYS / MANUAL / NEVER> |
| PDF export | <yes / no> |
| PDF config | <PdfConfig(margins=..., scale=..., page_format=...) or `none`> |

**book.py config**: `ExportConfig(asset_mode=AssetMode.EXTERNAL, mode=ExportMode.MANUAL)`

<If no export needed: "Default export configuration — EXTERNAL asset mode, MANUAL export.">

## Execution Order

| Step | Action | Blocks Affected | Dependencies |
|------|--------|----------------|-------------|
| 1 | <action description> | <block name(s)> | <none / step #> |
| 2 | <...> | <...> | <...> |
| 3 | <...> | <...> | <...> |

## Pre-Production Checklist

- [ ] Project created (`stx project new` or `/stx-designer:init`)
- [ ] Source files accessible and readable
- [ ] Conversion tools available (pandoc, etc.)
- [ ] Design profile selected and configured
- [ ] book.py skeleton matches planned structure
- [ ] Assets directory prepared
- [ ] Dependencies resolved (images, bibliographies)
- [ ] AI image provider API key available (if AI images configured)

## Next Step

Proceed with `/stx-ce:produce` to execute this plan.
```
