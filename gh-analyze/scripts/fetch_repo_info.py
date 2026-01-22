#!/usr/bin/env python3
"""
GitHub Repository Info Fetcher
Fetches basic repository information from GitHub API without authentication.
Supports both direct API calls and gh CLI fallback.
"""

import json
import sys
import urllib.request
import urllib.error
import subprocess
from pathlib import Path


def parse_repo_identifier(input_str):
    """Parse various input formats to extract owner/repo."""
    input_str = input_str.strip()

    # Remove trailing slash if present
    input_str = input_str.rstrip('/')

    # Handle github.com URLs
    if 'github.com/' in input_str:
        parts = input_str.split('github.com/')[1].split('/')
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"

    # Handle owner/repo format
    if '/' in input_str and not input_str.startswith('http'):
        parts = input_str.split('/')
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1]}"

    return None


def fetch_via_github_api(repo):
    """Fetch repository info using GitHub API (no auth required for public repos)."""
    api_url = f"https://api.github.com/repos/{repo}"

    try:
        with urllib.request.urlopen(api_url, timeout=10) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Repository '{repo}' not found or private.", file=sys.stderr)
        else:
            print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error fetching from API: {e}", file=sys.stderr)
        return None


def fetch_via_gh_cli(repo):
    """Fetch repository info using gh CLI."""
    try:
        result = subprocess.run(
            ['gh', 'repo', 'view', repo, '--json'],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            # Parse available fields from gh
            fields = "name,description,primaryLanguage,stargazerCount,forksCount,watchersCount,createdAt,updatedAt,licenseInfo,defaultBranchRef,url,homepageUrl,owner"
            result = subprocess.run(
                ['gh', 'repo', 'view', repo, '--json', fields],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"gh CLI not available or timeout: {e}", file=sys.stderr)

    return None


def get_languages(repo):
    """Fetch language breakdown for the repository."""
    api_url = f"https://api.github.com/repos/{repo}/languages"

    try:
        with urllib.request.urlopen(api_url, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching languages: {e}", file=sys.stderr)
        return None


def get_contributors(repo, max_count=10):
    """Fetch top contributors for the repository."""
    api_url = f"https://api.github.com/repos/{repo}/contributors?per_page={max_count}"

    try:
        with urllib.request.urlopen(api_url, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching contributors: {e}", file=sys.stderr)
        return None


def format_repo_info(info, languages=None, contributors=None):
    """Format repository info for display."""
    if not info:
        return None

    output = {
        "name": info.get("name"),
        "full_name": info.get("full_name"),
        "description": info.get("description"),
        "html_url": info.get("html_url"),
        "homepage": info.get("homepage"),
        "language": info.get("language"),
        "languages": languages,
        "stars": info.get("stargazers_count"),
        "forks": info.get("forks_count"),
        "watchers": info.get("watchers_count"),
        "open_issues": info.get("open_issues_count"),
        "license": info.get("license", {}).get("name") if info.get("license") else None,
        "created_at": info.get("created_at"),
        "updated_at": info.get("updated_at"),
        "pushed_at": info.get("pushed_at"),
        "size_kb": info.get("size"),
        "default_branch": info.get("default_branch"),
        "is_archived": info.get("archived", False),
        "is_fork": info.get("fork", False),
        "contributors": contributors
    }

    return output


def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_repo_info.py <repo-url-or-identifier>", file=sys.stderr)
        print("Examples:", file=sys.stderr)
        print("  python fetch_repo_info.py https://github.com/torvalds/linux", file=sys.stderr)
        print("  python fetch_repo_info.py torvalds/linux", file=sys.stderr)
        sys.exit(1)

    repo_input = sys.argv[1]
    repo = parse_repo_identifier(repo_input)

    if not repo:
        print(f"Error: Could not parse repository identifier from '{repo_input}'", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching info for {repo}...", file=sys.stderr)

    # Try gh CLI first (often more reliable for authenticated users), then API
    info = fetch_via_github_api(repo)

    if not info:
        info = fetch_via_gh_cli(repo)

    if not info:
        print("Failed to fetch repository information.", file=sys.stderr)
        sys.exit(1)

    # Fetch additional info
    languages = get_languages(repo)
    contributors = get_contributors(repo)

    # Format and output
    result = format_repo_info(info, languages, contributors)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
