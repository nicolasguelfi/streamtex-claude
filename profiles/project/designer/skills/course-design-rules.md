# Course Design Rules — `course`

**Scope**: the default design rules for StreamTeX **pedagogical courses**.
Primary reference for the `course-designer` agent and for `/stx-block:*` when
the project's `identity.type` is `course`.

A course **extends** `web-document-design-rules.md` (read the base
`visual-design-rules.md` first, then the web-document overlay, then this file).
It adds the pedagogical layer: learning progression, exercises, and the
discipline of teaching by example. Where a rule here conflicts, **this file wins**.

> A course block is usually a reading document (scrolled, code-and-explanation
> driven). When a course is *delivered as slides*, follow `slide-design-rules.md`
> instead and treat this file's pedagogy section as content guidance.

## 1. Learning progression

- **One learning objective per block.** State it (or make it obvious) at the top.
- Order blocks by increasing difficulty; each builds on the previous.
- **Progressive disclosure**: introduce a concept, show it, let the learner try,
  then reveal detail/edge-cases — do not front-load everything.
- Close a module with a recap / checkpoint of what was learned.

## 2. Teaching by example (mandatory)

- The web-document **content idioms** (§5 of `web-document-design-rules.md`) are
  **mandatory** in a course: explanation box → code box → live rendering →
  optional details. Every example shows runnable code (`show_code()`), and
  every live rendering is preceded by its code.
- Prefer `show_explanation()` for the "what & why" and `show_details()` for
  defaults/edge-cases, so the main flow stays readable and the depth is opt-in.

## 3. Exercises & solutions

- Use the `exercise_flow` component (or the project's equivalent) for the
  **briefing → action → debrief** structure rather than ad-hoc layout.
- Keep a solution reachable but not in the reader's face: a `show_details()`
  / collapsible / `st_hover_tooltip` reveal, so the learner attempts first.
- Concept boxes (definitions, key terms) use a callout variant consistently
  across the course.

## 4. Consistency across the course

- Same idiom for the same purpose on every block (an "objective" looks the same
  everywhere; a "try it" looks the same everywhere). Inconsistency is a finding.
- Register every section/module in the TOC (`toc_lvl`) — learners navigate a
  course non-linearly when revising.

## 5. Interaction with design guidelines

`academic-structured` is the usual fit for courses; `dense-informative` for
reference-heavy modules. The active guideline (`custom/design-guideline.md`)
wins over these defaults. See `designer/guidelines/_index.md`.
