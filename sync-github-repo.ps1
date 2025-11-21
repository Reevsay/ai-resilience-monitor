# GitHub Repository Sync Script
# This script will clean up the GitHub repo and sync it with your local structure
# It removes old files and pushes the current clean structure

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GitHub Repository Sync Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to the project directory
Set-Location -Path "ai-resilience-monitor"

Write-Host "[1/6] Checking Git status..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "[2/6] Fetching latest from GitHub..." -ForegroundColor Yellow
git fetch origin main

Write-Host ""
Write-Host "[3/6] Pulling latest changes..." -ForegroundColor Yellow
git pull origin main --allow-unrelated-histories

Write-Host ""
Write-Host "[4/6] Adding all current files..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "[5/6] Committing changes..." -ForegroundColor Yellow
$commitMessage = "Sync repository structure - Remove old files and update to clean architecture

- Removed unused modules (alertMonitor, notificationService, failureInjector, multiAIService)
- Consolidated database operations to backend/database.py
- Updated project structure with proper organization
- Added comprehensive documentation and LaTeX flowcharts
- Cleaned up test results and logs
- Updated .gitignore for better file management
- Organized literature and research papers
- Added GitHub workflow configurations"

git commit -m $commitMessage

Write-Host ""
Write-Host "[6/6] Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "This will sync your local structure to GitHub..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to push to GitHub, or Ctrl+C to cancel..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

git push origin main --force

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Repository sync completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your GitHub repository now matches your local structure." -ForegroundColor Green
Write-Host "Visit: https://github.com/Reevsay/ai-resilience-monitor" -ForegroundColor Cyan
