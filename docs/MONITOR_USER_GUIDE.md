# Comprehensive Service Monitor - User Guide

## What This Fixes

### ✅ Problems Solved
1. **Memory Crowding** - Kills ALL old processes before starting
2. **Manual Restarts** - Auto-restarts crashed services instantly
3. **No Visibility** - Opens dashboard in browser automatically
4. **Lost Crashes** - Logs every crash with reason and stderr
5. **Database Locking** - WAL mode enabled for concurrent access
6. **Process Orphans** - Cleans up zombie Node/Python processes

## Quick Start

### Option 1: PowerShell Script (Easiest)
```powershell
.\START-MONITOR.ps1
```
That's it! Everything starts automatically.

### Option 2: Manual Start
```powershell
# Kill old processes
Get-Process | Where-Object {$_.ProcessName -match "node|python"} | Stop-Process -Force

# Start monitor
python scripts\monitoring\monitor-all-services.py
```

## What It Does

### Phase 1: Cleanup 🧹
- Scans for ALL Node.js processes running `index.js`
- Scans for ALL Python processes running `app.py`
- Kills them (except itself)
- Waits 3 seconds for ports to release

### Phase 2: Service Start 🚀
1. **Starts Backend** (Node.js on port 3000)
   - With WAL mode for database
   - With 15s health check timeout
   - Captures crash logs
   
2. **Starts Frontend** (Flask on port 8080)
   - Connects to same database safely
   - Serves the dashboard
   - Auto-opens in browser

### Phase 3: Monitoring 👁️
Every 5 seconds:
- ✅ Checks if processes are alive
- ✅ Checks health endpoints
- ✅ Monitors memory usage
- ✅ Detects crashes and logs reasons
- ✅ Auto-restarts on failure (up to 200 times)

Every 1 minute:
- 📊 Logs status update

Every 5 minutes:
- 📋 Prints full status report

## Features

### Auto-Restart Logic
```
Backend/Frontend crashed or unhealthy?
  ↓
Wait 2 seconds
  ↓
Kill old process
  ↓
Start new process
  ↓
Verify health
  ↓
Continue monitoring
```

### Health Checks
- **Backend**: `GET http://localhost:3000/test`
- **Frontend**: `GET http://localhost:8080`
- **Timeout**: 15 seconds (tolerates chaos delays)
- **Max Failures**: 3 consecutive failures → restart

### Crash Detection
Detects and logs:
- Process died unexpectedly
- Health check timeouts
- Connection refused errors
- Startup failures with stderr
- Port conflicts

### Memory Monitoring
- Tracks RSS memory usage
- Reports in MB
- Logs with status updates
- Helps detect memory leaks

## Logs

### Console Output
Real-time log stream showing:
- Service startups
- Health check results  
- Restarts
- Errors
- Status reports

### File: `logs/all-services-monitor.log`
Permanent log with all events timestamped

## Status Report Example

```
======================================================================
SERVICE MONITOR STATUS REPORT
======================================================================
Start Time: 2025-11-10 05:00:45
Uptime: 1:23:15

BACKEND STATUS:
  Restarts: 2
  Current PID: 12345
  Memory: 58.3 MB
  Consecutive Failures: 0

FRONTEND STATUS:
  Restarts: 1
  Current PID: 12346
  Memory: 45.7 MB
  Consecutive Failures: 0

CRASH HISTORY (Last 10):
  [05:15:23] backend: Health check failures: Timeout (>15s)
  [05:45:12] frontend: Process died

======================================================================
```

## Running Chaos Tests

With monitor running, in a **new terminal**:

```powershell
# Quick validation test (2 minutes)
python scripts\testing\chaos-test.py --validation --output-dir chaos-validation

# Long-term test (24 hours)
python scripts\testing\chaos-test.py --duration 24 --output-dir chaos-24hr

# Custom duration (4 hours)
python scripts\testing\chaos-test.py --duration 4 --output-dir chaos-4hr
```

The monitor will:
- ✅ Keep services running during chaos
- ✅ Restart if they crash
- ✅ Handle database locks
- ✅ Tolerate chaos-induced delays

## Stopping Everything

### Method 1: Ctrl+C in Monitor Window
Press `Ctrl+C` in the monitor window. It will:
1. Show final status report
2. Stop backend
3. Stop frontend
4. Exit cleanly

