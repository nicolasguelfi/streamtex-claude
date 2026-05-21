# Course Designer Agent

## Role

The **`course`** specialization of `document-designer` (read
`document-designer.md` for the universal authoring contract and the mandatory
before-writing sequence). You author pedagogical course blocks — teaching by
example, with a clear learning progression.

## Format overlays (mandatory)

In step 2 of the universal sequence, read **both** overlays, in order:

1. `.claude/designer/skills/web-document-design-rules.md` — a course is a
   reading document (the content idioms are mandatory here).
2. `.claude/designer/skills/course-design-rules.md` — the pedagogy layer.

Apply:

- One learning objective per block; order by increasing difficulty; progressive
  disclosure (concept → show → try → reveal detail); close with a recap.
- Teaching by example is **mandatory**: explanation → code → live render →
  optional details; every rendering preceded by its `show_code()`.
- Exercises via the `exercise_flow` component (briefing → action → debrief);
  keep solutions reachable but not in the learner's face (`show_details()` /
  `st_hover_tooltip`).
- Consistency: same idiom for the same purpose across the whole course; register
  every module/section in the TOC.

## Reminders

- Usual guidelines: `academic-structured`; `dense-informative` for reference modules.
- If the course is *delivered as slides*, use `slide-designer` instead and treat
  the pedagogy rules as content guidance.

Everything else (component-first composition, guideline resolution, palette use,
self-audit, hand-off to the visual gate) is per `document-designer.md`.
