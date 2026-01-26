---
name: analyze-project-style
description: Auto-analyze and enforce project code style. First call: scans project to generate .claude/CODE_STYLE.md. Subsequent calls: reads cached style guide. Use when user requests code/style modifications, formatting, or refactoring. Keywords: "调整样式", "修改样式", "adjust style", "format code", "optimize code", "代码规范", "代码风格".
user-invocable: true
---


# Project Code Style Analyzer

## Workflow

**IMPORTANT**: Always check if `.claude/CODE_STYLE.md` exists in the project root first.

### First Call (No cached style guide)

```bash
# Run the analysis script to generate style guide
python {skill_path}/scripts/analyze_style.py
```

The script will:
- Scan `frontend/` and `backend/` directories
- Analyze config files (Prettier, ESLint, Ruff, etc.)
- Detect naming conventions from actual code
- Generate `.claude/CODE_STYLE.md`

### Subsequent Calls (Cached style guide exists)

Simply read the cached file:
```bash
Read .claude/CODE_STYLE.md
```

Then apply the style rules to the requested modifications.

## Quick Reference Summary

After reading the style guide, follow these core principles:

### Frontend
- Check: semicolons? quotes? indentation? line width?
- Styles: Use `.module.scss`, camelCase class names
- Imports: React → Third-party → @/ internal → types → styles

### Backend
- Check: quotes? indentation? line width?
- Imports: stdlib → third-party → local app
- Naming: PascalCase classes, snake_case functions

### Before Making Changes
- Read `.claude/CODE_STYLE.md`
- Confirm target format (indentation, quotes, etc.)
- Follow naming conventions detected
