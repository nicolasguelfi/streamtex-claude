# CE Produce

Skill for the PRODUCE phase of the Compound Engineering cycle. Execute the plan increment item by item, creating, importing, or improving content as specified. This phase is **command-driven** — it delegates to `/stx-block:*`, `/stx-import:*`, `/stx-export:*`, and `/stx-deploy:*` commands rather than using standalone agents.

Consults the master plan for components to apply (`components.applied[*].blocks` mapping). Updates per-block statuses in `master-plan.yaml -> toc` as production progresses.

Read `.claude/ce/skills/ce-conventions.md` before invoking any user-facing question. Before mutating any block file, invoke the `plan-reconciler` agent — silent passage if aligned, QCM if divergence.

## Workflow

### Phase 1: Initialize

1. Load the most recent plan increment from `docs/plans/` (or the path provided by caller).
2. Load `docs/master-plan.yaml` to retrieve the components mapping (`components.applied`) — these components must be applied to the blocks they list.
3. Run the `plan-reconciler` agent. If divergence, surface QCM and resolve before producing any new block.
4. If the target project does not exist yet, run `/stx-block:init --template <type>` where type is derived from the plan (project, presentation, collection, course).
5. Create a task list from the plan items, scoped to the current increment. Each task has:
   - ID (sequential)
   - Description
   - Type (IMPORT, IMPROVE, CREATE)
   - Target block name
   - Components to apply (from `master-plan.yaml -> components.applied`)
   - Status (pending, in-progress, done, failed)
4. Configure `book.py` according to the plan:
   - Set document metadata (title, author, description)
   - Configure navigation style
   - Set theme and style parameters
   - If plan includes bibliography: add `set_bib_config(BibConfig(format=..., style=...))` call in book.py, load bibliography file with `load_bib()`, and prepare citation integration
   - If plan includes AI images: add `set_ai_image_config(AIImageConfig(provider=..., model=..., size=..., quality=...))` call in book.py. Verify API key availability via env vars (`STX_OPENAI_API_KEY`, `STX_GOOGLE_AI_KEY`, or `STX_FAL_KEY`)

### Phase 2: Produce Iteratively

Process each plan item according to its type. After each item:
- Mark complete in the task list.
- Update the corresponding block status in `master-plan.yaml -> toc[*].sections[*].blocks[*].status` to `produced`.
- Append a `decisions_log` entry for any user QCM answered during production (style choices, content trade-offs).

#### IMPORT Items

1. Run the appropriate import command based on source format:
   - HTML sources: `/stx-import:html`
   - Marp sources: `/stx-import:marp`
   - LaTeX sources: `/stx-import:latex`
   - Other formats: manual conversion following plan instructions
2. Run `/stx-block:audit --target <block>` on the imported block.
3. Run `/stx-block:fix --target <block>` to resolve any issues found.
4. Verify the block renders correctly.

#### IMPROVE Items

1. Run `/stx-block:update` with the improvement instructions from the plan.
2. If style changes are needed, run `/stx-block:style-refactor`.
3. Run `/stx-block:audit --target <block>` on the modified block.
4. Run `/stx-block:fix --target <block>` to resolve any issues found.
5. Verify the block renders correctly.

#### CREATE Items

1. Create the block using `/stx-block:new` or `/stx-block:slide-new` as appropriate.
2. Read the section's `Propositions brutes` from `master-plan.md` — use it as the starting content for the block.
3. Write content according to the plan's content outline for this section.
4. **Apply mapped components**: for each component listed in `master-plan.yaml -> components.applied` for this block, read the full component module from its pack and respect its INVARIANTS / PARAMS / INTERDITS. Adapt the call to the project's design system.
5. Apply styles as specified in the plan's design section.
6. Integrate assets (images, diagrams, code samples) as listed in the plan.
5. If AI images are configured:
   - Use `st_image(prompt="<prompt>", editable=True, name="<name>")` for all AI-generated images — this single call covers declarative rendering AND opens the editor panel on click for regeneration; craft prompts following the plan's prompt guidelines for style consistency
   - Use fixed seeds (`seed=<value>`) for reproducibility when specified in the plan
   - Verify generated images render correctly and match the intended visual style
6. If bibliography is configured: insert `cite()` calls in content blocks where sources are referenced, and add `st_bibliography()` in the designated bibliography block.
7. **Reference traceability**: For every factual claim, statistic, or attribution written in content, add a `# REF: <source url or citation>` comment above the corresponding `st_write()` call. This applies regardless of whether bibliography is configured — source traceability in code is always required. If the plan specifies visible references, also add inline attribution or `cite()` calls.
8. Run `/stx-block:audit --target <block>` on the new block.
9. Run `/stx-block:fix --target <block>` to resolve any issues found.
10. Verify the block renders correctly.

### Phase 3: Global Verification

1. Run `/stx-block:audit --all` to check the entire project.
2. Verify `book.py` navigation:
   - All blocks are registered in the correct order.
   - No blocks are missing from the plan.
   - Navigation flow is correct (previous/next links).
3. If bibliography is configured:
   - Verify all `cite()` keys exist in the loaded bibliography
   - Verify `st_bibliography()` is present if any `cite()` calls exist
   - Check for uncited bibliography entries (optional warning)
4. If AI images are configured:
   - Verify all `st_image(prompt=..., editable=True, name=...)` calls render without errors
   - Check visual coherence between AI-generated images (consistent style across blocks)
   - Verify image cache is populated (no redundant regenerations)
   - Confirm seeds are set where reproducibility was specified in the plan
5. Perform a preview check to ensure the document renders as expected.
6. If audit reveals critical issues, fix them before proceeding.

### Phase 4: Deliver

1. If the plan requires HTML export, run `/stx-export:html`.
2. If the plan requires deployment (and `--no-deploy` is not set), run `/stx-deploy:deploy`.
3. Mark the plan as DONE in `docs/plans/` by updating the plan file status field.
4. Produce a production summary listing:
   - Items completed (with status)
   - Items that required manual intervention
   - Audit results
   - Deployment status (if applicable)
5. Suggest next step: run `/stx-ce:review` for a multi-perspective quality review.
