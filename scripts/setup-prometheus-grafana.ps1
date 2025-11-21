# Prometheus and Grafana Setup Script for Windows
# This script downloads and configures Prometheus and Grafana to run natively on Windows

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Resilience Monitor - Monitoring Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Define versions
$PROMETHEUS_VERSION = "2.54.1"
$GRAFANA_VERSION = "11.3.0"

# Define paths
$PROJECT_ROOT = "c:\Users\yashv\OneDrive - BML MUNJAL UNIVERSITY\Documents\Work\Projects\AI related Projects\Devops try-2\ai-resilience-monitor"
$MONITORING_DIR = Join-Path $PROJECT_ROOT "monitoring"
$PROMETHEUS_DIR = Join-Path $MONITORING_DIR "prometheus"
$GRAFANA_DIR = Join-Path $MONITORING_DIR "grafana"

Write-Host "[1/6] Creating monitoring directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $MONITORING_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $PROMETHEUS_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $GRAFANA_DIR | Out-Null
Write-Host "✓ Directories created" -ForegroundColor Green
Write-Host ""

# Download Prometheus
Write-Host "[2/6] Downloading Prometheus $PROMETHEUS_VERSION..." -ForegroundColor Yellow
$PROMETHEUS_URL = "https://github.com/prometheus/prometheus/releases/download/v$PROMETHEUS_VERSION/prometheus-$PROMETHEUS_VERSION.windows-amd64.zip"
$PROMETHEUS_ZIP = Join-Path $MONITORING_DIR "prometheus.zip"

if (Test-Path (Join-Path $PROMETHEUS_DIR "prometheus.exe")) {
    Write-Host "✓ Prometheus already installed" -ForegroundColor Green
} else {
    Invoke-WebRequest -Uri $PROMETHEUS_URL -OutFile $PROMETHEUS_ZIP
    Expand-Archive -Path $PROMETHEUS_ZIP -DestinationPath $MONITORING_DIR -Force
    
    # Move files from extracted folder to prometheus directory
    $EXTRACTED_DIR = Join-Path $MONITORING_DIR "prometheus-$PROMETHEUS_VERSION.windows-amd64"
    Get-ChildItem -Path $EXTRACTED_DIR | Move-Item -Destination $PROMETHEUS_DIR -Force
    Remove-Item -Path $EXTRACTED_DIR -Force
    Remove-Item -Path $PROMETHEUS_ZIP -Force
    
    Write-Host "✓ Prometheus downloaded and extracted" -ForegroundColor Green
}
Write-Host ""

# Copy Prometheus config
Write-Host "[3/6] Configuring Prometheus..." -ForegroundColor Yellow
$CONFIG_SOURCE = Join-Path $PROJECT_ROOT "config\prometheus.yml"
$CONFIG_DEST = Join-Path $PROMETHEUS_DIR "prometheus.yml"
Copy-Item -Path $CONFIG_SOURCE -Destination $CONFIG_DEST -Force
Write-Host "✓ Prometheus configured to scrape localhost:3000/metrics" -ForegroundColor Green
Write-Host ""

# Download Grafana
Write-Host "[4/6] Downloading Grafana $GRAFANA_VERSION..." -ForegroundColor Yellow
$GRAFANA_URL = "https://dl.grafana.com/oss/release/grafana-$GRAFANA_VERSION.windows-amd64.zip"
$GRAFANA_ZIP = Join-Path $MONITORING_DIR "grafana.zip"

if (Test-Path (Join-Path $GRAFANA_DIR "bin\grafana-server.exe")) {
    Write-Host "✓ Grafana already installed" -ForegroundColor Green
} else {
    Invoke-WebRequest -Uri $GRAFANA_URL -OutFile $GRAFANA_ZIP
    Expand-Archive -Path $GRAFANA_ZIP -DestinationPath $MONITORING_DIR -Force
    
    # Move files from extracted folder to grafana directory
    $EXTRACTED_DIR = Join-Path $MONITORING_DIR "grafana-v$GRAFANA_VERSION"
    Get-ChildItem -Path $EXTRACTED_DIR | Move-Item -Destination $GRAFANA_DIR -Force
    Remove-Item -Path $EXTRACTED_DIR -Force
    Remove-Item -Path $GRAFANA_ZIP -Force
    
    Write-Host "✓ Grafana downloaded and extracted" -ForegroundColor Green
}
Write-Host ""

# Configure Grafana
Write-Host "[5/6] Configuring Grafana..." -ForegroundColor Yellow
$GRAFANA_INI = Join-Path $GRAFANA_DIR "conf\custom.ini"
$GRAFANA_INI_CONTENT = @"
[server]
http_port = 3001

[security]
admin_user = admin
admin_password = admin

[dashboards]
default_home_dashboard_path = ""
"@
Set-Content -Path $GRAFANA_INI -Value $GRAFANA_INI_CONTENT
Write-Host "✓ Grafana configured on port 3001 (admin/admin)" -ForegroundColor Green
Write-Host ""

# Create Grafana datasource provisioning
Write-Host "[6/6] Setting up Grafana Prometheus datasource..." -ForegroundColor Yellow
$PROVISIONING_DIR = Join-Path $GRAFANA_DIR "conf\provisioning\datasources"
New-Item -ItemType Directory -Force -Path $PROVISIONING_DIR | Out-Null

$DATASOURCE_YAML = Join-Path $PROVISIONING_DIR "prometheus.yml"
$DATASOURCE_CONTENT = @"
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://localhost:9090
    isDefault: true
    editable: true
"@
Set-Content -Path $DATASOURCE_YAML -Value $DATASOURCE_CONTENT
Write-Host "✓ Prometheus datasource configured" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services installed:" -ForegroundColor Cyan
Write-Host "  • Prometheus: $PROMETHEUS_DIR" -ForegroundColor White
Write-Host "  • Grafana:    $GRAFANA_DIR" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run START-MONITOR.ps1 to start all services" -ForegroundColor White
Write-Host "  2. Access Grafana at http://localhost:3001 (admin/admin)" -ForegroundColor White
Write-Host "  3. Access Prometheus at http://localhost:9090" -ForegroundColor White
Write-Host ""
