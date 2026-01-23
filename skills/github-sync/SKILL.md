---
name: github-sync
description: Automatically commit and push changes to GitHub repository. Use this when users ask to sync changes to GitHub, push to repository, upload to GitHub, or commit and push code changes.
license: Apache-2.0
---

# GitHub Sync

Automatically stage, commit, and push changes to a GitHub repository. This skill handles the full git workflow: adding changed files, creating commits with meaningful messages, and pushing to the remote repository.

## Core Workflow

1. **Check git status** - Identify what has changed
2. **Stage changes** - Add modified/new files to git
3. **Create commit** - Generate a descriptive commit message
4. **Push to remote** - Upload changes to GitHub

## Commit Message Guidelines

Follow conventional commit format:
```
<type>: <description>

Types: add, update, fix, refactor, remove, docs
```

Examples:
- `Add new feature for user authentication`
- `Update web-scraper skill with async support`
- `Fix error handling in content parser`
- `Refactor database connection logic`

## Standard Procedure

### Full Sync (Commit + Push)

```bash
# Check what changed
git status

# Stage all changes
git add .

# Create commit with descriptive message
git commit -m "<commit message>"

# Push to remote
git push
```

### Selective Sync (Specific Files)

```bash
# Stage specific files
git add path/to/file1.py path/to/file2.py

# Commit
git commit -m "<commit message>"

# Push
git push
```

### Quick Check Before Sync

Always run these commands before pushing:

```bash
# Check current branch
git branch

# Check remote URL
git remote -v

# Check for uncommitted changes
git status

# Check recent commits
git log --oneline -5
```

## Handling Common Situations

### Untracked Files

```bash
# Add all untracked files
git add -A

# Or add specific patterns
git add *.py
git add skills/*/
```

### Merge Conflicts

```bash
# Pull first to check for conflicts
git pull

# If conflicts exist, resolve them manually
# Then mark as resolved
git add <resolved-files>
git commit
git push
```

### Large Files / Git LFS

```bash
# Check if git lfs is available
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.zip"
git add .gitattributes
```

## Pre-Push Checklist

Before pushing, always verify:

- [ ] Commit message is clear and descriptive
- [ ] No sensitive data (API keys, passwords) is included
- [ ] All related files are staged
- [ ] Code is tested (if applicable)
- [ ] Correct branch is selected

## Automation Scripts

### Python Script for Auto-Sync

```python
#!/usr/bin/env python3
"""
Auto-commit and push changes to GitHub.
Usage: python auto_sync.py "<commit message>"
"""

import subprocess
import sys
from datetime import datetime


def run_command(cmd, check=True):
    """Run shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        check=check
    )
    return result.stdout, result.stderr, result.returncode


def check_git_status():
    """Check if there are changes to commit."""
    stdout, _, _ = run_command("git status --porcelain")
    return bool(stdout.strip())


def get_current_branch():
    """Get current git branch name."""
    stdout, _, _ = run_command("git rev-parse --abbrev-ref HEAD")
    return stdout.strip()


def sync_to_github(message=None):
    """Stage, commit, and push changes."""

    # Check if there are changes
    if not check_git_status():
        print("No changes to commit.")
        return True

    # Get current branch
    branch = get_current_branch()
    print(f"Current branch: {branch}")

    # Stage all changes
    print("Staging changes...")
    run_command("git add .")

    # Generate commit message if not provided
    if not message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        message = f"Update changes - {timestamp}"

    # Commit
    print(f"Committing: {message}")
    stdout, stderr, code = run_command(f'git commit -m "{message}"', check=False)
    if code != 0 and "nothing to commit" in stdout:
        print("Nothing to commit.")
        return True
    elif code != 0:
        print(f"Commit failed: {stderr}")
        return False

    # Push
    print("Pushing to GitHub...")
    stdout, stderr, code = run_command("git push", check=False)
    if code != 0:
        print(f"Push failed: {stderr}")
        print("\nTrying with --set-upstream...")
        stdout, stderr, code = run_command(f"git push -u origin {branch}", check=False)
        if code != 0:
            print(f"Push failed again: {stderr}")
            return False

    print("Successfully pushed to GitHub!")
    return True


if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else None
    sync_to_github(msg)
```

