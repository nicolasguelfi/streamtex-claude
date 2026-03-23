# Template: Producer Profile

Persistent file capturing the producer's recurring preferences, style, and patterns across CE cycles.

## Structure

```markdown
---
title: Producer Profile
last_updated: <YYYY-MM-DD>
projects_count: <number of CE cycles completed>
---

# Producer Profile

## Style Preferences
- <recurring visual preferences: palettes, layouts, typography>
- <preferred color schemes>
- <layout patterns (e.g., always use 2-column for comparisons)>

## Content Preferences
- <preferred tone: formal, conversational, academic, technical>
- <preferred level of detail: concise, standard, comprehensive>
- <preferred structure: linear progression, topic clusters, problem-solution>

## Production Priorities
- <what matters most: accessibility, speed, fidelity to source, visual polish>
- <quality thresholds: acceptable number of MINOR findings, etc.>

## Favorite Patterns
- <StreamTeX techniques used regularly>
- <block patterns that work well for this producer>
- <asset strategies: AI images, Mermaid diagrams, code snippets>

## Anti-patterns Identified
- <recurring mistakes to avoid>
- <approaches that did not work in past projects>

## Git Preferences
- branch_suggestions: true
  <!-- Set to false to disable branch creation suggestions for document projects -->
```

## Usage

- **COLLECT**: If this file exists in `docs/solutions/producer-profile.md`, load it and inform the user. If not, remind the user they can provide one.
- **ASSESS**: Use preferences to pre-fill form requirements (R9-R12).
- **PLAN**: Pass to `structure-architect` and `visual-reviewer` (interactive step 3) for informed proposals.
- **COMPOUND**: Enrich with new preferences and anti-patterns discovered during the cycle. Increment `projects_count`.
- **Consolidation**: When multiple projects have their own profiles, COMPOUND proposes merging them into a unified profile.
