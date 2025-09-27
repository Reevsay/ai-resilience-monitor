# AI Resilience Monitor - Load Testing Script (PowerShell)
# This script generates test traffic to validate the monitoring system

Write-Host "🚀 AI Resilience Monitor Load Testing Script" -ForegroundColor Green
Write-Host "=============================================="

# Check if backend is running
Write-Host "🔍 Checking if backend is running..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/test" -Method GET -TimeoutSec 5
    Write-Host "✅ Backend is running on port 3000" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend is not running. Please start it with 'npm start'" -ForegroundColor Red
    exit 1
}

# Test different AI services
$services = @("gemini", "cohere", "huggingface")
$prompts = @(
    "What is artificial intelligence?",
    "Explain machine learning in simple terms",
    "How do neural networks work?",
    "What is the future of AI?",
    "Compare different AI models"
)

Write-Host ""
Write-Host "📊 Generating test traffic..." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow

$requestCount = 0

while ($true) {
    try {
        # Select random service and prompt
        $service = $services | Get-Random
        $prompt = $prompts | Get-Random
        
        # Create request body
        $body = @{
            prompt = $prompt
            service = $service
        } | ConvertTo-Json
        
        # Make API request
        $response = Invoke-RestMethod -Uri "http://localhost:3000/ai" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 10
        
        $requestCount++
        Write-Host "✅ Request $requestCount`: $service - Success" -ForegroundColor Green
        
    } catch {
        $requestCount++
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "❌ Request $requestCount`: $service - Failed (HTTP $statusCode)" -ForegroundColor Red
    }
    
    # Random delay between 1-3 seconds
    $sleepTime = Get-Random -Minimum 1 -Maximum 4
    Start-Sleep -Seconds $sleepTime
    
    # Show metrics every 10 requests
    if ($requestCount % 10 -eq 0) {
        Write-Host ""
        Write-Host "📈 Current Metrics:" -ForegroundColor Cyan
        try {
            $metrics = Invoke-RestMethod -Uri "http://localhost:3000/metrics" -Method GET -TimeoutSec 5
            Write-Host "Total Requests: $($metrics.totalRequests)"
            Write-Host "Success Rate: $($metrics.successRate)%"
            Write-Host "Avg Latency: $($metrics.avgLatency)ms"
        } catch {
            Write-Host "Failed to fetch metrics" -ForegroundColor Red
        }
        Write-Host ""
    }
}