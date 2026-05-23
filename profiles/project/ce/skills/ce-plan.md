# CE Plan

Skill for the PLAN phase of the Compound Engineering cycle. Produces a plan **for the current increment**, in coherence with the master plan. In first iteration also produces the global master plan TOC.

Read `.claude/ce/skills/ce-conventions.md` before invoking any user-facing question.

## Workflow

### Phase 0: Load Master Plan, Assessment, and Producer Profile

1. Load `docs/master-plan.yaml` and `docs/master-plan.md` if present.
   - **First iteration**: master plan was initialized in ASSESS. The TOC is empty; PLAN will fill it (global skeleton) and produce the detailed plan for the first increment.
   - **Subsequent iterations**: TOC exists; PLAN focuses on the current increment scope only. The master plan TOC is updated only if the user has requested a change in the global structure.
2. Scan `docs/assess/` for the most recent assessment file.
3. If no assessment is found, inform the user and suggest running `/stx-ce:assess` first. Do not proceed.
4. Parse the assessment to extract pathway, requirements, audience profile, and gap analysis.
5. **Producer profile**: If `docs/solutions/producer-profile.md` exists, load it and pass it to the planning agents. The `structure-architect` uses favorite patterns and anti-patterns. The `domain-researcher` uses domain context to inform research scope. Read `dialog_level`.
6. **Scope**: read the scope established by the caller (typically `ce-go`). If invoked standalone, surface a scope QCM based on the master plan state (see `ce-go` Step 0 for the question template).

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

### Phase 3: Generate Plan Document and Update Master Plan

1. Determine the daily sequence number by scanning `docs/plans/` for files matching today's date (`YYYY-MM-DD-NNN-*`). Increment NNN from the highest found, or start at 001.
2. Write to `docs/plans/YYYY-MM-DD-NNN-<scope>-<name>-plan.md` using the pathway-specific template from `.claude/ce/templates/`. The `<scope>` segment is `doc` for full document, `part-<id>` for a part, `section-<id>` for a section.

#### Phase 3.1: Update Master Plan

Before writing the plan increment, snapshot the master plan if either file differs from the last snapshot. Then:

**First iteration**:
- Populate `master-plan.yaml -> toc` with the full global skeleton (parts → sections → planned blocks with status `planned`).
- Update `master-plan.md` TOC section with titles and `Intention` notes for each node. Add `Notes de conception` reflecting design choices.
- Populate `transverse_decisions` with palette, profiles, bibliography, AI image config, export, spacing.
- Append the current iteration entry in `iterations` with scope, pathway, started date.

**Subsequent iterations**:
- Update only the nodes in the current scope: refine titles, sources, notes, draft content proposals in the MD; refine statuses, components mapping in the YAML.
- If the user requested a global structural change during this PLAN, surface a QCM before applying it: *"Modify the master plan's global skeleton?"* → `Apply (Recommended)` / `Limit to the current increment` / `Let's discuss`.
- Append a new entry in `iterations`.
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
   - Reference traceability strategy: decide per-project whether references are displayed (inline attribution, bibliography) or hidden (source-code `# REF:` comments only). In all cases, every factual claim must be traceable in the block source.
   - Deployment configuration (if applicable)
   - Total effort estimate
4. **GATE (fundamental)**: surface QCM to validate the plan. Options: `Approve and continue (Recommended)` / `Request modifications` / `Let's discuss`. Append `decisions_log` entry.
5. Suggest next step: PROTOTYPE (`/stx-ce:prototype`) if styles/patterns need validation; otherwise PRODUCE (`/stx-ce:produce`).
