#!/usr/bin/env python3
"""
Project Code Style Analyzer

Scans project to detect and document code style conventions.
Generates .claude/CODE_STYLE.md with detected patterns.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any] | None:
    """Safely read JSON file."""
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return None


def read_text(path: Path) -> str | None:
    """Safely read text file."""
    try:
        if path.exists():
            return path.read_text(encoding="utf-8")
    except Exception:
        pass
    return None


def detect_frontend_style(project_root: Path) -> dict[str, Any]:
    """Detect frontend code style from configs and code."""
    frontend = project_root / "frontend"
    if not frontend.exists():
        return {}

    style = {
        "config": {},
        "naming": {},
        "patterns": {}
    }

    # Prettier config
    prettier = frontend / ".prettierrc"
    prettier_json = frontend / "prettier.config.json"
    for config_path in [prettier, prettier_json]:
        data = read_json(config_path)
        if data:
            style["config"].update({
                "prettier": data
            })
            break

    # ESLint config
    eslint = frontend / ".eslintrc.json"
    eslint_pkg = frontend / ".eslintrc"
    for config_path in [eslint, eslint_pkg]:
        if config_path.exists():
            data = read_json(config_path) or read_text(config_path)
            if data:
                style["config"]["eslint"] = data if isinstance(data, dict) else {"file": str(config_path)}
                break

    # TypeScript config
    tsconfig = frontend / "tsconfig.json"
    data = read_json(tsconfig)
    if data:
        style["config"]["typescript"] = {
            "target": data.get("compilerOptions", {}).get("target"),
            "strict": data.get("compilerOptions", {}).get("strict", False),
            "jsx": data.get("compilerOptions", {}).get("jsx"),
            "pathAlias": data.get("compilerOptions", {}).get("paths", {})
        }

    # Package.json for scripts and deps
    pkg = frontend / "package.json"
    data = read_json(pkg)
    if data:
        style["framework"] = {
            "name": data.get("name"),
            "deps": list(data.get("dependencies", {}).keys())[:20],  # First 20
            "devDeps": list(data.get("devDependencies", {}).keys())[:20]
        }

    # Analyze actual code patterns
    src = frontend / "src"
    if src.exists():
        # Sample TSX/TS files to detect patterns
        tsx_files = list(src.rglob("*.tsx"))[:5]
        ts_files = list(src.rglob("*.ts"))[:5]

        all_files = tsx_files + ts_files
        if all_files:
            style["patterns"] = detect_ts_patterns(all_files)

        # Check for CSS Modules usage
        scss_modules = list(src.rglob("*.module.scss"))
        if scss_modules:
            style["styling"] = {
                "method": "CSS Modules (.module.scss)",
                "preprocessor": "SCSS"
            }

    return style


def detect_ts_patterns(files: list[Path]) -> dict[str, Any]:
    """Detect TypeScript/React code patterns."""
    patterns = {
        "imports": [],
        "component_exports": [],
        "class_names": []
    }

    for file in files:
        content = read_text(file)
        if not content:
            continue

        # Detect export patterns
        if "export default function" in content:
            patterns["component_exports"].append("default export")
        if "export function" in content:
            patterns["component_exports"].append("named export")

        # Detect class names in SCSS imports
        scss_imports = re.findall(r'import\s+\w+\s+from\s+["\'](.+\.module\.scss)["\']', content)
        if scss_imports:
            patterns["has_css_modules"] = True

        # Detect import order (simplified)
        import_lines = re.findall(r'^import\s+.+', content, re.MULTILINE)
        if import_lines:
            if any("react" in imp.lower() for imp in import_lines[:3]):
                patterns["imports"].append("React imports first")

    # Get most common patterns
    patterns["component_exports"] = list(set(patterns["component_exports"]))

    return patterns


def detect_backend_style(project_root: Path) -> dict[str, Any]:
    """Detect backend code style from configs and code."""
    backend = project_root / "backend"
    if not backend.exists():
        return {}

    style = {
        "config": {},
        "patterns": {}
    }

    # pyproject.toml for Ruff/MyPy
    pyproject = backend / "pyproject.toml"
    if pyproject.exists():
        content = read_text(pyproject)
        if content:
            # Parse basic Ruff config
            line_length = None
            quote_style = None
            for line in content.split("\n"):
                if "line-length" in line:
                    match = re.search(r'line-length\s*=\s*(\d+)', line)
                    if match:
                        line_length = match.group(1)
                if "quote-style" in line:
                    match = re.search(r'quote-style\s*=\s*"(\w+)"', line)
                    if match:
                        quote_style = match.group(1)

            style["config"]["ruff"] = {
                "line_length": line_length,
                "quote_style": quote_style
            }

    # Sample Python files to detect patterns
    src = backend / "app"
    if src.exists():
        py_files = list(src.rglob("*.py"))[:5]
        if py_files:
            style["patterns"] = detect_python_patterns(py_files)

    return style


def detect_python_patterns(files: list[Path]) -> dict[str, Any]:
    """Detect Python code patterns."""
    patterns = {
        "imports": [],
        "docstring_style": [],
        "type_annotations": []
    }

    for file in files:
        content = read_text(file)
        if not content:
            continue

        # Check for type hints
        if ": " in content and " -> " in content:
            patterns["type_annotations"].append("modern")

        # Check for Annotated usage
        if "from typing import Annotated" in content or "Annotated[" in content:
            patterns["uses_annotated"] = True

        # Check docstring style
        triple_quotes = re.findall(r'"""([^"]+)"""', content, re.DOTALL)
        if triple_quotes:
            patterns["docstring_style"].append("triple-double")

    return patterns


def generate_style_md(project_root: Path, frontend_style: dict, backend_style: dict) -> str:
    """Generate markdown style guide."""
    lines = [
        "# Project Code Style",
        "",
        "> Auto-generated by analyze-project-style skill. Update manually as needed.",
        "",
        "---",
        ""
    ]

    # Frontend section
    if frontend_style:
        lines.extend([
            "## Frontend (frontend/)",
            ""
        ])

        config = frontend_style.get("config", {})

        # Prettier
        if "prettier" in config:
            p = config["prettier"]
            lines.extend([
                "### Format (Prettier)",
                "",
                f"- **Semicolons**: {'Yes' if p.get('semi') else 'No'}",
                f"- **Quotes**: `{p.get('singleQuote') and 'single' or 'double'}` quotes",
                f"- **Indent**: `{p.get('tabWidth', 2)}` spaces",
                f"- **Line width**: `{p.get('printWidth', 80)}` characters",
                ""
            ])

        # TypeScript
        if "typescript" in config:
            ts = config["typescript"]
            lines.extend([
                "### TypeScript",
                "",
                f"- **Target**: {ts.get('target', 'ES2020')}",
                f"- **Strict mode**: {ts.get('strict', False)}",
                f"- **JSX**: {ts.get('jsx', 'react-jsx')}",
                ""
            ])
            if ts.get("pathAlias"):
                lines.append("**Path aliases**:")
                for alias, paths in ts["pathAlias"].items():
                    lines.append(f"- `{alias}` → {paths}")
                lines.append("")

        # Styling
        if "styling" in frontend_style:
            s = frontend_style["styling"]
            lines.extend([
                "### Styling",
                "",
                f"- **Method**: {s.get('method', 'Unknown')}",
                f"- **Preprocessor**: {s.get('preprocessor', 'None')}",
                ""
            ])

        # Patterns
        patterns = frontend_style.get("patterns", {})
        if patterns:
            lines.extend([
                "### Code Patterns",
                ""
            ])
            if patterns.get("component_exports"):
                exports = patterns["component_exports"]
                lines.append(f"- **Components**: {' and '.join(exports)}")
            if patterns.get("has_css_modules"):
                lines.append("- **Uses**: CSS Modules")
            lines.append("")

    # Backend section
    if backend_style:
        lines.extend([
            "---",
            "",
            "## Backend (backend/)",
            ""
        ])

        config = backend_style.get("config", {})

        # Ruff
        if "ruff" in config:
            r = config["ruff"]
            lines.extend([
                "### Format (Ruff)",
                "",
                f"- **Line width**: {r.get('line_width', '100')} characters",
                f"- **Quotes**: `{r.get('quote_style', 'double')}` quotes",
                ""
            ])

        # Patterns
        patterns = backend_style.get("patterns", {})
        if patterns:
            lines.extend([
                "### Code Patterns",
                ""
            ])
            if patterns.get("uses_annotated"):
                lines.append("- **Type annotations**: Uses `Annotated` for dependencies")
            if patterns.get("docstring_style"):
                lines.append("- **Docstrings**: Triple double quotes `\"\"\"`")
            lines.append("")

    # Naming conventions (common patterns)
    lines.extend([
        "---",
        "",
        "## Naming Conventions",
        "",
        "| Language | Components | Functions | Variables | Constants |",
        "|----------|------------|-----------|-----------|-----------|",
        "| TypeScript | PascalCase | camelCase | camelCase | UPPER_SNAKE_CASE |",
        "| Python | PascalCase | snake_case | snake_case | UPPER_SNAKE_CASE |",
        "| SCSS | camelCase | - | - | kebab-case (CSS vars) |",
        ""
    ])

    # Import order
    lines.extend([
        "## Import Order",
        "",
        "### TypeScript",
        "```typescript",
        "// 1. React imports",
        "// 2. Third-party libraries",
        "// 3. Internal imports (@/ alias)",
        "// 4. Type imports",
        "// 5. Styles",
        "```",
        "",
        "### Python",
        "```python",
        "# 1. Standard library",
        "# 2. Third-party imports",
        "# 3. Local app imports (app.*)",
        "```",
        ""
    ])

    lines.extend([
        "---",
        "",
        "*Generated by analyze-project-style skill*"
    ])

    return "\n".join(lines)


def main():
    """Main entry point."""
    # Find project root (where script is called from or current dir)
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1])
    else:
        project_root = Path.cwd()

    print(f"Analyzing project style in: {project_root}")

    # Detect styles
    frontend_style = detect_frontend_style(project_root)
    backend_style = detect_backend_style(project_root)

    if not frontend_style and not backend_style:
        print("No frontend or backend directories found.")
        sys.exit(1)

    # Generate output
    output_dir = project_root / ".claude"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "CODE_STYLE.md"

    content = generate_style_md(project_root, frontend_style, backend_style)
    output_file.write_text(content, encoding="utf-8")

    print(f"Generated: {output_file}")
    print(f"  - Frontend config: {'Yes' if frontend_style else 'N/A'}")
    print(f"  - Backend config: {'Yes' if backend_style else 'N/A'}")


if __name__ == "__main__":
    main()
