# Template: Plan Create

Creation production plan — detailed execution plan for building a new StreamTeX document from scratch.

## Structure

```markdown
# Production Plan — Pathway C: CREATION

## Metadata

| Field | Value |
|-------|-------|
| Project name | <project name> |
| Document type | <manual / presentation / course / report / collection> |
| Profile | <design profile name> |
| Template | <project / presentation / collection / course> |
| Planning mode | <auto / interactive> |
| Estimated blocks | <number> |
| Estimated parts | <number> |
| Assess report ref | <assess report file or date> |
| Context | <standalone / part of series / companion to X> |

## Document Structure

### Skeleton (validated)

| Part | Section | Objective | Sources | Content Type | Detail Level | Blocks |
|------|---------|-----------|---------|-------------|-------------|--------|
| <Part 1: Title> | <Section 1.1> | <what this section achieves> | <reference material, if any> | <text / code / mixed / visual> | <overview / detailed / reference> | <block_name_1, block_name_2> |
| | <Section 1.2> | <...> | <...> | <...> | <...> | <...> |
| <Part 2: Title> | <Section 2.1> | <...> | <...> | <...> | <...> | <...> |

### Skeleton Validation

- [ ] All requirements (R1-R15) are addressed by at least one section
- [ ] Part progression follows chosen narrative arc
- [ ] No empty parts or sections
- [ ] Estimated block count: <number>
- [ ] Complexity is appropriate for target audience

## Design Choices

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Theme | <StreamTeX theme name> | <why this theme> |
| Color palette | <palette description or name> | <why this palette> |
| Layouts | <single column / two column / tabs / mixed> | <why this layout> |
| Typography | <default / custom font choices> | <why this typography> |
| Asset types | <diagrams / screenshots / icons / code snippets / tables> | <why these assets> |
| Conventions | <naming, styling, or structural conventions> | <source of conventions> |

### Design Guideline Integration
- **Guideline**: <name>
- **Archetype mapping**: Map each planned block to its expected content archetype
- **PresentationProfile**: Recommended values from guideline

### Presentation Profiles

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Preset | <responsive_preset() / presentation_preset() / desktop_mobile_preset() / custom> | <why this preset> |

| Profile Name | ViewMode | Width% | Zoom% | SlideBreak Enabled | SlideBreak Mode |
|-------------|----------|--------|-------|-------------------|-----------------|
| <profile name> | <PAGINATED / CONTINUOUS> | <width%> | <zoom%> | <yes / no> | <PAGINATED / CONTINUOUS / HIDDEN> |
| <...> | <...> | <...> | <...> | <...> | <...> |

**book.py config**: `ProfileConfig` setup with `save()`/`load()` and selected profiles.

### Section Spacing

| Level | Config | Value | Rationale |
|-------|--------|-------|-----------|
| Global | `set_spacing(SpacingConfig(...))` | `Spacing(top=<>, bottom=<>, left=<>, right=<>)` | <why these values> |
| Per-profile | `PresentationProfile.spacing` | <override or "inherit global"> | <why> |
| Per-block overrides | `set_block_spacing()` on specific blocks | <block name: Spacing values> | <justification for each override> |

**Override hierarchy**: built-in < book < profile < block < call-site

### Bibliography Setup

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Source | <path to .bib / .ris / .json file, URL, or `none`> | <why this source> |
| Format | <BibFormat: HARVARD / APA / CHICAGO / IEEE / CUSTOM> | <why this format> |
| Citation style | <CitationStyle: NUMBERED / AUTHOR_YEAR> | <why this style> |
| Placement | <block name where `st_bibliography()` will be rendered> | <why this location> |

**book.py config**: `set_bib_config(BibConfig(format=BibFormat.APA, style=CitationStyle.AUTHOR_YEAR))`

<If no bibliography: "No bibliography — `none`.">

### AI Image Configuration

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Provider | <openai / google / fal or `none`> | <why this provider> |
| Model | <provider-specific model name> | <why this model> |
| Default size | <size preset (e.g., 1024x1024)> | <why this size> |
| Default quality | <quality preset (e.g., standard / hd)> | <why this quality> |
| Generation mode | <manual / auto> | <why this mode> |
| Seed strategy | <fixed seed value / random> | <why this strategy> |
| Estimated image count | <number> | <based on content plan> |

#### Prompt Guidelines

- Visual style: <realistic / illustration / diagram / abstract>
- Color temperature: <warm / cool / neutral — aligned with document palette>
- Consistency rules: <shared style terms to use across all prompts>

**book.py config**: `set_ai_image_config(AIImageConfig(provider="openai", model="gpt-image-1", size="1024x1024", quality="standard"))`

<If no AI images: "No AI images — `none`.">

### Export Configuration

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Asset mode | <AssetMode: EMBEDDED / EXTERNAL (default)> | <why this mode — e.g., single-file delivery vs media-rich with deduplication> |
| Export mode | <ExportMode: ALWAYS / MANUAL / NEVER> | <why this mode> |
| PDF export | <yes / no> | <why> |
| PDF config | <PdfConfig(margins=..., scale=..., page_format=...) or `none`> | <why these settings> |

**book.py config**: `ExportConfig(asset_mode=AssetMode.EXTERNAL, mode=ExportMode.MANUAL)`

<If no export needed: "Default export configuration — EXTERNAL asset mode, MANUAL export.">

## Dependencies

### Assets

| Asset | Type | Status | Source |
|-------|------|--------|--------|
| <asset name> | <image / diagram / data file / icon> | <to create / exists / to acquire> | <where it comes from> |

### Prerequisite Blocks

| Block | Dependency | Type |
|-------|-----------|------|
| <block_name> | <other block or config> | <must exist before / shared asset / shared style> |

<If no dependencies: "No inter-block dependencies.">

### book.py Configuration

| Config Item | Value | Notes |
|-------------|-------|-------|
| Title | <document title> | |
| Theme | <theme name> | |
| Custom settings | <any st_book kwargs> | |

### Coherence with Existing Documents

| Document | Coherence Point | Action Required |
|----------|----------------|----------------|
| <existing document> | <shared terminology / shared style / cross-reference> | <what to ensure> |

<If standalone: "No coherence constraints — standalone document.">

## Pre-Production Checklist

- [ ] Project created (`stx project new` or `/stx-designer:init`)
- [ ] Design profile selected and configured
- [ ] book.py initialized with skeleton structure
- [ ] blocks/ directory created
- [ ] Assets directory prepared
- [ ] Reference materials accessible
- [ ] Conventions documented or profile applied
- [ ] AI image provider API key available (if AI images configured)

## Next Step

Proceed with `/stx-ce:produce` to execute this plan.
```
