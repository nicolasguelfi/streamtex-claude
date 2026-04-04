# Source Analysis Report

**Task**: {{ task_description }}
**Date**: {{ date }}
**Source**: {{ source_path }}
**Line range**: {{ line_range }} (or "full document")

## Document Structure

{{ hierarchical outline of sections/subsections }}

## Themes Extracted

| # | Theme | Lines | Description | Relevance |
|---|-------|-------|-------------|-----------|
| 1 | {{ theme }} | {{ lines }} | {{ description }} | {{ relevance }} |

## Statistics Found

| # | Statistic | Value | Context | Source/Citation |
|---|-----------|-------|---------|----------------|
| 1 | {{ stat_name }} | {{ value }} | {{ context }} | {{ citation }} |

## Citations & References

| # | Author(s) | Year | Title | Lines |
|---|-----------|------|-------|-------|
| 1 | {{ authors }} | {{ year }} | {{ title }} | {{ lines }} |

## Key Concepts / Definitions

| # | Term | Definition | Lines |
|---|------|-----------|-------|
| 1 | {{ term }} | {{ definition }} | {{ lines }} |

## Integration Notes

This analysis is available for:
- Plan amendments: `/stx-ce:task "Update plan based on source analysis"`
- Coverage comparison: `/stx-ce:task "Compare this analysis with produced blocks"`
- Production: `/stx-ce:task "Produce blocks for themes X, Y, Z"`
