#!/usr/bin/env python3
"""
Code Quality Scanner
Run ESLint, TypeScript checks, and analyze code quality metrics.
"""

import subprocess
import json
import sys
import re
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def detect_project_config(project_path):
    """Detect project configuration and tools."""
    project_path = Path(project_path)
    config = {
        "has_eslint": False,
        "has_prettier": False,
        "has_typescript": False,
        "has_vitest": False,
        "has_jest": False,
        "package_manager": None,
        "framework": None
    }

    # Check package.json
    pkg_file = project_path / "package.json"
    if pkg_file.exists():
        with open(pkg_file) as f:
            pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

            config["has_eslint"] = any(
                "eslint" in d for d in deps.keys()
            )
            config["has_prettier"] = any(
                "prettier" in d for d in deps.keys()
            )
            config["has_typescript"] = any(
                "typescript" in d for d in deps.keys()
            )
            config["has_vitest"] = any(
                "vitest" in d or "@vitest" in d for d in deps.keys()
            )
            config["has_jest"] = any(
                "jest" in d for d in deps.keys()
            )

            # Detect framework
            if "react" in deps or "react-dom" in deps:
                config["framework"] = "react"
            elif "vue" in deps:
                config["framework"] = "vue"
            elif "next" in deps:
                config["framework"] = "next"
            elif "nuxt" in deps:
                config["framework"] = "nuxt"
            elif "angular" in deps:
                config["framework"] = "angular"
            elif "svelte" in deps:
                config["framework"] = "svelte"

    # Check for config files
    config_files = list(project_path.glob("*eslintrc*")) + list(project_path.glob(".eslint*"))
    config["has_eslint"] = config["has_eslint"] or len(config_files) > 0

    tsconfig_files = list(project_path.glob("tsconfig*.json"))
    config["has_typescript"] = config["has_typescript"] or len(tsconfig_files) > 0

    # Detect package manager
    if (project_path / "pnpm-lock.yaml").exists():
        config["package_manager"] = "pnpm"
    elif (project_path / "yarn.lock").exists():
        config["package_manager"] = "yarn"
    elif (project_path / "package-lock.json").exists():
        config["package_manager"] = "npm"

    return config


def run_eslint(project_path):
    """Run ESLint and parse results."""
    config = detect_project_config(project_path)

    if not config["has_eslint"]:
        return {"status": "not_configured", "errors": 0, "warnings": 0}

    # Try to run ESLint
    cmd = "npx eslint . --format json --ext .js,.jsx,.ts,.tsx,.vue"

    rc, stdout, stderr = run_command(cmd, cwd=project_path)

    if rc == -1:
        return {"status": "error", "message": stderr}

    # Parse ESLint JSON output
    try:
        results = json.loads(stdout)
        total_errors = 0
        total_warnings = 0
        files_with_issues = []

        for file_result in results:
            file_errors = sum(1 for m in file_result.get("messages", []) if m.get("severity") == 2)
            file_warnings = sum(1 for m in file_result.get("messages", []) if m.get("severity") == 1)

            if file_errors + file_warnings > 0:
                files_with_issues.append({
                    "path": file_result.get("filePath", "unknown"),
                    "errors": file_errors,
                    "warnings": file_warnings,
                    "messages": file_result.get("messages", [])[:5]  # First 5 messages
                })

            total_errors += file_errors
            total_warnings += file_warnings

        return {
            "status": "success",
            "errors": total_errors,
            "warnings": total_warnings,
            "files": files_with_issues
        }
    except json.JSONDecodeError:
        # ESLint might have returned text output
        return {"status": "parse_error", "output": stdout[:500]}


def run_typescript_check(project_path):
    """Run TypeScript compiler check."""
    config = detect_project_config(project_path)

    if not config["has_typescript"]:
        return {"status": "not_typescript"}

    # Run tsc --noEmit
    cmd = "npx tsc --noEmit"

    rc, stdout, stderr = run_command(cmd, cwd=project_path)

    errors = []
    if stderr:
        # Parse TypeScript errors
        lines = stderr.split("\n")
        for line in lines:
            if ".ts" in line or ".tsx" in line:
                errors.append(line.strip())

    return {
        "status": "success" if rc == 0 else "errors",
        "error_count": len(errors),
        "errors": errors[:10]  # First 10 errors
    }


