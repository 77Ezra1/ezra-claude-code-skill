---
name: docpilot-code-style
description: DocPilot project code style enforcement. Use this skill when modifying, adjusting, or formatting code/styles in the DocPilot project. Automatically enforces frontend (React/TypeScript/SCSS) and backend (Python/FastAPI) coding standards. Triggered by: "调整样式", "修改样式", "adjust style", "change style", "format code", or any styling/formatting request.
user-invocable: true
---


# DocPilot Code Style

## Quick Reference

Before any style or code modification, always read the full style guide: [references/CODE_STYLE.md](references/CODE_STYLE.md)

## Frontend Rules Summary

- **No semicolons, single quotes** (Prettier enforced)
- **Use `.module.scss`** for all component styles
- **Class names**: camelCase (e.g., `.messageBubble`, `.userAvatar`)
- **Use CSS custom properties**: `var(--color-bg-secondary)`, `var(--spacing-md)`
- **Import order**: React → Third-party → Internal (`@/`) → Types → Styles → Relative
- **Component naming**: PascalCase for components, camelCase for functions
- **Event handlers**: `handle` prefix (e.g., `handleClick`, `handleSubmit`)
- **Boolean vars**: `is`/`has` prefix (e.g., `isLoading`, `hasPermission`)

## Backend Rules Summary

- **Double quotes, 100 char line width** (Ruff enforced)
- **Import order**: Stdlib → Third-party → Local (`app.*`)
- **Naming**: Classes PascalCase, functions/variables snake_case
- **Use `Annotated`** for dependency injection
- **Docstrings**: Google style for functions
- **Unified error format**: `{"success": false, "error": {"code": "...", "message": "..."}}`

## Style Modification Checklist

When user requests style changes:
1. Read [references/CODE_STYLE.md](references/CODE_STYLE.md)
2. Confirm `.module.scss` usage
3. Use CSS custom properties (`var(--*)`)
4. Follow naming conventions
5. Avoid inline styles
6. Check responsive design
