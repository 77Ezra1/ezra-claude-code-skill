# Optimization Workflow

Step-by-step process for generating optimization documents from test results.

## 1. Input Collection

First, gather all test results and bug reports:

```markdown
## Input Sources

### Required
- [ ] frontend-test skill output OR
- [ ] Bug reports in standard format OR
- [ ] List of issues with severities

### Optional (enhances document)
- [ ] Lighthouse report (performance, a11y scores)
- [ ] Bundle analysis results
- [ ] TypeScript/ESLint error counts
- [ ] Screenshot evidence for UI issues
```

## 2. Parse and Categorize

Process raw input into structured data:

```python
# Pseudo-code for categorization
issues = parse_test_results(input)

for issue in issues:
    # Assign priority based on severity
    if issue.severity == "Critical":
        issue.priority = "P0"
        issue.effort = calculate_effort(issue)  # XS/S/M/L/XL
        issue.impact = "HIGH"
    elif issue.severity == "High":
        issue.priority = "P1"
        # ...
```

## 3. Calculate Health Score

```
Base Score: 100
Deductions:
  - P0 × 25 points each
  - P1 × 10 points each
  - P2 × 3 points each
  - P3 × 1 point each

Category Scores (if available):
  - Security: 100 - (security_issues × weight)
  - Performance: Lighthouse score or calculated
  - Accessibility: Lighthouse a11y score or calculated
  - Code Quality: Based on lint/type errors
```

## 4. Generate Document Sections

### Executive Summary
- Health score with visual indicator (color-coded)
- Issue counts by priority
- 3-5 quick wins (XS-S effort, high impact)

### Issue Inventory
- Group by priority (P0 → P3)
- For each issue include:
  - Title and severity
  - Location (file:line or component)
  - Brief description
  - Effort estimate

### Action Plan
- Sprint 1: All P0 issues + top P1 quick wins
- Sprint 2: Remaining P1 + high-impact P2
- Sprint 3: P2 issues
- Sprint 4: P3 and improvements

### Solutions Matrix
- For each issue category, provide:
  - Root cause analysis
  - Concrete solution steps
  - Code examples (from solutions.md)
  - Related issues to fix together

## 5. Quality Checks

Before outputting document:

```markdown
## Document Quality Checklist

- [ ] All P0 issues are in Sprint 1
- [ ] Health score calculation is correct
- [ ] Each issue has a location reference
- [ ] Each issue has an effort estimate
- [ ] Solutions are specific and actionable
- [ ] Code examples are included for complex fixes
- [ ] Quick wins are highlighted
- [ ] Document follows template structure
```

## 6. Output Format

Generate as markdown with:

1. **Table of Contents** - For navigation
2. **Checkboxes** - For progress tracking
3. **Code Blocks** - With syntax highlighting
4. **Tables** - For summaries and metrics
5. **Links** - To affected files and docs

## Example Output Generation

```markdown
# Project Optimization Document

## Executive Summary

### Health Score: 65/100

<span style="color: orange;">**Fair** - Needs attention before production</span>

| Priority | Count | Status |
|----------|-------|--------|
| P0 | 2 | Security vulnerability, data loss bug |
| P1 | 5 | Performance issues, broken features |
| P2 | 8 | UI inconsistencies, minor bugs |
| P3 | 12 | Cosmetic issues |

### Quick Wins
- [ ] Add loading states (XS) - Improves perceived performance
- [ ] Fix color contrast on CTA button (XS) - Improves accessibility
- [ ] Add aria-label to icon buttons (S) - Improves accessibility
```

## Customization Options

### For Production Projects
- Emphasize P0/P1 issues
- Include rollback strategies
- Add A/B testing recommendations

### For Development Projects
- Focus on code quality improvements
- Include testing recommendations
- Add documentation tasks

### For Legacy Projects
- Include technical debt assessment
- Recommend incremental refactoring
- Suggest migration paths for outdated patterns
