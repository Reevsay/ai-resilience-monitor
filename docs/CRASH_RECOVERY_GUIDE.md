# 🔧 Backend Crash Recovery Guide

## ❌ Problem: Backend Keeps Crashing

Your backend is crashing and not recovering automatically. This guide will help you fix it.

---

## ✅ Solution: Enhanced Monitoring Script

I've created an **enhanced monitoring script** that:
- ✓ Checks health every **5 seconds** (faster detection)
- ✓ Automatically **restarts** on crash
- ✓ **Kills zombie processes** before restarting
- ✓ Logs **detailed error information**
- ✓ Monitors **CPU and memory usage**
- ✓ Handles **100 restart attempts** before giving up

---

## 🚀 Quick Fix (3 Steps)

### Step 1: Stop Everything
```powershell
# Kill any running Node.js backend
Get-Process -Name node -ErrorAction SilentlyContinue | Stop-Process -Force

# Kill any running monitors
Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*monitor*" } | Stop-Process -Force
```

### Step 2: Start Enhanced Monitor
**Double-click**: `START_MONITOR_ENHANCED.bat`

OR run in PowerShell:
```powershell
.\start-monitor-enhanced.ps1
```

### Step 3: Watch the Logs
The monitor will:
1. ✅ Kill any existing backend processes
2. ✅ Start fresh backend
3. ✅ Monitor health every 5 seconds
4. ✅ Auto-restart on crash
5. ✅ Log everything to `monitor.log`

---

## 📊 What You'll See

### Normal Operation:
```
[2025-11-09 19:45:30] [INFO] ✅ Backend started successfully (PID: 12345)
[2025-11-09 19:46:30] [STATUS] ✅ Backend healthy | Uptime: 1m 0s | CPU: 2.3%, Memory: 45.2MB | Checks: 12
[2025-11-09 19:47:30] [STATUS] ✅ Backend healthy | Uptime: 2m 0s | CPU: 1.8%, Memory: 46.1MB | Checks: 24
```

### When Crash Happens:
```
[2025-11-09 19:48:15] [ERROR] ❌ Backend process died!
[2025-11-09 19:48:15] [ERROR] Exit code: 1
[2025-11-09 19:48:15] [INFO] 🔄 Restarting backend (attempt 1)...
[2025-11-09 19:48:18] [INFO] ✅ Backend started successfully (PID: 12456)
```

---

## 🔍 Checking If It's Working

### 1. Check Monitor Status
Look for this in the console:
```
✅ Backend healthy | Uptime: 5m 23s | CPU: 2.1%, Memory: 44.8MB
```

### 2. Check Backend Directly
Open browser: http://localhost:3000/test

Should see: `{"status":"ok","message":"Backend is running"}`

### 3. Check Log File
Open `monitor.log` in the project folder:
```
[2025-11-09 19:45:30] [SUCCESS] ✅ Backend started successfully
[2025-11-09 19:46:30] [STATUS] ✅ Backend healthy
```

---

## 🐛 Common Issues & Fixes

### Issue 1: "Module psutil not found"
**Fix**:
```powershell
pip install psutil requests
```

### Issue 2: "Backend script not found"
**Fix**: Make sure you're in the correct directory
```powershell
cd "ai-resilience-monitor"
.\start-monitor-enhanced.ps1
```

### Issue 3: Backend crashes immediately
**Check**: `monitor.log` for error details

**Common causes**:
- Port 3000 already in use
- Missing dependencies
- Syntax errors in code

