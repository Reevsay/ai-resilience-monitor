Write-Host "🚀 Starting AI Service Resilience System in PRODUCTION mode" -ForegroundColor Green
Write-Host "⚠️  WARNING: This will make real API calls and incur costs!" -ForegroundColor Yellow
Write-Host ""

# Check if OpenAI API key is set
$dockerCompose = Get-Content "docker-compose.yml" -Raw
if ($dockerCompose -match "sk-your-real-openai-key-here") {
    Write-Host "❌ ERROR: OpenAI API key not configured!" -ForegroundColor Red
    Write-Host "   Please update docker-compose.yml with your real API key"
    Write-Host "   Replace 'sk-your-real-openai-key-here' with your actual key"
    Write-Host ""
    Write-Host "📋 Steps to get API key:"
    Write-Host "   1. Go to https://platform.openai.com/"
    Write-Host "   2. Sign up/Login to your account"
    Write-Host "   3. Go to 'API Keys' section"
    Write-Host "   4. Click 'Create new secret key'"
    Write-Host "   5. Copy the key (starts with sk-proj- or sk-)"
    Write-Host "   6. Add $5-10 credit to your account"
    Write-Host ""
    exit 1
}

Write-Host "✅ API key configured" -ForegroundColor Green

# Confirm with user
$confirm = Read-Host "Continue with real API calls? This will cost money! (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Cancelled"
    exit 0
}

Write-Host ""
Write-Host "🐳 Starting Docker containers..." -ForegroundColor Blue
docker-compose up -d

Write-Host ""
Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "🌐 Services available at:" -ForegroundColor Green
Write-Host "   • AI Proxy:     http://localhost:3000"
Write-Host "   • Dashboard:    http://localhost:3000/dashboard"
Write-Host "   • Metrics:      http://localhost:3000/metrics"
Write-Host "   • Prometheus:   http://localhost:9090"
Write-Host "   • Grafana:      http://localhost:3001"
Write-Host ""

Write-Host "🧪 Running small test with real API..." -ForegroundColor Cyan
npm run openai-test-small

Write-Host ""
Write-Host "📊 Check your results:" -ForegroundColor Green
Write-Host "   • Dashboard: http://localhost:3000/dashboard"
Write-Host "   • View logs: docker-compose logs ai-proxy"
Write-Host ""
Write-Host "⚠️  Monitor your OpenAI usage at: https://platform.openai.com/usage" -ForegroundColor Yellow
