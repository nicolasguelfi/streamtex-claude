# CE Assess

Skill for the ASSESS phase of the Compound Engineering cycle. Evaluate existing material and define objectives through structured dialogue with the user.

## Workflow

### Phase 0: Auto-Detect Pathway and Load Producer Profile

1. Check `docs/collect/` for reports containing external sources. If found, enable mode **IMPORT (A)**.
2. Check if the current directory is a StreamTeX project with a `blocks/` directory. If found, enable mode **IMPROVEMENT (B)**.
3. If neither condition is met, set mode to **CREATION (C)**.
4. If both conditions 1 and 2 are met, combine **A+B** (import and improve).
5. Log the detected pathway for the user.
6. **Producer profile**: If `docs/solutions/producer-profile.md` exists, load it. Use the producer's style preferences, content preferences, and production priorities to pre-fill form requirements R9-R12 in Phase 2. Inform the user which preferences were pre-filled and allow them to override.

### Phase 1: Evaluate

Evaluation strategy depends on the detected pathway.

#### Pathway A (Import)

1. Use the **audience-analyst** agent to profile the target audience from collected sources.
2. Use the **content-strategist** agent to evaluate content quality, coverage, and coherence.
3. Use the **gap-analyst** agent to identify gaps between collected material and a complete document.

#### Pathway B (Improvement)

1. Run `/stx-designer:audit --all` to get the current project quality report.
2. Use the **gap-analyst** agent to compare current state vs. target quality level.
3. Identify blocks that need rework, missing sections, and style inconsistencies.

#### Pathway C (Creation)

1. Use the **audience-analyst** agent to help define the target audience.
2. Use the **content-strategist** agent to explore content scope and structure.
3. Use the **format-explorer** agent to suggest document formats and presentation styles.
4. Use the **angle-generator** agent to propose original angles and approaches.

### Phase 2: Dialogue with User

Ask focused questions to capture requirements R1 through R26. Use AskUserQuestion for each group.

1. **Identity** (R1-R3):
   - R1: Document title
   - R2: Document type (course, presentation, report, manual, collection)
   - R3: Author / organization context
2. **Content** (R4-R8):
   - R4: Subject matter and scope
   - R5: Key topics to cover
   - R6: Target depth (introductory, intermediate, advanced)
   - R7: Prerequisites assumed
   - R8: Learning objectives or document goals
3. **Form** (R9-R12):
   - R9: Visual style preferences
     - Target display profiles: responsive (desktop/tablet/mobile), presentation (presenter/audience/handout), or custom
     - Preferred ViewMode per profile: PAGINATED or CONTINUOUS
     - Factory presets available: `responsive_preset()`, `presentation_preset()`, `desktop_mobile_preset()`
   - R10: Branding constraints (colors, logos, fonts)
   - R11: Navigation style (linear, tabbed, sidebar)
   - R12: Estimated length (number of sections/slides)
4. **Delivery** (R13-R15):
   - R13: Target platform (web, PDF, both)
   - R14: Deployment target (local, Render, Hetzner, other)
   - R15: Timeline and deadlines
5. **Sources** (R16-R18, pathway A only):
   - R16: Priority ranking of collected sources
   - R17: Content to exclude or skip
   - R18: Adaptation instructions (update, simplify, restructure)
6. **Bibliography** (R19-R21):
   - R19: Bibliography sources — bibliographic source files (.bib, .ris, .json, CSL-JSON) or URLs. `none` if not applicable
   - R20: Citation format — preferred `BibFormat` (HARVARD | APA | CHICAGO | IEEE | CUSTOM). Default: APA
   - R21: Citation style — preferred `CitationStyle` (NUMBERED | AUTHOR_YEAR). Default: AUTHOR_YEAR
7. **Data Sources** (R25-R26):
   - R25: Google Sheets sources — spreadsheet IDs or URLs (`docs.google.com/spreadsheets/d/{id}`), sheet names, header/skip row configuration. `none` if not applicable
   - R26: Google Sheets access — path to service account JSON file for `GSheetConfig`, cache TTL preference. Required for `load_gsheet()` / `load_gsheet_df()` in book.py via `set_gsheet_config()`
7. **AI Images** (R22-R24):
   - R22: AI image needs — estimated quantity, visual style (realistic, illustration, diagram, abstract), thematic coherence requirements. `none` if not applicable
   - R23: AI image provider — preferred provider (openai | google | fal) and model, or `auto` for default. API key availability
   - R24: AI image mode — generation mode (manual | auto), seed strategy for reproducibility (fixed seed | random)

### Phase 3: Generate Assessment Document

1. Write to `docs/assess/YYYY-MM-DD-<name>-assess-<pathway>.md` using the appropriate pathway template from `.claude/ce/templates/`.
2. The document must include:
   - Detected pathway with justification
   - Audience profile
   - Requirements R1-R26 (as captured)
   - Content evaluation results
   - Gap analysis findings
   - Recommended approach for the PLAN phase
3. Suggest next step: run `/stx-ce:plan` to create a structured production plan.
