require('dotenv').config();
const express = require('express');
const cors = require('cors');
const axios = require('axios');
const client = require('prom-client');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

// ========== CRITICAL: Global Error Handlers to Prevent Crashes ==========
process.on('unhandledRejection', (reason, promise) => {
  console.error('❌❌❌ [GLOBAL] Unhandled Promise Rejection detected!');
  console.error('[GLOBAL] Reason:', reason);
  console.error('[GLOBAL] Promise:', promise);
  if (reason && reason.stack) {
    console.error('[GLOBAL] Stack trace:', reason.stack);
  }
  // Don't exit - log and continue
});

process.on('uncaughtException', (error) => {
  console.error('❌❌❌ [GLOBAL] Uncaught Exception detected!');
  console.error('[GLOBAL] Error message:', error.message);
  console.error('[GLOBAL] Error name:', error.name);
  console.error('[GLOBAL] Stack trace:', error.stack);
  // Don't exit - log and continue
});

process.on('warning', (warning) => {
  console.warn('⚠️ [GLOBAL] Node.js warning:', warning.name);
  console.warn('[GLOBAL] Warning message:', warning.message);
  console.warn('[GLOBAL] Stack trace:', warning.stack);
});

const app = express();
const PORT = process.env.PORT || 3000;

// ========== Database Setup for Persistent Metrics ==========
const DB_PATH = path.join(__dirname, '..', 'data', 'monitoring.db');

// Ensure data directory exists
const dataDir = path.join(__dirname, '..', 'data');
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// Initialize SQLite database with WAL mode for better concurrent access
const db = new sqlite3.Database(DB_PATH, (err) => {
  if (err) {
    console.error('❌ Database connection error:', err);
  } else {
    console.log('✅ Connected to SQLite database:', DB_PATH);
  }
});

// Enable WAL mode for better concurrent access (critical for multi-process access)
db.run('PRAGMA journal_mode = WAL;', (err) => {
  if (err) {
    console.error('❌ Failed to enable WAL mode:', err);
  } else {
    console.log('✅ WAL mode enabled for concurrent access');
  }
});

// Set busy timeout to handle locks gracefully
db.run('PRAGMA busy_timeout = 5000;', (err) => {
  if (err) {
    console.error('❌ Failed to set busy timeout:', err);
  } else {
    console.log('✅ Busy timeout set to 5000ms');
  }
});

// Create cumulative_metrics table for persistent counters
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS cumulative_metrics (
      key TEXT PRIMARY KEY,
      value INTEGER DEFAULT 0,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  
  // Initialize totalRequests counter if not exists
  db.run(`
    INSERT OR IGNORE INTO cumulative_metrics (key, value) 
    VALUES ('totalRequests', 0)
  `);
  
  console.log('✅ Database tables initialized');
});

// Helper: Get cumulative metric from database
function getCumulativeMetric(key) {
  return new Promise((resolve, reject) => {
    db.get('SELECT value FROM cumulative_metrics WHERE key = ?', [key], (err, row) => {
      if (err) reject(err);
      else resolve(row ? row.value : 0);
    });
  });
}

// Helper: Increment cumulative metric in database
function incrementCumulativeMetric(key, amount = 1) {
  return new Promise((resolve, reject) => {
    db.run(
      'UPDATE cumulative_metrics SET value = value + ?, updated_at = CURRENT_TIMESTAMP WHERE key = ?',
      [amount, key],
      function(err) {
        if (err) reject(err);
        else resolve(this.changes);
      }
    );
  });
}

// Helper: Reset cumulative metric in database
function resetCumulativeMetric(key) {
  return new Promise((resolve, reject) => {
    db.run(
      'UPDATE cumulative_metrics SET value = 0, updated_at = CURRENT_TIMESTAMP WHERE key = ?',
      [key],
      function(err) {
        if (err) reject(err);
        else resolve(this.changes);
      }
    );
  });
}
// =============================================================

// API Configuration from environment variables
const API_KEYS = {
  google: process.env.GOOGLE_API_KEY,
  cohere: process.env.COHERE_API_KEY,
  huggingface: process.env.HUGGINGFACE_API_KEY
};

const API_URLS = {
  google: process.env.GOOGLE_API_URL || 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
  cohere: process.env.COHERE_API_URL || 'https://api.cohere.ai/v1/generate',
  huggingface: process.env.HUGGINGFACE_API_URL || 'https://api-inference.huggingface.co/models/gpt2'
};

