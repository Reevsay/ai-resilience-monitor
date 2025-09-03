# 🧪 Testing Guide

## 🎯 Testing Overview

The AI Resilience Monitor includes comprehensive testing capabilities for validating service reliability, performance, and failure scenarios.

## 🚀 Quick Test Commands

### Basic Testing
```bash
# Health check all services
npm run test

# Test specific AI services
npm run test-cohere
npm run test-gemini
npm run test-huggingface
```

### Load Testing
```bash
# Balanced load testing
npm run load-test

# Light testing (50 requests)
npm run load-test-small

# Heavy testing (500 requests)
npm run load-test-large

# Custom load test
npm run load-test -- --requests 100 --concurrency 5
```

### Chaos Engineering
```bash
# Random failure injection
npm run chaos-test

# Specific failure types
npm run test:network-errors
npm run test:auth-failures
npm run test:slow-responses
```

## 📊 Load Testing Scenarios

### 🎯 Scenario 1: Normal Load
```bash
npm run load-test
```
- **Requests**: 100
- **Concurrency**: 5
- **Duration**: ~2 minutes
- **Expected Success Rate**: >95%

### 🔥 Scenario 2: Stress Test
```bash
npm run load-test-large
```
- **Requests**: 500
- **Concurrency**: 10
- **Duration**: ~5 minutes
- **Expected Success Rate**: >90%

### ⚡ Scenario 3: Burst Test
```bash
npm run load-test -- --requests 50 --concurrency 20
```
- **Requests**: 50
- **Concurrency**: 20
- **Duration**: ~30 seconds
- **Expected Success Rate**: >85%

## 💥 Failure Injection Testing

### Network Failure Tests
```bash
# Test connection timeouts
curl -X POST http://localhost:3000/test/inject \
  -H "Content-Type: application/json" \
  -d '{"type": "network", "duration": 60}'

# Test DNS resolution failures
curl -X POST http://localhost:3000/test/inject \
  -H "Content-Type: application/json" \
  -d '{"type": "dns", "duration": 30}'
```

### Authentication Failures
```bash
# Test invalid API keys
curl -X POST http://localhost:3000/test/inject \
  -H "Content-Type: application/json" \
  -d '{"type": "auth", "duration": 120}'
```

### Memory Pressure Tests
```bash
# Simulate out-of-memory conditions
curl -X POST http://localhost:3000/test/inject \
  -H "Content-Type: application/json" \
  -d '{"type": "memory", "duration": 90}'
```

### Latency Injection
```bash
# Add artificial delays
curl -X POST http://localhost:3000/test/inject \
  -H "Content-Type: application/json" \
  -d '{"type": "latency", "delay": 5000, "duration": 60}'
```

## 🔄 Circuit Breaker Testing

### Test Circuit States
```bash
# Check circuit breaker status
curl http://localhost:3000/test/circuit

# Force circuit to open
curl -X POST http://localhost:3000/test/circuit/open

# Force circuit to close
curl -X POST http://localhost:3000/test/circuit/close

# Reset circuit breaker
curl -X POST http://localhost:3000/test/circuit/reset
```

### Circuit Breaker Scenarios
```bash
# Test automatic opening
npm run test:circuit-open

# Test recovery behavior
npm run test:circuit-recovery

# Test half-open state
npm run test:circuit-half-open
```

## 📈 Performance Testing

### Baseline Performance
```bash
# Establish baseline metrics
npm run test:baseline

# Compare current vs baseline
npm run test:performance-regression
```

### Memory Usage Testing
```bash
# Monitor memory during load
npm run test:memory-usage

# Test for memory leaks
npm run test:memory-leaks
```

### Latency Testing
```bash
# Test response times
npm run test:latency

# Test percentile distributions
npm run test:latency-percentiles
```

## 🧪 Integration Testing

### End-to-End Tests
```bash
# Full system test
npm run test:e2e

# Test user workflows
npm run test:user-journey

# Test data flow
npm run test:data-pipeline
```

### API Contract Testing
```bash
# Test API contracts
npm run test:contracts

# Test schema validation
npm run test:schemas

# Test error responses
npm run test:error-handling
```

## 🎯 Test Results Analysis

### Performance Metrics
- **Request Success Rate**: Should be >95% under normal load
- **Average Latency**: Should be <500ms for healthy services  
- **P95 Latency**: Should be <2000ms
- **Circuit Breaker Recovery**: Should recover within 30 seconds

### Failure Scenarios
- **Network Failures**: Circuit should open after 50% failure rate
- **Auth Failures**: Should return 401 with proper error messages
- **Memory Issues**: Should trigger graceful degradation
- **Timeout Handling**: Should fail fast after 5 seconds

## 📊 Monitoring During Tests

### Real-time Monitoring
1. **Open Dashboard**: http://localhost:3000/dashboard
2. **Watch Metrics**: Live charts show test progress
3. **Monitor Logs**: Real-time request logging
4. **Track Circuit State**: Visual circuit breaker status

### Prometheus Metrics
```bash
# View metrics during testing
curl http://localhost:3000/metrics | grep ai_service
```

### Key Metrics to Watch
- `ai_service_requests_total`
- `ai_service_request_duration_seconds`
- `ai_service_circuit_breaker_state`
- `ai_service_errors_total`

## 🛠️ Custom Test Scripts

### Create Custom Load Test
```javascript
// tests/custom-load-test.js
const { loadTest } = require('../src/testing/load-tester');

const config = {
  requests: 200,
  concurrency: 8,
  duration: 180, // seconds
  endpoints: ['/ai'],
  payload: { message: 'Custom test message' }
};

loadTest(config);
```

### Create Failure Injection Test
```javascript
// tests/custom-chaos-test.js
const { injectFailure } = require('../src/testing/failure-injector');

const scenarios = [
  { type: 'network', duration: 60 },
  { type: 'latency', delay: 3000, duration: 120 },
  { type: 'auth', duration: 90 }
];

scenarios.forEach(scenario => {
  setTimeout(() => injectFailure(scenario), Math.random() * 60000);
});
```

## 🚨 Troubleshooting Tests

### Common Issues

**Tests Failing Unexpectedly**
```bash
# Check service health first
npm run health-check

# Verify Docker containers
docker ps

# Check logs
docker logs ai-resilience-monitor
```

**High Error Rates**
```bash
# Check circuit breaker state
curl http://localhost:3000/test/circuit

# Reset if needed
curl -X POST http://localhost:3000/test/circuit/reset
```

**Slow Test Performance**
```bash
# Check system resources
docker stats

# Reduce concurrency
npm run load-test -- --concurrency 2
```

## 📋 Test Checklists

### Pre-deployment Checklist
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Load test meets performance targets
- [ ] Circuit breaker functions correctly
- [ ] Failure injection scenarios covered
- [ ] Recovery mechanisms validated

### Post-deployment Checklist
- [ ] Health checks passing
- [ ] Metrics collection working
- [ ] Dashboard accessible
- [ ] Alerting configured
- [ ] Performance within SLA

---

🎯 **Testing Best Practices**
- Run tests in isolated environments
- Use realistic data volumes
- Test failure scenarios regularly
- Monitor resource usage during tests
- Document test results and patterns

Need help with testing? [Open an issue](https://github.com/Reevsay/ai-resilience-monitor/issues) or check our [main documentation](../README.md).
