# Stop All Services Script
# Stops Prometheus, Grafana, Node.js backend, and Python frontend

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  STOPPING ALL SERVICES" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🛑 Stopping processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -match "node|python|prometheus|grafana"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host "✅ All services stopped" -ForegroundColor Green
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
