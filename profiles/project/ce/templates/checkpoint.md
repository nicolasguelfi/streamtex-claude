# CE Session Checkpoint

---
project: {{ project_name }}
checkpoint_date: {{ YYYY-MM-DDTHH:MM:SS }}
session_started: {{ YYYY-MM-DDTHH:MM:SS (estimated from first CE artifact or git log) }}
current_plan: {{ docs/plans/YYYY-MM-DD-NNN-...-plan.md or "none" }}
current_phase: {{ COLLECT | ASSESS | PLAN | PRODUCE | REVIEW | FIX | COMPOUND }}
phase_progress: {{ e.g. "PRODUCE 8/12 blocks" or "REVIEW 3/5 perspectives" }}
guideline: {{ active design guideline name or "none" }}
---

## Active Work Items

{{ For each block or artifact currently being worked on: }}

- [ ] {{ block_filename }} — {{ status: IN PROGRESS / INCOMPLETE / OUT-OF-PLAN }}: {{ brief description of what was being done }}
- [x] {{ block_filename }} — DONE this session: {{ brief note }}

## Decisions Log

{{ Numbered list of decisions made during this session that are NOT captured in artifacts. }}
{{ Each decision should include: what was decided, why, and what it affects. }}

1. {{ decision description }}
2. {{ decision description }}

## Pending Issues

{{ Known problems, blockers, or items that need attention next session. }}

- {{ issue description — e.g., "bck_llm_layers.py: AI image generation failed, prompt needs rework" }}
- {{ issue description — e.g., "Review partial: only 3/5 perspectives completed" }}

## Uncommitted Changes

{{ Summary of git status at checkpoint time. }}

| File | Status | Note |
|------|--------|------|
| {{ path }} | {{ M/A/D/? }} | {{ brief description }} |

## Context for Next Session

{{ Free-text paragraph summarizing where things stand, what the focus was, and what to prioritize next. This is the most important section for session resumption — write it as a briefing for your future self. }}

{{ user_message if --message was provided, otherwise extracted from session context }}
