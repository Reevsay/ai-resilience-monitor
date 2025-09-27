#!/bin/bash

# AI Resilience Monitor - Load Testing Script
# This script generates test traffic to validate the monitoring system

echo "🚀 AI Resilience Monitor Load Testing Script"
echo "=============================================="

# Check if backend is running
echo "🔍 Checking if backend is running..."
if curl -s http://localhost:3000/test > /dev/null; then
    echo "✅ Backend is running on port 3000"
else
    echo "❌ Backend is not running. Please start it with 'npm start'"
    exit 1
fi

# Test different AI services
services=("gemini" "cohere" "huggingface")
prompts=(
    "What is artificial intelligence?"
    "Explain machine learning in simple terms"
    "How do neural networks work?"
    "What is the future of AI?"
    "Compare different AI models"
)

echo ""
echo "📊 Generating test traffic..."
echo "Press Ctrl+C to stop"

request_count=0

while true; do
    # Select random service and prompt
    service=${services[$RANDOM % ${#services[@]}]}
    prompt=${prompts[$RANDOM % ${#prompts[@]}]}
    
    # Make API request
    response=$(curl -s -X POST http://localhost:3000/ai \
        -H "Content-Type: application/json" \
        -d "{\"prompt\": \"$prompt\", \"service\": \"$service\"}" \
        -w "HTTP_STATUS:%{http_code}")
    
    request_count=$((request_count + 1))
    
    # Parse response
    http_status=$(echo "$response" | sed -n 's/.*HTTP_STATUS:\([0-9]*\)/\1/p')
    
    if [ "$http_status" = "200" ]; then
        echo "✅ Request $request_count: $service - Success"
    else
        echo "❌ Request $request_count: $service - Failed (HTTP $http_status)"
    fi
    
    # Random delay between 1-3 seconds
    sleep_time=$(echo "scale=1; $(($RANDOM % 30)) / 10 + 1" | bc)
    sleep $sleep_time
    
    # Show metrics every 10 requests
    if [ $((request_count % 10)) -eq 0 ]; then
        echo ""
        echo "📈 Current Metrics:"
        curl -s http://localhost:3000/metrics | python3 -m json.tool | grep -E "(totalRequests|successRate|avgLatency)" | head -3
        echo ""
    fi
done