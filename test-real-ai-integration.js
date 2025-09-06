#!/usr/bin/env node

const axios = require('axios');

async function testRealAI() {
    console.log('🧪 Testing Real AI Integration');
    console.log('============================\n');
    
    const testCases = [
        {
            service: 'gemini',
            message: 'Tell me a short joke about programming'
        },
        {
            service: 'cohere', 
            message: 'What is the capital of France?'
        },
        {
            service: 'huggingface',
            message: 'How are you today?'
        }
    ];
    
    for (const test of testCases) {
        try {
            console.log(`🤖 Testing ${test.service.toUpperCase()}...`);
            
            const response = await axios.post('http://localhost:3000/ai/chat', {
                message: test.message,
                service: test.service
            }, {
                headers: { 'Content-Type': 'application/json' },
                timeout: 15000
            });
            
            console.log(`✅ ${test.service} Response:`);
            console.log(`   Query: "${test.message}"`);
            console.log(`   AI Response: "${response.data.content}"`);
            console.log(`   Provider: ${response.data.provider}`);
            console.log(`   Model: ${response.data.model}\n`);
            
        } catch (error) {
            console.log(`❌ ${test.service} Error:`);
            console.log(`   ${error.response?.data || error.message}\n`);
        }
    }
    
    console.log('🎉 Real AI Integration Test Complete!');
}

testRealAI().catch(console.error);
