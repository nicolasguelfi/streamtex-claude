# Task Review Report

**Task**: {{ task_description }}
**Date**: {{ date }}
**Scope**: {{ scope }}
**Criteria**: {{ criteria }}
**Perspective**: {{ perspective }} (built-in / ad-hoc)

## Findings

| # | Block | Finding | Severity | Recommendation |
|---|-------|---------|----------|----------------|
| 1 | {{ block }} | {{ finding }} | {{ severity }} | {{ recommendation }} |

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | {{ count }} |
| MAJOR | {{ count }} |
| MINOR | {{ count }} |
| SUGGESTION | {{ count }} |
| **Total** | {{ total }} |

## Integration

These findings will be picked up by `/stx-ce:fix` in the next fix cycle.
To fix now: `/stx-ce:fix --target <block> --severity <level>`