### Method 2: Force Kill All
```powershell
Get-Process | Where-Object {$_.ProcessName -match "node|python"} | Stop-Process -Force
```

## Troubleshooting

### "Port already in use"
**Solution**: Monitor automatically detects and force-cleans port conflicts

### "Process died immediately"
**Check**: Look at the stderr in crash history
**Common causes**:
- Missing node_modules: `npm install`
- Missing Python packages: `pip install -r requirements.txt`
- Syntax error in code

### "Health checks always fail"
**Check**: Is chaos active? Health checks show "chaos testing active"
**Solution**: Monitor tolerates this with 15s timeout

### "Too many restarts"
**Check**: Crash history for patterns
**Solution**: Fix the underlying cause (database lock, syntax error, etc.)

### "Memory keeps growing"
**Cause**: Potential memory leak
**Solution**: Monitor will restart before it becomes critical

## Architecture

```
monitor-all-services.py
    │
    ├─> Cleanup Phase
    │   └─> Kill old Node/Python processes
    │
    ├─> Start Phase
    │   ├─> Start backend (Node.js)
    │   │   └─> Enable WAL mode
    │   └─> Start frontend (Flask)
    │       └─> Open browser
    │
    └─> Monitor Loop (every 5s)
        ├─> Check backend alive
        ├─> Check backend health
        ├─> Check frontend alive
        ├─> Check frontend health
        ├─> Log memory usage
        └─> Auto-restart on failure
```

## Key Improvements from Old Monitor

| Feature | Old Monitor | New Monitor |
|---------|-------------|-------------|
| Cleanup | Manual | ✅ Automatic |
| Frontend monitoring | ❌ No | ✅ Yes |
| Crash reasons | ❌ No | ✅ Logged |
| Memory tracking | ❌ No | ✅ Yes |
| Browser open | ❌ Manual | ✅ Auto |
| Restart limit | 100 | 200 (longer tests) |
| Health timeout | 5s | 15s (chaos-tolerant) |
| Process cleanup | Partial | ✅ Complete |

## Configuration

Edit `scripts/monitoring/monitor-all-services.py`:

```python
# Timeouts
CHECK_INTERVAL = 5          # Check every 5 seconds
HEALTH_CHECK_TIMEOUT = 15   # Health check timeout
MAX_CONSECUTIVE_FAILURES = 3 # Failures before restart

# Limits
MAX_RESTART_ATTEMPTS = 200  # Max restarts per service

# Ports
BACKEND_PORT = 3000
FRONTEND_PORT = 8080
```

## Best Practices

### For Long Chaos Tests (24h+)
1. Start monitor first
2. Wait until dashboard opens
3. Verify both services healthy
4. Then start chaos test
5. Monitor can run indefinitely

### For Development
1. Use monitor for auto-restart convenience
2. Watch console for errors
3. Check crash history for patterns
4. Fix issues and let it auto-restart

### For Production Testing
1. Review logs regularly
2. Check memory usage trends
3. Set up separate log analysis
4. Monitor crash frequency

## FAQ

**Q: Can I run chaos test without monitor?**
A: Yes, but services may crash and not restart

**Q: Does monitor interfere with chaos testing?**
A: No, it detects chaos and allows it

**Q: What if I need to update code?**
A: Stop monitor (Ctrl+C), update code, restart monitor

**Q: Can I monitor just backend?**
A: Yes, comment out frontend sections in code

**Q: How do I know if it's working?**
A: Dashboard opens automatically, console shows "Backend healthy"

## Technical Details

### Database Fixes Applied
- **WAL Mode**: Enables concurrent read/write
- **Busy Timeout**: 5000ms (Node.js) / 10000ms (Python)
- **Connection Timeout**: 10s (Python)

### Process Management
- Uses `psutil` for reliable process detection
- Creates new process groups (Windows)
- Captures stdout/stderr for crash diagnosis
- Graceful shutdown with timeout fallback

### Health Checks
- HTTP requests with timeout
- JSON response parsing
- Chaos-aware (detects `chaos_active` flag)
- Retry logic with exponential backoff

---

**Status**: ✅ READY FOR LONG-TERM CHAOS TESTING
**Version**: 2.0
**Last Updated**: November 10, 2025
