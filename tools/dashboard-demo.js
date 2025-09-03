#!/usr/bin/env node

const axios = require('axios');

class DashboardDemo {
    constructor() {
        this.baseUrl = 'http://localhost:3000';
        this.isRunning = false;
    }

    async testService(service, message) {
        try {
            const response = await axios.post(`${this.baseUrl}/ai/${service}`, {
                message: message
            }, {
                headers: { 'Content-Type': 'application/json' },
                timeout: 10000
            });
            
            console.log(`✅ ${service}: ${response.data.content?.substring(0, 50)}...`);
            return true;
        } catch (error) {
            console.log(`❌ ${service}: ${error.message}`);
            return false;
        }
    }

    async runDemoLoop() {
        console.log('🎪 Starting Enhanced Dashboard Demo');
        console.log('=====================================');
        console.log('🌐 Open: http://localhost:3000/dashboard');
        console.log('👀 Watch real-time metrics updating!');
        console.log('=====================================\n');

        this.isRunning = true;
        let iteration = 1;

        const services = ['cohere', 'gemini', 'huggingface'];
        const messages = [
            'Tell me a programming joke',
            'What is artificial intelligence?',
            'Explain machine learning in simple terms',
            'What are the benefits of cloud computing?',
            'How does a neural network work?'
        ];

        while (this.isRunning) {
            console.log(`🔄 Demo Iteration ${iteration}`);
            
            // Test a random service with a random message
            const service = services[Math.floor(Math.random() * services.length)];
            const message = messages[Math.floor(Math.random() * messages.length)];
            
            console.log(`🤖 Testing ${service} with: "${message}"`);
            await this.testService(service, message);
            
            // Random delay between 2-8 seconds
            const delay = 2000 + Math.random() * 6000;
            console.log(`⏱️  Waiting ${(delay/1000).toFixed(1)}s for next request...\n`);
            
            await new Promise(resolve => setTimeout(resolve, delay));
            iteration++;
            
            // Stop after 20 iterations or if interrupted
            if (iteration > 20) {
                this.isRunning = false;
                console.log('🎯 Demo completed after 20 iterations');
            }
        }
    }

    stop() {
        this.isRunning = false;
        console.log('\n🛑 Demo stopped');
        process.exit(0);
    }
}

const demo = new DashboardDemo();

// Handle Ctrl+C gracefully
process.on('SIGINT', () => demo.stop());
process.on('SIGTERM', () => demo.stop());

// Start the demo
demo.runDemoLoop().catch(console.error);