def analyze_bundle_size(project_path):
    """Analyze bundle size from build output."""
    dist_path = Path(project_path) / "dist"
    build_path = Path(project_path) / "build"
    out_path = Path(project_path) / ".next"  # Next.js

    output_dirs = [d for d in [dist_path, build_path, out_path] if d.exists()]

    if not output_dirs:
        return {"status": "no_build"}

    results = {"dirs": [], "total_size": 0}

    for output_dir in output_dirs:
        size = 0
        file_count = 0

        for file_path in output_dir.rglob("*"):
            if file_path.is_file():
                size += file_path.stat().st_size
                file_count += 1

        results["dirs"].append({
            "path": str(output_dir.name),
            "size_mb": round(size / (1024 * 1024), 2),
            "file_count": file_count
        })
        results["total_size"] += size

    results["total_size_mb"] = round(results["total_size"] / (1024 * 1024), 2)

    return results


def check_code_health(project_path):
    """Check general code health indicators."""
    project_path = Path(project_path)

    checks = {
        "has_gitignore": (project_path / ".gitignore").exists(),
        "has_env_file": len(list(project_path.glob(".env*"))) > 0,
        "has_readme": (project_path / "README.md").exists(),
        "has_tests_folder": (project_path / "tests").exists() or (project_path / "__tests__").exists(),
        "has_ci_config": (
            (project_path / ".github").exists() or
            (project_path / ".gitlab-ci.yml").exists() or
            (project_path / "Jenkinsfile").exists()
        )
    }

    return checks


def print_quality_report(project_path):
    """Print comprehensive code quality report."""
    print("\n" + "=" * 60)
    print("CODE QUALITY REPORT")
    print("=" * 60)

    config = detect_project_config(project_path)
    print(f"\n[PROJECT CONFIG]")
    print(f"  Framework: {config.get('framework', 'Unknown')}")
    print(f"  TypeScript: {'Yes' if config['has_typescript'] else 'No'}")
    print(f"  ESLint: {'Yes' if config['has_eslint'] else 'No'}")
    print(f"  Prettier: {'Yes' if config['has_prettier'] else 'No'}")
    print(f"  Package Manager: {config.get('package_manager', 'Unknown')}")

    # ESLint Results
    print("\n[ESLINT]")
    eslint_result = run_eslint(project_path)
    if eslint_result["status"] == "success":
        print(f"  Errors: {eslint_result['errors']}")
        print(f"  Warnings: {eslint_result['warnings']}")
        if eslint_result["files"]:
            print(f"  Files with issues: {len(eslint_result['files'])}")
            for f in eslint_result["files"][:3]:
                print(f"    - {Path(f['path']).name}: {f['errors']}E, {f['warnings']}W")
    elif eslint_result["status"] == "not_configured":
        print("  Not configured")
    else:
        print(f"  Status: {eslint_result['status']}")

    # TypeScript Results
    print("\n[TYPESCRIPT]")
    if config["has_typescript"]:
        ts_result = run_typescript_check(project_path)
        if ts_result["status"] == "success":
            print("  No type errors")
        else:
            print(f"  Errors: {ts_result['error_count']}")
            for err in ts_result["errors"][:3]:
                print(f"    - {err[:80]}")
    else:
        print("  Not a TypeScript project")

    # Bundle Size
    print("\n[BUNDLE SIZE]")
    bundle_result = analyze_bundle_size(project_path)
    if bundle_result["status"] != "no_build":
        print(f"  Total: {bundle_result['total_size_mb']} MB")
        for d in bundle_result["dirs"]:
            print(f"  - {d['path']}: {d['size_mb']} MB ({d['file_count']} files)")
    else:
        print("  No build output found")

    # Code Health
    print("\n[CODE HEALTH]")
    health = check_code_health(project_path)
    for check, passed in health.items():
        status = "OK" if passed else "MISSING"
        print(f"  [{status}] {check}")

    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python code_quality.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    print_quality_report(project_path)


if __name__ == "__main__":
    main()
