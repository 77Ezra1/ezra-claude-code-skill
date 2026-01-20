#!/usr/bin/env python3
"""
Smart Frontend Scanner
Intelligently detect project type and run appropriate tests.
"""

import subprocess
import json
import sys
import os
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
            timeout=300
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def detect_project_info(project_path):
    """Comprehensive project detection."""
    project_path = Path(project_path)
    info = {
        "framework": "vanilla",
        "has_typescript": False,
        "has_eslint": False,
        "has_build_script": False,
        "has_dev_script": False,
        "has_tests": False,
        "build_tool": None,
        "port": 3000
    }

    # Read package.json
    pkg_file = project_path / "package.json"
    if pkg_file.exists():
        with open(pkg_file) as f:
            pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

            # Detect framework
            if "next" in deps:
                info["framework"] = "next"
                info["port"] = 3000
            elif "nuxt" in deps:
                info["framework"] = "nuxt"
                info["port"] = 3000
            elif "react" in deps or "react-dom" in deps:
                info["framework"] = "react"
                info["port"] = 5173 if "vite" in deps else 3000
            elif "vue" in deps:
                info["framework"] = "vue"
                info["port"] = 5173 if "vite" in deps else 8080
            elif "angular" in deps:
                info["framework"] = "angular"
                info["port"] = 4200
            elif "svelte" in deps:
                info["framework"] = "svelte"
                info["port"] = 5173

            # Detect tools
            info["has_typescript"] = "typescript" in deps
            info["has_eslint"] = "eslint" in deps
            info["has_tests"] = any(
                "jest" in d or "vitest" in d or "cypress" in d or "playwright" in d
                for d in deps.keys()
            )

            # Detect build tool
            if "vite" in deps:
                info["build_tool"] = "vite"
            elif "webpack" in deps:
                info["build_tool"] = "webpack"
            elif "next" in deps:
                info["build_tool"] = "next"
            elif "nuxt" in deps:
                info["build_tool"] = "nuxt"

            # Check scripts
            scripts = pkg.get("scripts", {})
            info["has_build_script"] = "build" in scripts
            info["has_dev_script"] = "dev" in scripts or "start" in scripts

    return info


def check_server_running(url, timeout=5):
    """Check if a server is running at the URL."""
    try:
        import urllib.request
        import urllib.error

        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.status == 200
    except:
        return False


def start_dev_server(project_path, port):
    """Start development server in background."""
    pkg_file = Path(project_path) / "package.json"

    if not pkg_file.exists():
        return None, "No package.json found"

    with open(pkg_file) as f:
        pkg = json.load(f)
        scripts = pkg.get("scripts", {})

    # Find dev command
    dev_cmd = None
    if "dev" in scripts:
        dev_cmd = "npm run dev"
    elif "start" in scripts:
        dev_cmd = "npm start"
    else:
        return None, "No dev or start script found"

    # Check if port is specified
    url = f"http://localhost:{port}"

    if check_server_running(url):
        print(f"Server already running at {url}")
        return url, None

    print(f"Starting dev server on port {port}...")
    print(f"Please run: {dev_cmd}")
    print(f"Then tests will connect to {url}")
    return url, "manual_start_required"


def run_tests(project_path, url=None):
    """Run all available tests."""
    info = detect_project_info(project_path)

    print("\n" + "=" * 60)
    print("SMART FRONTEND SCANNER")
    print("=" * 60)
    print(f"\nProject: {project_path}")
    print(f"Framework: {info['framework']}")
    print(f"Build Tool: {info.get('build_tool', 'Unknown')}")
    print(f"TypeScript: {info['has_typescript']}")
    print(f"ESLint: {info['has_eslint']}")

    # Determine URL
    if not url:
        url = f"http://localhost:{info['port']}"

    print(f"\nTarget URL: {url}")

    # Check if server is running
    if not check_server_running(url):
        print(f"\n[WARNING] Server not detected at {url}")
        print(f"Please start your dev server first:")
        if info["has_dev_script"]:
            print("  npm run dev")
        else:
            print("  [No dev script found]")
        print(f"\nWill run code quality checks only...\n")
        url = None

    results = {}

    # Run code quality (always available)
    print("\n" + "-" * 40)
    print("Running Code Quality Scan...")
    print("-" * 40)
    rc, stdout, stderr = run_command(
        f'python "{Path(__file__).parent / "code_quality.py"}" "{project_path}"'
    )
    results["code_quality"] = {"exit_code": rc, "output": stdout}

    if url:
        # Run Lighthouse
        print("\n" + "-" * 40)
        print("Running Lighthouse Analysis...")
        print("-" * 40)
        rc, stdout, stderr = run_command(
            f'python "{Path(__file__).parent / "lighthouse_scan.py"}" "{url}"'
        )
        results["lighthouse"] = {"exit_code": rc, "output": stdout}

        # Run E2E tests
        print("\n" + "-" * 40)
        print("Running E2E Tests...")
        print("-" * 40)
        rc, stdout, stderr = run_command(
            f'python "{Path(__file__).parent / "e2e_test.py"}" "{url}"'
        )
        results["e2e"] = {"exit_code": rc, "output": stdout}

    # Summary
    print("\n" + "=" * 60)
    print("SCAN SUMMARY")
    print("=" * 60)

    for test_name, result in results.items():
        status = "PASS" if result["exit_code"] == 0 else "DONE"
        print(f"  [{status}] {test_name.replace('_', ' ').title()}")

    print("\n" + "=" * 60)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python smart_scan.py <project_path> [url]")
        print("\nExamples:")
        print("  python smart_scan.py ./my-app")
        print("  python smart_scan.py ./my-app http://localhost:5173")
        sys.exit(1)

    project_path = sys.argv[1]
    url = sys.argv[2] if len(sys.argv) > 2 else None

    run_tests(project_path, url)


if __name__ == "__main__":
    main()
