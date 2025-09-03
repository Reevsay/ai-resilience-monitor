const express = require('express');
const axios = require('axios');
const CircuitBreaker = require('opossum');
const path = require('path');
const MultiAIService = require('./multiAIService');
const { 
  shouldInject, 
  injectDelay, 
  corruptData,
  injectNetworkError,
  injectMemoryError,
  injectAuthError,
  injectRateLimitError,
  injectPartialResponse,
  injectSlowResponse
} = require('./failureInjector');
const client = require('prom-client');

// Collect default metrics for Prometheus
client.collectDefaultMetrics();

const app = express();
const port = process.env.PORT || 3000;

// AI service call function with REAL AI APIs
async function callAIService(reqData) {
  // If in test mode, return request data as echo and skip real API call
  if (process.env.TEST_MODE === 'true') return { echo: reqData };
  
  // Initialize Multi-AI Service
  const multiAI = new MultiAIService();
  
  // Extract message from request
  const message = reqData.message || reqData.prompt || reqData.query || JSON.stringify(reqData);
  
  // Get preferred service from request or environment
  const preferredService = reqData.preferredService || process.env.PREFERRED_AI_SERVICE;
  
  // Call the multi-AI service
  const response = await multiAI.callAI(message, preferredService);
  
  return response;
}

// Circuit breaker options
const options = {
  timeout: 5000, // If service doesn't respond in 5 seconds, trigger a failure
  errorThresholdPercentage: 50, // When 50% of requests fail, open the circuit
  resetTimeout: 30000 // After 30 seconds, try again.
};

// Failure injection configuration (rates between 0 and 1)
const FAIL_RATE = parseFloat(process.env.FAIL_RATE) || 0;
const DELAY_RATE = parseFloat(process.env.DELAY_RATE) || 0;
const MIN_DELAY = parseInt(process.env.MIN_DELAY, 10) || 0;
const MAX_DELAY = parseInt(process.env.MAX_DELAY, 10) || 0;
const CORRUPT_RATE = parseFloat(process.env.CORRUPT_RATE) || 0;

// Wrapper around real AI call to inject failures, delays, and corruptions
async function unreliableAIService(reqData) {
  if (shouldInject(FAIL_RATE)) throw new Error('Injected failure');
  if (shouldInject(DELAY_RATE)) await injectDelay(MIN_DELAY, MAX_DELAY);
  const result = await callAIService(reqData);
  return corruptData(result, CORRUPT_RATE);
}

const breaker = new CircuitBreaker(unreliableAIService, options);

// Fallback function
breaker.fallback(() => ({ message: 'AI service is currently unavailable. Please try again later.' }));
// Prometheus metrics definitions
const requestCounter = new client.Counter({ name: 'ai_requests_total', help: 'Total AI requests' });
const fallbackCounter = new client.Counter({ name: 'ai_fallbacks_total', help: 'Total fallback invocations' });
const failureCounter = new client.Counter({ name: 'ai_failures_total', help: 'Total AI call failures' });
const latencyHistogram = new client.Histogram({ name: 'ai_request_latency_ms', help: 'Latency in ms', buckets: [50,100,200,500,1000,2000,5000] });
const circuitStateGauge = new client.Gauge({ name: 'ai_circuit_state', help: 'Circuit state: 0 closed, 1 open, 2 half-open' });
// Opossum event handlers to update metrics
breaker.on('success', () => requestCounter.inc());
breaker.on('failure', () => failureCounter.inc());
breaker.on('fallback', () => fallbackCounter.inc());
breaker.on('timeout', () => failureCounter.inc());
breaker.on('open', () => circuitStateGauge.set(1));
breaker.on('halfOpen', () => circuitStateGauge.set(2));
breaker.on('close', () => circuitStateGauge.set(0));

app.use(express.json());

// Enable CORS for dashboard
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

// Test endpoint
app.get('/test', (req, res) => {
  res.json({ message: 'Server is working', timestamp: new Date().toISOString() });
});

// Serve NEW dashboard 
const newDashboardPath = path.resolve(__dirname, 'new-dashboard.html');

app.get('/', (req, res) => {
  console.log('Serving NEW dashboard from:', newDashboardPath);
  res.sendFile(newDashboardPath, {
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    }
  });
});

app.get('/dashboard', (req, res) => {
  console.log('Serving NEW dashboard from:', newDashboardPath);
  res.sendFile(newDashboardPath, {
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    }
  });
});

app.post('/ai', async (req, res) => {
  // Track request count and latency
  const endTimer = latencyHistogram.startTimer();
  try {
    const result = await breaker.fire(req.body);
    endTimer();
    res.json(result);
  } catch (err) {
    endTimer();
    res.status(500).json({ error: 'Internal error' });
  }
});

// AI Service Health Check
app.get('/ai/health', async (req, res) => {
  try {
    const multiAI = new MultiAIService();
    const healthStatus = await multiAI.checkServiceHealth();
    
    res.json({
      status: "healthy",
      services: healthStatus,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({
      status: "error",
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// AI Service with specific provider
app.post('/ai/:provider', async (req, res) => {
  try {
    const { provider } = req.params;
    const reqData = { ...req.body, preferredService: provider };
    
    const start = Date.now();
    const result = await breaker.fire(reqData);
    const latency = Date.now() - start;
    
    latencyHistogram.observe(latency);
    
    res.json({
      ...result,
      latency: `${latency}ms`,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    failureCounter.inc();
    res.status(500).json({ 
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Expose Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

app.listen(port, () => console.log(`AI proxy listening on port ${port}`));
