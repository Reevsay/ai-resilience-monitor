require('dotenv').config();
const express = require('express');
const cors = require('cors');
const axios = require('axios');
const client = require('prom-client');

const app = express();
const PORT = process.env.PORT || 3000;

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

// Enable CORS for all routes
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());

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

// Circuit breaker implementation
class CircuitBreaker {
  constructor(threshold = 5, timeout = 60000) {
    this.threshold = threshold;
    this.timeout = timeout;
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
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
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
    }
  }
}

const circuitBreakers = {
  gemini: new CircuitBreaker(),
  cohere: new CircuitBreaker(),
  huggingface: new CircuitBreaker()
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
      acc[service] = {
        requests: serviceData.requests,
        failures: serviceData.failures,
        successRate: serviceData.requests > 0 
          ? Math.round(((serviceData.requests - serviceData.failures) / serviceData.requests) * 100 * 10) / 10
          : 100,
        avgLatency: serviceData.requests > 0 && serviceData.totalLatency > 0
          ? Math.round(serviceData.totalLatency / (serviceData.requests - serviceData.failures))
          : 0,
        status: serviceData.status,
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

// Health check endpoint
app.get('/test', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    uptime: Date.now() - metricsHistory.startTime
  });
});

// Get current metrics
app.get('/metrics', (req, res) => {
  try {
    const metrics = calculateMetrics();
    res.json(metrics);
  } catch (error) {
    console.error('Error calculating metrics:', error);
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
    metricsHistory.totalRequests++;
    
    const { service = 'gemini', prompt, ...options } = req.body;
    
    if (!prompt) {
      throw new Error('Prompt is required');
    }

    console.log(`🔄 Processing AI request - Service: ${service}, Prompt: "${prompt}"`);

    let aiResponse;
    let isRealAPI = false;

    try {
      // Try to use real API first
      switch (service) {
        case 'gemini':
          aiResponse = await circuitBreakers.gemini.call(() => callGemini(prompt));
          isRealAPI = true;
          break;
        case 'cohere':
          aiResponse = await circuitBreakers.cohere.call(() => callCohere(prompt));
          isRealAPI = true;
          break;
        case 'huggingface':
          aiResponse = await circuitBreakers.huggingface.call(() => callHuggingFace(prompt));
          isRealAPI = true;
          break;
        default:
          throw new Error(`Unknown service: ${service}`);
      }
    } catch (apiError) {
      console.log(`⚠️ Real API failed for ${service}: ${apiError.message}, falling back to simulation`);
      
      // Fallback to simulation if real API fails or not configured
      const simulationTime = Math.random() * 2000 + 500; // 500-2500ms
      await new Promise(resolve => setTimeout(resolve, simulationTime));
      
      // 10% simulation failure rate
      if (Math.random() < 0.1) {
        throw new Error(`Simulated ${service} service failure`);
      }
      
      aiResponse = `Simulated ${service} response for: "${prompt}"`;
      isRealAPI = false;
    }

    const latency = Date.now() - start;
    
    // Update service-specific metrics - COUNT REQUEST FIRST
    if (metricsHistory.aiServices[service]) {
      metricsHistory.aiServices[service].requests++;
      metricsHistory.aiServices[service].totalLatency += latency;
    }
    
    // Only count as successful if it's not a disabled service
    if (isRealAPI) {
      metricsHistory.successfulRequests++;
      metricsHistory.totalLatency += latency;
    }
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
    
    // Update service-specific failure metrics
    const service = req.body?.service || 'gemini';
    if (metricsHistory.aiServices[service]) {
      metricsHistory.aiServices[service].requests++; // Count the request
      metricsHistory.aiServices[service].failures++; // Count the failure
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

// Start server
app.listen(PORT, () => {
  console.log(`🚀 AI Resilience Monitor Backend running on http://localhost:${PORT}`);
  console.log(`📊 Available endpoints:`);
  console.log(`   GET  /test - Health check`);
  console.log(`   GET  /metrics - Current metrics`);
  console.log(`   GET  /ai/health - AI services health`);
  console.log(`   POST /ai - AI service proxy`);
  console.log(`   GET  /prometheus - Prometheus metrics`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 Received SIGTERM, shutting down gracefully...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('🛑 Received SIGINT, shutting down gracefully...');
  process.exit(0);
});