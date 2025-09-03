# 🎨 Dashboard Demo Script

## 🚀 Overview

The dashboard demo script creates realistic AI service traffic to showcase the monitoring capabilities of the AI Resilience Monitor. It simulates various scenarios including successful requests, failures, and different response patterns.

## 🎯 Quick Start

```bash
# Start the demo with default settings
npm run dashboard-demo

# Run with custom parameters
node tools/dashboard-demo.js --requests 50 --interval 2000
```

## 🛠️ Demo Features

### 📊 Real-time Traffic Simulation
- **Multiple AI Services**: Rotates between Cohere, Gemini, and HuggingFace
- **Realistic Patterns**: Simulates real user behavior with varying message types
- **Mixed Outcomes**: Includes successful responses, timeouts, and errors
- **Dynamic Load**: Varies request frequency to show different traffic patterns

### 🎭 Scenario Simulation
- **Normal Operations**: 85% success rate with typical response times
- **Degraded Performance**: Increased latency and error rates
- **Service Outages**: Complete failures to test circuit breaker
- **Recovery Patterns**: Gradual return to normal operations

### 📈 Visual Effects
- **Live Charts**: Request volume, success rates, and latency trends
- **Circuit Breaker**: Visual state changes with animations
- **Request Log**: Real-time streaming of AI service calls
- **Health Indicators**: Color-coded service status with pulse effects

## 🎮 Demo Modes

### 🌟 Standard Demo
```bash
npm run dashboard-demo
```
- **Duration**: Continuous (Ctrl+C to stop)
- **Request Rate**: 1 request every 3-5 seconds
- **Success Rate**: ~90%
- **Services**: All AI services

### ⚡ High Traffic Demo
```bash
node tools/dashboard-demo.js --mode high-traffic
```
- **Duration**: Continuous
- **Request Rate**: 2-3 requests per second
- **Success Rate**: ~85%
- **Services**: All AI services with load balancing

### 💥 Chaos Demo
```bash
node tools/dashboard-demo.js --mode chaos
```
- **Duration**: 10 minutes
- **Request Rate**: Variable (1-5 per second)
- **Success Rate**: 60-95% (varies over time)
- **Failures**: Random injection of various error types

### 🔄 Circuit Breaker Demo
```bash
node tools/dashboard-demo.js --mode circuit-breaker
```
- **Duration**: 15 minutes
- **Pattern**: Gradual degradation → circuit open → recovery
- **Success Rate**: Starts at 95%, drops to 20%, recovers to 90%
- **Focus**: Demonstrates circuit breaker state transitions

## 📊 Demo Configuration

### Custom Parameters
```bash
# Customize request rate
node tools/dashboard-demo.js --interval 1000  # 1 request per second

# Set specific duration
node tools/dashboard-demo.js --duration 300   # 5 minutes

# Focus on specific service
node tools/dashboard-demo.js --service cohere

# Simulate high error rate
node tools/dashboard-demo.js --error-rate 0.3  # 30% errors
```

### Advanced Configuration
```javascript
// tools/demo-config.js
module.exports = {
  // Request patterns
  interval: {
    min: 2000,    // Minimum delay between requests (ms)
    max: 5000     // Maximum delay between requests (ms)
  },
  
  // Service distribution
  services: {
    cohere: 0.4,      // 40% of requests
    gemini: 0.35,     // 35% of requests
    huggingface: 0.25 // 25% of requests
  },
  
  // Error simulation
  errorRates: {
    network: 0.05,    // 5% network errors
    timeout: 0.03,    // 3% timeouts
    auth: 0.02,       // 2% auth errors
    rateLimit: 0.01   // 1% rate limit errors
  },
  
  // Message variety
  messages: [
    "Explain quantum computing",
    "Write a haiku about technology",
    "Summarize machine learning",
    "Generate creative story ideas",
    "Analyze market trends",
    "Describe cloud architecture"
  ]
};
```

## 🎨 Visual Showcase

### 📊 Chart Animations
The demo triggers various chart updates:
- **Request Volume**: Bar chart with sliding window
- **Success Rate**: Line chart with color transitions
- **Latency Trends**: Area chart with gradient fills
- **Service Health**: Donut chart with animated segments

### 🔄 Circuit Breaker States
Watch the circuit breaker transition through states:
1. **🟢 Closed**: Normal operation, green indicator
2. **🟡 Half-Open**: Testing recovery, yellow indicator  
3. **🔴 Open**: Protecting service, red indicator with breathing animation