// DEBUG: Log ALL incoming requests FIRST - before any parsing or CORS
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[RAW-REQUEST] ${req.method} ${req.url}`);
  next();
});

// Enable CORS for all routes
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Increase body size limit - default is 100kb which might be too small
app.use(express.json({ limit: '10mb' }));

// Log after successful parsing
app.use((req, res, next) => {
  const timestamp = new Date().toISOString();
  console.log(`[PARSED-REQUEST] ${req.method} ${req.url}`);
  
  // Set timeout for all requests to prevent hanging
  req.setTimeout(15000, () => {
    console.error(`[REQUEST-TIMEOUT] Request timed out after 15s: ${req.method} ${req.url}`);
  });
  
  next();
});

// Prometheus metrics setup
const register = new client.Registry();
client.collectDefaultMetrics({ register });

const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'status_code'],
  registers: [register]
});

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request latency',
  labelNames: ['method', 'status_code'],
  registers: [register]
});

// In-memory metrics storage
const metricsHistory = {
  totalRequests: 0,
  successfulRequests: 0,
  failedRequests: 0,
  totalLatency: 0,
  startTime: Date.now(),
  aiServices: {
    gemini: { requests: 0, failures: 0, totalLatency: 0, lastCheck: null, status: 'unknown' },
    cohere: { requests: 0, failures: 0, totalLatency: 0, lastCheck: null, status: 'unknown' },
    huggingface: { requests: 0, failures: 0, totalLatency: 0, lastCheck: null, status: 'unknown' }
  }
};

// Chaos Engineering State
const activeChaos = {
  gemini: { type: null, intensity: 0, endTime: null, startTime: null },
  cohere: { type: null, intensity: 0, endTime: null, startTime: null },
  huggingface: { type: null, intensity: 0, endTime: null, startTime: null }
};

// Chaos Engineering Middleware
async function applyChaosToRequest(service) {
  const chaos = activeChaos[service];
  
  // Check if chaos is active and not expired
  if (!chaos || !chaos.type || !chaos.endTime) {
    return; // No chaos active
  }
  
  if (Date.now() > chaos.endTime) {
    // Chaos expired, clear it
    chaos.type = null;
    chaos.intensity = 0;
    chaos.endTime = null;
    chaos.startTime = null;
    console.log(`🔵 Chaos experiment expired for ${service}`);
    return;
  }
  
  const { type, intensity } = chaos;
  
  console.log(`🔥 Applying chaos to ${service}: ${type} (${intensity}% intensity)`);
  
  switch (type) {
    case 'latency':
      // Inject artificial delay (intensity = milliseconds, 0-10000)
      const delay = Math.min(intensity, 10000);
      await new Promise(resolve => setTimeout(resolve, delay));
      console.log(`   ⏱️  Added ${delay}ms latency`);
      break;
      
    case 'failure':
      // Force request to fail (intensity = failure rate 0-100%)
      const failureChance = Math.random() * 100;
      if (failureChance < intensity) {
        console.log(`   ❌ Forcing request failure (${intensity}% rate)`);
        throw new Error(`Chaos: Simulated ${service} failure`);
      }
      break;
      
    case 'timeout':
      // Simulate timeout by hanging (intensity = hang duration in ms)
      const hangTime = Math.min(intensity * 30, 3000); // Max 3s (reduced to prevent backend hang)
      console.log(`   ⏱️  Hanging request for ${hangTime}ms`);
      await new Promise(resolve => setTimeout(resolve, hangTime));
      throw new Error(`Chaos: Request timeout for ${service}`);
      
    case 'intermittent':
      // Random failures (intensity = failure rate 0-100%)
      if (Math.random() * 100 < intensity) {
        console.log(`   🎲 Intermittent failure triggered (${intensity}% rate)`);
        throw new Error(`Chaos: Intermittent failure for ${service}`);
      }
      break;
      
    case 'unavailable':
      // Service completely unavailable
      console.log(`   🚫 Service marked as unavailable`);
      throw new Error(`Chaos: ${service} is unavailable`);
      
    case 'corruption':
      // This will be handled by returning corrupted data after the API call
      console.log(`   🔀 Response corruption will be applied`);
      break;
      
    default:
      console.log(`   ⚠️  Unknown chaos type: ${type}`);
  }
}

// Enhanced Circuit Breaker Implementation with Half-Open State
class CircuitBreaker {
  constructor(name, options = {}) {
    this.name = name;
    this.failureThreshold = options.failureThreshold || 5;      // Failures before opening
    this.successThreshold = options.successThreshold || 2;       // Successes in half-open to close
    this.timeout = options.timeout || 30000;                     // Time before trying half-open (30s)
    this.halfOpenTimeout = options.halfOpenTimeout || 10000;     // Max time in half-open (10s)
    
    // State tracking
    this.state = 'CLOSED';                    // CLOSED, OPEN, HALF_OPEN
    this.failureCount = 0;
    this.successCount = 0;
    this.consecutiveSuccesses = 0;
    this.lastFailureTime = null;
    this.lastStateChange = Date.now();
    this.stateHistory = [];
    
    // Metrics
    this.metrics = {
      totalCalls: 0,
      successfulCalls: 0,
      failedCalls: 0,
      rejectedCalls: 0,                       // Rejected due to open circuit
      stateTransitions: {
        'CLOSED->OPEN': 0,
        'OPEN->HALF_OPEN': 0,
        'HALF_OPEN->CLOSED': 0,
        'HALF_OPEN->OPEN': 0
      },
      timeInStates: {
        CLOSED: 0,
        OPEN: 0,
        HALF_OPEN: 0
      },
      lastTransitionTime: null
    };
  }

  async call(fn) {
    this.metrics.totalCalls++;

    // Check if circuit should transition from OPEN to HALF_OPEN
    if (this.state === 'OPEN') {
      const timeSinceLastFailure = Date.now() - this.lastFailureTime;
      if (timeSinceLastFailure >= this.timeout) {
        this.transitionTo('HALF_OPEN');
      } else {
        this.metrics.rejectedCalls++;
        const waitTime = Math.ceil((this.timeout - timeSinceLastFailure) / 1000);
        throw new Error(`⛔ Circuit breaker [${this.name}] is OPEN. Retry in ${waitTime}s`);
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.metrics.successfulCalls++;
    this.consecutiveSuccesses++;
    
    if (this.state === 'HALF_OPEN') {
      if (this.consecutiveSuccesses >= this.successThreshold) {
        // Enough successes in half-open, close the circuit
        this.transitionTo('CLOSED');
        this.failureCount = 0;
        this.consecutiveSuccesses = 0;
      }
    } else if (this.state === 'CLOSED') {
      // Reset failure count on success
      this.failureCount = 0;
    }
  }

  onFailure() {
    this.metrics.failedCalls++;
    this.failureCount++;
    this.consecutiveSuccesses = 0;
    this.lastFailureTime = Date.now();

    if (this.state === 'HALF_OPEN') {
      // Any failure in half-open immediately reopens circuit
      this.transitionTo('OPEN');
    } else if (this.state === 'CLOSED') {
      // Check if threshold reached
      if (this.failureCount >= this.failureThreshold) {
        this.transitionTo('OPEN');
      }
    }
  }

  transitionTo(newState) {
    const oldState = this.state;
    if (oldState === newState) return;

    // Record time spent in old state
    const timeInState = Date.now() - this.lastStateChange;
    this.metrics.timeInStates[oldState] += timeInState;

    // Transition
    this.state = newState;
    this.lastStateChange = Date.now();
    this.metrics.lastTransitionTime = this.lastStateChange;

    // Record transition
    const transition = `${oldState}->${newState}`;
    if (this.metrics.stateTransitions[transition] !== undefined) {
      this.metrics.stateTransitions[transition]++;
    }

    // Add to history
    this.stateHistory.push({
      from: oldState,
      to: newState,
      timestamp: this.lastStateChange,
      reason: this.getTransitionReason(oldState, newState)
    });

    // Keep only last 10 transitions
    if (this.stateHistory.length > 10) {
      this.stateHistory.shift();
    }

    console.log(`🔄 Circuit Breaker [${this.name}]: ${oldState} -> ${newState} (${this.getTransitionReason(oldState, newState)})`);
  }

  getTransitionReason(from, to) {
    if (from === 'CLOSED' && to === 'OPEN') {
      return `Failure threshold reached (${this.failureCount}/${this.failureThreshold})`;
    } else if (from === 'OPEN' && to === 'HALF_OPEN') {
      return `Timeout expired (${this.timeout}ms), testing recovery`;
    } else if (from === 'HALF_OPEN' && to === 'CLOSED') {
      return `Success threshold reached (${this.consecutiveSuccesses}/${this.successThreshold})`;
    } else if (from === 'HALF_OPEN' && to === 'OPEN') {
      return `Failure during recovery test`;
    }
    return 'Unknown';
  }

  getStatus() {
    const currentTime = Date.now();
    const timeInCurrentState = currentTime - this.lastStateChange;
    
    return {
      name: this.name,
      state: this.state,
      failureCount: this.failureCount,
      consecutiveSuccesses: this.consecutiveSuccesses,
      failureThreshold: this.failureThreshold,
      successThreshold: this.successThreshold,
      timeInCurrentState: timeInCurrentState,
      lastFailureTime: this.lastFailureTime,
      metrics: {
        ...this.metrics,
        successRate: this.metrics.totalCalls > 0 
          ? ((this.metrics.successfulCalls / this.metrics.totalCalls) * 100).toFixed(2) 
          : 0,
        rejectionRate: this.metrics.totalCalls > 0
          ? ((this.metrics.rejectedCalls / this.metrics.totalCalls) * 100).toFixed(2)
          : 0
      },
      stateHistory: this.stateHistory.slice(-5) // Last 5 transitions
    };
  }

  reset() {
    this.state = 'CLOSED';
    this.failureCount = 0;
    this.consecutiveSuccesses = 0;
    this.lastFailureTime = null;
    this.lastStateChange = Date.now();
    console.log(`🔄 Circuit Breaker [${this.name}]: Manual reset`);
  }
}

const circuitBreakers = {
  gemini: new CircuitBreaker('Gemini', {
    failureThreshold: 3,      // Open after 3 failures
    successThreshold: 2,       // Close after 2 successes in half-open
    timeout: 20000,            // Wait 20s before trying half-open
    halfOpenTimeout: 10000     // Max 10s in half-open state
  }),
  cohere: new CircuitBreaker('Cohere', {
    failureThreshold: 3,
    successThreshold: 2,
    timeout: 20000,
    halfOpenTimeout: 10000
  }),
  huggingface: new CircuitBreaker('HuggingFace', {
    failureThreshold: 3,
    successThreshold: 2,
    timeout: 20000,
    halfOpenTimeout: 10000
  })
};

// Helper function to calculate metrics
function calculateMetrics() {
  const successRate = metricsHistory.totalRequests > 0 
    ? (metricsHistory.successfulRequests / metricsHistory.totalRequests) * 100 
    : 100;
  
  const avgLatency = metricsHistory.successfulRequests > 0 
    ? metricsHistory.totalLatency / metricsHistory.successfulRequests 
    : 0;

  return {
    totalRequests: metricsHistory.totalRequests,
    successfulRequests: metricsHistory.successfulRequests,
    failedRequests: metricsHistory.failedRequests,
    successRate: Math.round(successRate * 10) / 10,
    avgLatency: Math.round(avgLatency),
    uptime: Date.now() - metricsHistory.startTime,
    aiServices: Object.keys(metricsHistory.aiServices).reduce((acc, service) => {
      const serviceData = metricsHistory.aiServices[service];
      const successCount = serviceData.requests - serviceData.failures;
      acc[service] = {
        requests: serviceData.requests,
        failures: serviceData.failures,
        successRate: serviceData.requests > 0 
          ? Math.round(((serviceData.requests - serviceData.failures) / serviceData.requests) * 100 * 10) / 10
          : 100,
        avgLatency: successCount > 0 && serviceData.totalLatency > 0
          ? Math.round(serviceData.totalLatency / successCount)
          : 0,
        status: serviceData.failures > 5 ? 'degraded' : (serviceData.status || 'unknown'),
        lastCheck: serviceData.lastCheck
      };
      return acc;
    }, {})
  };
}

// Real AI API Integration Functions
async function callGemini(prompt) {
  if (!API_KEYS.google || API_KEYS.google === 'your_google_api_key_here') {
    throw new Error('Google API key not configured');
  }

  const response = await axios.post(`${API_URLS.google}?key=${API_KEYS.google}`, {
    contents: [{ parts: [{ text: prompt }] }]
  }, {
    headers: { 'Content-Type': 'application/json' },
    timeout: 10000
  });

  return response.data.candidates[0].content.parts[0].text;
}

async function callCohere(prompt) {
  if (!API_KEYS.cohere || API_KEYS.cohere === 'your_cohere_api_key_here') {
    throw new Error('Cohere API key not configured');
  }

  const response = await axios.post(API_URLS.cohere, {
    model: 'command',
    prompt: prompt,
    max_tokens: 100
  }, {
    headers: {
      'Authorization': `Bearer ${API_KEYS.cohere}`,
      'Content-Type': 'application/json'
    },
    timeout: 10000
  });

  return response.data.generations[0].text;
}

async function callHuggingFace(prompt) {
  if (!API_KEYS.huggingface || API_KEYS.huggingface === 'your_huggingface_api_key_here') {
    throw new Error('Hugging Face API key not configured');
  }

  const response = await axios.post(API_URLS.huggingface, {
    inputs: prompt,
    parameters: { max_length: 100 }
  }, {
    headers: {
      'Authorization': `Bearer ${API_KEYS.huggingface}`,
      'Content-Type': 'application/json'
    },
    timeout: 10000
  });

  return response.data[0].generated_text;
}

// AI Service Health Check Functions
async function checkGeminiHealth() {
  try {
    const start = Date.now();
    
    if (!API_KEYS.google || API_KEYS.google === 'your_google_api_key_here') {
      await new Promise(resolve => setTimeout(resolve, Math.random() * 300 + 100));
      const latency = Date.now() - start;
      metricsHistory.aiServices.gemini.lastCheck = new Date().toISOString();
      metricsHistory.aiServices.gemini.status = 'not_configured';
      return { status: 'not_configured', latency };
    }

    // Real API health check - simple request to check API availability
    await axios.get(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro?key=${API_KEYS.google}`, {
      timeout: 5000
    });

    const latency = Date.now() - start;
    metricsHistory.aiServices.gemini.lastCheck = new Date().toISOString();
    metricsHistory.aiServices.gemini.status = 'healthy';
    return { status: 'healthy', latency };
  } catch (error) {
    metricsHistory.aiServices.gemini.status = 'error';
    throw error;
  }
}

