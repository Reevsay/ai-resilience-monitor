# Quick Test Script - Generates test traffic to see real-time dashboard updates
Write-Host "🧪 AI Resilience Monitor - Quick Test Traffic Generator" -ForegroundColor Green
Write-Host "This will generate test requests to see live dashboard updates" -ForegroundColor Yellow
Write-Host ""

# Test different services
$services = @("gemini", "cohere", "huggingface")
$prompts = @(
    "Hello, world!",
    "What is AI?", 
    "Explain machine learning",
    "Tell me a joke",
    "How does the internet work?"
)

Write-Host "📊 Generating 10 test requests..." -ForegroundColor Cyan

for ($i = 1; $i -le 10; $i++) {
    try {
        # Random service and prompt
        $service = $services | Get-Random
        $prompt = $prompts | Get-Random
        
        # Create request
        $body = @{
            prompt = "$prompt (Request $i)"
            service = $service
        } | ConvertTo-Json
        
        # Send request
        $response = Invoke-RestMethod -Uri "http://localhost:3000/ai" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 10
        
        Write-Host "✅ Request $i - $service`: Success ($($response.latency)ms)" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ Request $i - $service`: Failed" -ForegroundColor Red
    }
    
    # Wait 2 seconds between requests
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "📈 Final Metrics:" -ForegroundColor Cyan
try {
    $metrics = Invoke-RestMethod -Uri "http://localhost:3000/metrics" -Method GET
    Write-Host "Total Requests: $($metrics.totalRequests)" -ForegroundColor White
    Write-Host "Success Rate: $($metrics.successRate)%" -ForegroundColor White
    Write-Host "Avg Latency: $($metrics.avgLatency)ms" -ForegroundColor White
} catch {
    Write-Host "Failed to fetch final metrics" -ForegroundColor Red
}

Write-Host ""
Write-Host "🌐 Check your dashboard at: http://localhost:8080" -ForegroundColor Green
Write-Host "The metrics should update automatically every 5 seconds!" -ForegroundColor Yellow