### 📝 Request Logging
Real-time request log shows:
- **Timestamp**: Precise request timing
- **Service**: Which AI service was called
- **Status**: Success/failure with color coding
- **Response Time**: Latency measurement
- **Message**: Truncated request content

## 🧪 Testing Scenarios

### Scenario 1: Normal Operations
```bash
node tools/dashboard-demo.js --mode normal --duration 300
```
**What to Watch:**
- Steady request flow with consistent success rates
- Circuit breaker remains closed (green)
- Latency stays within normal ranges
- All services showing healthy status

### Scenario 2: Service Degradation
```bash
node tools/dashboard-demo.js --mode degraded --duration 600
```
**What to Watch:**
- Gradually increasing error rates
- Latency spikes in charts
- Circuit breaker transitions to half-open
- Service health indicators change color

### Scenario 3: Complete Failure
```bash
node tools/dashboard-demo.js --mode failure --duration 180
```
**What to Watch:**
- High error rates trigger circuit breaker
- Circuit opens (red indicator with animation)
- Fallback responses activate
- Request volume drops as circuit protects service

### Scenario 4: Recovery
```bash
node tools/dashboard-demo.js --mode recovery --duration 900
```
**What to Watch:**
- Service gradually improves
- Circuit breaker tests with half-open state
- Successful recovery closes circuit
- Metrics return to healthy baselines

## 🎯 Demo Best Practices

### 🚀 Before Starting Demo
1. **Start Services**: Ensure main application is running
2. **Open Dashboard**: Navigate to http://localhost:3000/dashboard
3. **Clear Browser Cache**: Force refresh for clean start
4. **Check Network**: Verify stable internet connection

### 👀 During Demo
1. **Watch Multiple Panels**: Keep eye on charts, logs, and status
2. **Note Transitions**: Observe circuit breaker state changes
3. **Check Responsiveness**: Verify dashboard updates smoothly
4. **Monitor Performance**: Ensure browser handles updates well

### 📈 Demo Presentation Tips
1. **Start with Overview**: Explain dashboard components first
2. **Show Normal State**: Begin with stable operations
3. **Introduce Chaos**: Gradually add failures for drama
4. **Highlight Recovery**: Demonstrate resilience features
5. **End on High Note**: Show system returning to stability

## 🛠️ Customizing Demo

### Adding New Scenarios
```javascript
// tools/scenarios/custom-scenario.js
module.exports = {
  name: 'custom-scenario',
  duration: 300, // 5 minutes
  phases: [
    {
      duration: 60,
      errorRate: 0.1,
      interval: 2000
    },
    {
      duration: 180,
      errorRate: 0.5,
      interval: 1000
    },
    {
      duration: 60,
      errorRate: 0.05,
      interval: 3000
    }
  ]
};
```

### Custom Message Sets
```javascript
// Add domain-specific messages
const customMessages = [
  "Analyze financial portfolio risk",
  "Generate marketing campaign ideas",
  "Optimize supply chain logistics",
  "Predict customer behavior patterns",
  "Automate code review process"
];
```

## 🚨 Troubleshooting Demo

### Common Issues

**Demo Not Showing Traffic**
```bash
# Check if demo is actually running
ps aux | grep dashboard-demo

# Verify dashboard is accessible
curl http://localhost:3000/dashboard
```

**Charts Not Updating**
```bash
# Clear browser cache
# Hard refresh (Ctrl+Shift+R)
# Check browser console for errors
```

**High CPU Usage**
```bash
# Reduce demo frequency
node tools/dashboard-demo.js --interval 5000

# Use lighter demo mode
node tools/dashboard-demo.js --mode light
```

**Memory Issues**
```bash
# Restart demo periodically
# Monitor with: docker stats
# Reduce chart history in dashboard
```

## 📱 Mobile Demo

The dashboard demo works great on mobile devices:
- **Responsive Design**: Charts adapt to screen size
- **Touch Interactions**: Tap to explore chart details
- **Optimized Performance**: Reduced update frequency on mobile
- **Battery Friendly**: Efficient rendering for longer demos

---

🎭 **Pro Demo Tips**
- Use fullscreen mode for presentations
- Prepare talking points for each scenario
- Have backup plans if network issues occur
- Practice scenario timing for smooth flow
- Keep browser developer tools handy for debugging

Need help with the demo? [Open an issue](https://github.com/Reevsay/ai-resilience-monitor/issues) or check our [main documentation](../README.md).
