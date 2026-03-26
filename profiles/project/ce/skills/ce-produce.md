# CE Produce

Skill for the PRODUCE phase of the Compound Engineering cycle. Execute the production plan item by item, creating, importing, or improving content as specified. This phase is **command-driven** — it delegates to `/stx-designer:*`, `/stx-import:*`, `/stx-export:*`, and `/stx-deploy:*` commands rather than using standalone agents.

## Workflow

### Phase 1: Initialize

1. Load the approved plan from `docs/plans/`. Use the most recent plan file unless a specific path is provided.
2. If the target project does not exist yet, run `/stx-designer:init --template <type>` where type is derived from the plan (project, presentation, collection, course).
3. Create a task list from the plan items. Each task has:
   - ID (sequential)
   - Description
   - Type (IMPORT, IMPROVE, CREATE)
   - Target block name
   - Status (pending, in-progress, done, failed)
4. Configure `book.py` according to the plan:
   - Set document metadata (title, author, description)
   - Configure navigation style
   - Set theme and style parameters
   - If plan includes bibliography: add `set_bib_config(BibConfig(format=..., style=...))` call in book.py, load bibliography file with `load_bib()`, and prepare citation integration
   - If plan includes AI images: add `set_ai_image_config(AIImageConfig(provider=..., model=..., size=..., quality=...))` call in book.py. Verify API key availability via env vars (`STX_OPENAI_API_KEY`, `STX_GOOGLE_AI_KEY`, or `STX_FAL_KEY`)

### Phase 2: Produce Iteratively

Process each plan item according to its type. After each item, mark it complete in the task list.

#### IMPORT Items

1. Run the appropriate import command based on source format:
   - HTML sources: `/stx-import:html`
   - Marp sources: `/stx-import:marp`
   - LaTeX sources: `/stx-import:latex`
   - Other formats: manual conversion following plan instructions
2. Run `/stx-designer:audit --target <block>` on the imported block.
3. Run `/stx-designer:fix --target <block>` to resolve any issues found.
4. Verify the block renders correctly.

#### IMPROVE Items

1. Run `/stx-designer:update` with the improvement instructions from the plan.
2. If style changes are needed, run `/stx-designer:style-refactor`.
3. Run `/stx-designer:audit --target <block>` on the modified block.
4. Run `/stx-designer:fix --target <block>` to resolve any issues found.
5. Verify the block renders correctly.

#### CREATE Items

1. Create the block using `/stx-designer:block-new` or `/stx-designer:slide-new` as appropriate.
2. Write content according to the plan's content outline for this section.
3. Apply styles as specified in the plan's design section.
4. Integrate assets (images, diagrams, code samples) as listed in the plan.
5. If AI images are configured:
   - Use `st_ai_image(prompt)` for standalone generated images — craft prompts following the plan's prompt guidelines for style consistency
   - Use `st_image(editable=True, name="<name>", prompt="<prompt>")` for editable images that users can regenerate
   - Use fixed seeds (`seed=<value>`) for reproducibility when specified in the plan
   - Verify generated images render correctly and match the intended visual style
6. If bibliography is configured: insert `cite()` calls in content blocks where sources are referenced, and add `st_bibliography()` in the designated bibliography block.
7. Run `/stx-designer:audit --target <block>` on the new block.
8. Run `/stx-designer:fix --target <block>` to resolve any issues found.
9. Verify the block renders correctly.

### Phase 3: Global Verification

1. Run `/stx-designer:audit --all` to check the entire project.
2. Verify `book.py` navigation:
   - All blocks are registered in the correct order.
   - No blocks are missing from the plan.
   - Navigation flow is correct (previous/next links).
3. If bibliography is configured:
   - Verify all `cite()` keys exist in the loaded bibliography
   - Verify `st_bibliography()` is present if any `cite()` calls exist
   - Check for uncited bibliography entries (optional warning)
4. If AI images are configured:
   - Verify all `st_ai_image()` and `st_image(editable=True)` calls render without errors
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
