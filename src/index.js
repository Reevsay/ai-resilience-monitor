// Global error handlers for diagnostics
process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  process.exit(1);
});
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});
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
  resetTimeout: 30000, // After 30 seconds, try again.
  // Make circuit reactive for demos; can be overridden via env
  volumeThreshold: parseInt(process.env.CIRCUIT_VOLUME_THRESHOLD, 10) || 2
};

// Failure injection configuration (rates between 0 and 1)
let FAIL_RATE = parseFloat(process.env.FAIL_RATE) || 0;
let DELAY_RATE = parseFloat(process.env.DELAY_RATE) || 0;
let MIN_DELAY = parseInt(process.env.MIN_DELAY, 10) || 0;
let MAX_DELAY = parseInt(process.env.MAX_DELAY, 10) || 0;
let CORRUPT_RATE = parseFloat(process.env.CORRUPT_RATE) || 0;
let NETWORK_ERROR_RATE = parseFloat(process.env.NETWORK_ERROR_RATE) || 0;
let MEMORY_ERROR_RATE = parseFloat(process.env.MEMORY_ERROR_RATE) || 0;
let AUTH_ERROR_RATE = parseFloat(process.env.AUTH_ERROR_RATE) || 0;
let RATE_LIMIT_ERROR_RATE = parseFloat(process.env.RATE_LIMIT_ERROR_RATE) || 0;
let PARTIAL_RESPONSE_RATE = parseFloat(process.env.PARTIAL_RESPONSE_RATE) || 0;
let SLOW_RESPONSE_RATE = parseFloat(process.env.SLOW_RESPONSE_RATE) || 0;

// Wrapper around real AI call to inject failures, delays, and corruptions
async function unreliableAIService(reqData) {
  // Optionally inject various failures for demo/testing
  if (shouldInject(FAIL_RATE)) throw new Error('Injected failure');
  if (shouldInject(NETWORK_ERROR_RATE)) await injectNetworkError();
  if (shouldInject(MEMORY_ERROR_RATE)) injectMemoryError();
  if (shouldInject(AUTH_ERROR_RATE)) injectAuthError();
  if (shouldInject(RATE_LIMIT_ERROR_RATE)) injectRateLimitError();
  if (shouldInject(PARTIAL_RESPONSE_RATE)) injectPartialResponse();
  if (shouldInject(SLOW_RESPONSE_RATE)) await injectSlowResponse();
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
// Initialize circuit state to closed on startup so metric is present
circuitStateGauge.set(0);
// Opossum event handlers to update metrics
breaker.on('fire', () => requestCounter.inc());
breaker.on('success', () => {});
breaker.on('failure', () => failureCounter.inc());
breaker.on('fallback', () => fallbackCounter.inc());
breaker.on('timeout', () => failureCounter.inc());
breaker.on('reject', () => failureCounter.inc()); // rejected due to open circuit
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

// Serve ENHANCED dashboard (primary UI)
const enhancedDashboardPath = path.resolve(__dirname, 'enhanced-dashboard.html');

app.get('/', (req, res) => {
  console.log('Serving ENHANCED dashboard from:', enhancedDashboardPath);
  res.sendFile(enhancedDashboardPath, {
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    }
  });
});

app.get('/dashboard', (req, res) => {
  console.log('Serving ENHANCED dashboard from:', enhancedDashboardPath);
  res.sendFile(enhancedDashboardPath, {
    headers: {
      'Cache-Control': 'no-cache, no-store, must-revalidate',
      'Pragma': 'no-cache',
      'Expires': '0'
    }
  });
});

// Runtime configuration endpoints (for demo/testing)
app.get('/config', (req, res) => {
  res.json({
    testMode: process.env.TEST_MODE === 'true',
    failureConfig: {
      FAIL_RATE,
      DELAY_RATE,
      MIN_DELAY,
      MAX_DELAY,
      CORRUPT_RATE,
      NETWORK_ERROR_RATE,
      MEMORY_ERROR_RATE,
      AUTH_ERROR_RATE,
      RATE_LIMIT_ERROR_RATE,
      PARTIAL_RESPONSE_RATE,
      SLOW_RESPONSE_RATE
    }
  });
});

app.post('/admin/failure-config', (req, res) => {
  try {
    const cfg = req.body || {};
    const clamp01 = (v) => Math.max(0, Math.min(1, Number(v)));
    if (cfg.FAIL_RATE !== undefined) FAIL_RATE = clamp01(cfg.FAIL_RATE);
    if (cfg.DELAY_RATE !== undefined) DELAY_RATE = clamp01(cfg.DELAY_RATE);
    if (cfg.MIN_DELAY !== undefined) MIN_DELAY = Number(cfg.MIN_DELAY) || 0;
    if (cfg.MAX_DELAY !== undefined) MAX_DELAY = Number(cfg.MAX_DELAY) || 0;
    if (cfg.CORRUPT_RATE !== undefined) CORRUPT_RATE = clamp01(cfg.CORRUPT_RATE);
    if (cfg.NETWORK_ERROR_RATE !== undefined) NETWORK_ERROR_RATE = clamp01(cfg.NETWORK_ERROR_RATE);
    if (cfg.MEMORY_ERROR_RATE !== undefined) MEMORY_ERROR_RATE = clamp01(cfg.MEMORY_ERROR_RATE);
    if (cfg.AUTH_ERROR_RATE !== undefined) AUTH_ERROR_RATE = clamp01(cfg.AUTH_ERROR_RATE);
    if (cfg.RATE_LIMIT_ERROR_RATE !== undefined) RATE_LIMIT_ERROR_RATE = clamp01(cfg.RATE_LIMIT_ERROR_RATE);
    if (cfg.PARTIAL_RESPONSE_RATE !== undefined) PARTIAL_RESPONSE_RATE = clamp01(cfg.PARTIAL_RESPONSE_RATE);
    if (cfg.SLOW_RESPONSE_RATE !== undefined) SLOW_RESPONSE_RATE = clamp01(cfg.SLOW_RESPONSE_RATE);

    res.json({ ok: true, failureConfig: { FAIL_RATE, DELAY_RATE, MIN_DELAY, MAX_DELAY, CORRUPT_RATE, NETWORK_ERROR_RATE, MEMORY_ERROR_RATE, AUTH_ERROR_RATE, RATE_LIMIT_ERROR_RATE, PARTIAL_RESPONSE_RATE, SLOW_RESPONSE_RATE } });
  } catch (e) {
    res.status(400).json({ ok: false, error: e.message });
  }
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
