---
name: iteration-planner
description: Project code analyzer and feature iteration advisor. Use when user asks to analyze project code, propose feature iterations, identify missing functionality, or create development roadmap based on existing codebase. Performs comprehensive codebase traversal, analyzes current implementation status, and provides structured iteration suggestions with prioritized recommendations.
---

# Iteration Planner

Systematically analyze a project codebase and provide feature iteration recommendations.

## Workflow

### Phase 1: Project Understanding

```
1. Scan project structure
   ├─ Identify tech stack (frontend, backend, database)
   ├─ Map directory organization
   └─ List entry points and main modules

2. Read configuration files
   ├─ package.json / pyproject.toml / requirements.txt
   ├─ tsconfig.json, vite.config, etc.
   ├─ .env.example or config files
   └─ prisma/schema.prisma or database models
```

### Phase 2: Feature Inventory

```
3. Traverse frontend pages
   ├─ Scan pages/ directory for all route pages
   ├─ Identify components and their purposes
   └─ Extract user-facing features

4. Traverse backend APIs
   ├─ Scan api/endpoints/ or routers/
   ├─ List all HTTP routes and their handlers
   └─ Extract business logic coverage

5. Cross-reference analysis
   ├─ Frontend feature vs Backend endpoint mapping
   └─ Identify gaps and inconsistencies
```

### Phase 3: Gap Analysis & Recommendations

Use [analysis-framework.md](references/analysis-framework.md) for systematic analysis patterns.

### Phase 4: Generate Report

Output follows [report-template.md](assets/report-template.md).

## Analysis Dimensions

| Dimension | Focus Area | Reference |
|-----------|-----------|-----------|
| Feature Completeness | Missing core functionality vs product type | [feature-checklist.md](references/feature-checklist.md) |
| Technical Architecture | Scalability, maintainability, technical debt | [architecture-patterns.md](references/architecture-patterns.md) |
| User Experience | Interaction flows, UX improvements | [ux-patterns.md](references/ux-patterns.md) |
| Data Flow | Business logic, data integrity | [data-flows.md](references/data-flows.md) |
| Integration | Third-party services, AI capabilities | [integration-options.md](references/integration-options.md) |

## Scanning Strategy

### Frontend Patterns
```bash
# React/Vue route pages
frontend/src/pages/**/*.tsx
frontend/src/pages/**/*.vue
frontend/src/App.tsx

# Components
frontend/src/components/**/*.tsx
frontend/src/components/**/*.vue

# State management
frontend/src/stores/**/*.ts
frontend/src/context/**/*.tsx
```

### Backend Patterns
```bash
# API endpoints
backend/app/api/**/*.py
backend/app/routers/**/*.py
backend/app/endpoints/**/*.py

# Services (business logic)
backend/app/services/**/*.py

# Database models
backend/app/models/**/*.py
backend/prisma/schema.prisma
```

## Output Format

Generate structured report with:

1. **Project Overview** - Tech stack, architecture summary
2. **Implemented Features** - Complete feature inventory
3. **Feature Gap Analysis** - Missing features by category
4. **Technical Debt** - Refactoring recommendations
5. **Iteration Roadmap** - Prioritized suggestions with effort estimates
6. **Quick Wins** - High-value, low-effort improvements

## Quality Checks

Before finalizing report:
- All suggested features are specific to the project
- Each recommendation includes rationale and complexity estimate
- Technical debt items reference specific files/locations
- Quick wins are clearly distinguished from major features
- Report follows the template structure
