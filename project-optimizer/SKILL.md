---
name: project-optimizer
description: Project optimization specialist that generates comprehensive optimization documents based on frontend-test results or any issue findings. Use this skill when user requests creating optimization plans, generating reports, prioritizing bug fixes, or organizing improvement strategies. 当用户提到「帮我整理/分析/总结这些问题、这些bug/问题怎么修/怎么处理、生成优化计划/报告/方案、帮我制定修复计划/roadmap、根据测试结果生成文档、这些问题优先级怎么排、帮我生成优化建议、创建修复清单、问题太多怎么办、帮我规划一下优化路线、检测出这么多问题，怎么处理、我想优化一下项目、给个修复计划、这些问题怎么安排、生成问题分析报告」等关键词时触发。
user-invocable: true
---


# Project Optimizer

Generate comprehensive project optimization documents from frontend test results.

## Quick Start

1. **Obtain test results** - Get frontend-test skill output or bug reports
2. **Analyze findings** - Categorize issues by severity and type
3. **Create optimization plan** - Generate structured document with prioritized actions
4. **Provide solutions** - Include concrete fixes for each issue

## Workflow

### Phase 1: Collect Test Results

Gather input from:
- **frontend-test skill output** - Bug reports, test findings
- **Direct bug reports** - User-reported issues in Bug Report format
- **Code quality scans** - ESLint, TypeScript, bundle analysis
- **Performance reports** - Lighthouse scores, metrics

### Phase 2: Analysis and Categorization

Organize findings by:

**Priority Levels:**
- **P0 (Critical)** - Security issues, data loss, app unusable
- **P1 (High)** - Major features broken, significant UX problems
- **P2 (Medium)** - Minor bugs, visual inconsistencies
- **P3 (Low)** - Cosmetic issues, nice-to-have improvements

**Issue Categories:**
- **Security** - Vulnerabilities, XSS, injection risks
- **Performance** - Load time, bundle size, runtime optimization
- **Accessibility** - ARIA, keyboard navigation, screen readers
- **UI/UX** - Layout, responsiveness, visual consistency
- **Functionality** - Features, interactions, state management
- **Code Quality** - Type safety, linting, best practices

### Phase 3: Generate Optimization Document

Use template from [OPTIMIZATION_TEMPLATE.md](assets/OPTIMIZATION_TEMPLATE.md)

Document structure:
1. **Executive Summary** - Overview of findings and health score
2. **Issue Inventory** - Complete list with severities
3. **Prioritized Action Plan** - P0 → P3 ordered fixes
4. **Solutions Matrix** - Detailed fix recommendations
5. **Prevention Measures** - Process improvements for future

### Phase 4: Output Format

Generate markdown document with:
- Table of contents for navigation
- Interactive checklist for tracking progress
- Code examples for complex fixes
- Links to relevant documentation
- Estimated effort indicators

## Solution Guidelines

### Performance Issues
- **Bundle size**: Code splitting, tree shaking, lazy loading
- **Load time**: Image optimization, CDN, caching strategies
- **Runtime**: Memoization, virtualization, debouncing

### Accessibility Issues
- **ARIA labels**: Add descriptive labels to interactive elements
- **Keyboard navigation**: Ensure tab order and focus management
- **Color contrast**: Meet WCAG AA standards (4.5:1)
- **Screen readers**: Semantic HTML and landmark regions

### UI/UX Issues
- **Responsive**: Mobile-first approach, breakpoint testing
- **Consistency**: Design system adherence, shared components
- **Layout**: CSS Grid/Flexbox, proper spacing

### Code Quality Issues
- **Type safety**: Fix TypeScript errors, add proper types
- **Linting**: Address ESLint warnings, configure rules
- **Best practices**: React patterns, error boundaries, proper hooks usage

## Effort Estimation

Use these indicators for each fix:
- **XS** - < 15 minutes (simple typo, one-line fix)
- **S** - < 1 hour (small refactor, straightforward change)
- **M** - 1-4 hours (moderate complexity, multiple files)
- **L** - 1-2 days (significant refactor, requires testing)
- **XL** - 3+ days (architectural change, needs design)

## Health Score Calculation

Calculate project health score (0-100):

```
Base Score: 100
- P0 issues × 25
- P1 issues × 10
- P2 issues × 3
- P3 issues × 1

Final Score = max(0, Base Score - Deductions)
```

Health Rating:
- **90-100**: Excellent - Production ready
- **70-89**: Good - Minor issues only
- **50-69**: Fair - Needs attention before production
- **30-49**: Poor - Significant issues
- **0-29**: Critical - Major refactoring needed

## Best Practices

1. **Be specific** - Include exact file locations and code snippets
2. **Prioritize correctly** - Critical issues first, quick wins second
3. **Provide context** - Explain why each fix matters
4. **Include examples** - Show before/after code when helpful
5. **Link resources** - Reference docs for complex solutions
