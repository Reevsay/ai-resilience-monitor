# 🚀 Quick Start Guide

## ⚡ 5-Minute Setup

### Prerequisites
- 🐳 Docker and Docker Compose
- 📦 Node.js 18+ (for local development)
- 🔑 AI API keys (optional for demo mode)

## 🎯 Option 1: Docker (Fastest)

```bash
# 1. Clone the repository
git clone https://github.com/Reevsay/ai-resilience-monitor.git
cd ai-resilience-monitor

# 2. Start everything
docker compose up --build

# 3. Open your browser
# 🌐 Dashboard: http://localhost:3000/dashboard
# 📊 Metrics: http://localhost:3000/metrics
```

That's it! 🎉 Your AI Resilience Monitor is running!

## 🛠️ Option 2: Local Development

```bash
# 1. Install dependencies
npm install

# 2. Copy environment template
cp .env.example .env

# 3. Add your AI API keys (optional)
# COHERE_API_KEY=your_key_here
# GEMINI_API_KEY=your_key_here
# HUGGINGFACE_API_KEY=your_key_here

# 4. Start the server
npm start

# 5. Run the demo (in another terminal)
npm run dashboard-demo
```

## 🧪 Test Your Setup

### Quick Health Check
```bash
# Test the main service
curl http://localhost:3000/health

# Test the dashboard
curl http://localhost:3000/dashboard
```

### Try the AI Proxy
```bash
curl -X POST http://localhost:3000/ai \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'
```

### Check Metrics
```bash
curl http://localhost:3000/metrics
```

## 🎮 Explore the Dashboard

1. **🌐 Open** http://localhost:3000/dashboard
2. **👀 Watch** real-time metrics updating
3. **🎛️ Try** the failure injection controls
4. **📊 Monitor** the circuit breaker status
5. **🔍 Explore** the request logs

## 🚨 Troubleshooting

### Common Issues

**🐳 Docker Issues**
```bash
# Clean Docker cache
docker system prune -a

# Restart with fresh build
docker compose down
docker compose up --build
```

**📡 Port Conflicts**
```bash
# Check what's using port 3000
netstat -an | grep 3000

# Or use different port
PORT=3001 npm start
```

**🔑 API Key Issues**
- The demo works without API keys
- Real AI responses require valid keys
- Check logs for authentication errors

## 🎯 Next Steps

1. **📚 Read** the [Configuration Guide](CONFIGURATION.md)
2. **🧪 Try** the [Testing Guide](TESTING.md)  
3. **📊 Setup** [Monitoring](MONITORING.md)
4. **🚀 Deploy** to [Production](DEPLOYMENT.md)

## 💡 Pro Tips

- **🔄 Auto-refresh**: Dashboard updates every 5 seconds
- **📱 Mobile**: Works great on mobile devices
- **🎨 Themes**: Blue-black theme is optimized for dark mode
- **⚡ Performance**: Use Docker for best performance
- **🔍 Debug**: Check browser console for detailed logs

---

🎉 **Congratulations!** You're now running the AI Resilience Monitor!

Need help? [Open an issue](https://github.com/Reevsay/ai-resilience-monitor/issues) or check our [documentation](../README.md).
