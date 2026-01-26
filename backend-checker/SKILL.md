---
name: backend-checker
description: Comprehensive backend code analyzer for Python/FastAPI/Flask/Django projects. Performs security, performance, and code quality analysis with actionable recommendations. Use when users ask to analyze, audit, review, or check backend code via natural language (e.g., "检查后端代码", "分析一下后端", "backend code review", "analyze backend security", "check for performance issues"). Generates detailed reports with health scores, prioritized issues, and sprint plans.
user-invocable: false
---


# Backend Checker

Comprehensive analysis tool for backend code focusing on security, performance, and code quality.

## When to Use

Trigger this skill when users mention:
- Backend code review/analysis ("检查后端", "分析后端代码")
- Security audit ("安全检查", "security audit")
- Performance analysis ("性能分析", "performance issues")
- Code quality assessment ("代码质量", "code review")

## Supported Frameworks

- **Python**: FastAPI, Flask, Django, Tornado
- **Node.js**: Express, NestJS, Fastify
- **Go**: Gin, Echo, Fiber
- **Java**: Spring Boot, Jakarta EE

## Analysis Workflow

### Phase 1: Pre-Check Analysis

1. **Identify project structure**:
   - Framework detection
   - ORM identification (SQLAlchemy, Prisma, Django ORM, etc.)
   - Entry points (main.py, app.py, index.ts)
   - Configuration files

2. **Technology stack**:
   - Language version
   - Dependencies (requirements.txt, package.json, go.mod)
   - Database type
   - External services (Redis, S3, etc.)

### Phase 2: Security Analysis

**Detection Patterns**:
- SQL injection vulnerabilities
- Hardcoded secrets/API keys
- Unsafe deserialization (pickle, yaml.load)
- Weak cryptography (MD5, SHA1)
- Missing authentication/authorization
- CORS misconfigurations

**Severity Classification**:
- **P0 (Critical)**: SQL injection, hardcoded secrets, auth bypass
- **P1 (High)**: Missing auth, unsafe deserialization, XSS/CSRF
- **P2 (Medium)**: Weak crypto, missing rate limiting
- **P3 (Low)**: Logging issues, config recommendations

### Phase 3: Performance Analysis

**Detection Patterns**:
- N+1 query problems
- Missing pagination
- Synchronous I/O in async handlers
- Unoptimized database queries
- Missing indexes
- Connection pool issues

### Phase 4: Code Quality Analysis

**Detection Patterns**:
- Missing type hints
- Bare except clauses
- Print statements instead of logging
- Missing error handling
- Code complexity issues
- Unused imports/code

## Health Score Calculation

```
Base Score: 100
Deductions:
  - P0 × 25 points
  - P1 × 10 points
  - P2 × 3 points
  - P3 × 1 point
```

Category Scores:
- Security: 100 - (security_issues × 15)
- Performance: 100 - (perf_issues × 10)
- Quality: 100 - (quality_issues × 5)

## Report Structure

Generate reports using the template in `assets/REPORT_TEMPLATE.md`:

1. **Executive Summary** - Health scores, issue counts, quick wins
2. **Service Health** - Component status, response times
3. **Security Findings** - Vulnerabilities by severity
4. **Performance Analysis** - Slow endpoints, query analysis
5. **Code Quality** - Type coverage, linting, testing
6. **Dependencies** - Outdated packages, vulnerabilities
7. **Action Plan** - Prioritized fixes by sprint

## Reference Materials

- `references/workflow.md` - Detailed step-by-step workflow
- `references/security-solutions.md` - Security fix recommendations
- `references/performance-solutions.md` - Performance optimization guides
- `references/code-quality-solutions.md` - Code quality improvements

## Special Cases

### When Backend is Running

Perform runtime checks:
```bash
# Health endpoints
GET /health
GET /health/ready
GET /health/live
GET /metrics
```

### When Using Docker

```bash
docker ps                    # Check containers
docker stats                 # Resource usage
docker logs <container>      # Logs
```

### When Using Kubernetes

```bash
kubectl get pods             # Pod status
kubectl describe pod <name>  # Pod details
kubectl logs <pod>           # Logs
```

## Quality Checklist

Before finalizing report:
- [ ] All P0 issues have code examples
- [ ] Each issue has file location reference
- [ ] Health score calculation is correct
- [ ] Solutions are specific and actionable
- [ ] Quick wins are highlighted
- [ ] Severity classifications are appropriate
