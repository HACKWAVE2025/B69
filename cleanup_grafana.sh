#!/bin/bash
# Quick cleanup script for Grafana files

echo "🧹 Cleaning up Grafana files from Git..."

# Remove from staging if exists
git rm --cached grafana-enterprise_12.2.1_18655849634_darwin_amd64.tar.gz 2>/dev/null || true
git rm -r --cached grafana-12.2.1/ 2>/dev/null || true

# Stage .gitignore
git add .gitignore

echo "✅ Files removed from Git tracking"
echo ""
echo "📝 Next steps:"
echo "   1. Commit: git commit -m 'Remove large Grafana files'"
echo "   2. If files were in previous commits, clean history first:"
echo "      git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch grafana-enterprise_12.2.1_18655849634_darwin_amd64.tar.gz grafana-12.2.1/bin/grafana' --prune-empty --tag-name-filter cat -- --all"
echo "   3. Push: git push origin main (or --force if you cleaned history)"
