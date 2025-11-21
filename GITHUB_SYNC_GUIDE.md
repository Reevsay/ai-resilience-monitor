# GitHub Repository Sync Guide

## Overview
This guide helps you sync your GitHub repository to match your current local clean structure, removing old files and updating the repository organization.

## Current Local Structure

```
ai-resilience-monitor/
├── .github/workflows/          # GitHub Actions CI/CD
├── backend/                    # Database operations
│   └── database.py
├── chaos-test-results/         # Chaos experiment results
├── config/                     # Configuration files
│   ├── .env
│   ├── grafana-dashboard.json
│   ├── prometheus.yml
│   └── README.md
├── data/                       # SQLite database storage
│   └── README.md
├── docs/                       # Project documentation
│   ├── CONTRIBUTING.md
│   ├── FRONTEND_REDESIGN_SPECIFICATION.md
│   ├── LITERATURE_REVIEW.md
│   └── README.md
├── documentation/              # LaTeX flowcharts and technical docs
│   ├── *.tex (4 flowcharts)
│   ├── FLOWCHARTS_QUICK_REFERENCE.md
│   ├── LATEX_FLOWCHARTS_README.md
│   └── MULTI_PROVIDER_AI_OVERVIEW.md
├── literature/                 # Academic papers and research
│   ├── *.pdf (8 papers)
│   ├── PAPER_SUMMARIES.md
│   └── reference texts
├── logs/                       # Application logs
│   └── README.md
├── scripts/                    # Utility scripts
│   ├── monitoring/
│   ├── research-paper/
│   ├── setup/
│   ├── testing/
│   ├── utilities/
│   └── README.md
├── src/                        # Node.js backend source
│   └── index.js
├── templates/                  # Flask HTML templates
│   └── dashboard.html
├── test/                       # Test suites
│   ├── ci-test.js
│   ├── payloads.json
│   └── real-ai-load-tester.js
├── app.py                      # Flask frontend server
├── package.json                # Node.js dependencies
├── requirements.txt            # Python dependencies
├── README.md                   # Main documentation
└── LICENSE                     # MIT License
```

## Files Removed from Old Structure

The following files were removed during cleanup and will be deleted from GitHub:

### Removed Modules (Consolidated into index.js)
- `src/alertMonitor.js` - Merged into main server
- `src/notificationService.js` - Merged into main server
- `src/failureInjector.js` - Merged into main server
- `src/multiAIService.js` - Merged into main server
- `src/app.js` - Duplicate server implementation

### Removed Documentation (Outdated/Redundant)
- `FINAL_RESEARCH_PAPER.md` - Moved to docs/
- `DEEP_PAPER_ANALYSIS.md` - Consolidated
- `LITERATURE_REVIEW.md` - Moved to docs/
- `IEEE_LITERATURE_PAPERS.md` - Consolidated
- `CLEANUP_REPORT_2024.md` - Archived

### Removed Test Files (Empty/Incomplete)
- `test/load-tester.js` - Replaced by real-ai-load-tester.js
- `test/metrics-test.js` - Incomplete
- `test/free-tier-load-tester.js` - Replaced

### Removed Database Files (Old Location)
- `database.py` (root) - Moved to backend/database.py

## Sync Methods

### Method 1: Force Push (Recommended - Clean Sync)

This method will completely sync your GitHub repo to match your local structure:

```powershell
# Run the automated sync script
.\sync-github-repo.ps1
```

**What it does:**
1. Fetches latest from GitHub
2. Pulls changes with merge strategy
3. Adds all current files
4. Commits with comprehensive message
5. Force pushes to GitHub (removes old files)

### Method 2: Manual Sync (Step-by-Step)

If you prefer manual control:

```powershell
cd ai-resilience-monitor

# 1. Fetch and pull latest
git fetch origin main
git pull origin main --allow-unrelated-histories

# 2. Add all current files
git add .

# 3. Commit changes
git commit -m "Sync repository structure - Remove old files and update to clean architecture"

# 4. Force push to sync
git push origin main --force
```

