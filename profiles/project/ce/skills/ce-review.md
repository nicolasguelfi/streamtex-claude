# CE Review

Skill for the REVIEW phase of the Compound Engineering cycle. Perform a multi-perspective document review using parallel agent analysis and synthesize findings.

## Workflow

### Phase 1: Load Context

1. Identify the project to review (current directory or specified path).
2. Load the production plan from `docs/plans/` if it exists, to understand original objectives.
3. Load the assessment from `docs/assess/` if it exists, to compare against requirements.
4. Inventory all blocks in the project for the review scope.

### Phase 2: Multi-Agent Review (Parallel)

Launch 5 review agents in parallel. Each agent analyzes the entire project from its perspective.

1. **audience-advocate**: Evaluate the document from the reader/learner perspective.
   - Is the content accessible to the target audience?
   - Are prerequisites clearly stated?
   - Is the progression logical and learner-friendly?

2. **pedagogy-analyst**: Evaluate pedagogical design.
   - Are learning objectives met?
   - Is the balance between theory and practice appropriate?
   - Are examples and exercises effective?

3. **visual-reviewer**: Evaluate visual design.
   - Is the layout consistent and professional?
   - Are styles applied correctly and uniformly?
   - Are assets (images, diagrams) appropriate and well-integrated?

4. **style-consistency-checker**: Evaluate technical coherence.
   - Are StreamTeX conventions followed?
   - Is the code structure clean and maintainable?
   - Are block names, function signatures, and imports consistent?

5. **content-editor**: Evaluate editorial quality.
   - Is the writing clear, concise, and error-free?
   - Is terminology consistent throughout?
   - Are transitions between sections smooth?
   - **Reference traceability** (RECOMMENDATION): Are factual claims, statistics, and attributions traceable to verifiable sources? Check for `# REF:` comments in block source code. Flag unsourced claims as MINOR (missing comment) or MAJOR (dubious/unverifiable claim).

Each agent produces findings with severity levels:
- **CRITICAL**: Must be fixed before publication. Blocks functionality or comprehension.
- **MAJOR**: Should be fixed. Significantly impacts quality.
- **MINOR**: Nice to fix. Small improvements to quality.
- **SUGGESTION**: Optional enhancement for future iterations.

If more than 5 agents would run, switch to serial mode to avoid context saturation.

### Phase 3: Ultra-Thinking Synthesis

1. Cross-reference all 5 agent reports to identify:
   - Findings confirmed by multiple agents (higher confidence).
   - Contradictions between agent perspectives (require judgment).
   - Patterns across findings (systemic issues vs. isolated problems).
2. Prioritize findings by impact:
   - Weight CRITICAL and MAJOR findings by number of blocks affected.
   - Identify quick wins (low effort, high impact fixes).
3. Produce a unified prioritized finding list.

### Phase 4: Generate Review Report

1. Write to `docs/reviews/YYYY-MM-DD-<name>-review.md` using the **review-report** template from `.claude/ce/templates/`.
2. The report must include:
   - Executive summary (overall quality score and key findings)
   - Per-perspective detailed findings
   - Prioritized action list
   - Comparison against assessment requirements (if available)
   - Comparison against plan objectives (if available)
3. **GATE**: Present the review summary to the user and ask for explicit validation.

### After Review

Suggest next steps to the user:
1. Run `/stx-ce:fix` to correct automatable findings.
2. Run `/stx-ce:fix --severity MAJOR` to also fix MAJOR findings.
3. Skip fixes and proceed directly to `/stx-ce:compound` if the review is satisfactory.

The REVIEW -> FIX cycle can be iterated: after FIX, run `/stx-ce:review` again to validate corrections.
