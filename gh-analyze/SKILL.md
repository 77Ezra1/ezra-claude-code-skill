---
name: gh-analyze
description: Comprehensive GitHub repository analyzer that provides deep analysis of any GitHub repository. Use when users ask to analyze, examine, investigate, or understand a GitHub repository via natural language (e.g., "帮我分析这个GitHub仓库", "分析一下github.com/user/repo", "看看这个项目怎么样", "了解这个仓库的代码质量"). The skill performs multi-dimensional analysis including: (1) README and project documentation, (2) Code structure and architecture, (3) Dependencies and tech stack, (4) Commit history and activity, (5) Code quality assessment, (6) Security review, (7) Performance analysis, (8) Test coverage analysis.
---

# GitHub Repository Analyzer

Perform comprehensive analysis of GitHub repositories across multiple dimensions.

## Quick Start

When a user provides a GitHub repository URL or asks to analyze a repository:

```bash
# Example triggers:
- "分析这个GitHub仓库: https://github.com/user/repo"
- "帮我看看github.com/user/repo这个项目"
- "分析一下这个项目的代码质量"
- "这个仓库架构怎么样？"
```

## Analysis Workflow

### Phase 1: Repository Discovery

1. **Extract repository info** from user input:
   - Parse GitHub URL (format: `github.com/owner/repo`)
   - Handle partial inputs (e.g., `owner/repo`)

2. **Clone or fetch repository data**:
   - Use `gh` CLI or `git clone` to access repository
   - Fallback: Use GitHub API via web scraping if CLI unavailable

3. **Basic repository metadata**:
   - Repository name, description, topics
   - Stars, forks, watchers count
   - License information
   - Primary language
   - Creation and last update dates

### Phase 2: Documentation Analysis

1. **README Analysis**:
   - Project overview and purpose
   - Installation instructions quality
   - Usage examples completeness
   - Contributing guidelines presence
   - Documentation structure and clarity

2. **Additional docs**:
   - CONTRIBUTING.md, CODE_OF_CONDUCT.md
   - CHANGELOG or HISTORY
   - API docs, architecture docs (docs/ folder)

### Phase 3: Code Structure & Architecture

1. **Directory structure analysis**:
   - Overall organization patterns (monorepo, multi-package, standard)
   - Source code layout (src/, lib/, app/, etc.)
   - Configuration files placement
   - Test organization

2. **Architecture patterns**:
   - Identify design patterns (MVC, microservices, layered, etc.)
   - Module coupling and cohesion
   - Entry points and core modules
   - Separation of concerns

3. **File-level analysis** (for key files):
   - Main application files
   - Core business logic
   - Configuration files

### Phase 4: Dependencies & Tech Stack

1. **Language detection**:
   - Primary language (from GitHub or file extensions)
   - Secondary languages

2. **Dependency analysis**:
   - Read package manifests: `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`, etc.
   - Categorize dependencies: production vs dev/test
   - Identify key frameworks and libraries
   - Check for outdated dependencies

3. **Build & tooling**:
   - Build systems (Webpack, Vite, Gradle, Maven, Make, etc.)
   - CI/CD configuration (.github/workflows, .gitlab-ci.yml, etc.)
   - Package managers used

### Phase 5: Activity & Community

1. **Commit analysis**:
   - Total commit count
   - Commit frequency patterns
   - Recent activity (last 30/90 days)
   - Contribution distribution

2. **Contributors**:
   - Contributor count
   - Top contributors
   - Organization vs individual contributions

3. **Issues & Pull Requests**:
   - Open/closed issues ratio
   - PR merge rate
   - Response time metrics
   - Issue labeling practices

### Phase 6: Code Quality Assessment

1. **Code style & formatting**:
   - Presence of linter configurations (.eslintrc, .pylintrc, etc.)
   - Formatter usage (Prettier, Black, gofmt, etc.)
   - Code consistency

2. **Complexity analysis**:
   - Function/class length patterns
   - Cyclomatic complexity indicators
   - Code duplication signs

3. **Best practices**:
   - Error handling patterns
   - Logging practices
   - Configuration management
   - Environment variable usage

4. **Documentation in code**:
   - Comment density
   - Docstring/JSDoc presence
   - Type annotation usage (TypeScript, Python type hints)

### Phase 7: Security Review

1. **Dependency security**:
   - Known vulnerabilities in dependencies
   - Outdated packages with security issues

2. **Code security patterns**:
   - Secrets detection (API keys, tokens in code)
   - Input validation practices
   - Authentication/authorization patterns
   - SQL injection/XSS prevention

3. **Security configurations**:
   - .gitignore presence and completeness
   - Security policies (.github/SECURITY.md)
   - Dependency scanning tools

### Phase 8: Performance Analysis

1. **Performance patterns**:
   - Caching strategies
   - Database query optimization signs
   - Lazy loading implementation
   - Async/concurrency usage

2. **Resource usage indicators**:
   - Bundle size (for frontend)
   - Asset optimization
   - Memory management patterns

### Phase 9: Test Coverage

1. **Test presence**:
   - Test directory existence
   - Test files count vs source files
   - Test framework identification

2. **Test quality indicators**:
   - Test types present (unit, integration, e2e)
   - Mock/stub usage
   - Coverage configuration
   - CI test execution

## Analysis Output Format

Structure the analysis report as follows:

```markdown
# Repository Analysis: [owner/repo]

## Overview
- Description: [project description]
- Stars: [count] | Forks: [count]
- Language: [primary language]
- License: [license type]
- Last Updated: [date]

## Documentation Quality
[Assessment of README and documentation completeness]

## Architecture & Structure
[Directory structure and architectural patterns]

## Tech Stack & Dependencies
[Primary frameworks, key dependencies, build tools]

## Activity & Community
[Commit patterns, contributors, issues/PRs status]

## Code Quality
[Style, complexity, best practices assessment]

## Security Assessment
[Security findings and recommendations]

## Performance Considerations
[Performance patterns and potential issues]

## Testing Coverage
[Test coverage analysis and quality]

## Overall Assessment
[Summary score and recommendations]
```

## Commands Reference

Use these commands during analysis:

```bash
# Clone repository
git clone --depth 1 https://github.com/owner/repo.git

# Get repository info via GitHub CLI
gh repo view owner/repo --json name,description,primaryLanguage,stargazerCount,createdAt,updatedAt

# Get languages
gh api repos/owner/repo/languages

# Get contributors
gh api repos/owner/repo/contributors

# Get commit activity
gh api repos/owner/repo/stats/commit_activity

# List repository files
gh api repos/owner/repo/contents/
```

## Analysis Tips

1. **Adapt depth to repository size**: For large repositories, focus on key directories and files
2. **Prioritize based on user context**: If user asks about security, emphasize security analysis
3. **Provide actionable insights**: Don't just describe, provide recommendations
4. **Use examples**: Reference specific files when making observations
5. **Be honest about limitations**: State what couldn't be analyzed due to access/size constraints

## Handling Edge Cases

- **Private repositories**: Request access or API token
- **Very large repositories**: Use shallow clone and sampling
- **Monorepos**: Analyze each package separately
- **Multiple languages**: Analyze each language's patterns independently
- **No README**: Note missing documentation and analyze code directly
