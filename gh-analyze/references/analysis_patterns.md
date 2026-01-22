# GitHub Repository Analysis Patterns

This reference provides detailed patterns for analyzing different aspects of GitHub repositories.

## Code Quality Patterns

### Indicators of High Quality
- Clear separation of concerns (models, views, controllers separated)
- Consistent naming conventions
- Small, focused functions (< 50 lines typically)
- Proper error handling with try/catch or error propagation
- Type definitions (TypeScript, Python type hints, Go interfaces)
- Comprehensive README with setup instructions

### Red Flags
- Large monolithic files (> 1000 lines)
- God objects/classes with too many responsibilities
- Inconsistent indentation or formatting
- Missing error handling
- Hardcoded configuration values
- Commented-out code blocks
- Copy-pasted code patterns

## Security Patterns to Check

### Common Vulnerabilities
1. **Hardcoded secrets**: API keys, passwords, tokens in source code
2. **SQL injection**: String concatenation in database queries
3. **XSS**: Unsanitized user input rendered to HTML
4. **CSRF**: Missing CSRF tokens on state-changing operations
5. **Auth bypass**: Missing authentication on sensitive endpoints
6. **Dependency vulnerabilities**: Outdated packages with known CVEs

### Files to Check for Security
- `.env.example` (should not contain real secrets)
- `config/` or `config.*` files
- Authentication/authorization modules
- Database query builders
- Input validation middleware
- `.gitignore` (should exclude sensitive files)

## Architecture Patterns Recognition

### Monolithic Structure
```
repo/
├── src/
│   ├── components/
│   ├── utils/
│   └── index.ts
├── tests/
└── package.json
```

### Modular/Monorepo Structure
```
repo/
├── packages/
│   ├── package-a/
│   ├── package-b/
│   └── package-c/
├── apps/
└── package.json
```

### Layered Architecture
```
repo/
├── src/
│   ├── controllers/  # Request handling
│   ├── services/     # Business logic
│   ├── models/       # Data models
│   └── repositories/ # Data access
```

### Microservices Style (in monorepo)
```
repo/
├── services/
│   ├── auth-service/
│   ├── user-service/
│   └── payment-service/
```

## Technology Stack Identification

### JavaScript/TypeScript
- **package.json**: Check `dependencies` and `devDependencies`
- **tsconfig.json**: TypeScript configuration
- **Frameworks**: React, Vue, Angular, Next.js, NestJS, Express

### Python
- **requirements.txt** or **pyproject.toml**: Dependencies
- **setup.py** or **setup.cfg**: Package configuration
- **Frameworks**: Django, Flask, FastAPI, asyncio

### Go
- **go.mod**: Module definition and dependencies
- **main.go** or **cmd/**: Entry points
- **Frameworks**: Gin, Echo, gRPC

### Java/Kotlin
- **pom.xml** (Maven) or **build.gradle** (Gradle)
- **src/main/java**: Standard source structure
- **Frameworks**: Spring Boot, Jakarta EE

### Ruby
- **Gemfile**: Ruby dependencies
- **Rakefile**: Build tasks
- **Frameworks**: Ruby on Rails, Sinatra

## CI/CD Detection

### GitHub Actions
`.github/workflows/*.yml` - Check for:
- Build and test automation
- Deployment configurations
- Security scanning steps
- Code quality checks

### Other CI Systems
- `.gitlab-ci.yml` - GitLab CI
- `.travis.yml` - Travis CI
- `circleci/config.yml` - CircleCI
- `azure-pipelines.yml` - Azure DevOps
- `Jenkinsfile` - Jenkins

## Test Organization Patterns

### Standard Test Structure
```
repo/
├── src/
└── tests/ or __tests__/
    ├── unit/
    ├── integration/
    └── e2e/
```

### Co-located Tests
```
repo/
└── src/
    ├── feature/
    │   ├── feature.ts
    │   └── feature.test.ts
```

### Test Files to Look For
- `*.test.js/ts` - Jest/UVU
- `*_test.go` - Go testing
- `test_*.py` - pytest
- `*.spec.js/ts` - Jasmine/Mocha
- `__tests__/` - Jest default directory
- `spec/` - RSpec (Ruby)

## License Identification

### Common Licenses by File
- **MIT**: LICENSE file with "MIT License"
- **Apache 2.0**: LICENSE file with "Apache License"
- **GPL**: LICENSE or COPYING with "GNU General Public License"
- **BSD**: LICENSE file with "BSD License"
- **Unlicense**: UNLICENSE file

### License Compatibility Notes
- MIT/Apache/BSD: Permissive, commercial-friendly
- GPL: Copyleft, requires derivative works to be GPL
- LGPL: Weak copyleft, allows linking from non-GPL code

## Activity Metrics Interpretation

| Metric | Active | Warning Sign |
|--------|--------|--------------|
| Recent commits | Commits within last 30 days | No commits in 6+ months |
| Issue response | Responses within days | Open issues > 6 months old |
| PR merge rate | High merge rate | Stale PRs not reviewed |
| Contributors | Growing or stable | Single contributor only |

## Documentation Quality Checklist

- [ ] README exists with project description
- [ ] Installation instructions present
- [ ] Usage examples provided
- [ ] API documentation (if library)
- [ ] Contributing guidelines (CONTRIBUTING.md)
- [ ] Changelog (CHANGELOG.md)
- [ ] Code of conduct (CODE_OF_CONDUCT.md)
- [ ] License clearly stated
- [ ] Examples or demo included
