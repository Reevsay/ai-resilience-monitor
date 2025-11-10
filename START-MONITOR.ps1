# AI Resilience Monitor - Quick Start Script
# Kills old processes, starts services with auto-restart, opens dashboard

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  AI RESILIENCE MONITOR - QUICK START" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Change to project directory
Set-Location "c:\Users\yashv\OneDrive - BML MUNJAL UNIVERSITY\Documents\Work\Projects\AI related Projects\Devops try-2\ai-resilience-monitor"

Write-Host "`n🧹 STEP 1: Cleaning up old processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -match "node|python"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3
Write-Host "✅ Cleanup complete`n" -ForegroundColor Green

Write-Host "🚀 STEP 2: Starting comprehensive monitor..." -ForegroundColor Yellow
Write-Host "   This will:" -ForegroundColor White
Write-Host "   - Start backend (Node.js on port 3000)" -ForegroundColor White
Write-Host "   - Start frontend (Flask on port 8080)" -ForegroundColor White
Write-Host "   - Auto-restart on crashes" -ForegroundColor White
Write-Host "   - Monitor memory usage" -ForegroundColor White
Write-Host "   - Open dashboard in browser`n" -ForegroundColor White

# Start monitor in new window
Start-Process cmd -ArgumentList "/k", "cd /d `"$PWD`" && python scripts\monitoring\monitor-all-services.py"

Write-Host "✅ Monitor started in new window" -ForegroundColor Green
Write-Host "`n📊 Dashboard will open automatically at: http://localhost:8080" -ForegroundColor Cyan
Write-Host "`nℹ️  To run chaos test:" -ForegroundColor Yellow
Write-Host "   python scripts\testing\chaos-test.py --validation --output-dir chaos-validation" -ForegroundColor White
Write-Host "`nℹ️  To stop everything:" -ForegroundColor Yellow
Write-Host "   Close the monitor window or press Ctrl+C in it" -ForegroundColor White
Write-Host "`n======================================================================`n" -ForegroundColor Cyan