### Node.js Script for Auto-Sync

```javascript
#!/usr/bin/env node
/**
 * Auto-commit and push changes to GitHub.
 * Usage: node auto_sync.js "<commit message>"
 */

const { execSync } = require('child_process');
const fs = require('fs');

function run(command, silent = false) {
    try {
        const output = execSync(command, { encoding: 'utf-8' });
        if (!silent) console.log(output.trim());
        return { success: true, output };
    } catch (error) {
        if (!silent) console.error(error.message);
        return { success: false, error: error.message };
    }
}

function hasChanges() {
    const result = run('git status --porcelain', true);
    return result.success && result.output.trim().length > 0;
}

function getCurrentBranch() {
    const result = run('git rev-parse --abbrev-ref HEAD', true);
    return result.success ? result.output.trim() : 'main';
}

function syncToGitHub(message) {
    // Check for changes
    if (!hasChanges()) {
        console.log('No changes to commit.');
        return;
    }

    const branch = getCurrentBranch();
    console.log(`Current branch: ${branch}`);

    // Stage changes
    console.log('Staging changes...');
    run('git add .');

    // Default commit message
    const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
    const commitMsg = message || `Update changes - ${timestamp}`;

    // Commit
    console.log(`Committing: ${commitMsg}`);
    const commitResult = run(`git commit -m "${commitMsg}"`, true);

    if (!commitResult.success && commitResult.error.includes('nothing to commit')) {
        console.log('Nothing to commit.');
        return;
    }

    // Push
    console.log('Pushing to GitHub...');
    let pushResult = run('git push', true);

    if (!pushResult.success) {
        console.log('Trying with --set-upstream...');
        pushResult = run(`git push -u origin ${branch}`, true);
    }

    if (pushResult.success) {
        console.log('Successfully pushed to GitHub!');
    } else {
        console.error('Push failed. Please check your remote configuration.');
    }
}

// Run
const message = process.argv[2];
syncToGitHub(message);
```

### Shell Script (Linux/Mac)

```bash
#!/bin/bash
# Auto-commit and push changes to GitHub
# Usage: ./auto_sync.sh "commit message"

COMMIT_MSG=${1:-"Update changes - $(date '+%Y-%m-%d %H:%M')"}

# Check for changes
if [ -z "$(git status --porcelain)" ]; then
    echo "No changes to commit."
    exit 0
fi

# Show current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $BRANCH"

# Stage all changes
echo "Staging changes..."
git add .

# Commit
echo "Committing: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

# Push
echo "Pushing to GitHub..."
git push || git push -u origin $BRANCH

echo "Successfully pushed to GitHub!"
```

### PowerShell Script (Windows)

```powershell
# Auto-commit and push changes to GitHub
# Usage: .\auto_sync.ps1 "commit message"

param(
    [string]$Message = "Update changes - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
)

# Check for changes
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "No changes to commit." -ForegroundColor Yellow
    exit 0
}

# Show current branch
$branch = git rev-parse --abbrev-ref HEAD
Write-Host "Current branch: $branch" -ForegroundColor Cyan

# Stage all changes
Write-Host "Staging changes..." -ForegroundColor Cyan
git add .

# Commit
Write-Host "Committing: $Message" -ForegroundColor Cyan
git commit -m $Message

# Push
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
$pushResult = git push 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Trying with --set-upstream..." -ForegroundColor Yellow
    git push -u origin $branch
}

Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
```

## Workflow Integration

### After Skill Updates

When you update or create skills, follow this pattern:

```bash
cd path/to/skills/repository
git status
git add skills/<skill-name>/
git commit -m "Add/update <skill-name> skill"
git push
```

### Batch Multiple Skills

```bash
# Add multiple skill updates
git add skills/web-scraper/ skills/github-sync/

# Single commit for all changes
git commit -m "Add web-scraper and github-sync skills"

# Push once
git push
```

## Troubleshooting

### Authentication Issues

```bash
# Check current remote URL
git remote -v

# If using HTTPS, use GitHub CLI
gh auth login

# Or switch to SSH
git remote set-url origin git@github.com:username/repo.git
```

