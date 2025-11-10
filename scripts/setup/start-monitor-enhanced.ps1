# Enhanced Backend Monitor Launcher
# Starts the monitoring script with auto-recovery

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 Backend Monitor with Auto-Recovery" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$monitorScript = Join-Path $scriptDir "monitor-backend-enhanced.py"
$logFile = Join-Path $scriptDir "monitor.log"

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python first." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit 1
}

# Check if monitor script exists
if (-not (Test-Path $monitorScript)) {
    Write-Host "❌ Monitor script not found: $monitorScript" -ForegroundColor Red
    pause
    exit 1
}

# Check if psutil is installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import psutil, requests" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Dependencies missing"
    }
    Write-Host "✅ Dependencies OK" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Installing required packages..." -ForegroundColor Yellow
    pip install psutil requests
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        pause
        exit 1
    }
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Monitor Script: monitor-backend-enhanced.py" -ForegroundColor White
Write-Host "  Backend Script: src/index.js" -ForegroundColor White
Write-Host "  Backend Port:   3000" -ForegroundColor White
Write-Host "  Check Interval: 5 seconds" -ForegroundColor White
Write-Host "  Log File:       monitor.log" -ForegroundColor White
Write-Host ""
Write-Host "Features:" -ForegroundColor Cyan
Write-Host "  ✓ Auto-restart on crash" -ForegroundColor Green
Write-Host "  ✓ Health monitoring every 5s" -ForegroundColor Green
Write-Host "  ✓ Detailed logging" -ForegroundColor Green
Write-Host "  ✓ Process cleanup" -ForegroundColor Green
Write-Host "  ✓ Memory monitoring" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop monitoring" -ForegroundColor Yellow
Write-Host "Log file: $logFile" -ForegroundColor Yellow
Write-Host ""
Write-Host "Starting monitor..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start the monitor
try {
    python $monitorScript
} catch {
    Write-Host ""
    Write-Host "❌ Monitor stopped with error" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Monitor stopped" -ForegroundColor Yellow
    Write-Host "Check log file for details: $logFile" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Cyan
}

pause