**Fix port conflict**:
```powershell
# Find what's using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### Issue 4: Monitor keeps restarting backend
**Cause**: Backend is unhealthy (not responding to health checks)

**Check**:
1. Look at backend logs in monitor console
2. Check for errors in `monitor.log`
3. Try starting backend manually: `node src/index.js`

### Issue 5: "Too many consecutive failures"
**Cause**: Backend crashes 5 times in a row

**Fix**:
1. Check `monitor.log` for error messages
2. Fix the underlying issue
3. Restart monitor

---

## 📝 Differences: Old vs Enhanced Monitor

| Feature | Old Monitor | Enhanced Monitor |
|---------|-------------|------------------|
| Check Interval | 10 seconds | **5 seconds** |
| Process Cleanup | ❌ No | ✅ **Yes** (kills zombies) |
| Error Logging | Basic | ✅ **Detailed** (exit codes, stack traces) |
| Memory Monitoring | ❌ No | ✅ **Yes** |
| CPU Monitoring | ❌ No | ✅ **Yes** |
| Max Restarts | 10 | ✅ **100** |
| Log File | ❌ No | ✅ **Yes** (monitor.log) |
| Process Info | ❌ No | ✅ **Yes** (PID, uptime, resources) |

---

## 🎯 Best Practices

### For Development:
1. **Always use the monitor** - Don't run backend manually
2. **Keep monitor running** - Leave it open in a terminal
3. **Check logs regularly** - Review `monitor.log` for patterns
4. **Fix crashes** - Don't rely on auto-restart forever

### For Production:
1. **Use PM2 or similar** - Better for production
2. **Set up alerts** - Get notified on crashes
3. **Monitor metrics** - Track CPU, memory, response times
4. **Log aggregation** - Centralize logs for analysis

---

## 📊 Monitoring the Monitor

### Is the monitor running?
```powershell
Get-Process -Name python | Where-Object { $_.CommandLine -like "*monitor*" }
```

### How many times has backend restarted?
Check `monitor.log`:
```powershell
Select-String "Restarting backend" monitor.log | Measure-Object
```

### What's the current uptime?
Look for latest "Backend healthy" message in console or log

---

## 🔧 Advanced Configuration

You can edit `monitor-backend-enhanced.py` to customize:

```python
# Line 14-16: Configuration
BACKEND_PORT = 3000          # Change if using different port
CHECK_INTERVAL = 5           # How often to check (seconds)
MAX_RESTART_ATTEMPTS = 100   # Max restarts before giving up
RESTART_DELAY = 3            # Wait before restarting (seconds)
```

---

## 🆘 Still Crashing? Debug Checklist

If backend still crashes with the enhanced monitor:

- [ ] Check `monitor.log` for error messages
- [ ] Run backend manually: `node src/index.js` and watch output
- [ ] Check Node.js version: `node --version` (should be 14+)
- [ ] Check for missing dependencies: `npm install`
- [ ] Check `.env` file exists with API keys
- [ ] Check port 3000 is not in use: `netstat -ano | findstr :3000`
- [ ] Check system resources (CPU, memory not maxed out)
- [ ] Check for syntax errors: `node --check src/index.js`
- [ ] Review recent code changes for bugs
- [ ] Check for infinite loops or memory leaks

---

## 📞 Quick Commands Reference

### Start Monitor
```powershell
# Easiest way
.\START_MONITOR_ENHANCED.bat

# Or PowerShell
.\start-monitor-enhanced.ps1

# Or directly
python monitor-backend-enhanced.py
```

### Stop Everything
```powershell
# Stop all Node.js
Get-Process -Name node | Stop-Process -Force

# Stop all Python monitors
Get-Process -Name python | Where-Object { $_.CommandLine -like "*monitor*" } | Stop-Process -Force
```

### Check Status
```powershell
# Check backend
curl http://localhost:3000/test

# Check processes
Get-Process -Name node, python
```

### View Logs
```powershell
# Live tail (PowerShell)
Get-Content monitor.log -Tail 20 -Wait

# View all
cat monitor.log

# Search for errors
Select-String "ERROR" monitor.log
```

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Console shows "Backend healthy" every minute
2. ✅ Backend responds to http://localhost:3000/test
3. ✅ Dashboard loads at http://localhost:8080
4. ✅ No crash messages in `monitor.log`
5. ✅ Uptime keeps increasing
6. ✅ CPU and memory usage stable

---

## 🎉 Summary

**Before**: Backend crashes → Manual restart required → Downtime

**After**: Backend crashes → Monitor detects in 5s → Auto-restart → Back online in 8s

**Total downtime reduced from minutes to seconds!**

---

## 📚 Next Steps

1. ✅ Start enhanced monitor: `.\START_MONITOR_ENHANCED.bat`
2. ✅ Test crash recovery: Kill backend manually and watch it restart
3. ✅ Monitor for 1 hour to ensure stability
4. ✅ Review `monitor.log` for any issues
5. ✅ If stable, leave running 24/7

**Good luck!** 🚀
