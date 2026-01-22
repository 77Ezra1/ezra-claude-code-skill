# Backend Checker Workflow

Step-by-step process for analyzing backend code and generating reports.

## 1. Pre-Check Analysis

Before starting, gather context:

```markdown
## Pre-Check Checklist

### Project Structure
- [ ] Identify framework (FastAPI, Flask, Django, etc.)
- [ ] Identify ORM (Prisma, SQLAlchemy, Django ORM, etc.)
- [ ] List all entry points (main.py, app.py, etc.)
- [ ] Identify configuration files (pyproject.toml, requirements.txt, .env)

### Technology Stack
- [ ] Python version
- [ ] Main dependencies
- [ ] Database type (PostgreSQL, MySQL, SQLite, etc.)
- [ ] External services (Redis, S3, etc.)
```

## 2. File Scanning Strategy

Scan these file patterns:

```python
# API endpoints
backend/app/api/**/*.py
backend/app/routers/**/*.py
backend/app/endpoints/**/*.py

# Core logic
backend/app/core/**/*.py
backend/app/services/**/*.py
backend/app/models/**/*.py

# Database
backend/app/db/**/*.py
backend/app/models/**/*.py

# Configuration
backend/app/config.py
backend/app/settings.py
backend/pyproject.toml
backend/requirements.txt
```

## 3. Detection Patterns

### Security Detection

```python
# Scan for these patterns:
SECURITY_PATTERNS = {
    "sql_injection": [
        (r'execute\([f"\'\{]', "Potential SQL injection with f-string"),
        (r'\.format\(.+\).*(SELECT|INSERT|UPDATE|DELETE)', "SQL with format()"),
    ],
    "hardcoded_secrets": [
        (r'(password|api_key|secret|token)\s*=\s*["\'][^"\']+["\']', "Hardcoded credential"),
        (r'(sk-|ghp_|gho_|ghu_|ghs_|ghr_)', "Secret token pattern"),
    ],
    "unsafe_deserialize": [
        (r'pickle\.loads?\(', "Unsafe pickle deserialization"),
        (r'yaml\.load\(', "Unsafe YAML load (use safe_load)"),
    ],
    "weak_crypto": [
        (r'md5\(', "Weak hash algorithm MD5"),
        (r'sha1\(', "Weak hash algorithm SHA1"),
    ],
}
```

### Performance Detection

```python
PERFORMANCE_PATTERNS = {
    "sync_io_in_async": [
        (r'async\s+def.*:\s*.*requests\.', "Synchronous requests in async handler"),
        (r'async\s+def.*:\s*.*time\.sleep\(', "Blocking sleep in async handler"),
    ],
    "missing_pagination": [
        (r'def.*get.*:\s*return.*\.all\(\)', "Returning all records without pagination"),
    ],
}
```

### Code Quality Detection

```python
QUALITY_PATTERNS = {
    "missing_type_hints": [
        (r'def\s+\w+\([^)]*\):', "Function without type hints"),
    ],
    "bare_except": [
        (r'except\s*:', "Bare except clause"),
    ],
    "print_instead_of_log": [
        (r'print\(', "Using print instead of logger"),
    ],
}
```

## 4. Analysis Process

### Step 1: Read Main Entry Point

```python
# Start with backend/app/main.py or similar
# Look for:
- App initialization
- Middleware configuration
- CORS settings
- Included routers
- Event handlers (startup/shutdown)
```

### Step 2: Scan API Endpoints

```python
# For each endpoint file, check:
- Authentication requirements (@login_required, Depends(get_current_user))
- Authorization checks
- Input validation (Pydantic models)
- Error handling
- Rate limiting
- Response models
```

### Step 3: Analyze Database Operations

```python
# Check for:
- Raw SQL queries (potential injection)
- N+1 query patterns
- Missing indexes hints
- Pagination
- Connection pool configuration
```

### Step 4: Review Configuration

```python
# Check config files for:
- Hardcoded secrets
- Debug mode in production
- Allowed hosts
- CORS configuration
- Database URL handling
```

## 5. Severity Classification

```python
def classify_issue(issue_type, context):
    """Classify issue severity based on type and context"""

    # P0 - Critical
    if issue_type in ["sql_injection", "hardcoded_secrets", "auth_bypass"]:
        return "P0"

    # P1 - High
    if issue_type in ["missing_auth", "unsafe_deserialize", "n_plus_one"]:
        return "P1"

    # P2 - Medium
    if issue_type in ["missing_logging", "no_error_handling", "slow_query"]:
        return "P2"

    # P3 - Low
    return "P3"
```

## 6. Report Generation

### Health Score Calculation

```python
def calculate_health_score(issues):
    """
    Base Score: 100
    Deductions:
      - P0 × 25 points
      - P1 × 10 points
      - P2 × 3 points
      - P3 × 1 point
    """
    base_score = 100
    deductions = (
        issues.get("P0", 0) * 25 +
        issues.get("P1", 0) * 10 +
        issues.get("P2", 0) * 3 +
        issues.get("P3", 0) * 1
    )
    return max(0, base_score - deductions)
```

### Category Scores

```python
def calculate_category_scores(issues):
    """Calculate scores for each category"""
    return {
        "security": max(0, 100 - security_issues * 15),
        "performance": max(0, 100 - perf_issues * 10),
        "quality": max(0, 100 - quality_issues * 5),
    }
```

## 7. Output Format

Generate report following the template structure:

1. **Executive Summary** - High-level overview
2. **Health Status** - Service availability
3. **Security Findings** - Vulnerabilities by severity
4. **Performance Analysis** - Slow endpoints, queries
5. **Code Quality** - Type hints, linting, tests
6. **Dependencies** - Outdated, vulnerable packages
7. **Action Plan** - Prioritized fixes

## 8. Quality Checks

Before finalizing report:

```markdown
## Report Quality Checklist

- [ ] All P0 issues have code examples
- [ ] Each issue has a file location reference
- [ ] Health score calculation is correct
- [ ] Solutions are specific and actionable
- [ ] Quick wins are highlighted
- [ ] Report follows template structure
- [ ] Severity classifications are appropriate
```

## 9. Special Cases

### When Backend is Running

If backend is accessible, perform runtime checks:

```python
# Health endpoints
requests.get("http://localhost:8000/health")
requests.get("http://localhost:8000/health/ready")
requests.get("http://localhost:8000/health/live")

# Metrics if available
requests.get("http://localhost:8000/metrics")
```

### When Using Docker

```bash
# Check running containers
docker ps

# Check resource usage
docker stats

# Check logs
docker logs <container_name>
```

### When Using Kubernetes

```bash
# Check pod status
kubectl get pods

# Check health
kubectl describe pod <pod_name>

# Check logs
kubectl logs <pod_name>
```

## 10. Customization

### For Production Systems

- Emphasize security and performance
- Include rollback strategies
- Add monitoring recommendations
- Focus on stability issues

### For Development Systems

- Focus on code quality
- Include testing recommendations
- Suggest development workflow improvements
- Add documentation tasks

### For Legacy Systems

- Assess technical debt
- Recommend incremental improvements
- Suggest migration paths
- Identify architectural issues
