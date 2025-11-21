# 🤖 AI Resilience Monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-v18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Prometheus](https://img.shields.io/badge/Prometheus-2.54+-orange.svg)](https://prometheus.io/)
[![Grafana](https://img.shields.io/badge/Grafana-11.3+-orange.svg)](https://grafana.com/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

A comprehensive real-time monitoring dashboard for AI services featuring circuit breakers, chaos engineering, automated resilience testing, and **professional Prometheus + Grafana monitoring stack**. Built to ensure high availability and fault tolerance in AI-powered applications.

## 🚀 Quick Start

```powershell
# Clone the repository
git clone <repository-url>
cd ai-resilience-monitor

# Install dependencies
npm install
pip install -r requirements.txt

# Set up API keys (optional - works with simulations too)
cp .env.example .env
# Edit .env with your API keys

# Start everything (auto-installs Prometheus + Grafana)
.\START-MONITOR.ps1
```

**Access Points:**
- 📊 Main Dashboard: http://localhost:8080
- 📈 Grafana: http://localhost:3001 (admin/admin)
- 🔍 Prometheus: http://localhost:9090
- 🔌 Backend API: http://localhost:3000

## 📸 Screenshots

> 🎯 **Dashboard v2.0.3** - Real-time monitoring with circuit breakers and chaos experiments
> 📈 **Grafana Dashboards** - Professional time-series visualizations

*(Add screenshots here)*

---

## 🌟 Key Features

### 🔄 **AI Service Integration**
- **Multi-provider Support**: Gemini, Cohere, HuggingFace
- **Intelligent Fallback**: Automatic simulation when APIs are unavailable
- **Real API Integration**: Use your own API keys or test with simulations

### ⚡ **Circuit Breakers**
- **Smart Failure Detection**: Automatically opens after threshold failures
- **Half-Open State**: Gradual recovery testing
- **Per-Service Isolation**: Independent circuit breakers for each AI service
- **Real-time Monitoring**: Track state transitions (CLOSED → OPEN → HALF_OPEN)

### 🔥 **Chaos Engineering**
- **Latency Injection**: Test system behavior under slow responses (0-10s delays)
- **Failure Simulation**: Force random failures at configurable rates
- **Timeout Scenarios**: Test timeout handling (hang requests)
- **Intermittent Issues**: Random failure patterns
- **Service Unavailability**: Complete service outage simulation
- **Response Corruption**: Test data integrity handling

### 📊 **Professional Monitoring Stack** ⭐ NEW
- **Prometheus Integration**: Industry-standard time-series metrics database
- **Grafana Dashboards**: Professional visualizations and analytics
- **Real-time Metrics**: 5-second scrape interval for immediate insights
- **PromQL Queries**: Powerful query language for advanced analytics
- **Auto-Installation**: One-command setup downloads and configures everything
- **Export Ready**: High-quality PNG/PDF exports for research papers

### 📈 **Real-time Analytics**
- **Live Metrics**: Request count, success rate, latency tracking
- **Interactive Charts**: Line charts with timestamps, bar charts, pie charts
- **Performance Trends**: Historical data visualization with Chart.js
- **Service Health**: Individual metrics per AI service
- **Circuit Breaker States**: Visual state tracking
- **Grafana Panels**: Request rate, latency percentiles (p50, p95), error rates

### 🤖 **Automation**
- **Automated Testing**: Send requests at configurable intervals (2-10 seconds)
- **Custom Prompts**: Define test prompts for realistic scenarios
- **Service Rotation**: Test all services automatically
- **Background Execution**: Non-blocking automation

### 💾 **Data Persistence**
- **SQLite Database**: All requests logged with full details
- **Historical Analysis**: Query past performance data
- **Export Functionality**: JSON export for external analysis
- **Request History**: View last 100+ requests with filtering

### �️ **Resilience & Stability**
- **Crash Protection**: Global error handlers prevent backend crashes
- **Auto-recovery**: Circuit breakers automatically attempt recovery
- **Graceful Degradation**: Fallback to simulation when APIs fail
- **Error Logging**: Comprehensive error tracking and debugging

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Browser Dashboard                        │
│  (http://localhost:8080) - React-like UI with Chart.js     │
│  • Real-time charts • Analytics • Automation controls       │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│              Flask Frontend Server (app.py)                  │
│  Port: 8080 • Serves dashboard • Proxies requests           │
│  • Database operations • Request logging                    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│           Node.js Backend (src/index.js)                     │
│  Port: 3000 • AI service proxy • Circuit breakers           │
│  • Chaos engineering • Prometheus metrics                   │
│  • Global error handlers • Request validation               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│    AI Services (Gemini / Cohere / HuggingFace)              │
│    Or Simulation Fallback (when APIs unavailable)           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** v18+ ([Download](https://nodejs.org/))
- **Python** 3.8+ ([Download](https://www.python.org/))
- **Git** ([Download](https://git-scm.com/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Reevsay/ai-resilience-monitor.git
   cd ai-resilience-monitor
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the template
   cp .env.template .env
   
   # Edit .env and add your API keys (optional)
   # The system works with simulations if no API keys provided
   ```

5. **Start the backend** (Terminal 1)
   ```bash
   node src/index.js
   ```

6. **Start the frontend** (Terminal 2)
   ```bash
   python app.py
   ```

7. **Open your browser**
   ```
   http://localhost:8080
   ```

---

## 📖 Usage Guide

### Basic Operations

#### 1️⃣ **Send Manual Request**
- Select AI service (Gemini/Cohere/HuggingFace)
- Enter a prompt (e.g., "What is machine learning?")
- Click **"Send Request"**
- View response and latency

#### 2️⃣ **Start Automation**
- Click **"Start Automation"**
- Requests sent automatically every 2 seconds
- Watch metrics update in real-time
- Click **"Stop Automation"** to halt

#### 3️⃣ **Inject Chaos Experiment**
- Select service to test
- Choose chaos type (Latency/Failure/Timeout/etc.)
- Set intensity (0-100% or milliseconds)
- Set duration (10-120 seconds)
- Click **"Inject Chaos"**
- Observe system behavior

#### 4️⃣ **Monitor Circuit Breakers**
- View current state (CLOSED/OPEN/HALF_OPEN)
- Track failure counts and success counts
- See state transition history
- Reset breakers manually if needed

#### 5️⃣ **View Historical Data**
- Scroll to "Request History" section
- Filter by service or time range
- Export data to JSON
- Analyze trends and patterns

---

## � Configuration

### Environment Variables (.env)

```bash
# Node.js Backend Port
PORT=3000

# AI Service API Keys (Optional - uses simulation if not provided)
GOOGLE_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# API URLs (Optional - uses defaults)
GOOGLE_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent
COHERE_API_URL=https://api.cohere.ai/v1/generate
HUGGINGFACE_API_URL=https://api-inference.huggingface.co/models/gpt2
```

### Circuit Breaker Settings

Located in `src/index.js`:

```javascript
const circuitBreakers = {
  gemini: new CircuitBreaker('gemini', {
    failureThreshold: 5,      // Failures before opening
    successThreshold: 2,       // Successes to close from half-open
    timeout: 30000,            // Time before trying half-open (30s)
  }),
  // ... similar for cohere and huggingface
};
```

---

## 📊 Monitoring & Metrics

### Available Endpoints

**Backend (Port 3000):**
- `GET /test` - Health check
- `GET /metrics` - Current metrics JSON
- `POST /ai` - AI service proxy
- `GET /ai/health` - AI services health status
- `GET /prometheus` - Prometheus metrics

**Chaos Engineering:**
- `POST /chaos/inject` - Inject chaos experiment
- `POST /chaos/stop` - Stop chaos experiment
- `GET /chaos/status` - Get active experiments

**Circuit Breakers:**
- `GET /circuit-breaker/status` - Get all breaker states
- `POST /circuit-breaker/reset` - Reset breakers

**Frontend (Port 8080):**
- `GET /` - Dashboard UI
- `GET /api/metrics` - Metrics API
- `POST /api/log-request` - Log request to database
- `GET /api/history/requests` - Get request history
- `GET /api/database/stats` - Database statistics

---

## 🧪 Testing

### Manual Testing
1. Start both services
2. Open dashboard
3. Send requests manually
4. Verify metrics update correctly

### Automated Testing
1. Click "Start Automation"
2. Let run for 5-10 minutes
3. Verify:
   - Success rate is accurate
   - Charts update correctly
   - Circuit breakers respond to failures
   - Database logs all requests

### Chaos Testing
1. Inject latency (5000ms) on Gemini
2. Observe increased latency in charts
3. Inject failures (80% rate) on Cohere
4. Watch circuit breaker open after 5 failures
5. Stop chaos and verify recovery

---

## � Project Structure

```
ai-resilience-monitor/
├── src/
│   └── index.js              # Node.js backend (1105 lines)
├── templates/
│   └── dashboard.html        # Frontend UI (3985 lines)
├── app.py                    # Flask server (493 lines)
├── database.py               # SQLite handler (488 lines)
├── checkpoints/              # Project snapshots
│   ├── checkpoint2/          # Production-ready state
│   └── CHECKPOINTS_INDEX.md
├── documentation/            # Research & docs
│   ├── FLOWCHART_PROMPTS.md
│   ├── RESEARCH_GAPS.md
│   └── ...
├── literature/               # Research papers
├── data/                     # SQLite database
├── package.json              # Node.js dependencies
├── requirements.txt          # Python dependencies
├── .env.template             # Environment template
├── .gitignore               # Git ignore rules
├── CLEANUP_REPORT.md        # Cleanup documentation
└── README.md                # This file
```

---

## 🛠️ Technologies Used

### Backend
- **Node.js** - JavaScript runtime
- **Express.js** - Web framework
- **Axios** - HTTP client for API calls
- **prom-client** - Prometheus metrics

### Frontend
- **Flask** - Python web framework
- **HTML5/CSS3** - Modern web standards
- **JavaScript (ES6+)** - Client-side logic
- **Chart.js** - Data visualization
- **Bootstrap** - UI components

### Database
- **SQLite** - Lightweight database
- **Python sqlite3** - Database interface

### DevOps & Monitoring
- **Prometheus** - Metrics collection
- **Circuit Breakers** - Fault tolerance
- **Chaos Engineering** - Resilience testing

---

## � Security Notes

- **API Keys**: Never commit `.env` to Git (already in `.gitignore`)
- **CORS**: Currently set to allow all origins (`*`) - restrict in production
- **Rate Limiting**: Not implemented - add for production use
- **Authentication**: Not implemented - add for production deployment
- **HTTPS**: Use reverse proxy (nginx/Apache) for production

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 3000 is in use
netstat -ano | findstr :3000

# Kill the process if needed
taskkill /PID <process_id> /F

# Restart backend
node src/index.js
```

### Frontend shows "Backend Offline"
- Ensure backend is running on port 3000
- Check backend terminal for errors
- Verify `BACKEND_URL` in `app.py` is correct

### Database errors
```bash
# Backup current database
cp data/monitoring.db data/monitoring.db.backup

# Delete and recreate
rm data/monitoring.db
python app.py  # Will recreate tables
```

### Circuit breakers stuck OPEN
- Click "Reset All Circuit Breakers" button
- Or restart the backend service

---

## 📈 Performance

- **Backend Memory**: ~50-70 MB
- **Frontend Memory**: ~20-30 MB
- **Database Size**: ~1-2 KB per request
- **Max Throughput**: 100+ requests/second (simulated)
- **Latency Tracking**: Last 15 entries per service
- **Uptime**: Indefinite (with error handlers)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards
- **JavaScript**: Use ES6+ syntax, async/await
- **Python**: Follow PEP 8
- **Comments**: Document complex logic
- **Commits**: Use descriptive messages

---

## 📝 Changelog

### v2.0.3 (Current - October 24, 2024)
- ✅ Backend crash protection with global error handlers
- ✅ Accurate metrics (Total = Success + Failure)
- ✅ Line charts with real timestamps (HH:MM:SS)
- ✅ Circuit breakers wrap simulation fallback correctly
- ✅ Timestamp string-to-Date conversion fixes
- ✅ Project cleanup (15 unused files removed)
- ✅ Comprehensive documentation

### v2.0.2
- Circuit breaker state management improvements
- Chaos engineering enhancements

### v2.0.1
- Initial stable release
- Basic monitoring and circuit breakers

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Yashveer Ahlawat** - *Initial work* - [Reevsay](https://github.com/Reevsay)

---

## 🙏 Acknowledgments

- Circuit breaker pattern inspired by Michael Nygard's "Release It!"
- Chaos engineering concepts from Netflix's Chaos Monkey
- UI/UX inspired by Grafana and Prometheus dashboards

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Reevsay/ai-resilience-monitor/issues)
- **Email**: yashveer4661ahlawat@gmail.com
- **Documentation**: See `/documentation` folder for research papers

---

## 🎯 Roadmap

- [ ] Docker containerization
- [ ] Kubernetes deployment configs
- [ ] Real-time alerts (Email/Slack)
- [ ] Multi-user authentication
- [ ] Advanced analytics dashboard
- [ ] Load testing suite
- [ ] CI/CD pipeline
- [ ] API documentation (Swagger)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ for resilient AI systems

</div>