# 🚀 AI Service Resilience Monitor

A real-time monitoring system for AI services with automated testing, circuit breakers, and performance analytics.

## ⚡ Quick Start

### Prerequisites
- Node.js 14+ and npm
- Python 3.7+ and pip

### Installation & Startup
```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Start services (Windows)
start.bat

# Access dashboard
# Dashboard: http://localhost:8080
# Backend API: http://localhost:3000
```

## 🏗️ Architecture

**Two-tier system:**
- **Python Flask Dashboard** (Port 8080) - Web interface with real-time charts
- **Node.js Backend** (Port 3000) - API monitoring with circuit breakers

**Monitored Services:**
- Google Gemini
- Cohere  
- Hugging Face

## 📊 Features

- **Real-time monitoring** with 5-second updates
- **Performance analytics** with Chart.js visualizations
- **Automated testing** with configurable intervals
- **Circuit breaker pattern** for fault tolerance
- **CSV data export** for analysis
- **Prometheus metrics** integration

## 🎮 Usage

1. **Start System**: Run `start.bat` to launch both servers
2. **Monitor Services**: View real-time dashboard at http://localhost:8080
3. **Enable Automation**: Click "Start Auto Requests" for continuous testing
4. **Analyze Data**: View charts, export CSV, or access metrics API

## 📋 API Configuration (Optional)

Copy `.env.template` to `.env` and add your API keys:
```bash
cp .env.template .env
```

Then edit `.env` with your actual API keys:
```env
GOOGLE_API_KEY=your_google_key
COHERE_API_KEY=your_cohere_key
HUGGINGFACE_API_KEY=your_huggingface_key
```

*System works with simulated responses if no API keys provided.*

## 🔧 Project Structure

```
ai-resilience-monitor/
├── src/index.js           # Node.js backend server
├── templates/dashboard.html # Dashboard interface  
├── app.py                 # Python Flask server
├── package.json           # Node.js dependencies
├── requirements.txt       # Python dependencies
├── start.bat             # Startup script
├── quick_test.ps1        # Test script
└── test_load.ps1         # Load testing
```

## 📈 Key Metrics

- **Service Reliability**: Success rate percentage
- **Performance**: Average response latency
- **Availability**: Uptime tracking
- **Load**: Requests per minute

## 🛠️ Development

**Backend Dependencies:**
- express, cors, axios, dotenv, prom-client

**Frontend Dependencies:**  
- Flask, requests, Chart.js

## 📄 License

MIT License