### Method 3: Incremental Sync (Preserve All History)

If you want to keep all commit history:

```powershell
cd ai-resilience-monitor

# 1. Pull latest
git pull origin main

# 2. Remove old files explicitly
git rm src/alertMonitor.js
git rm src/notificationService.js
git rm src/failureInjector.js
git rm src/multiAIService.js
git rm src/app.js
git rm database.py
git rm test/load-tester.js
git rm test/metrics-test.js
git rm test/free-tier-load-tester.js

# 3. Add new structure
git add .

# 4. Commit
git commit -m "Clean up repository structure and remove unused files"

# 5. Push
git push origin main
```

## What Will Happen

### Files That Will Be Removed from GitHub:
- Old unused modules in src/
- Duplicate database.py in root
- Outdated test files
- Redundant documentation files
- Any files not in your current local structure

### Files That Will Be Added/Updated:
- Clean src/index.js (consolidated)
- backend/database.py (new location)
- All documentation in docs/ and documentation/
- LaTeX flowcharts
- Updated test suite
- Organized scripts
- Current chaos test results
- All configuration files

## Verification Steps

After syncing, verify your GitHub repository:

1. **Visit your repository:**
   https://github.com/Reevsay/ai-resilience-monitor

2. **Check the file structure matches local:**
   - backend/ folder exists with database.py
   - src/ contains only index.js
   - documentation/ has LaTeX files
   - No old unused modules

3. **Verify key files:**
   - README.md is updated
   - package.json and requirements.txt are current
   - .gitignore is properly configured

4. **Check commit history:**
   - Your 46 previous commits are preserved (if using Method 2 or 3)
   - New sync commit is added

## Important Notes

### Before Syncing:
- ✅ Backup your local repository
- ✅ Ensure all important files are committed locally
- ✅ Review .gitignore to ensure sensitive files are excluded
- ✅ Check that API keys are not in tracked files

### After Syncing:
- ✅ Verify GitHub repository structure
- ✅ Test clone on a different machine
- ✅ Update any documentation links
- ✅ Notify team members of structure changes

### Files Excluded by .gitignore:
- `.env` files (API keys)
- `node_modules/`
- `__pycache__/`
- `data/monitoring.db*` (database files)
- `*.log` files
- LaTeX source files (keeping PDFs only)
- Test result logs and CSVs

## Troubleshooting

### Issue: "Updates were rejected"
```powershell
# Use force push (overwrites remote)
git push origin main --force
```

### Issue: "Merge conflicts"
```powershell
# Accept local version
git checkout --ours .
git add .
git commit -m "Resolve conflicts - use local structure"
git push origin main --force
```

### Issue: "Old files still showing on GitHub"
- GitHub may cache the file tree
- Wait 5-10 minutes and refresh
- Clear browser cache
- Check in incognito mode

### Issue: "Large files rejected"
```powershell
# Check file sizes
git ls-files -z | xargs -0 du -h | sort -h | tail -20

# Remove large files from history if needed
git filter-branch --tree-filter 'rm -f path/to/large/file' HEAD
```

## Post-Sync Checklist

- [ ] GitHub repository structure matches local
- [ ] README.md displays correctly
- [ ] All documentation is accessible
- [ ] No sensitive files (API keys) are exposed
- [ ] CI/CD workflows are working
- [ ] Clone test successful
- [ ] Team members notified
- [ ] Documentation links updated

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review Git status: `git status`
3. Check remote: `git remote -v`
4. View commit history: `git log --oneline -10`

## Next Steps

After successful sync:
1. Update repository description on GitHub
2. Add topics/tags for discoverability
3. Update README badges if needed
4. Consider adding GitHub Pages for documentation
5. Set up branch protection rules
6. Configure GitHub Actions for CI/CD

---

**Repository:** https://github.com/Reevsay/ai-resilience-monitor
**Current Commits:** 46 (will be preserved with Method 2/3)
**Last Updated:** November 21, 2025
