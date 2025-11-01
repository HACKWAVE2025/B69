# 🔧 Fix GitHub Large File Error

## Problem

GitHub rejected your push because these files exceed the 100MB limit:
- `grafana-enterprise_12.2.1_18655849634_darwin_amd64.tar.gz` (289.88 MB)
- `grafana-12.2.1/bin/grafana` (502.67 MB)

## Solution Steps

### Step 1: Remove Files from Git (Already Done)

The tar.gz file has been removed from git tracking. Now we need to handle the extracted directory.

### Step 2: Remove Grafana Directory from Git

If `grafana-12.2.1/` directory exists in git:

```bash
# Remove the entire directory from git (but keep local files)
git rm -r --cached grafana-12.2.1/

# Or if it's in a different location:
git rm -r --cached **/grafana-12.2.1/
```

### Step 3: Clean Up Git History (If Files Were Already Pushed)

If these files were in previous commits, you need to remove them from git history:

**Option A: Use BFG Repo-Cleaner (Recommended for large repos)**

```bash
# Install BFG
brew install bfg  # macOS
# OR download from: https://rtyley.github.io/bfg-repo-cleaner/

# Remove large files from history
bfg --strip-blobs-bigger-than 100M

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

**Option B: Use git filter-branch (Built-in, but slower)**

```bash
# Remove specific files from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch grafana-enterprise_12.2.1_18655849634_darwin_amd64.tar.gz grafana-12.2.1/bin/grafana" \
  --prune-empty --tag-name-filter cat -- --all

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

**Option C: Use git filter-repo (Modern alternative)**

```bash
# Install git-filter-repo
pip install git-filter-repo

# Remove files
git filter-repo --path grafana-enterprise_12.2.1_18655849634_darwin_amd64.tar.gz --invert-paths
git filter-repo --path grafana-12.2.1/ --invert-paths
```

### Step 4: Update .gitignore (Already Done)

The `.gitignore` file has been updated to ignore Grafana files. Verify it includes:

```
# Grafana (if downloaded - large binary files)
grafana-*/
grafana-*.tar.gz
grafana-*.zip
grafana*/
**/grafana-*/
```

### Step 5: Commit and Force Push

⚠️ **Warning:** Force pushing rewrites history. Only do this if:
- You're working alone, OR
- You coordinate with your team
- You're sure no one else has pulled your commits

```bash
# Commit the removal
git add .gitignore
git commit -m "Remove large Grafana files and update .gitignore"

# Force push (only if you cleaned history)
git push --force origin main

# OR if you didn't clean history, just push normally
git push origin main
```

## Alternative: Use Git LFS (If You Need These Files)

If you actually need to track large Grafana binaries:

```bash
# Install Git LFS
brew install git-lfs  # macOS
git lfs install

# Track large files
git lfs track "*.tar.gz"
git lfs track "grafana-*/**"

# Add .gitattributes
git add .gitattributes

# Re-add files
git add grafana-enterprise_12.2.1_18655849634_darwin_amd64.tar.gz
git commit -m "Add Grafana files with Git LFS"
```

## Quick Fix (Simplest Solution)

If you just want to get unblocked quickly:

```bash
# 1. Remove from git
git rm --cached grafana-enterprise_12.2.1_18655849634_darwin_amd64.tar.gz
git rm -r --cached grafana-12.2.1/ 2>/dev/null || true

# 2. Commit
git add .gitignore
git commit -m "Remove large Grafana files"

# 3. If this is a new repo or you haven't pushed yet:
git push origin main

# 4. If files were in previous commits, clean history first:
# (See Step 3 above)
```

## Verification

After cleanup, verify:

```bash
# Check git status
git status

# Check for large files
git ls-files | xargs ls -lh | awk '$5 > 100000000 {print $9, $5}'

# Try push again
git push origin main
```

## Notes

- **Grafana binaries don't belong in git** - they're large and platform-specific
- Keep them in `.gitignore` and document where to download them in README
- Use package managers (brew, apt) or direct downloads for Grafana installation
- Consider using Docker for Grafana instead of binaries

