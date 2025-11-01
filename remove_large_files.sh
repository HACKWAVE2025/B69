#!/bin/bash
# Complete removal of large files using git filter-repo or manual method

echo "🧹 Attempting complete removal..."

# Method 1: Try git filter-repo (if available)
if command -v git-filter-repo &> /dev/null; then
    echo "Using git-filter-repo..."
    git filter-repo --path grafana-enterprise_12.2.1_18655849634_darwin_amd64.tar.gz --invert-paths --force
    git filter-repo --path grafana-12.2.1/ --invert-paths --force
    exit 0
fi

# Method 2: Manual approach - remove from all commits
echo "Using git filter-branch (manual)..."

# Remove tar.gz file
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch grafana-enterprise_12.2.1_18655849634_darwin_amd64.tar.gz" \
    --prune-empty --tag-name-filter cat -- --all

# Remove directory  
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch --force --index-filter \
    "git rm -rf --cached --ignore-unmatch grafana-12.2.1/" \
    --prune-empty --tag-name-filter cat -- --all

# Clean up
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo "✅ Cleanup complete!"
