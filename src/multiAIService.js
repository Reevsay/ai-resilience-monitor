const axios = require('axios');

class MultiAIService {
  constructor() {
    this.services = [
      {
        name: 'huggingface',
        endpoint: 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium',
        headers: (apiKey) => ({ 'Authorization': `Bearer ${apiKey}` }),
        formatRequest: (message) => ({ inputs: message }),
        formatResponse: (data) => ({
          content: data[0]?.generated_text || data.error || "No response",
          model: "DialoGPT-medium",
          provider: "Hugging Face",
          usage: { total_tokens: 0, cost: 0 }
        })
      },
      {
        name: 'gemini',
        endpoint: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent',
        headers: (apiKey) => ({ 'Content-Type': 'application/json' }),
        formatRequest: (message) => ({
          contents: [{ parts: [{ text: message }] }]
        }),
        formatResponse: (data) => ({
          content: data.candidates?.[0]?.content?.parts?.[0]?.text || "No response",
          model: "gemini-1.5-flash",
          provider: "Google Gemini",
          usage: { total_tokens: data.usageMetadata?.totalTokenCount || 0, cost: 0 }
        }),
        urlWithKey: (endpoint, apiKey) => `${endpoint}?key=${apiKey}`
      },
      {
        name: 'cohere',
        endpoint: 'https://api.cohere.ai/v1/generate',
        headers: (apiKey) => ({ 
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }),
        formatRequest: (message) => ({
          model: 'command',
          prompt: message,
          max_tokens: 100,
          temperature: 0.7
        }),
        formatResponse: (data) => ({
          content: data.generations?.[0]?.text || "No response",
          model: "command",
          provider: "Cohere",
          usage: { total_tokens: data.meta?.billed_units?.output_tokens || 0, cost: 0 }
        })
      },
      {
        name: 'openai',
        endpoint: 'https://api.openai.com/v1/chat/completions',
        headers: (apiKey) => ({ 
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        }),
        formatRequest: (message) => ({
          model: "gpt-3.5-turbo",
          messages: [{ role: "user", content: message }],
          max_tokens: 150,
          temperature: 0.7
        }),
        formatResponse: (data) => ({
          content: data.choices?.[0]?.message?.content || "No response",
          model: data.model || "gpt-3.5-turbo",
          provider: "OpenAI",
          usage: data.usage || { total_tokens: 0, cost: 0 }
        })
      }
    ];
  }

  async callAI(message, preferredService = null) {
    const servicesToTry = preferredService 
      ? [this.services.find(s => s.name === preferredService), ...this.services.filter(s => s.name !== preferredService)]
      : this.services;

    for (const service of servicesToTry) {
      if (!service) continue;
      
      try {
        const apiKey = process.env[`${service.name.toUpperCase()}_API_KEY`];
        if (!apiKey || apiKey === 'your-key-here') {
          console.log(`⚠️ Skipping ${service.name}: No API key configured`);
          continue;
        }

        console.log(`🤖 Trying ${service.provider}...`);
        
        const url = service.urlWithKey ? service.urlWithKey(service.endpoint, apiKey) : service.endpoint;
        const requestData = service.formatRequest(message);
        const headers = service.headers(apiKey);

        const response = await axios.post(url, requestData, {
          headers,
          timeout: 15000
        });

        const formattedResponse = service.formatResponse(response.data);
        console.log(`✅ ${service.provider} responded successfully`);
        
        return {
          ...formattedResponse,
          success: true,
          service: service.name
        };

      } catch (error) {
        console.log(`❌ ${service.provider} failed: ${error.response?.data?.error || error.message}`);
        continue;
      }
    }

    // If all services fail, return fallback
    return {
      content: "All AI services are currently unavailable. This is a fallback response to ensure system reliability.",
      model: "fallback",
      provider: "System Fallback",
      usage: { total_tokens: 0, cost: 0 },
      success: false,
      service: "fallback"
    };
  }

  // Get available services with their status
  async checkServiceHealth() {
    const results = [];
    const testMode = process.env.TEST_MODE === 'true';
    
    for (const service of this.services) {
      const apiKey = process.env[`${service.name.toUpperCase()}_API_KEY`];
      const status = {
        name: service.name,
        provider: service.provider,
        configured: apiKey && apiKey !== 'your-key-here',
        endpoint: service.endpoint
      };
      
      if (testMode) {
        // In TEST_MODE, simulate healthy services for demo purposes
        status.healthy = true;
        status.lastResponse = 'Simulated healthy (TEST_MODE)';
      } else if (status.configured) {
        try {
          // Simple health check
          const response = await this.callAI("Hello", service.name);
          status.healthy = response.success;
          status.lastResponse = response.content.substring(0, 50) + "...";
        } catch (error) {
          status.healthy = false;
          status.error = error.message;
        }
      } else {
        status.healthy = false;
        status.error = "No API key configured";
      }
      
      results.push(status);
    }
    
    return results;
  }
}

module.exports = MultiAIService;
