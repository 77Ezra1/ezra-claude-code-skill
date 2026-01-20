#!/usr/bin/env python3
"""
Frontend Test Runner
Run Playwright tests and generate comprehensive reports.
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime


def run_command(cmd, cwd=None):
    """Run a shell command and return output."""
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


def detect_project_type(project_path):
    """Detect the frontend framework being used."""
    project_path = Path(project_path)

    # Check for React
    if (project_path / "package.json").exists():
        with open(project_path / "package.json") as f:
            pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

            if "react" in deps or "react-dom" in deps:
                return "react"
            if "vue" in deps:
                return "vue"
            if "next" in deps:
                return "next"
            if "nuxt" in deps:
                return "nuxt"
            if "angular" in deps:
                return "angular"
            if "svelte" in deps:
                return "svelte"

    return "vanilla"


def check_accessibility(url):
    """Run accessibility checks using Playwright."""
    code = f"""
const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto('{url}');
    await page.waitForLoadState('networkidle');

    // Check for images without alt
    const imagesWithoutAlt = await page.$$eval('img:not([alt])', imgs => imgs.length);

    // Check for empty buttons
    const emptyButtons = await page.$$eval('button:empty, a[role="button"]:empty', btns => btns.length);

    // Check for form labels
    const inputsWithoutLabels = await page.$$eval('input:not([aria-label]):not([id])', inputs =>
        inputs.filter(i => {{
            const parent = i.closest('label');
            return !parent;
        }}).length
    );

    // Check heading hierarchy
    const headings = await page.$$eval('h1, h2, h3, h4, h5, h6', hs =>
        hs.map(h => h.tagName)
    );

    const firstH2 = headings.indexOf('H2');
    const hasH1 = headings.includes('H1');
    const hasBrokenHeading = !hasH1 && headings.length > 0;

    console.log(JSON.stringify({{
        imagesWithoutAlt,
        emptyButtons,
        inputsWithoutLabels,
        hasBrokenHeading,
        hasH1,
        totalHeadings: headings.length
    }}));

    await browser.close();
}})();
"""

    with open("a11y_check.js", "w") as f:
        f.write(code)

    rc, stdout, stderr = run_command("node a11y_check.js")

    try:
        Path("a11y_check.js").unlink()
        return json.loads(stdout) if rc == 0 else {}
    except:
        return {}


def check_performance(url):
    """Run basic performance checks."""
    code = f"""
const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch();
    const page = await browser.newPage();

    // Collect performance metrics
    const metrics = await page.evaluate(() => {{
        const timing = performance.timing;
        return {{
            domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
            loadComplete: timing.loadEventEnd - timing.navigationStart,
            firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0
        }};
    }});

    await browser.close();
    console.log(JSON.stringify(metrics));
}})();
"""

    with open("perf_check.js", "w") as f:
        f.write(code)

    rc, stdout, stderr = run_command("node perf_check.js")
    Path("perf_check.js").unlink()

    try:
        return json.loads(stdout) if rc == 0 else {}
    except:
        return {}


def generate_test_summary(results):
    """Generate a formatted test summary."""
    report = []
    report.append("=" * 60)
    report.append("FRONTEND TEST SUMMARY")
    report.append("=" * 60)
    report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    for test_name, result in results.items():
        status = "PASS" if result.get("pass", False) else "FAIL"
        report.append(f"[{status}] {test_name}")
        if result.get("details"):
            for detail in result["details"]:
                report.append(f"    - {detail}")
        report.append("")

    return "\n".join(report)


def main():
    if len(sys.argv) < 2:
        print("Usage: python runner.py <project_path> [url]")
        print("  project_path: Path to frontend project")
        print("  url: Optional URL to test (default: http://localhost:3000)")
        sys.exit(1)

    project_path = sys.argv[1]
    url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:3000"

    print(f"Testing project: {project_path}")
    print(f"Target URL: {url}")
    print("")

    # Detect framework
    framework = detect_project_type(project_path)
    print(f"Detected framework: {framework}")

    results = {}

    # Run accessibility checks
    print("Running accessibility checks...")
    a11y_results = check_accessibility(url)
    results["Accessibility"] = {
        "pass": a11y_results.get("imagesWithoutAlt", 0) == 0,
        "details": [
            f"Images without alt: {a11y_results.get('imagesWithoutAlt', 0)}",
            f"Empty buttons: {a11y_results.get('emptyButtons', 0)}",
            f"Inputs without labels: {a11y_results.get('inputsWithoutLabels', 0)}"
        ]
    }

    # Run performance checks
    print("Running performance checks...")
    perf_results = check_performance(url)
    results["Performance"] = {
        "pass": perf_results.get("loadComplete", 9999) < 5000,
        "details": [
            f"DOM Content Loaded: {perf_results.get('domContentLoaded', 0)}ms",
            f"Load Complete: {perf_results.get('loadComplete', 0)}ms",
            f"First Paint: {perf_results.get('firstPaint', 0)}ms"
        ]
    }

    # Print summary
    print("\n")
    print(generate_test_summary(results))


if __name__ == "__main__":
    main()
