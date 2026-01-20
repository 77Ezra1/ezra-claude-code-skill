#!/usr/bin/env python3
"""
Lighthouse Automated Scanning
Run Lighthouse CI and generate comprehensive performance, accessibility, SEO reports.
"""

import subprocess
import json
import sys
from pathlib import Path


def run_lighthouse(url, output_path="lighthouse-report.json"):
    """Run Lighthouse analysis and save results."""
    cmd = f"npx lighthouse {url} --output json --output-path {output_path} --quiet"

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0 and Path(output_path).exists():
            with open(output_path) as f:
                return json.load(f)
        return None
    except subprocess.TimeoutExpired:
        print("Lighthouse scan timed out")
        return None
    except Exception as e:
        print(f"Error running Lighthouse: {e}")
        return None


def parse_lighthouse_results(data):
    """Parse Lighthouse results into readable format."""
    if not data:
        return None

    categories = data.get("categories", {})
    audits = data.get("audits", {})

    results = {
        "scores": {},
        "issues": {"critical": [], "warning": [], "info": []},
        "metrics": {}
    }

    # Extract category scores
    for cat_id, cat_data in categories.items():
        title = cat_data.get("title", cat_id)
        score = cat_data.get("score", 0)
        results["scores"][title] = int(score * 100) if score <= 1 else int(score)

    # Extract critical audits
    critical_audits = [
        "cumulative-layout-shift",
        "speed-index",
        "largest-contentful-paint",
        "first-contentful-paint",
        "interactive",
        "total-blocking-time",
        "lcp-lazy-loading",
        "render-blocking-resources",
        "unused-javascript",
        "unminified-css",
        "unminified-javascript",
        "modern-image-formats",
        "uses-responsive-images",
        "offscreen-images",
        "mainthread-work-breakdown",
        "bootup-time",
        "no-document-write",
        "cookies",
        "doctype",
        "no-vulnerable-libraries",
        "js-libraries",
        "uses-http2",
        "uses-text-compression",
        "uses-long-cache-ttl",
        "total-byte-weight",
        "uses-optimized-images",
        "efficient-animated-content",
        "minified-css",
        "minified-javascript",
        "unused-css-rules",
        "accessible-name",
        "aria-labels",
        "aria-allowed-attr",
        "aria-required-attr",
        "aria-required-children",
        "aria-roles",
        "aria-valid-attr-value",
        "aria-valid-attr",
        "button-name",
        "bypass",
        "color-contrast",
        "definition-list",
        "dlitem",
        "document-title",
        "duplicate-id-active",
        "duplicate-id-aria",
        "form-field-multiple-labels",
        "header-attribute",
        "html-has-lang",
        "html-lang-valid",
        "image-alt",
        "image-redundant-alt",
        "input-image-alt",
        "label",
        "link-name",
        "list",
        "listitem",
        "meta-viewport",
        "meta-viewport-large",
        "object-alt",
        "role-img-alt",
        "tabindex",
        "tap-targets",
        "td-headers-attr",
        "th-has-data-cells",
        "valid-lang",
        "video-caption",
        "video-description",
        "aria-hidden-focus",
        "focus-controls",
        "focus-tab-order",
        "focus-traps",
        "frame-title",
        "frame-title-unique",
        "heading-order",
        "hidden-content",
        "identical-links-same-purpose",
        "skip-link",
        "target-size",
        "parsing",
        "autocomplete-valid",
        "valid-aria-authored"
    ]

    for audit_id in critical_audits:
        if audit_id in audits:
            audit = audits[audit_id]
            score = audit.get("score")
            title = audit.get("title", audit_id)

            if score is None or score == 0:
                results["issues"]["critical"].append(title)
            elif score < 1:
                results["issues"]["warning"].append(title)

    # Extract key metrics
    metrics_audits = [
        "first-contentful-paint",
        "largest-contentful-paint",
        "total-blocking-time",
        "cumulative-layout-shift",
        "speed-index",
        "interactive",
        "total-byte-weight",
        "unminified-css",
        "unminified-javascript",
        "unused-css-rules",
        "unused-javascript"
    ]

    for metric_id in metrics_audits:
        if metric_id in audits:
            audit = audits[metric_id]
            display_value = audit.get("displayValue", "N/A")
            results["metrics"][metric_id] = display_value

    return results


def print_report(results):
    """Print formatted Lighthouse report."""
    if not results:
        print("No Lighthouse results available")
        return

    print("\n" + "=" * 60)
    print("LIGHTHOUSE REPORT")
    print("=" * 60)

    print("\n[SCORES]")
    for name, score in results["scores"].items():
        status = "PASS" if score >= 90 else "WARN" if score >= 50 else "FAIL"
        print(f"  [{status}] {name}: {score}")

    if results["metrics"]:
        print("\n[METRICS]")
        for name, value in results["metrics"].items():
            print(f"  - {name}: {value}")

    if results["issues"]["critical"]:
        print("\n[CRITICAL ISSUES]")
        for issue in results["issues"]["critical"][:10]:
            print(f"  - {issue}")

    if results["issues"]["warning"]:
        print(f"\n[WARNINGS] ({len(results['issues']['warning'])} items)")
        for issue in results["issues"]["warning"][:5]:
            print(f"  - {issue}")

    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python lighthouse_scan.py <url> [output_path]")
        sys.exit(1)

    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "lighthouse-report.json"

    print(f"Running Lighthouse scan on: {url}")

    data = run_lighthouse(url, output_path)
    results = parse_lighthouse_results(data)
    print_report(results)


if __name__ == "__main__":
    main()