async function checkCohereHealth() {
  try {
    const start = Date.now();
    
    if (!API_KEYS.cohere || API_KEYS.cohere === 'your_cohere_api_key_here') {
      await new Promise(resolve => setTimeout(resolve, Math.random() * 250 + 75));
      const latency = Date.now() - start;
      metricsHistory.aiServices.cohere.lastCheck = new Date().toISOString();
      metricsHistory.aiServices.cohere.status = 'not_configured';
      return { status: 'not_configured', latency };
    }

    // Real API health check
    await axios.get('https://api.cohere.ai/v1/models', {
      headers: { 'Authorization': `Bearer ${API_KEYS.cohere}` },
      timeout: 5000
    });

    const latency = Date.now() - start;
    metricsHistory.aiServices.cohere.lastCheck = new Date().toISOString();
    metricsHistory.aiServices.cohere.status = 'healthy';
    return { status: 'healthy', latency };
  } catch (error) {
    metricsHistory.aiServices.cohere.status = 'error';
    throw error;
  }
}

async function checkHuggingFaceHealth() {
  try {
    const start = Date.now();
    
    if (!API_KEYS.huggingface || API_KEYS.huggingface === 'your_huggingface_api_key_here') {
      await new Promise(resolve => setTimeout(resolve, Math.random() * 400 + 150));
      const latency = Date.now() - start;
      metricsHistory.aiServices.huggingface.lastCheck = new Date().toISOString();
      metricsHistory.aiServices.huggingface.status = 'not_configured';
      return { status: 'not_configured', latency };
    }

    // Real API health check
    await axios.post('https://api-inference.huggingface.co/models/gpt2', 
      { inputs: 'health check' },
      { 
        headers: { 'Authorization': `Bearer ${API_KEYS.huggingface}` },
        timeout: 5000 
      }
    );

    const latency = Date.now() - start;
    metricsHistory.aiServices.huggingface.lastCheck = new Date().toISOString();
    metricsHistory.aiServices.huggingface.status = 'healthy';
    return { status: 'healthy', latency };
  } catch (error) {
    metricsHistory.aiServices.huggingface.status = 'error';
    throw error;
  }
}

