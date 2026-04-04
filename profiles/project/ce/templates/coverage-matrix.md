# Coverage Analysis Report

**Task**: {{ task_description }}
**Date**: {{ date }}
**Source**: {{ source_path }} (lines {{ line_range }})
**Target blocks**: {{ target_pattern }}

## Coverage Matrix

| # | Source Theme | Lines | Status | Block(s) | Fidelity |
|---|------------|-------|--------|----------|----------|
| 1 | {{ theme }} | {{ lines }} | {{ status }} | {{ blocks }} | {{ fidelity }} |

**Status legend**: COVERED (present and faithful), PARTIAL (incomplete), REPLACED (deliberately adapted), MISSING (absent)
**Fidelity legend**: Exact (verbatim), Summarized (condensed), Adapted (changed for context), Absent (not produced)

## Summary

| Status | Count | % |
|--------|-------|---|
| COVERED | {{ n }} | {{ pct }} |
| PARTIAL | {{ n }} | {{ pct }} |
| REPLACED | {{ n }} | {{ pct }} |
| MISSING | {{ n }} | {{ pct }} |

## Gap Recommendations

{{ for each MISSING theme }}
- **{{ theme }}** (lines {{ lines }}): Recommend creating `{{ suggested_block_name }}` — {{ brief_description }}
{{ end }}

## Plan Impact

{{ if gaps_significant }}
Consider creating a new plan version to include the {{ missing_count }} missing themes.
Command: `/stx-ce:task "Update plan to add blocks for uncovered source themes"`
{{ else }}
Coverage is adequate. No plan changes recommended.
{{ end }}
