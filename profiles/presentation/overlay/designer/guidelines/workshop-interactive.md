# Design Guideline: Workshop Interactive

> **Scope**: This skill defines a graphical design philosophy optimized for
> **interactive workshops** (hands-on sessions, small groups, exercises).
> It balances information density with readability for participants
> who follow along on their own screens or in close proximity.

---

## Philosophy

Every slide serves the hands-on experience. Theory slides are brief and
lead directly to practice. Exercise slides are self-contained instruction
cards. Code is real, runnable, and copy-pasteable.

---

## Principles (ordered by priority)

### P1 — Exercises are self-contained

Each exercise slide contains everything the participant needs:
- Clear objective (what to achieve)
- Step-by-step instructions
- Expected outcome or validation criteria
- No "refer to slide 12" — all context on this slide

### P2 — Code is real and complete

No pseudocode, no "..." ellipsis, no "// your code here":
- Show complete, runnable code examples
- Syntax highlighting mandatory
- Line numbers for reference during discussion
- Copy-paste ready (no slide artifacts in code)

### P3 — Theory is minimal and leads to practice

For every concept slide, ask: "What will participants DO with this?"
- Concept → example → exercise (max 2 slides of theory before practice)
- Prefer live demos over static explanations
- Use diagrams over text for architecture/flow concepts

### P4 — Progressive difficulty

Structure exercises from simple to complex:
- Guided exercises first (step-by-step)
- Semi-guided exercises next (objective + hints)
- Open exercises last (objective only)
- Each builds on the previous

---

## Application par type de contenu

### When the slide is an exercise

- Clear title: "Exercise: [objective]"
- Numbered steps with `st_list` (ordered)
- Font: `large` (32pt) for instructions (readable on individual screens)
- Include expected output or success criteria
- Time estimate if applicable
- Container: light background accent to distinguish from theory slides
- Goal: participant can follow independently without trainer

### When the slide has code

- Code block: 60-70% of viewport
- Font: `big` (24pt) minimum for code
- Complete, runnable code — no truncation
- Highlight key lines with comments or accent
- Side-by-side before/after when showing transformations
- Goal: copy-paste ready, immediately runnable

### When the slide is theoretical (concept)

- Brief: max 4 bullets, keyword style
- Always include a "Why this matters" or practical connection
- Diagram or visual preferred over text
- Font: `Large` (48pt) for body
- Goal: quick context, then move to practice

### When the slide has a diagram

- Architecture/flow diagrams: clear, labeled, moderate detail
- Can include more detail than auditorium (participants are closer)
- Mermaid/PlantUML preferred (reproducible, editable)
- Goal: reference diagram participants can study

### When the slide is a transition

- Brief: section title + "In this section, you will..."
- 2-3 bullet learning objectives
- Goal: orient participants, set expectations

---

## Recommended PresentationProfile

```python
PresentationProfile(
    name="Workshop",
    mode=ViewMode.CONTINUOUS,
    layout=PageLayout(width=90, zoom=90),
    breaks=SlideBreakDisplayConfig(mode=SlideBreakMode.FULL, space=3),
)
```

Note: CONTINUOUS mode is preferred for workshops — participants scroll
at their own pace during exercises.

---

## Constraints (absolute)

- No font below 24pt (`s.big`)
- Code blocks: complete and runnable — no pseudocode
- Exercise slides: must include objective + steps + expected outcome
- Maximum 2 theory slides before an exercise
- Dark theme recommended (easier on eyes during long sessions)
- 16:9 viewport ratio

---

## Anti-patterns

- Long theory sections without hands-on practice
- Pseudocode or incomplete code examples
- Exercise instructions that reference other slides
- Dense reference-style slides during a hands-on session (put those in handouts)
- Exercises without clear success criteria

---

## Combinability

### Combines well with
- **`dense-informative`** — for reference/cheatsheet slides within the workshop
  (use `@guideline: dense-informative` for reference blocks, workshop for exercises)
- **`academic-structured`** — for theory blocks that require rigor

### Conflicts with
- **`minimalist-visual`** — workshops need actionable detail, not visual minimalism
- **`auditorium-projection`** — font size constraints too aggressive for close viewing
