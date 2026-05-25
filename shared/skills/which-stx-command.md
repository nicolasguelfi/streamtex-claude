# Which stx command for this situation?

This skill is the **lazy-loader entry point** for routing decision-style
questions to the canonical reference (`/stx-guide`). It is intentionally
short — the full content lives in `streamtex-claude/shared/commands/stx-guide.md`.

## When this skill activates

Load this skill whenever the user (or an autonomous flow) asks:

- "Which stx command should I run for X?"
- "How do I sync / align / refresh the library + workspace + docs?"
- "I'm working on <thing>, what command do I run?"
- "What's the difference between `stx update`, `stx sync`, and `uv sync`?"
- "My uv.lock keeps changing — what should I do?"

## How to answer

1. **Identify the situation** in one of these categories:

   | Category | Section to read in stx-guide.md |
   |----------|---------------------------------|
   | Workspace alignment / sync / lock churn | §4.13 Alignment & sync |
   | Developing a pack (link/unlink/test in consumer) | §4.12 Pack development |
   | Releasing a new version of streamtex | §4.10 Release — developer workflow |
   | Receiving an update as a user | §4.11 Update — user workflow |
   | Deployment to Hetzner/Coolify | §4.4 + §4g |
   | Block authoring | §4.9 Working with blocks |
   | Style system / themes | §4d Style system |
   | AI image generation | §4b AI image generation |
   | Anything else | Section 6 Quick reference card |

2. **Read the relevant section** of
   `streamtex-claude/shared/commands/stx-guide.md` (or, in a project that
   has the mirror installed, `.claude/commands/stx-guide.md`).

3. **Answer the user from that content.** The answer should be the same
   they would get if they typed `/stx-guide <topic>` explicitly.

4. **For very common situations**, the decision table in
   `stx-guide.md` Section 6 ("Decision table — which command for my
   situation?") gives a one-line answer per row. Use it as a fast lookup
   when the question matches a row directly.

## Why this skill exists

- Single source of truth: all decision content lives in `stx-guide.md`.
  This skill is a thin auto-trigger layer.
- Bidirectional: whether the user types `/stx-guide` explicitly or just
  describes their situation in natural language, they get the same answer.
- Helps Claude itself: when working autonomously (sub-agents, `/loop`,
  long sessions), this skill ensures Claude consults the canonical
  reference instead of guessing.
