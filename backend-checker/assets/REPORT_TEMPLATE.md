# Backend Analysis Report

**Project**: {{PROJECT_NAME}}
**Date**: {{DATE}}
**Backend**: {{BACKEND_TYPE}}
**Python Version**: {{PYTHON_VERSION}}
**Framework**: {{FRAMEWORK}}

---

## Executive Summary

### Health Score

| Metric | Score | Status |
|--------|-------|--------|
| Overall Health | {{HEALTH_SCORE}}/100 | {{HEALTH_STATUS}} |
| Security | {{SECURITY_SCORE}}/100 | {{SECURITY_STATUS}} |
| Performance | {{PERFORMANCE_SCORE}}/100 | {{PERFORMANCE_STATUS}} |
| Code Quality | {{CODE_QUALITY_SCORE}}/100 | {{CODE_QUALITY_STATUS}} |

### Issue Summary

| Priority | Count | Description |
|----------|-------|-------------|
| P0 (Critical) | {{P0_COUNT}} | {{P0_DESCRIPTION}} |
| P1 (High) | {{P1_COUNT}} | {{P1_DESCRIPTION}} |
| P2 (Medium) | {{P2_COUNT}} | {{P2_DESCRIPTION}} |
| P3 (Low) | {{P3_COUNT}} | {{P3_DESCRIPTION}} |
| **Total** | **{{TOTAL_COUNT}}** | |

### Quick Wins (XS-S effort, high impact)

{{QUICK_WINS_LIST}}

---

## Service Health Status

| Component | Status | Response Time | Details |
|-----------|--------|---------------|---------|
| API Service | {{API_STATUS}} | {{API_RESPONSE_TIME}} | {{API_DETAILS}} |
| Database | {{DB_STATUS}} | {{DB_RESPONSE_TIME}} | {{DB_DETAILS}} |
| Redis/Cache | {{CACHE_STATUS}} | {{CACHE_RESPONSE_TIME}} | {{CACHE_DETAILS}} |
| External APIs | {{EXT_API_STATUS}} | {{EXT_API_RESPONSE_TIME}} | {{EXT_API_DETAILS}} |

---

## Security Findings

### P0 - Critical Security Issues

{{P0_SECURITY_ISSUES}}

### P1 - High Priority Security Issues

{{P1_SECURITY_ISSUES}}

### P2 - Medium Priority Security Issues

{{P2_SECURITY_ISSUES}}

### P3 - Low Priority Security Issues

{{P3_SECURITY_ISSUES}}

---

## Performance Analysis

### Slow Endpoints (P50 > 500ms or P95 > 1s)

| Endpoint | P50 | P95 | P99 | Issues |
|----------|-----|-----|-----|--------|
{{SLOW_ENDPOINTS_TABLE}}

### Database Query Analysis

- **Slow Queries**: {{SLOW_QUERY_COUNT}}
- **N+1 Query Issues**: {{N_PLUS_1_COUNT}}
- **Missing Indexes**: {{MISSING_INDEX_COUNT}}
- **Connection Pool Issues**: {{CONNECTION_POOL_ISSUES}}

{{DB_QUERY_DETAILS}}

### Resource Usage

- **Memory**: {{MEMORY_USAGE}} / {{MEMORY_LIMIT}}
- **CPU**: {{CPU_USAGE}}
- **Active Connections**: {{ACTIVE_CONNECTIONS}} / {{MAX_CONNECTIONS}}

---

## Code Quality Assessment

### Type Coverage

```
Type Safety: {{TYPE_COVERAGE}}%
```
- Files with type hints: {{TYPED_FILES}} / {{TOTAL_FILES}}
- Files with full coverage: {{FULLY_TYPED_FILES}}
- Files using `typing.Any`: {{ANY_TYPE_FILES}}

### Linting Violations

| Category | Count | Files Affected |
|----------|-------|----------------|
| Import ordering | {{IMPORT_ISSUES}} | {{IMPORT_FILES}} |
| Line length | {{LINE_LENGTH_ISSUES}} | {{LINE_LENGTH_FILES}} |
| Unused imports | {{UNUSED_IMPORTS}} | {{UNUSED_IMPORT_FILES}} |
| Code complexity | {{COMPLEXITY_ISSUES}} | {{COMPLEXITY_FILES}} |

### Error Handling

- **Endpoints without error handling**: {{NO_ERROR_HANDLING_COUNT}}
- **Bare except clauses**: {{BARE_EXCEPT_COUNT}}
- **Missing logging on errors**: {{NO_LOGGING_COUNT}}

### Testing Coverage

```
Overall Coverage: {{TEST_COVERAGE}}%
```
- Unit tests: {{UNIT_TEST_COVERAGE}}%
- Integration tests: {{INTEGRATION_TEST_COVERAGE}}%
- Endpoints with tests: {{TESTED_ENDPOINTS}} / {{TOTAL_ENDPOINTS}}

---

## Dependency Analysis

### Outdated Dependencies

| Package | Current | Latest | Severity |
|---------|---------|--------|----------|
{{OUTDATED_DEPENDENCIES_TABLE}}

### Known Vulnerabilities

| Package | Version | CVE | Severity |
|---------|---------|-----|----------|
{{VULNERABILITIES_TABLE}}

### Unused Dependencies

{{UNUSED_DEPENDENCIES_LIST}}

---

## Prioritized Action Plan

### Sprint 1 - Critical Fixes (Week 1)

- [ ] {{SPRINT1_ITEM_1}}
- [ ] {{SPRINT1_ITEM_2}}
- [ ] {{SPRINT1_ITEM_3}}

**Expected Impact**: Resolve critical security and performance blockers

### Sprint 2 - High Priority (Week 2-3)

- [ ] {{SPRINT2_ITEM_1}}
- [ ] {{SPRINT2_ITEM_2}}
- [ ] {{SPRINT2_ITEM_3}}

**Expected Impact**: Fix major performance issues, improve security posture

### Sprint 3 - Medium Priority (Week 4-5)

- [ ] {{SPRINT3_ITEM_1}}
- [ ] {{SPRINT3_ITEM_2}}
- [ ] {{SPRINT3_ITEM_3}}

**Expected Impact**: Enhance code quality, reduce technical debt

### Sprint 4 - Low Priority & Improvements (Week 6+)

- [ ] {{SPRINT4_ITEM_1}}
- [ ] {{SPRINT4_ITEM_2}}
- [ ] {{SPRINT4_ITEM_3}}

**Expected Impact**: Polish and optimization

---

## Detailed Findings

### Security Solutions

{{SECURITY_SOLUTIONS}}

### Performance Solutions

{{PERFORMANCE_SOLUTIONS}}

### Code Quality Solutions

{{CODE_QUALITY_SOLUTIONS}}

---

## Prevention Measures

### Development Process

{{PROCESS_IMPROVEMENTS}}

### CI/CD Recommendations

{{CI_CD_RECOMMENDATIONS}}

### Monitoring Enhancements

{{MONITORING_RECOMMENDATIONS}}

---

## Appendix

### A. Health Check Implementation

{{HEALTH_CHECK_CODE}}

### B. Security Best Practices

{{SECURITY_BEST_PRACTICES}}

### C. Performance Optimization Checklist

{{PERFORMANCE_CHECKLIST}}

### D. Useful Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [SQLAlchemy Performance](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- [Prisma Performance](https://www.prisma.io/docs/guides/performance-and-optimization)
