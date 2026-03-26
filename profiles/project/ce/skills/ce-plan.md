# CE Plan

Skill for the PLAN phase of the Compound Engineering cycle. Create a structured production plan from the assessment. Supports two modes: auto (default) and interactive.

## Workflow

### Phase 0: Load Assessment and Producer Profile

1. Scan `docs/assess/` for the most recent assessment file.
2. If no assessment is found, inform the user and suggest running `/stx-ce:assess` first. Do not proceed.
3. Parse the assessment to extract pathway, requirements, audience profile, and gap analysis.
4. **Producer profile**: If `docs/solutions/producer-profile.md` exists, load it and pass it to the planning agents. The `structure-architect` uses favorite patterns and anti-patterns. The `domain-researcher` uses domain context to inform research scope.

### Phase 1: Research

1. Use the **learnings-researcher** agent to search `docs/solutions/` for relevant patterns and lessons learned from previous projects.
2. Use the **domain-researcher** agent to gather domain knowledge, best practices, and technical references relevant to the planned content.
3. If `--deep` flag is set: run all PLAN agents in parallel for comprehensive research before planning.

### Phase 2: Plan

#### Auto Mode (default)

1. The **structure-architect** agent generates the full plan in one pass based on:
   - Assessment requirements
   - Research findings
   - Pathway constraints
2. The plan includes: document skeleton, per-section objectives, design choices (including presentation profiles), bibliography setup, AI image configuration, export configuration, and production sequence.

#### Interactive Mode (--interactive flag)

Execute 4 steps with user dialogue between each.

**Step 1 - Skeleton:**
1. The **structure-architect** agent proposes a document structure (parts, sections, blocks).
2. Present the skeleton to the user for validation.
3. User can modify, reorder, add, or remove sections.

**Step 2 - Objectives:**
1. The **domain-researcher** agent proposes per-section objectives and content outlines based on domain expertise.
2. The **learnings-researcher** agent validates against past project patterns.
3. Present to the user for adjustments.

**Step 3 - Design:**
1. The **structure-architect** agent proposes design options based on the skeleton:
   - Navigation pattern and layout
   - Block density and section granularity
   - Asset strategy (images, diagrams, icons)
   - Presentation profiles: preset selection, ViewMode per profile, PageLayout dimensions, SlideBreakDisplayConfig per profile
   - Bibliography setup (if R19 is not `none`):
     - Source: path to bibliography file or URL
     - Format: BibFormat (HARVARD | APA | CHICAGO | IEEE | CUSTOM)
     - Citation style: CitationStyle (NUMBERED | AUTHOR_YEAR)
     - Placement: block name where `st_bibliography()` will be rendered
     - book.py config: `set_bib_config(BibConfig(format=BibFormat.APA, style=CitationStyle.AUTHOR_YEAR))`
   - AI image configuration (if R22 is not `none`):
     - Provider: openai | google | fal (default: openai)
     - Model: provider-specific model name
     - Default size/quality: size and quality presets
     - Cache strategy: reuse across blocks (deterministic hash)
     - Prompt guidelines: style consistency rules for generated images
     - book.py config: `set_ai_image_config(AIImageConfig(provider="openai", ...))`
   - Export configuration:
     - Asset mode: AssetMode.EMBEDDED (base64 data URIs, single HTML file) | AssetMode.EXTERNAL (assets in data/ folder, ZIP download, default)
     - Recommendation: EXTERNAL for documents with many images/videos/audio — smaller output, SHA-256 deduplication
     - Export mode: ExportMode (ALWAYS | MANUAL | NEVER)
     - PDF config: PdfConfig if PDF export needed (margins, scale, page_format)
     - book.py config: `ExportConfig(asset_mode=AssetMode.EXTERNAL, mode=ExportMode.MANUAL)`
   - Section spacing:
     - Global spacing: `Spacing(top=, bottom=, left=, right=)` via `set_spacing()`
     - Per-profile overrides: `SpacingConfig` in `PresentationProfile.spacing`
     - Per-block overrides: `set_block_spacing()` for blocks needing custom margins
     - Override hierarchy: built-in < book < profile < block < call-site
2. Present options to the user for selection.

**Step 4 - Final Plan:**
1. The **structure-architect** agent assembles the complete plan from validated choices.
2. The **learnings-researcher** agent enriches with applicable patterns from previous solutions.

### Phase 3: Generate Plan Document

1. Determine the daily sequence number by scanning `docs/plans/` for files matching today's date (`YYYY-MM-DD-NNN-*`). Increment NNN from the highest found, or start at 001.
2. Write to `docs/plans/YYYY-MM-DD-NNN-<pathway>-<name>-plan.md` using the pathway-specific template from `.claude/ce/templates/`.
3. The plan document must include:
   - Document structure with all sections and blocks
   - Per-section: objective, content outline, block type, estimated effort
   - Design specifications (colors, styles, layout)
   - Presentation profiles configuration (preset, ViewMode per profile, PageLayout, SlideBreakDisplayConfig)
   - Bibliography setup (source file, format, citation style, placement block, book.py config)
   - Section spacing strategy (global SpacingConfig, per-profile overrides, per-block overrides with justification)
   - AI image configuration (provider, model, size/quality, cache strategy, prompt guidelines, book.py config)
   - Export configuration (asset mode, export mode, PDF config, book.py ExportConfig)
   - Production sequence (order of execution)
   - Asset list (images, diagrams, code samples needed)
   - Deployment configuration (if applicable)
   - Total effort estimate
4. **GATE**: Present the plan summary to the user and ask for explicit validation before proceeding. The plan must be approved to continue.
5. Suggest next step: run `/stx-ce:produce` to execute the plan.
