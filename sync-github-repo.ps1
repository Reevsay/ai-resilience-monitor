# GitHub Repository Sync Script
# This script will clean up the GitHub repo and sync it with your local structure
# It removes old files and pushes the current clean structure

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Repository Sync Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to the project directory
Set-Location -Path "ai-resilience-monitor"

Write-Host "[1/7] Checking Git status..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "[2/7] Fetching latest from GitHub..." -ForegroundColor Yellow
git fetch origin main

Write-Host ""
Write-Host "[3/7] Pulling latest changes..." -ForegroundColor Yellow
git pull origin main --allow-unrelated-histories

Write-Host ""
Write-Host "[4/7] Removing unnecessary documentation files..." -ForegroundColor Yellow
# Remove files that were already deleted locally but might exist on GitHub
git rm --cached CLEANUP_SUMMARY.md 2>$null
git rm --cached PUSH_TO_GITHUB.md 2>$null
git rm --cached GITHUB_COMMIT_GUIDE.md 2>$null
git rm --cached READY_FOR_GITHUB.md 2>$null
git rm --cached commit-to-github.ps1 2>$null
Write-Host "Removed unnecessary MD files" -ForegroundColor Green

Write-Host ""
Write-Host "[5/7] Adding all current files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "[6/7] Committing changes..." -ForegroundColor Yellow
$commitMessage = "Clean repository structure and update README

✨ Changes:
- Removed unnecessary documentation files (CLEANUP_SUMMARY, PUSH_TO_GITHUB, etc.)
- Updated README.md with modern, attractive design
- Removed old unused modules (alertMonitor, notificationService, failureInjector, multiAIService)
- Consolidated database operations to backend/database.py
- Added comprehensive documentation and LaTeX flowcharts
- Cleaned up test results and logs
- Updated .gitignore for better file management
- Organized literature and research papers
- Added proper project structure

🎯 Result: Clean, professional repository ready for production"

git commit -m $commitMessage

Write-Host ""
Write-Host "[7/7] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "This will sync your local structure to GitHub..." -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  This will force push and remove old files from GitHub" -ForegroundColor Yellow
Write-Host "Press any key to continue, or Ctrl+C to cancel..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

git push origin main --force

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ Repository sync completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "✨ Your GitHub repository now matches your local structure" -ForegroundColor Green
Write-Host "🔗 Visit: https://github.com/Reevsay/ai-resilience-monitor" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Verify the repository structure on GitHub" -ForegroundColor White
Write-Host "   2. Check that README.md displays correctly" -ForegroundColor White
Write-Host "   3. Ensure all unnecessary files are removed" -ForegroundColor White
