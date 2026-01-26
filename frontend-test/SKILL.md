---
name: frontend-test
description: Comprehensive frontend testing suite for UI, functionality, performance, and code quality. Use when user asks to test frontend code, check for bugs, validate UI/UX, run frontend tests, perform quality assurance, or audit frontend projects. Supports React, Vue, vanilla JS, and other frameworks. Covers visual testing, interaction testing, performance analysis, accessibility checks, and code quality review.
user-invocable: true
---


# Frontend Test Suite

Comprehensive testing workflow for frontend applications covering UI/UX, functionality, performance, accessibility, and code quality.

## Quick Start

For immediate testing, use this workflow:

1. **Identify project type** - Detect framework (React/Vue/vanilla)
2. **Determine test scope** - UI, functionality, performance, or comprehensive
3. **Select test method** - Manual review, automated Playwright tests, or hybrid
4. **Execute tests** - Follow checklist for chosen scope
5. **Report findings** - Document bugs with severity and reproduction steps

## Test Scenarios

### User Request Patterns

| User Says | Action |
|-----------|--------|
| "Test my frontend" | Run comprehensive test suite |
| "Check for bugs" | Execute functionality testing |
| "Review UI/UX" | Perform visual and layout testing |
| "Performance issues" | Run performance profiling |
| "Is my code production-ready?" | Full quality audit |

## Testing Workflow

### Phase 1: Project Analysis

```
1. Scan package.json for framework and dependencies
2. Identify build tool (Vite, Webpack, Next.js, etc.)
3. Check for existing test setup (Jest, Cypress, Playwright, Vitest)
4. Review project structure and routing
```

### Phase 2: Choose Test Approach

**Local Dev Server Testing** (Preferred for active development):
- Start dev server locally
- Test in browser with DevTools
- Real-time debugging and inspection
- Hot-reload for quick iterations

**Automated Playwright Testing** (For regression checks):
- Use Playwright for E2E testing
- Capture screenshots for visual regression
- Test multiple viewports (mobile/tablet/desktop)
- Generate test reports

**Build Output Testing** (For production readiness):
- Test built/compiled output
- Check bundle size and composition
- Verify production optimizations
- Test in staging environment

### Phase 3: Execute Tests

Load appropriate checklist from `references/`:

- **[checklist.md](references/checklist.md)** - Complete testing checklist
- **[frameworks.md](references/frameworks.md)** - Framework-specific checks

**Core Testing Areas:**

1. **UI/Style** - Layout, responsiveness, visual consistency, browser compatibility
2. **Functionality** - User interactions, state management, API integration, edge cases
3. **Performance** - Load time, runtime performance, resource optimization
4. **Code Quality** - Type safety, linting, accessibility, best practices

### Phase 4: Bug Reporting Format

```markdown
## Bug Report

### [Severity] Title
- **Severity**: Critical / High / Medium / Low
- **Location**: Component/Page/File:line
- **Description**: What is wrong

**Steps to Reproduce:**
1. Step one
2. Step two
3. Observe the bug

**Expected Behavior:** What should happen

**Actual Behavior:** What actually happens

**Screenshots:** [If applicable]

**Environment:** Browser, OS, Screen size
```

## Severity Guidelines

- **Critical**: App unusable, data loss, security vulnerability
- **High**: Major feature broken, significant UX issue
- **Medium**: Minor feature broken, visual inconsistency
- **Low**: Cosmetic issue, suggestion for improvement

## Automated Testing Scripts

### Smart Scanner (Recommended)

```bash
python scripts/smart_scan.py <project_path> [url]
```

**Intelligent all-in-one scanner** that:
- Auto-detects framework (React/Vue/Next.js/Nuxt/Angular/Svelte)
- Identifies build tool (Vite/Webpack) and port
- Runs code quality scan (ESLint, TypeScript, bundle size)
- Runs Lighthouse analysis (Performance/SEO/Accessibility)
- Runs E2E tests (Navigation, Forms, Responsive, Console errors)

### Code Quality Scanner

```bash
python scripts/code_quality.py <project_path>
```

Checks:
- ESLint configuration and results
- TypeScript type errors
- Bundle size analysis
- Code health indicators (.gitignore, README.md, CI config)

### Lighthouse Scanner

```bash
python scripts/lighthouse_scan.py <url> [output_path]
```

Generates comprehensive report:
- Performance score and metrics (LCP, FCP, TBT, CLS)
- Accessibility score and issues
- Best Practices score
- SEO score
- Critical and warning issues list

### E2E Test Runner

```bash
python scripts/e2e_test.py <url>
```

Automated browser tests:
- Navigation (link checking)
- Forms (labels, validation, required fields)
- Responsive design (mobile/tablet/desktop)
- Console errors and warnings

## Best Practices

1. **Test systematically** - Follow checklist order, don't skip sections
2. **Reproduce bugs** - Always verify bugs can be reproduced before reporting
3. **Provide context** - Include exact steps, screenshots, and environment info
4. **Prioritize findings** - Group bugs by severity for actionable feedback
5. **Suggest fixes** - Where possible, provide concrete solutions

## Framework Detection

Automatically detect the framework:
- Check `package.json` for `react`, `vue`, `next`, `nuxt`, `angular`, `svelte`
- Apply framework-specific tests from `frameworks.md`
- Use appropriate DevTools (React DevTools, Vue DevTools)
