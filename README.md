<div align="center">

# 🛡️ AI Resilience Monitor

### *Real-time Monitoring & Chaos Engineering for AI Services*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-v18+-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Express](https://img.shields.io/badge/Express-4.x-000000?logo=express&logoColor=white)](https://expressjs.com/)
[![Flask](https://img.shields.io/badge/Flask-2.3-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

**Build resilient AI systems with intelligent circuit breakers, chaos engineering, and real-time monitoring**

[Features](#-features) • [Quick Start](#-quick-start) • [Demo](#-demo) • [Documentation](#-documentation) • [Contributing](#-contributing)

---

</div>

## 🎯 Overview

AI Resilience Monitor is a production-ready monitoring platform that helps you build fault-tolerant AI applications. It combines **circuit breaker patterns**, **chaos engineering**, and **real-time analytics** to ensure your AI services stay reliable under any conditions.

### Why AI Resilience Monitor?

- 🔄 **Multi-Provider Support** - Seamlessly integrate Google Gemini, Cohere, and HuggingFace
- ⚡ **Smart Circuit Breakers** - Automatic failure detection and recovery
- 🔥 **Chaos Engineering** - Test your system's resilience with controlled failure injection
- 📊 **Real-time Analytics** - Beautiful dashboards with Chart.js visualizations
- 🛡️ **Production Ready** - Global error handlers, graceful degradation, and comprehensive logging
- 🚀 **Zero Config** - Works out of the box with simulation mode (no API keys required)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔄 Circuit Breakers
- **Three-state pattern** (CLOSED → OPEN → HALF_OPEN)
- **Per-service isolation** prevents cascading failures
- **Automatic recovery** with configurable thresholds
- **Real-time state tracking** and visualization

</td>
<td width="50%">

### 🔥 Chaos Engineering
- **Latency injection** (0-10s delays)
- **Failure simulation** (configurable rates)
- **Timeout scenarios** (hang requests)
- **Service unavailability** testing
- **Response corruption** validation
- **Time-bounded experiments** with auto-rollback

</td>
</tr>
<tr>
<td width="50%">

### 📊 Real-time Monitoring
- **Live metrics dashboard** with Chart.js
- **Request tracking** (count, latency, success rate)
- **Historical analysis** with SQLite persistence
- **Service health monitoring**
- **Interactive visualizations**

</td>
<td width="50%">

### 🤖 AI Service Integration
- **Google Gemini** support
- **Cohere** integration
- **HuggingFace** models
- **Intelligent fallback** to simulation
- **Vendor-agnostic** architecture

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- Node.js v18+ 
- Python 3.8+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Reevsay/ai-resilience-monitor.git
cd ai-resilience-monitor

# Install dependencies
npm install
pip install -r requirements.txt

# Configure environment (optional - works without API keys)
cp config/.env config/.env.local
# Edit config/.env.local with your API keys if you have them
```

### Start the Application

**Option 1: Quick Start (Recommended)**
```bash
# Start both services automatically
npm start
```

**Option 2: Manual Start**
```bash
# Terminal 1 - Backend
node src/index.js

# Terminal 2 - Frontend
python app.py
```

### Access the Dashboard

Open your browser and navigate to:
- 🎨 **Dashboard**: http://localhost:8080
- 🔌 **Backend API**: http://localhost:3000
- 📊 **Metrics**: http://localhost:3000/metrics

---

## 🎬 Demo

### Dashboard Overview

The main dashboard provides:
- **Real-time request monitoring** with live charts
- **Circuit breaker status** for each AI service
- **Chaos experiment controls** for resilience testing
- **Historical data analysis** with filtering
- **Automated testing** with configurable intervals

### Example Workflow

1. **Send a Request**
   ```
   Service: Gemini
   Prompt: "Explain machine learning"
   → View response and latency
   ```

2. **Start Automation**
   ```
   Click "Start Automation"
   → Requests sent every 2 seconds
   → Watch metrics update in real-time
   ```

3. **Inject Chaos**
   ```
   Service: Cohere
   Type: Latency
   Intensity: 5000ms
   Duration: 60s
   → Observe system behavior under stress
   ```

4. **Monitor Circuit Breakers**
   ```
   Watch breakers open after failures
   → Automatic recovery attempts
   → System remains stable
   ```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser Dashboard                         │
│              (React-like UI with Chart.js)                   │
│   • Real-time charts  • Circuit breaker status              │
│   • Chaos controls    • Request history                     │
└────────────────┬────────────────────────────────────────────┘
                 │ HTTP/WebSocket
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Flask Frontend (Port 8080)                      │
│   • Serves dashboard  • Database operations                 │
│   • Request logging   • API proxying                        │
└────────────────┬────────────────────────────────────────────┘
                 │ REST API
                 ▼
┌─────────────────────────────────────────────────────────────┐
│            Node.js Backend (Port 3000)                       │
│   • Circuit breakers  • Chaos engineering                   │
│   • AI service proxy  • Metrics collection                  │
│   • Error handling    • Request validation                  │
└────────────────┬────────────────────────────────────────────┘
                 │ API Calls
                 ▼
┌─────────────────────────────────────────────────────────────┐
│         AI Services / Simulation Fallback                    │
│   Gemini  •  Cohere  •  HuggingFace  •  Simulation         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📖 Documentation

### Configuration

Create a `.env` file in the `config/` directory:

```bash
# Backend Configuration
PORT=3000

# AI Service API Keys (Optional)
GOOGLE_API_KEY=your_gemini_api_key
COHERE_API_KEY=your_cohere_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key

# Circuit Breaker Settings
CIRCUIT_BREAKER_THRESHOLD=5
CIRCUIT_BREAKER_TIMEOUT=30000
CIRCUIT_BREAKER_SUCCESS_THRESHOLD=2
```

### API Endpoints

#### Backend (Port 3000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/test` | GET | Health check |
| `/ai` | POST | AI service proxy |
| `/metrics` | GET | Current metrics |
| `/chaos/inject` | POST | Inject chaos experiment |
| `/chaos/stop` | POST | Stop chaos experiment |
| `/circuit-breaker/status` | GET | Circuit breaker states |
| `/circuit-breaker/reset` | POST | Reset circuit breakers |

#### Frontend (Port 8080)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard UI |
| `/api/metrics` | GET | Metrics API |
| `/api/log-request` | POST | Log request to database |
| `/api/history/requests` | GET | Request history |
| `/api/database/stats` | GET | Database statistics |

### Circuit Breaker Configuration

```javascript
const circuitBreakers = {
  gemini: new CircuitBreaker('gemini', {
    failureThreshold: 5,      // Open after 5 failures
    successThreshold: 2,       // Close after 2 successes
    timeout: 30000,            // Try recovery after 30s
  })
};
```

### Chaos Experiment Types

| Type | Description | Parameters |
|------|-------------|------------|
| **Latency** | Add artificial delays | 0-10000ms |
| **Failure** | Force random failures | 0-100% rate |
| **Timeout** | Hang requests indefinitely | Duration |
| **Intermittent** | Random failure patterns | 0-100% rate |
| **Unavailability** | Complete service outage | Duration |
| **Corruption** | Corrupt response data | 0-100% rate |

---

## 🛠️ Tech Stack

<table>
<tr>
<td align="center" width="25%">
<img src="https://nodejs.org/static/images/logo.svg" width="60" height="60" alt="Node.js"/>
<br><strong>Node.js</strong>
<br>Backend Runtime
</td>
<td align="center" width="25%">
<img src="https://www.python.org/static/community_logos/python-logo.png" width="60" height="60" alt="Python"/>
<br><strong>Python</strong>
<br>Frontend Server
</td>
<td align="center" width="25%">
<img src="https://expressjs.com/images/express-facebook-share.png" width="60" height="60" alt="Express"/>
<br><strong>Express.js</strong>
<br>Web Framework
</td>
<td align="center" width="25%">
<img src="https://flask.palletsprojects.com/en/2.3.x/_images/flask-logo.png" width="60" height="60" alt="Flask"/>
<br><strong>Flask</strong>
<br>Web Framework
</td>
</tr>
<tr>
<td align="center" width="25%">
<strong>Chart.js</strong>
<br>Visualizations
</td>
<td align="center" width="25%">
<strong>SQLite</strong>
<br>Database
</td>
<td align="center" width="25%">
<strong>Axios</strong>
<br>HTTP Client
</td>
<td align="center" width="25%">
<strong>Bootstrap</strong>
<br>UI Framework
</td>
</tr>
</table>

---

## 📁 Project Structure

```
ai-resilience-monitor/
├── 📂 src/                      # Node.js backend
│   └── index.js                 # Main server (1790 lines)
├── 📂 templates/                # Flask templates
│   └── dashboard.html           # Main UI (4663 lines)
├── 📂 backend/                  # Database layer
│   └── database.py              # SQLite operations
├── 📂 config/                   # Configuration files
│   ├── .env                     # Environment variables
│   ├── prometheus.yml           # Prometheus config
│   └── grafana-dashboard.json   # Grafana dashboard
├── 📂 test/                     # Test suites
│   ├── ci-test.js               # CI tests
│   └── real-ai-load-tester.js   # Load testing
├── 📂 scripts/                  # Utility scripts
│   ├── setup/                   # Setup scripts
│   ├── testing/                 # Test scripts
│   └── monitoring/              # Monitoring scripts
├── 📂 docs/                     # Documentation
│   ├── CONTRIBUTING.md
│   └── LITERATURE_REVIEW.md
├── 📂 documentation/            # Technical docs
│   └── *.tex                    # LaTeX flowcharts
├── 📂 literature/               # Research papers
│   └── *.pdf                    # Academic papers
├── 📂 data/                     # Database storage
│   └── monitoring.db            # SQLite database
├── 📂 logs/                     # Application logs
├── 📄 app.py                    # Flask server
├── 📄 package.json              # Node.js dependencies
├── 📄 requirements.txt          # Python dependencies
└── 📄 README.md                 # This file
```

---

## 🧪 Testing

### Run Tests

```bash
# Run CI tests
npm test

# Run load tests
node test/real-ai-load-tester.js

# Run chaos experiments
# Use the dashboard UI for interactive testing
```

### Test Scenarios

1. **Basic Functionality**
   - Send requests to all services
   - Verify responses and latency tracking
   - Check database logging

2. **Circuit Breaker Testing**
   - Inject failures to trigger circuit opening
   - Verify automatic recovery attempts
   - Test manual reset functionality

3. **Chaos Engineering**
   - Test each chaos type
   - Verify system stability under stress
   - Validate automatic rollback

4. **Load Testing**
   - Send 100+ requests/second
   - Monitor memory usage
   - Check for memory leaks

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Use descriptive commit messages

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Backend Memory | ~50-70 MB |
| Frontend Memory | ~20-30 MB |
| Database Size | ~1-2 KB per request |
| Max Throughput | 100+ req/sec |
| Latency Overhead | 5-15ms |
| Uptime | 99.9%+ with error handlers |

---

## 🔒 Security

- ✅ API keys stored in environment variables
- ✅ `.env` files excluded from Git
- ⚠️ CORS set to `*` (restrict in production)
- ⚠️ No authentication (add for production)
- ⚠️ No rate limiting (add for production)

**Production Recommendations:**
- Use HTTPS with reverse proxy (nginx/Apache)
- Implement authentication and authorization
- Add rate limiting
- Restrict CORS to specific origins
- Use secrets management (AWS Secrets Manager, HashiCorp Vault)

---

## 🐛 Troubleshooting

<details>
<summary><strong>Backend won't start</strong></summary>

```bash
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Kill the process
taskkill /PID <process_id> /F

# Restart
node src/index.js
```
</details>

<details>
<summary><strong>Frontend shows "Backend Offline"</strong></summary>

- Ensure backend is running on port 3000
- Check backend terminal for errors
- Verify firewall settings
</details>

<details>
<summary><strong>Database errors</strong></summary>

```bash
# Backup database
cp data/monitoring.db data/monitoring.db.backup

# Delete and recreate
rm data/monitoring.db
python app.py
```
</details>

<details>
<summary><strong>Circuit breakers stuck OPEN</strong></summary>

- Click "Reset All Circuit Breakers" in dashboard
- Or restart the backend service
</details>

---

## 📝 Changelog

### v2.0.3 (Current)
- ✅ Global error handlers prevent crashes
- ✅ Accurate metrics calculation
- ✅ Real timestamp tracking
- ✅ Circuit breaker improvements
- ✅ Project cleanup and documentation

### v2.0.2
- Circuit breaker state management
- Chaos engineering enhancements

### v2.0.1
- Initial stable release

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Yashveer Ahlawat**
- GitHub: [@Reevsay](https://github.com/Reevsay)
- Email: yashveer4661ahlawat@gmail.com

---

## 🙏 Acknowledgments

- Circuit breaker pattern inspired by Michael Nygard's *"Release It!"*
- Chaos engineering concepts from Netflix's Chaos Monkey
- UI/UX inspired by Grafana and Prometheus dashboards
- Research papers in `literature/` folder

---

## 🎯 Roadmap

- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Prometheus + Grafana integration
- [ ] Real-time alerts (Email/Slack)
- [ ] Multi-user authentication
- [ ] Advanced analytics
- [ ] Load testing suite
- [ ] API documentation (Swagger)
- [ ] WebSocket support for real-time updates

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Made with ❤️ for building resilient AI systems**

[Report Bug](https://github.com/Reevsay/ai-resilience-monitor/issues) • [Request Feature](https://github.com/Reevsay/ai-resilience-monitor/issues) • [Documentation](docs/)

</div>