### Push Rejected

```bash
# Pull remote changes first
git pull --rebase

# Resolve conflicts if any
# Then push
git push
```

### Branch Protection

If branch is protected:

```bash
# Create a feature branch
git checkout -b feature/update

# Commit and push to feature branch
git add .
git commit -m "Feature update"
git push -u origin feature/update

# Create pull request via GitHub web or CLI
gh pr create --title "Feature update" --body "Description of changes"
```

## GitHub CLI Integration

For even better automation, use GitHub CLI:

```bash
# Install gh CLI
# https://cli.github.com/

# Login
gh auth login

# Quick sync with PR
git add .
git commit -m "Update skills"
git push
gh pr create --fill
```

## Examples

### Example 1: Quick Sync After Editing

```bash
# You just edited a skill file
git status
git add skills/web-scraper/SKILL.md
git commit -m "Update web-scraper skill with new templates"
git push
```

### Example 2: Sync All Changes

```bash
# Multiple skills updated
git add -A
git commit -m "Add web-scraper and github-sync skills with Python and Node.js support"
git push
```

### Example 3: Using Python Script

```bash
# Save as auto_sync.py
python auto_sync.py "Add new web scraping templates"
```

## Best Practices

1. **Clear commit messages** - Describe what changed and why
2. **Atomic commits** - One logical change per commit
3. **Test before push** - Ensure changes work correctly
4. **Pull before push** - Avoid unnecessary merge conflicts
5. **Use branches** - For experimental changes
6. **Review git status** - Always check what's being committed

## Quick Reference

```bash
# Full workflow
git status && git add . && git commit -m "message" && git push

# Staged changes only
git diff --staged

# Amend last commit (if not pushed)
git commit --amend

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View commit history
git log --oneline -10
```

## Auto-Sync After Every Commit (Git Hook)

### Setup Auto-Push Hook

To automatically push to GitHub after every commit, set up a `post-commit` hook:

```bash
# Create the post-commit hook
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Auto-push after every commit
echo "Auto-pushing to GitHub..."
git push
EOF

# Make it executable
chmod +x .git/hooks/post-commit
```

After setting this up, every time you run `git commit`, the changes will automatically be pushed to GitHub.

### PowerShell Hook (Windows)

```powershell
# Create post-commit hook for Windows
$hookContent = @'
#!/bin/bash
# Auto-push after every commit
echo "Auto-pushing to GitHub..."
git push
'@

$hookPath = ".git/hooks/post-commit"
Set-Content -Path $hookPath -Value $hookContent -NoNewline
```

### Disable Auto-Push Hook

If you need to disable auto-push temporarily:

```bash
# Remove the hook
rm .git/hooks/post-commit

# Or rename it to disable
mv .git/hooks/post-commit .git/hooks/post-commit.disabled
```

### Enhanced Auto-Push Hook with Error Handling

```bash
cat > .git/hooks/post-commit << 'EOF'
#!/bin/bash
# Auto-push with error handling and notifications

echo "🔄 Auto-pushing to GitHub..."

# Attempt to push
if git push; then
    echo "✅ Successfully pushed to GitHub"
else
    echo "⚠️ Push failed. Trying with upstream..."
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    git push -u origin $BRANCH && echo "✅ Successfully pushed with upstream" || echo "❌ Push failed. Please push manually."
fi
EOF

chmod +x .git/hooks/post-commit
```

### One-Command Setup Script

```bash
# Run this to set up auto-push for any git repository
setup_auto_push() {
    cat > .git/hooks/post-commit << 'HOOK'
#!/bin/bash
echo "Auto-pushing to GitHub..."
git push 2>/dev/null || {
    BRANCH=$(git rev-parse --abbrev-ref HEAD)
    git push -u origin "$BRANCH" 2>/dev/null || echo "Push failed. Please check your connection."
}
HOOK
    chmod +x .git/hooks/post-commit
    echo "✅ Auto-push hook installed! Every commit will now be pushed automatically."
}

# Run the function
setup_auto_push
```

### Verify Hook is Installed

```bash
# Check if post-commit hook exists
ls -la .git/hooks/post-commit

# View hook contents
cat .git/hooks/post-commit
```
