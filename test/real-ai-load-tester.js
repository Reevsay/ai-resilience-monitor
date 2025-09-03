const axios = require('axios');

class RealAILoadTester {
  constructor() {
    this.baseUrl = 'http://localhost:3000';
    this.results = {
      total: 0,
      successful: 0,
      failed: 0,
      fallbacks: 0,
      latencies: [],
      serviceStats: {},
      responses: []
    };
  }

  // Generate realistic AI prompts for testing
  generateRealAIPrompts() {
    return [
      { message: "Explain quantum computing in simple terms" },
      { message: "Write a short poem about artificial intelligence" },
      { message: "What are the benefits of renewable energy?" },
      { message: "How does machine learning work?" },
      { message: "Describe the future of space exploration" },
      { message: "What is the significance of blockchain technology?" },
      { message: "Explain the concept of sustainable development" },
      { message: "How do neural networks learn?" },
      { message: "What are the ethical implications of AI?" },
      { message: "Describe the process of photosynthesis" },
      { message: "What is climate change and its effects?" },
      { message: "How does cryptocurrency work?" },
      { message: "Explain the theory of relativity" },
      { message: "What are the applications of robotics?" },
      { message: "Describe the importance of biodiversity" }
    ];
  }

  async makeRequest(specificService = null) {
    const startTime = Date.now();
    const prompts = this.generateRealAIPrompts();
    const payload = prompts[Math.floor(Math.random() * prompts.length)];
    
    try {
      const url = specificService 
        ? `${this.baseUrl}/ai/${specificService}`
        : `${this.baseUrl}/ai`;
        
      const response = await axios.post(url, payload, {
        timeout: 30000,  // Longer timeout for real AI services
        headers: { 'Content-Type': 'application/json' }
      });
      
      const endTime = Date.now();
      const latency = endTime - startTime;
      
      this.results.total++;
      this.results.latencies.push(latency);
      
      // Track service statistics
      const service = response.data.service || 'unknown';
      if (!this.results.serviceStats[service]) {
        this.results.serviceStats[service] = { count: 0, totalLatency: 0 };
      }
      this.results.serviceStats[service].count++;
      this.results.serviceStats[service].totalLatency += latency;
      
      // Check response type
      if (response.data.content && !response.data.content.includes('unavailable')) {
        this.results.successful++;
        // Store sample responses
        if (this.results.responses.length < 5) {
          this.results.responses.push({
            service: response.data.provider || service,
            model: response.data.model,
            prompt: payload.message.substring(0, 50) + "...",
            response: response.data.content.substring(0, 100) + "..."
          });
        }
      } else {
        this.results.fallbacks++;
      }
      
      return {
        success: true,
        latency,
        response: response.data,
        service
      };
      
    } catch (error) {
      const endTime = Date.now();
      const latency = endTime - startTime;
      
      this.results.total++;
      this.results.failed++;
      this.results.latencies.push(latency);
      
      return {
        success: false,
        latency,
        error: error.message
      };
    }
  }

  async testSpecificService(serviceName, requests = 5) {
    console.log(`🤖 Testing ${serviceName} service specifically...`);
    
    for (let i = 0; i < requests; i++) {
      await this.makeRequest(serviceName);
      process.stdout.write(`\rProgress: ${i + 1}/${requests} requests`);
    }
    
    console.log('\n');
  }

  async runRealAILoadTest(requests = 20, concurrency = 2) {
    console.log(`🚀 Starting REAL AI load test with ${requests} requests, concurrency: ${concurrency}`);
    console.log('📡 Testing multiple AI services with automatic failover...\n');
    
    // First, check service health
    try {
      const healthResponse = await axios.get(`${this.baseUrl}/ai/health`);
      console.log('🏥 AI Service Health Check:');
      healthResponse.data.services.forEach(service => {
        const status = service.configured ? '✅' : '❌';
        console.log(`   ${status} ${service.provider}: ${service.configured ? 'Configured' : 'No API key'}`);
      });
      console.log('');
    } catch (error) {
      console.log('⚠️ Could not check service health\n');
    }

    // Run load test in batches
    const batches = [];
    for (let i = 0; i < requests; i += concurrency) {
      const batchSize = Math.min(concurrency, requests - i);
      const batch = Array(batchSize).fill().map(() => this.makeRequest());
      batches.push(batch);
    }

    for (const [index, batch] of batches.entries()) {
      await Promise.all(batch);
      process.stdout.write(`\rProgress: ${Math.min((index + 1) * concurrency, requests)}/${requests} requests`);
    }
    
    console.log('\n✅ Real AI load test completed\n');
    this.printRealAIResults();
  }

  printRealAIResults() {
    const avgLatency = this.results.latencies.reduce((a, b) => a + b, 0) / this.results.latencies.length;
    const minLatency = Math.min(...this.results.latencies);
    const maxLatency = Math.max(...this.results.latencies);
    
    console.log('🤖 REAL AI Load Test Results:');
    console.log('==================================================');
    console.log(`Total Requests: ${this.results.total}`);
    console.log(`Successful: ${this.results.successful} (${(this.results.successful/this.results.total*100).toFixed(2)}%)`);
    console.log(`Failed: ${this.results.failed} (${(this.results.failed/this.results.total*100).toFixed(2)}%)`);
    console.log(`Fallback Responses: ${this.results.fallbacks}`);
    console.log(`Average Latency: ${avgLatency.toFixed(2)}ms`);
    console.log(`Min Latency: ${minLatency.toFixed(2)}ms`);
    console.log(`Max Latency: ${maxLatency.toFixed(2)}ms`);
    console.log('');
    
    // Service breakdown
    console.log('📊 Service Performance:');
    Object.entries(this.results.serviceStats).forEach(([service, stats]) => {
      const avgServiceLatency = stats.totalLatency / stats.count;
      console.log(`   ${service}: ${stats.count} requests, ${avgServiceLatency.toFixed(2)}ms avg`);
    });
    console.log('');
    
    // Sample responses
    if (this.results.responses.length > 0) {
      console.log('💬 Sample AI Responses:');
      this.results.responses.forEach((sample, index) => {
        console.log(`   ${index + 1}. ${sample.service} (${sample.model}):`);
        console.log(`      Q: ${sample.prompt}`);
        console.log(`      A: ${sample.response}`);
        console.log('');
      });
    }
    
    console.log('🎯 This is your REAL AI system with multiple providers and automatic failover!');
  }
}

// CLI execution
if (require.main === module) {
  const args = process.argv.slice(2);
  const requests = parseInt(args.find(arg => arg.startsWith('--requests='))?.split('=')[1]) || 20;
  const concurrency = parseInt(args.find(arg => arg.startsWith('--concurrency='))?.split('=')[1]) || 2;
  const service = args.find(arg => arg.startsWith('--service='))?.split('=')[1];

  const tester = new RealAILoadTester();
  
  if (service) {
    tester.testSpecificService(service, requests).catch(console.error);
  } else {
    tester.runRealAILoadTest(requests, concurrency).catch(console.error);
  }
}

module.exports = RealAILoadTester;