// Middleware for request tracking
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    const statusCode = res.statusCode.toString();
    
    httpRequestsTotal.inc({ method: req.method, status_code: statusCode });
    httpRequestDuration.observe({ method: req.method, status_code: statusCode }, duration / 1000);
  });
  
  next();
});

// API Endpoints

// Health check endpoint - EXCLUDED from chaos injection for monitoring stability
app.get('/test', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    uptime: Date.now() - metricsHistory.startTime,
    chaos_active: Object.keys(activeChaos).some(service => activeChaos[service].type !== null)
  });
});

// Get current metrics
app.get('/metrics', async (req, res) => {
  try {
    // Get cumulative total from database
    const cumulativeTotalRequests = await getCumulativeMetric('totalRequests');
    
    const metrics = calculateMetrics();
    
    // Override with database count for accurate cumulative total
    metrics.totalRequests = cumulativeTotalRequests;
    
    res.json(metrics);
  } catch (error) {
    console.error('Error calculating metrics:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Circuit Breaker Status Endpoint
app.get('/circuit-breaker/status', (req, res) => {
  try {
    const status = {
      gemini: circuitBreakers.gemini.getStatus(),
      cohere: circuitBreakers.cohere.getStatus(),
      huggingface: circuitBreakers.huggingface.getStatus()
    };
    res.json(status);
  } catch (error) {
    console.error('Error getting circuit breaker status:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Reset Circuit Breaker Endpoint
app.post('/circuit-breaker/reset', (req, res) => {
  try {
    const { service } = req.body;
    
    if (service && circuitBreakers[service]) {
      circuitBreakers[service].reset();
      res.json({ 
        success: true, 
        message: `Circuit breaker for ${service} reset successfully`,
        state: circuitBreakers[service].state
      });
    } else if (!service) {
      // Reset all circuit breakers
      Object.values(circuitBreakers).forEach(cb => cb.reset());
      res.json({ 
        success: true, 
        message: 'All circuit breakers reset successfully'
      });
    } else {
      res.status(400).json({ error: 'Invalid service name' });
    }
  } catch (error) {
    console.error('Error resetting circuit breaker:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Rig Current Metrics Endpoint - Inject ~10% failures into existing data
app.post('/metrics/rig', (req, res) => {
  try {
    const { errorPercentage = 10 } = req.body;
    const errorRate = errorPercentage / 100;
    
    console.log(`🎲 Rigging current metrics with ${errorPercentage}% error rate...`);
    
    const riggedServices = [];
    
    // Rig each service that has requests
    Object.keys(metricsHistory.aiServices).forEach(service => {
      const serviceData = metricsHistory.aiServices[service];
      
      if (serviceData.requests > 0) {
        // Calculate how many failures to inject based on current requests
        const targetFailures = Math.floor(serviceData.requests * errorRate);
        const failuresToAdd = Math.max(0, targetFailures - serviceData.failures);
        
        // Add failures
        serviceData.failures += failuresToAdd;
        
        // Update total failed requests
        metricsHistory.failedRequests += failuresToAdd;
        metricsHistory.successfulRequests -= failuresToAdd;
        
        // Set status to degraded if failures > 5
        serviceData.status = serviceData.failures > 5 ? 'degraded' : 'healthy';
        
        riggedServices.push({
          service,
          totalRequests: serviceData.requests,
          failures: serviceData.failures,
          failureRate: ((serviceData.failures / serviceData.requests) * 100).toFixed(1) + '%'
        });
        
        console.log(`   📊 ${service}: ${serviceData.requests} requests, ${serviceData.failures} failures (${((serviceData.failures / serviceData.requests) * 100).toFixed(1)}%)`);
      }
    });
    
    console.log('✅ Metrics rigged successfully');
    
    res.json({
      success: true,
      message: `Metrics rigged with ${errorPercentage}% error rate`,
      services: riggedServices,
      totalRequests: metricsHistory.totalRequests,
      totalFailures: metricsHistory.failedRequests,
      overallFailureRate: ((metricsHistory.failedRequests / metricsHistory.totalRequests) * 100).toFixed(1) + '%'
    });
  } catch (error) {
    console.error('Error rigging metrics:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Reset All Metrics Endpoint
app.post('/metrics/reset', async (req, res) => {
  try {
    // Reset all metrics to initial state
    metricsHistory.totalRequests = 0;
    metricsHistory.successfulRequests = 0;
    metricsHistory.failedRequests = 0;
    metricsHistory.totalLatency = 0;
    metricsHistory.startTime = Date.now();
    
    // IMPORTANT: Reset cumulative counter in database
    await resetCumulativeMetric('totalRequests');
    
    // Reset AI service metrics
    Object.keys(metricsHistory.aiServices).forEach(service => {
      metricsHistory.aiServices[service] = {
        requests: 0,
        failures: 0,
        totalLatency: 0,
        lastCheck: null,
        status: 'unknown'
      };
    });
    
    // Reset circuit breakers
    Object.values(circuitBreakers).forEach(cb => cb.reset());
    
    // Clear chaos experiments
    Object.keys(activeChaos).forEach(service => {
      activeChaos[service] = {
        type: null,
        intensity: 0,
        endTime: null,
        startTime: null
      };
    });
    
    console.log('🔄 All metrics and data have been reset (including database)');
    
    res.json({ 
      success: true, 
      message: 'All metrics, circuit breakers, and chaos experiments have been reset successfully'
    });
  } catch (error) {
    console.error('Error resetting metrics:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// AI service health check
app.get('/ai/health', async (req, res) => {
  try {
    const healthChecks = await Promise.allSettled([
      circuitBreakers.gemini.call(() => checkGeminiHealth()),
      circuitBreakers.cohere.call(() => checkCohereHealth()),
      circuitBreakers.huggingface.call(() => checkHuggingFaceHealth())
    ]);

    const services = ['gemini', 'cohere', 'huggingface'];
    const healthStatus = {};

    healthChecks.forEach((result, index) => {
      const serviceName = services[index];
      if (result.status === 'fulfilled') {
        healthStatus[serviceName] = {
          status: 'healthy',
          latency: result.value.latency,
          lastCheck: new Date().toISOString()
        };
      } else {
        healthStatus[serviceName] = {
          status: 'error',
          error: result.reason.message,
          lastCheck: new Date().toISOString()
        };
        metricsHistory.aiServices[serviceName].status = 'error';
      }
    });

    res.json({
      overall: 'healthy',
      services: healthStatus,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Health check error:', error);
    res.status(500).json({ error: 'Health check failed' });
  }
});

// AI service proxy endpoint
app.post('/ai', async (req, res) => {
  const start = Date.now();
  let success = false;
  
  try {
    const { service = 'gemini', prompt, ...options } = req.body;
    
    // Count TOTAL requests at the START (in-memory for current session)
    metricsHistory.totalRequests++;
    
    // ALSO increment cumulative counter in database for persistence
    await incrementCumulativeMetric('totalRequests');
    
    // Count service-specific request at the START
    if (metricsHistory.aiServices[service]) {
      metricsHistory.aiServices[service].requests++;
    }
    
    if (!prompt) {
      // Decrement counters if validation fails before processing
      metricsHistory.totalRequests--;
      await incrementCumulativeMetric('totalRequests', -1); // Decrement in DB too
      if (metricsHistory.aiServices[service]) {
        metricsHistory.aiServices[service].requests--;
      }
      throw new Error('Prompt is required');
    }

    console.log(`🔄 Processing AI request - Service: ${service}, Prompt: "${prompt}"`);

    let aiResponse;
    let isRealAPI = false;

    // Apply chaos engineering BEFORE circuit breaker (chaos should affect circuit breaker)
    await applyChaosToRequest(service);

    // Wrap the entire logic (including fallback) in circuit breaker
    const circuitBreakerLogic = async () => {
      let response;
      let usingRealAPI = false;

      try {
        // Try to use real API first
        switch (service) {
          case 'gemini':
            response = await callGemini(prompt);
            usingRealAPI = true;
            break;
          case 'cohere':
            response = await callCohere(prompt);
            usingRealAPI = true;
            break;
          case 'huggingface':
            response = await callHuggingFace(prompt);
            usingRealAPI = true;
            break;
          default:
            throw new Error(`Unknown service: ${service}`);
        }
        
        // Apply response corruption chaos if active
        if (activeChaos[service]?.type === 'corruption' && Date.now() < activeChaos[service]?.endTime) {
          console.log(`🔀 Corrupting response for ${service}`);
          response = `{CORRUPTED_DATA: ${Math.random()}, original_length: ${response?.length || 0}}`;
        }
      } catch (apiError) {
        // Check if this is a chaos-induced error - if so, let it propagate to circuit breaker
        if (apiError.message.startsWith('Chaos:')) {
          console.log(`🔥 Chaos-induced error detected, propagating: ${apiError.message}`);
          throw apiError; // Re-throw chaos errors to fail properly through circuit breaker
        }
        
        // Check if this is a circuit breaker error - if so, let it propagate
        if (apiError.message.includes('Circuit breaker')) {
          throw apiError; // Don't fallback on circuit breaker rejection
        }
        
        console.log(`⚠️ Real API failed for ${service}: ${apiError.message}, falling back to simulation`);
        
        // Fallback to simulation if real API fails or not configured
        const simulationTime = Math.random() * 2000 + 500; // 500-2500ms
        await new Promise(resolve => setTimeout(resolve, simulationTime));
        
        // 10% simulation failure rate
        if (Math.random() < 0.1) {
          throw new Error(`Simulated ${service} service failure`);
        }
        
        response = `Simulated ${service} response for: "${prompt}"`;
        usingRealAPI = false;
      }

      return { response, usingRealAPI };
    };

    try {
      // Execute through circuit breaker
      let result;
      switch (service) {
        case 'gemini':
          result = await circuitBreakers.gemini.call(circuitBreakerLogic);
          break;
        case 'cohere':
          result = await circuitBreakers.cohere.call(circuitBreakerLogic);
          break;
        case 'huggingface':
          result = await circuitBreakers.huggingface.call(circuitBreakerLogic);
          break;
        default:
          throw new Error(`Unknown service: ${service}`);
      }
      
      aiResponse = result.response;
      isRealAPI = result.usingRealAPI;
    } catch (circuitError) {
      // Circuit breaker is open or execution failed
      throw circuitError;
    }

    const latency = Date.now() - start;
    
    // Update service-specific latency (request already counted at start)
    if (metricsHistory.aiServices[service]) {
      metricsHistory.aiServices[service].totalLatency += latency;
    }
    
    // Count ALL successful responses (real API or simulation)
    metricsHistory.successfulRequests++;
    metricsHistory.totalLatency += latency;
    success = true;

    console.log(`✅ AI request completed - Service: ${service}, Latency: ${latency}ms, Real API: ${isRealAPI}`);

    res.json({
      success: true,
      service,
      response: aiResponse,
      latency,
      isRealAPI,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    const latency = Date.now() - start;
    
    metricsHistory.failedRequests++;
    
    // Update service-specific failure metrics (request already counted above, just count failure)
    const service = req.body?.service || 'gemini';
    if (metricsHistory.aiServices[service]) {
      metricsHistory.aiServices[service].failures++; // Count the failure
      metricsHistory.aiServices[service].totalLatency += latency; // Add latency even for failures
    }
    
    console.error(`❌ AI service error - Service: ${service}, Error: ${error.message}`);
    
    res.status(500).json({
      success: false,
      error: error.message,
      service,
      latency,
      timestamp: new Date().toISOString()
    });
  }
});

// Chaos Engineering Endpoints

// Inject chaos experiment
app.post('/chaos/inject', (req, res) => {
  try {
    const { service, type, intensity, duration } = req.body;
    
    // Validate inputs
    if (!service || !['gemini', 'cohere', 'huggingface'].includes(service)) {
      return res.status(400).json({ 
        success: false, 
        error: 'Invalid service. Must be gemini, cohere, or huggingface' 
      });
    }
    
    const validTypes = ['latency', 'failure', 'timeout', 'intermittent', 'unavailable', 'corruption'];
    if (!type || !validTypes.includes(type)) {
      return res.status(400).json({ 
        success: false, 
        error: `Invalid chaos type. Must be one of: ${validTypes.join(', ')}` 
      });
    }
    
    const intensityValue = parseInt(intensity) || 50;
    const durationValue = parseInt(duration) || 30;
    
    if (intensityValue < 0 || intensityValue > 10000) {
      return res.status(400).json({ 
        success: false, 
        error: 'Intensity must be between 0 and 10000' 
      });
    }
    
    if (durationValue < 1 || durationValue > 300) {
      return res.status(400).json({ 
        success: false, 
        error: 'Duration must be between 1 and 300 seconds' 
      });
    }
    
    // Set up chaos experiment
    const startTime = Date.now();
    const endTime = startTime + (durationValue * 1000);
    
    activeChaos[service] = {
      type,
      intensity: intensityValue,
      startTime,
      endTime
    };
    
    console.log(`🔥 Chaos experiment started: ${service} - ${type} (${intensityValue}% intensity) for ${durationValue}s`);
    
    res.json({
      success: true,
      experiment: {
        service,
        type,
        intensity: intensityValue,
        duration: durationValue,
        startTime: new Date(startTime).toISOString(),
        endTime: new Date(endTime).toISOString()
      }
    });
  } catch (error) {
    console.error('Chaos inject error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Stop chaos experiment
app.post('/chaos/stop', (req, res) => {
  try {
    const { service } = req.body;
    
    if (!service || !['gemini', 'cohere', 'huggingface', 'all'].includes(service)) {
      return res.status(400).json({ 
        success: false, 
        error: 'Invalid service. Must be gemini, cohere, huggingface, or all' 
      });
    }
    
    if (service === 'all') {
      // Stop all chaos experiments
      Object.keys(activeChaos).forEach(svc => {
        if (activeChaos[svc].type) {
          console.log(`🔵 Stopping chaos for ${svc}`);
          activeChaos[svc] = { type: null, intensity: 0, endTime: null, startTime: null };
        }
      });
      
      res.json({
        success: true,
        message: 'All chaos experiments stopped'
      });
    } else {
      // Stop specific service chaos
      if (activeChaos[service].type) {
        console.log(`🔵 Stopping chaos for ${service}`);
        activeChaos[service] = { type: null, intensity: 0, endTime: null, startTime: null };
        
        res.json({
          success: true,
          message: `Chaos experiment stopped for ${service}`
        });
      } else {
        res.json({
          success: true,
          message: `No active chaos for ${service}`
        });
      }
    }
  } catch (error) {
    console.error('Chaos stop error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get active chaos experiments
app.get('/chaos/status', (req, res) => {
  try {
    const now = Date.now();
    const activeExperiments = [];
    
    Object.keys(activeChaos).forEach(service => {
      const chaos = activeChaos[service];
      if (chaos.type && chaos.endTime && now < chaos.endTime) {
        const remainingTime = Math.ceil((chaos.endTime - now) / 1000);
        activeExperiments.push({
          service,
          type: chaos.type,
          intensity: chaos.intensity,
          remainingSeconds: remainingTime,
          startTime: new Date(chaos.startTime).toISOString(),
          endTime: new Date(chaos.endTime).toISOString()
        });
      }
    });
    
    res.json({
      success: true,
      active: activeExperiments,
      count: activeExperiments.length
    });
  } catch (error) {
    console.error('Chaos status error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Log request to database (called by frontend)
app.post('/api/log-request', async (req, res) => {
  try {
    const { 
      service, 
      success, 
      latency, 
      responseSize = 0, 
      errorType = null,
      errorMessage = null,
      prompt = null,
      circuitBreakerState = null,
      chaosActive = false,
      automated = false
    } = req.body;

    // Send to Flask/Python backend for database logging with timeout
    try {
      await axios.post('http://localhost:8080/api/log-request', {
        service,
        success,
        latency,
        responseSize,
        errorType,
        errorMessage,
        prompt,
        circuitBreakerState,
        chaosActive,
        automated
      }, {
        timeout: 5000,  // 5 second timeout
        validateStatus: () => true  // Accept any status code
      });
    } catch (err) {
      // Don't let database logging failures crash the backend
      console.error('Failed to log to database:', err.message);
    }

    // Always respond successfully even if database logging fails
    res.json({ success: true, message: 'Request logged' });
  } catch (error) {
    console.error('Log request error:', error);
    // Don't crash - respond with error but keep server running
    res.status(500).json({ success: false, error: error.message });
  }
});

// Prometheus metrics endpoint
app.get('/prometheus', async (req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (error) {
    console.error('Prometheus metrics error:', error);
    res.status(500).end(error.message);
  }
});

// ===========================================
// Chaos Testing Management Endpoints
// ===========================================

const { spawn } = require('child_process');
// fs and path already imported at top of file

// Store active chaos testing process
let chaosTestingProcess = null;
let chaosTestingStatus = {
  running: false,
  startTime: null,
  duration: 0,
  mode: null,
  totalRequests: 0,
  successfulRequests: 0,
  failedRequests: 0,
  currentScenario: '',
  lastOutput: '',
  outputLines: [],
  detailedLogs: []
};

// Start chaos testing - SYNC handler to prevent async issues
app.post('/chaos-testing/start', (req, res) => {
  // FIRST LINE - Log immediately before ANY processing
  console.log('========== [CHAOS-START] REQUEST RECEIVED ==========');
  console.log('[CHAOS-START] Timestamp:', new Date().toISOString());
  console.log('[CHAOS-START] Method:', req.method);
  console.log('[CHAOS-START] URL:', req.url);
  
  try {
    console.log('[CHAOS-START] Step 1: Checking if chaos test already running...');
    if (chaosTestingProcess) {
      console.log('[CHAOS-START] ❌ Chaos test already running, rejecting request');
      return res.json({
        success: false,
        message: 'Chaos testing is already running',
        status: chaosTestingStatus
      });
    }

    console.log('[CHAOS-START] Step 2: Parsing request parameters...');
    const { mode = 'validation', duration = 4, outputDir = 'chaos-test-results' } = req.body;
    console.log(`[CHAOS-START] ✅ Parameters: mode=${mode}, duration=${duration}, outputDir=${outputDir}`);

    console.log(`[CHAOS-START] Step 3: Building script path...`);
    const scriptPath = path.join(__dirname, '..', 'scripts', 'testing', 'chaos-test.py');
    console.log(`[CHAOS-START] ✅ Script path resolved: ${scriptPath}`);
    
    // Check if script exists
    const fs = require('fs');
    if (!fs.existsSync(scriptPath)) {
      const error = `Script not found at: ${scriptPath}`;
      console.error(`[CHAOS-START] ❌ ${error}`);
      throw new Error(error);
    }
    console.log('[CHAOS-START] ✅ Script file exists');

    const args = mode === 'validation' 
      ? [scriptPath, '--validation', '--output-dir', outputDir]
      : [scriptPath, '--duration', duration.toString(), '--output-dir', outputDir];
    console.log(`[CHAOS-START] ✅ Command args: python -u ${args.join(' ')}`);

    console.log('[CHAOS-START] Step 4: Creating log file for detached process...');
    const logDir = path.join(__dirname, '..', outputDir);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
      console.log(`[CHAOS-START] ✅ Created log directory: ${logDir}`);
    }
    
    const logFile = path.join(logDir, `chaos-test-${Date.now()}.log`);
    
    // Open file descriptor synchronously - don't use streams for detached processes!
    const logFd = fs.openSync(logFile, 'w');
    console.log(`[CHAOS-START] ✅ Log file opened: ${logFile} (fd: ${logFd})`);
    
    console.log('[CHAOS-START] Step 5: Spawning Python process...');
    const spawnOptions = {
      cwd: path.join(__dirname, '..'),
      env: process.env,
      detached: true,
      stdio: ['ignore', logFd, logFd]  // Use file descriptor instead of stream
    };
    console.log(`[CHAOS-START] Spawn options: cwd=${spawnOptions.cwd}, detached=${spawnOptions.detached}, logFd=${logFd}`);
    
    // Start the chaos testing process with UNBUFFERED output and DETACHED mode
    chaosTestingProcess = spawn('python', ['-u', ...args], spawnOptions);
    
    console.log(`[CHAOS-START] ✅ Process spawned with PID: ${chaosTestingProcess.pid}`);

    // Unref so Node.js doesn't wait for this process
    chaosTestingProcess.unref();
    console.log('[CHAOS-START] ✅ Process unref() called');

    console.log('[CHAOS-START] Step 6: Initializing status object...');
    chaosTestingStatus = {
      running: true,
      startTime: new Date(),
      duration: mode === 'validation' ? 0.5 : duration, // ~30 min for validation
      mode: mode,
      totalRequests: 0,
      lastOutput: '',
      outputLines: [],
      pid: chaosTestingProcess.pid,
      logFile: logFile
    };
    console.log(`[CHAOS-START] ✅ Status initialized for PID ${chaosTestingStatus.pid}, log file: ${logFile}`);

    console.log('[CHAOS-START] Step 7: Sending success response to client...');
    // Immediately respond to client - don't wait for process output
    const responseData = {
      success: true,
      message: `Chaos testing started in ${mode} mode`,
      status: chaosTestingStatus,
      pid: chaosTestingProcess.pid,
      logFile: logFile
    };

    // Send response IMMEDIATELY
    res.json(responseData);
    console.log(`[CHAOS-START] ✅ Response sent to client (PID: ${chaosTestingProcess.pid}, log: ${logFile})`);

    console.log('[CHAOS-START] Step 8: Process running in detached mode - output will be written to log file');
    console.log('[CHAOS-START] Step 9: Setting up process completion listener...');
    
    // NO stdout/stderr listeners - output goes directly to log file
    // This prevents hanging issues with detached processes
    
    // Set up close listener
    chaosTestingProcess.on('close', (code, signal) => {
      try {
        console.log(`[CHAOS-CLOSE] Process ${chaosTestingStatus.pid} closed - Code: ${code}, Signal: ${signal}`);
        
        chaosTestingStatus.running = false;
        chaosTestingStatus.endTime = new Date();
        chaosTestingStatus.exitCode = code;
        chaosTestingStatus.signal = signal;
        
        if (code === 0) {
          console.log('[CHAOS-CLOSE] ✅ Process completed successfully');
          chaosTestingStatus.lastOutput = 'Chaos testing completed successfully';
        } else {
          console.log(`[CHAOS-CLOSE] ⚠️  Process exited with code ${code}`);
          chaosTestingStatus.lastOutput = `Process exited with code ${code}`;
        }
        
        // Close file descriptor
        try {
          fs.closeSync(logFd);
          console.log('[CHAOS-CLOSE] ✅ Log file closed');
        } catch (fdError) {
          console.error(`[CHAOS-CLOSE] ⚠️  Error closing log fd: ${fdError.message}`);
        }
        
        chaosTestingProcess = null;
        console.log('[CHAOS-CLOSE] ✅ Process cleaned up');
      } catch (closeError) {
        console.error(`[CHAOS-CLOSE] ❌ Error in close handler: ${closeError.message}`);
      }
    });
    
    // Set up error listener
    chaosTestingProcess.on('error', (error) => {
      console.error(`[CHAOS-ERROR] ❌ Process error for PID ${chaosTestingStatus.pid}: ${error.message}`);
      chaosTestingStatus.running = false;
      chaosTestingStatus.error = error.message;
      chaosTestingStatus.endTime = new Date();
      
      // Close file descriptor on error
      try {
        fs.closeSync(logFd);
      } catch (fdError) {
        console.error(`[CHAOS-ERROR] Error closing log fd: ${fdError.message}`);
      }
    });
    
    console.log('[CHAOS-START] ✅ Process listeners attached (close, error)');
    console.log('[CHAOS-START] ========== CHAOS TEST STARTED SUCCESSFULLY ==========');

    console.log('[CHAOS-START] ✅✅✅ All setup complete, chaos test running in background');

  } catch (error) {
    console.error('[CHAOS-START] ❌❌❌ FATAL ERROR during chaos test start:');
    console.error(`[CHAOS-START] Error message: ${error.message}`);
    console.error(`[CHAOS-START] Error code: ${error.code}`);
    console.error(`[CHAOS-START] Error stack: ${error.stack}`);
    
    // Clean up if process was created
    if (chaosTestingProcess) {
      console.log('[CHAOS-START] Cleaning up failed process...');
      try {
        chaosTestingProcess.kill();
        chaosTestingProcess = null;
      } catch (killError) {
        console.error(`[CHAOS-START] Error killing process: ${killError.message}`);
      }
    }
    
    // Only send response if we haven't already
    if (!res.headersSent) {
      res.status(500).json({
        success: false,
        error: error.message,
        stack: error.stack,
        code: error.code
      });
    } else {
      console.error('[CHAOS-START] Response already sent, cannot send error response');
    }
  }
});

// Stop chaos testing
app.post('/chaos-testing/stop', (req, res) => {
  console.log('[CHAOS-STOP] Received stop request');
  
  try {
    if (!chaosTestingProcess) {
      console.log('[CHAOS-STOP] No process running, nothing to stop');
      return res.json({
        success: false,
        message: 'No chaos testing process running'
      });
    }

    console.log(`[CHAOS-STOP] Stopping chaos testing process PID: ${chaosTestingProcess.pid}`);
    
    // Send SIGINT to allow graceful shutdown
    try {
      chaosTestingProcess.kill('SIGINT');
      console.log('[CHAOS-STOP] ✅ SIGINT sent to process');
    } catch (killError) {
      console.error(`[CHAOS-STOP] ❌ Error sending SIGINT: ${killError.message}`);
      throw killError;
    }
    
    chaosTestingStatus.running = false;
    chaosTestingStatus.endTime = new Date();
    console.log('[CHAOS-STOP] ✅ Status updated');

    res.json({
      success: true,
      message: 'Chaos testing stopped',
      status: chaosTestingStatus
    });
    console.log('[CHAOS-STOP] ✅ Response sent');

  } catch (error) {
    console.error('[CHAOS-STOP] ❌ Error stopping chaos testing:', error.message);
    console.error('[CHAOS-STOP] Stack:', error.stack);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get chaos testing status
app.get('/chaos-testing/status', (req, res) => {
  try {
    const running = chaosTestingStatus.running;
    const pid = chaosTestingStatus.pid || 'N/A';
    const totalRequests = chaosTestingStatus.totalRequests || 0;
    
    // Read latest output from log file if it exists
    let outputLines = [];
    let lastOutput = chaosTestingStatus.lastOutput || '';
    
    if (chaosTestingStatus.logFile && fs.existsSync(chaosTestingStatus.logFile)) {
      try {
        const logContent = fs.readFileSync(chaosTestingStatus.logFile, 'utf8');
        const rawLines = logContent.split('\n').filter(line => line.trim());
        
        // Convert to format expected by dashboard: {timestamp, message, error}
        outputLines = rawLines.map(line => {
          const isError = line.includes('ERROR') || line.includes('❌') || line.includes('FAILED');
          return {
            timestamp: new Date().toISOString(),
            message: line,
            error: isError
          };
        });
        
        // Get last non-empty line as lastOutput
        if (rawLines.length > 0) {
          lastOutput = rawLines[rawLines.length - 1];
        }
        
        // Keep only last 100 lines for efficiency
        if (outputLines.length > 100) {
          outputLines = outputLines.slice(-100);
        }
      } catch (readError) {
        console.error(`[CHAOS-STATUS] ⚠️  Could not read log file: ${readError.message}`);
      }
    }
    
    console.log(`[CHAOS-STATUS] Status check - Running: ${running}, PID: ${pid}, Requests: ${totalRequests}, Output lines: ${outputLines.length}`);
    
    // Update status with fresh data
    const statusResponse = {
      ...chaosTestingStatus,
      outputLines: outputLines,
      lastOutput: lastOutput,
      totalRequests: totalRequests
    };
    
    res.json({
      success: true,
      status: statusResponse
    });
  } catch (error) {
    console.error('[CHAOS-STATUS] ❌ Error getting chaos testing status:', error.message);
    console.error('[CHAOS-STATUS] Stack:', error.stack);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get chaos testing results
app.get('/chaos-testing/results', (req, res) => {
  try {
    const resultsDir = path.join(__dirname, '..', 'chaos-test-results');
    
    if (!fs.existsSync(resultsDir)) {
      return res.json({
        success: true,
        results: []
      });
    }

    const files = fs.readdirSync(resultsDir);
    const results = files
      .filter(f => f.endsWith('.txt'))
      .map(f => {
        const filePath = path.join(resultsDir, f);
        const stats = fs.statSync(filePath);
        return {
          filename: f,
          path: filePath,
          size: stats.size,
          modified: stats.mtime,
          created: stats.birthtime
        };
      })
      .sort((a, b) => b.modified - a.modified);

    res.json({
      success: true,
      results: results
    });

  } catch (error) {
    console.error('Error getting chaos testing results:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get specific result file
app.get('/chaos-testing/results/:filename', (req, res) => {
  try {
    const { filename } = req.params;
    const filePath = path.join(__dirname, '..', 'chaos-test-results', filename);

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({
        success: false,
        error: 'File not found'
      });
    }

    const content = fs.readFileSync(filePath, 'utf8');
    
    res.json({
      success: true,
      filename: filename,
      content: content
    });

  } catch (error) {
    console.error('Error reading result file:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Error handling middleware
app.use((error, req, res, next) => {
  console.error('Unhandled error:', error);
  res.status(500).json({
    error: 'Internal server error',
    message: error.message
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    path: req.path,
    method: req.method
  });
});

// Start server with error handling
const server = app.listen(PORT, () => {
  console.log(`🚀 AI Resilience Monitor Backend running on http://localhost:${PORT}`);
  console.log(`📊 Available endpoints:`);
  console.log(`   GET  /test - Health check`);
  console.log(`   GET  /metrics - Current metrics`);
  console.log(`   GET  /ai/health - AI services health`);
  console.log(`   POST /ai - AI service proxy`);
  console.log(`   GET  /prometheus - Prometheus metrics`);
  console.log(`🔥 Chaos Engineering endpoints:`);
  console.log(`   POST /chaos/inject - Inject chaos experiment`);
  console.log(`   POST /chaos/stop - Stop chaos experiment`);
  console.log(`   GET  /chaos/status - Get active experiments`);
  console.log(`⚡ Circuit Breaker endpoints:`);
  console.log(`   GET  /circuit-breaker/status - Get circuit breaker status`);
  console.log(`   POST /circuit-breaker/reset - Reset circuit breakers`);
}).on('error', (error) => {
  if (error.code === 'EADDRINUSE') {
    console.error(`❌ Port ${PORT} is already in use!`);
    console.error('💡 Try one of these solutions:');
    console.error('   1. Stop the process using port 3000:');
    console.error('      Get-Process | Where-Object {$_.ProcessName -match "node"} | Stop-Process -Force');
    console.error('   2. Use a different port:');
    console.error('      $env:PORT=3001; node src/index.js');
    console.error('   3. Find what\'s using the port:');
    console.error('      Get-NetTCPConnection -LocalPort 3000');
    process.exit(1);
  } else {
    console.error('❌ Server error:', error);
    process.exit(1);
  }
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 Received SIGTERM, shutting down gracefully...');
  server.close(() => {
    console.log('✅ Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('🛑 Received SIGINT, shutting down gracefully...');
  server.close(() => {
    console.log('✅ Server closed');
    process.exit(0);
  });
});

// Handle uncaught exceptions (but allow EADDRINUSE to exit)
process.on('uncaughtException', (error) => {
  console.error('❌ Uncaught Exception:', error);
  console.error('Stack:', error.stack);
  console.error('Time:', new Date().toISOString());
  
  // Log error details
  if (error.code) console.error('Error Code:', error.code);
  if (error.errno) console.error('Error Number:', error.errno);
  if (error.syscall) console.error('System Call:', error.syscall);
  
  // Exit for critical errors like port conflicts
  if (error.code === 'EADDRINUSE') {
    console.error('❌ Critical error: Port already in use. Exiting...');
    process.exit(1);
  }
  
  // Don't exit for other errors - keep the server running
  console.log('⚠️  Server continuing despite error...');
  console.log('💓 Server still alive - monitoring will detect if crashed');
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Promise Rejection at:', promise);
  console.error('Reason:', reason);
  console.error('Time:', new Date().toISOString());
  
  // Log stack trace if available
  if (reason && reason.stack) {
    console.error('Stack:', reason.stack);
  }
  
  // Don't exit - keep the server running
  console.log('⚠️  Server continuing despite error...');
  console.log('💓 Server still alive - monitoring will detect if crashed');
});

// Keep alive - log heartbeat every 5 minutes
setInterval(() => {
  const uptime = Math.floor(process.uptime());
  const hours = Math.floor(uptime / 3600);
  const minutes = Math.floor((uptime % 3600) / 60);
  console.log(`💓 Backend heartbeat - Uptime: ${hours}h ${minutes}m - Memory: ${Math.round(process.memoryUsage().heapUsed / 1024 / 1024)}MB`);
}, 5 * 60 * 1000);