# 🚀 Quick Reference - New Project Structure

**Updated:** November 9, 2025

---

## 📂 Root Directory (Essentials Only)

```
ai-resilience-monitor/
├── app.py              # 🎯 Main Flask frontend server
├── README.md           # 📖 Project documentation
├── LICENSE             # ⚖️ License file
├── package.json        # 📦 Node.js dependencies
├── requirements.txt    # 🐍 Python dependencies
└── .gitignore          # 🚫 Git ignore rules
```

---

## 🗂️ Organized Folders

### 📚 `/docs` - All Documentation
All guides, fixes, and project documentation

| File | Description |
|------|-------------|
| `README.md` | Docs folder index |
| `CRASH_RECOVERY_GUIDE.md` | Backend auto-recovery |
| `ENHANCED_OUTPUT_GUIDE.md` | Live chaos output |
| `CUMULATIVE_REQUESTS_GUIDE.md` | SQLite persistence |
| `CHAOS_CRASH_FIX.md` | Unicode encoding fix |
| `CHAOS_OUTPUT_FIX.md` | Output streaming fix |
| `TOTAL_REQUESTS_FIX.md` | Request counter fix |
| `QUICK_REFERENCE_TOTAL_REQUESTS.md` | Quick reference |
| `FRONTEND_REDESIGN_SPECIFICATION.md` | UI spec |
| `LITERATURE_REVIEW.md` | Research review |
| `CLEANUP_REPORT.md` | Cleanup report |
| `REORGANIZATION_REPORT.md` | This reorganization |
| `CONTRIBUTING.md` | Contribution guide |

---

### 🔧 `/scripts` - Operational Scripts

#### 📡 `/scripts/monitoring` - Auto-Recovery Monitors
| Script | Purpose |
|--------|---------|
| `monitor-backend-enhanced.py` | Auto-restart Node.js backend |
| `monitor-frontend-continuous.py` | Auto-restart Flask frontend |

**Usage:**
```bash
python scripts/monitoring/monitor-backend-enhanced.py
python scripts/monitoring/monitor-frontend-continuous.py
```

---

#### 🧪 `/scripts/testing` - Chaos Engineering
| Script | Purpose |
|--------|---------|
| `chaos-test.py` | Comprehensive chaos testing with empirical validation |

**Usage:**
```bash
python scripts/testing/chaos-test.py
```

---

#### 🚀 `/scripts/setup` - Startup Scripts
| Script | Purpose |
|--------|---------|
| `START_MONITOR_ENHANCED.bat` | Windows batch startup |
| `start-monitor-enhanced.ps1` | PowerShell startup |

**Usage:**
```bash
# Batch
scripts\setup\START_MONITOR_ENHANCED.bat

# PowerShell
.\scripts\setup\start-monitor-enhanced.ps1
```

---

#### 🛠️ `/scripts/utilities` - Maintenance Tools
| Script | Purpose |
|--------|---------|
| `cleanup-project.py` | Remove duplicate/obsolete files |
| `reorganize-project.py` | Organize project structure |

**Usage:**
```bash
python scripts/utilities/cleanup-project.py
python scripts/utilities/reorganize-project.py
```

---

### ⚙️ `/config` - Configuration Files

| File | Purpose |
|------|---------|
| `README.md` | Config folder index |
| `.env` | **API keys & secrets** (⚠️ DO NOT COMMIT) |
| `prometheus.yml` | Prometheus metrics config |
| `docker-compose.yml` | Docker orchestration |
| `Dockerfile` | Container build instructions |

---

### 📋 `/logs` - Log Files

| File | Purpose |
|------|---------|
| `README.md` | Logs folder index |
| `frontend-monitor.log` | Frontend monitoring logs |
| `monitor.log` | Backend monitoring logs |

> **Note:** Log files are excluded from git (see `.gitignore`)

---

### 🗄️ `/backend` - Backend Modules

| File | Purpose |
|------|---------|
| `README.md` | Backend folder index |
| `database.py` | SQLite database operations |

---

### 💻 `/src` - Node.js Backend Source

Main backend API server files:
- `index.js` - Main server (1537 lines)
- `multiAIService.js` - AI service integration
- `failureInjector.js` - Chaos injection
- `alertMonitor.js` - Alert system
- `notificationService.js` - Notifications
- `dashboard.html` - Dashboard UI

---

### 🎨 `/templates` - Flask Templates

Flask frontend templates:
- `dashboard.html` - Main dashboard template

---

### 💾 `/data` - Data Storage

SQLite database and data files:
- `monitoring.db` - SQLite database
- `README.md` - Data folder index

---

### 🧪 `/test` - Test Scripts

Various test scripts:
- `ci-test.js`
- `load-tester.js`
- `metrics-test.js`
- `payloads.json`

---

### 📖 `/documentation` - Research Documentation

Research-related documentation and gap analysis

---

### 📚 `/literature` - Research Papers

Base papers and references:
- `Base Paper.txt`
- `reference paper.txt`
- `PAPER_SUMMARIES.md`

---

### 💾 `/checkpoints` - Version Checkpoints

Backup versions of major iterations

---

### 📊 `/chaos-test-results` - Test Results

Output from chaos testing runs

---

## 🎯 Common Commands (Updated Paths)

### Start Everything (Enhanced Monitoring)
```bash
# Windows (Batch)
scripts\setup\START_MONITOR_ENHANCED.bat

# PowerShell
.\scripts\setup\start-monitor-enhanced.ps1
```

### Manual Start

**Frontend (Flask):**
```bash
python app.py
```

**Backend (Node.js):**
```bash
cd src
npm install
node index.js
```

### Run Chaos Testing
```bash
python scripts/testing/chaos-test.py
```

### Monitoring
```bash
# Backend monitor
python scripts/monitoring/monitor-backend-enhanced.py

# Frontend monitor
python scripts/monitoring/monitor-frontend-continuous.py
```

---

## 📝 Important Notes

### ⚠️ Security
- **Never commit** `config/.env` to version control
- Contains sensitive API keys
- Use `.env.example` as template

### 🔄 Path Updates
If scripts reference old paths, update them to new locations:
- `monitor-backend-enhanced.py` → `scripts/monitoring/monitor-backend-enhanced.py`
- `chaos-test.py` → `scripts/testing/chaos-test.py`
- `.env` → `config/.env`
- `database.py` → `backend/database.py`

### 📊 Logs
- Logs grow over time
- Consider log rotation
- Excluded from git

---

## 🎉 Benefits of New Structure

✅ **Cleaner Root** - Only 7 essential files  
✅ **Logical Organization** - Files grouped by function  
✅ **Easy Navigation** - Clear folder purposes  
✅ **Professional** - Follows industry standards  
✅ **Better Maintainability** - README in each folder  
✅ **Version Control Friendly** - Proper .gitignore  

---

## 🆘 Need Help?

- **Guides:** Check `/docs` folder
- **API Docs:** See `README.md`
- **Contributing:** See `docs/CONTRIBUTING.md`
- **Issues:** Check fix guides in `/docs`

---

**Project reorganized:** November 9, 2025  
**Structure version:** 2.0  
**All processes:** ✅ Still running (no interruption)
