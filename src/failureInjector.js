// Failure injection utilities

function shouldInject(rate = 0) {
  return Math.random() < rate;
}

async function injectDelay(minMs = 0, maxMs = 0) {
  const delay = Math.floor(Math.random() * (maxMs - minMs + 1)) + minMs;
  return new Promise((resolve) => setTimeout(resolve, delay));
}

function corruptData(data, corruptionRate = 0) {
  if (Math.random() < corruptionRate && data && typeof data === 'object') {
    const keys = Object.keys(data);
    if (keys.length) {
      // Remove a random property
      delete data[keys[Math.floor(Math.random() * keys.length)]];
    }
  }
  return data;
}

// New failure injection types
function injectNetworkError(rate = 0) {
  if (shouldInject(rate)) {
    const errors = ['ECONNRESET', 'ETIMEDOUT', 'ENOTFOUND', 'ECONNREFUSED'];
    const error = new Error(`Network error: ${errors[Math.floor(Math.random() * errors.length)]}`);
    error.code = errors[Math.floor(Math.random() * errors.length)];
    throw error;
  }
}

function injectMemoryError(rate = 0) {
  if (shouldInject(rate)) {
    throw new Error('Out of memory: JavaScript heap out of memory');
  }
}

function injectAuthError(rate = 0) {
  if (shouldInject(rate)) {
    const error = new Error('Authentication failed: Invalid API key');
    error.status = 401;
    throw error;
  }
}

function injectRateLimitError(rate = 0) {
  if (shouldInject(rate)) {
    const error = new Error('Rate limit exceeded: Too many requests');
    error.status = 429;
    error.retryAfter = Math.floor(Math.random() * 60) + 30; // 30-90 seconds
    throw error;
  }
}

function injectPartialResponse(data, rate = 0) {
  if (shouldInject(rate) && data && typeof data === 'object') {
    // Return only partial data
    const keys = Object.keys(data);
    const keepKeys = keys.slice(0, Math.ceil(keys.length / 2));
    const partialData = {};
    keepKeys.forEach(key => partialData[key] = data[key]);
    partialData._partial = true;
    return partialData;
  }
  return data;
}

function injectSlowResponse(rate = 0, minMs = 5000, maxMs = 30000) {
  if (shouldInject(rate)) {
    const delay = Math.floor(Math.random() * (maxMs - minMs + 1)) + minMs;
    return new Promise((resolve) => setTimeout(resolve, delay));
  }
  return Promise.resolve();
}

module.exports = { 
  shouldInject, 
  injectDelay, 
  corruptData,
  injectNetworkError,
  injectMemoryError,
  injectAuthError,
  injectRateLimitError,
  injectPartialResponse,
  injectSlowResponse
};
