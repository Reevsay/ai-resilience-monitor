"""
Complete Service Monitor with Auto-Recovery and Crash Detection
Monitors backend, frontend, and provides live diagnostics
Features:
- Kills all old processes before starting
- Auto-restarts on crash
- Live crash detection and logging
- Memory monitoring
- Web view integration
- Runs until script completion or max duration
"""

import subprocess
import time
import requests
import sys
import os
from datetime import datetime, timedelta
import psutil
import webbrowser
import json
from pathlib import Path

# Configuration
BACKEND_PORT = 3000
FRONTEND_PORT = 8080
BACKEND_URL = f"http://localhost:{BACKEND_PORT}/test"
FRONTEND_URL = f"http://localhost:{FRONTEND_PORT}"
FRONTEND_HEALTH_URL = f"http://localhost:{FRONTEND_PORT}/api/health"  # Use health endpoint, not root
CHECK_INTERVAL = 5  # seconds
MAX_RESTART_ATTEMPTS = 200  # Effectively unlimited for long tests
HEALTH_CHECK_TIMEOUT = 15  # seconds
MAX_CONSECUTIVE_FAILURES = 3  # Failures before restart

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..", "..")
BACKEND_SCRIPT = os.path.join(PROJECT_ROOT, "src", "index.js")
FRONTEND_SCRIPT = os.path.join(PROJECT_ROOT, "app.py")
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "all-services-monitor.log")

# Global state
backend_process = None
frontend_process = None
backend_restart_count = 0
frontend_restart_count = 0
backend_consecutive_failures = 0
frontend_consecutive_failures = 0
start_time = datetime.now()
crash_history = []

def log(message, level="INFO"):
    """Log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    print(log_message)
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
    except Exception as e:
        print(f"Failed to write to log file: {e}")

def kill_all_old_processes():
    """Kill ALL old Node.js and Python processes to prevent memory crowding"""
    killed = []
    try:
        log("🧹 Cleaning up old processes...", "INFO")
        
        # Kill Node.js processes
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'node' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any('index.js' in str(cmd) for cmd in cmdline):
                        log(f"   Killing old backend (PID: {proc.info['pid']})", "INFO")
                        proc.kill()
                        proc.wait(timeout=5)
                        killed.append(('backend', proc.info['pid']))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
        
        # Kill Python processes (app.py)
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'python' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any('app.py' in str(cmd) for cmd in cmdline):
                        # Don't kill ourselves!
                        if proc.info['pid'] != os.getpid():
                            log(f"   Killing old frontend (PID: {proc.info['pid']})", "INFO")
                            proc.kill()
                            proc.wait(timeout=5)
                            killed.append(('frontend', proc.info['pid']))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass
        
        if killed:
            log(f"✅ Cleaned up {len(killed)} old processes", "SUCCESS")
            time.sleep(3)  # Wait for ports to be released
        else:
            log("✅ No old processes to clean", "INFO")
        
        return killed
    except Exception as e:
        log(f"Error during cleanup: {e}", "ERROR")
        return killed

def check_port_available(port):
    """Check if a port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def get_process_memory(pid):
    """Get memory usage of a process in MB"""
    try:
        proc = psutil.Process(pid)
        return proc.memory_info().rss / 1024 / 1024  # Convert to MB
    except:
        return 0

def check_backend_health():
    """Check if backend is responding"""
    try:
        response = requests.get(BACKEND_URL, timeout=HEALTH_CHECK_TIMEOUT)
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('chaos_active', False):
                    log("Backend healthy (chaos testing active)", "INFO")
            except:
                pass
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except requests.exceptions.Timeout:
        return False, f"Timeout (>{HEALTH_CHECK_TIMEOUT}s)"
    except Exception as e:
        return False, str(e)

def check_frontend_health():
    """Check if frontend is responding"""
    try:
        response = requests.get(FRONTEND_HEALTH_URL, timeout=HEALTH_CHECK_TIMEOUT)
        if response.status_code == 200:
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except requests.exceptions.Timeout:
        return False, f"Timeout (>{HEALTH_CHECK_TIMEOUT}s)"
    except Exception as e:
        return False, str(e)

def start_backend():
    """Start the Node.js backend"""
    global backend_process, backend_restart_count
    
    try:
        # Ensure port is available
        if not check_port_available(BACKEND_PORT):
            log(f"⚠️  Port {BACKEND_PORT} still in use, force cleaning...", "WARNING")
            kill_all_old_processes()
            time.sleep(3)
        
        log("Starting backend server...", "INFO")
        
        # Start new process with output capture
        backend_process = subprocess.Popen(
            ["node", BACKEND_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=PROJECT_ROOT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )
        
        backend_restart_count += 1
        
        # Wait for server to start
        time.sleep(5)
        
        # Check if process is still running
        if backend_process.poll() is not None:
            # Process already died - get error
            stdout, stderr = backend_process.communicate(timeout=1)
            log(f"❌ Backend failed to start!", "ERROR")
            if stdout:
                log(f"STDOUT: {stdout.decode('utf-8', errors='ignore')[:500]}", "ERROR")
            if stderr:
                log(f"STDERR: {stderr.decode('utf-8', errors='ignore')[:500]}", "ERROR")
            
            crash_history.append({
                'time': datetime.now(),
                'service': 'backend',
                'reason': 'Failed to start',
                'stderr': stderr.decode('utf-8', errors='ignore')[:200] if stderr else 'Unknown'
            })
            return False
        
        # Verify health
        healthy, reason = check_backend_health()
        if healthy:
            memory = get_process_memory(backend_process.pid)
            log(f"✅ Backend started (PID: {backend_process.pid}, Memory: {memory:.1f}MB)", "SUCCESS")
            return True
        else:
            log(f"⚠️  Backend started but unhealthy: {reason}", "WARNING")
            return False
        
    except FileNotFoundError:
        log(f"❌ Backend script not found: {BACKEND_SCRIPT}", "ERROR")
        return False
    except Exception as e:
        log(f"❌ Failed to start backend: {e}", "ERROR")
        return False

def start_frontend():
    """Start the Flask frontend"""
    global frontend_process, frontend_restart_count
    
    try:
        # Ensure port is available
        if not check_port_available(FRONTEND_PORT):
            log(f"⚠️  Port {FRONTEND_PORT} still in use, force cleaning...", "WARNING")
            kill_all_old_processes()
            time.sleep(3)
        
        log("Starting frontend server...", "INFO")
        
        # Start new process
        frontend_process = subprocess.Popen(
            ["python", FRONTEND_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=PROJECT_ROOT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )
        
        frontend_restart_count += 1
        
        # Wait for server to start
        time.sleep(5)
        
        # Check if process is still running
        if frontend_process.poll() is not None:
            stdout, stderr = frontend_process.communicate(timeout=1)
            log(f"❌ Frontend failed to start!", "ERROR")
            if stdout:
                log(f"STDOUT: {stdout.decode('utf-8', errors='ignore')[:500]}", "ERROR")
            if stderr:
                log(f"STDERR: {stderr.decode('utf-8', errors='ignore')[:500]}", "ERROR")
            
            crash_history.append({
                'time': datetime.now(),
                'service': 'frontend',
                'reason': 'Failed to start',
                'stderr': stderr.decode('utf-8', errors='ignore')[:200] if stderr else 'Unknown'
            })
            return False
        
        # Verify health
        healthy, reason = check_frontend_health()
        if healthy:
            memory = get_process_memory(frontend_process.pid)
            log(f"✅ Frontend started (PID: {frontend_process.pid}, Memory: {memory:.1f}MB)", "SUCCESS")
            return True
        else:
            log(f"⚠️  Frontend started but unhealthy: {reason}", "WARNING")
            return False
        
    except FileNotFoundError:
        log(f"❌ Frontend script not found: {FRONTEND_SCRIPT}", "ERROR")
        return False
    except Exception as e:
        log(f"❌ Failed to start frontend: {e}", "ERROR")
        return False

def restart_backend():
    """Restart backend service"""
    global backend_process, backend_consecutive_failures
    
    log(f"🔄 Restarting backend (attempt {backend_restart_count + 1})...", "INFO")
    
    # Stop existing process
    if backend_process and backend_process.poll() is None:
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
        except:
            try:
                backend_process.kill()
            except:
                pass
    
    time.sleep(2)
    return start_backend()

def restart_frontend():
    """Restart frontend service"""
    global frontend_process, frontend_consecutive_failures
    
    log(f"🔄 Restarting frontend (attempt {frontend_restart_count + 1})...", "INFO")
    
    # Stop existing process
    if frontend_process and frontend_process.poll() is None:
        try:
            frontend_process.terminate()
            frontend_process.wait(timeout=5)
        except:
            try:
                frontend_process.kill()
            except:
                pass
    
    time.sleep(2)
    return start_frontend()

def open_dashboard():
    """Open dashboard in web browser"""
    try:
        log(f"🌐 Opening dashboard in browser: {FRONTEND_URL}", "INFO")
        webbrowser.open(FRONTEND_URL)
    except Exception as e:
        log(f"Failed to open browser: {e}", "WARNING")

def generate_status_report():
    """Generate comprehensive status report"""
    uptime = datetime.now() - start_time
    
    report = f"""
{'='*70}
SERVICE MONITOR STATUS REPORT
{'='*70}
Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
Uptime: {str(uptime).split('.')[0]}

BACKEND STATUS:
  Restarts: {backend_restart_count}
  Current PID: {backend_process.pid if backend_process and backend_process.poll() is None else 'Not running'}
  Memory: {get_process_memory(backend_process.pid) if backend_process and backend_process.poll() is None else 0:.1f} MB
  Consecutive Failures: {backend_consecutive_failures}

FRONTEND STATUS:
  Restarts: {frontend_restart_count}
  Current PID: {frontend_process.pid if frontend_process and frontend_process.poll() is None else 'Not running'}
  Memory: {get_process_memory(frontend_process.pid) if frontend_process and frontend_process.poll() is None else 0:.1f} MB
  Consecutive Failures: {frontend_consecutive_failures}

CRASH HISTORY (Last 10):
"""
    
    for crash in crash_history[-10:]:
        report += f"  [{crash['time'].strftime('%H:%M:%S')}] {crash['service']}: {crash['reason']}\n"
    
    if not crash_history:
        report += "  No crashes detected\n"
    
    report += f"\n{'='*70}\n"
    
    return report

def main():
    global backend_consecutive_failures, frontend_consecutive_failures
    
    log("="*70, "INFO")
    log("🚀 AI RESILIENCE MONITOR - ALL SERVICES MONITOR", "INFO")
    log("="*70, "INFO")
    log(f"Backend URL: {BACKEND_URL}", "INFO")
    log(f"Frontend URL: {FRONTEND_URL}", "INFO")
    log(f"Check interval: {CHECK_INTERVAL} seconds", "INFO")
    log(f"Health timeout: {HEALTH_CHECK_TIMEOUT} seconds", "INFO")
    log(f"Log file: {LOG_FILE}", "INFO")
    log("="*70, "INFO")
    
    # Step 1: Clean up all old processes
    log("\n🧹 PHASE 1: Cleanup", "INFO")
    killed = kill_all_old_processes()
    
    # Step 2: Start services
    log("\n🚀 PHASE 2: Starting Services", "INFO")
    
    backend_ok = start_backend()
    if not backend_ok:
        log("❌ Failed to start backend initially. Will retry in monitoring loop.", "ERROR")
    
    time.sleep(3)
    
    frontend_ok = start_frontend()
    if not frontend_ok:
        log("❌ Failed to start frontend initially. Will retry in monitoring loop.", "ERROR")
    
    # Step 3: Open dashboard
    if frontend_ok:
        time.sleep(2)
        open_dashboard()
    
    # Step 4: Monitoring loop
    log("\n👁️  PHASE 3: Monitoring (Press Ctrl+C to stop)", "INFO")
    log("="*70, "INFO")
    
    check_count = 0
    
    try:
        while True:
            check_count += 1
            time.sleep(CHECK_INTERVAL)
            
            # Check backend
            if backend_process is None or backend_process.poll() is not None:
                log("❌ Backend process died!", "ERROR")
                crash_history.append({
                    'time': datetime.now(),
                    'service': 'backend',
                    'reason': 'Process died',
                    'stderr': 'Process not running'
                })
                restart_backend()
                backend_consecutive_failures = 0
            else:
                healthy, reason = check_backend_health()
                if not healthy:
                    backend_consecutive_failures += 1
                    log(f"⚠️  Backend health check failed ({backend_consecutive_failures}/{MAX_CONSECUTIVE_FAILURES}): {reason}", "WARNING")
                    
                    if backend_consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                        log(f"❌ Backend unhealthy after {MAX_CONSECUTIVE_FAILURES} checks. Restarting...", "ERROR")
                        crash_history.append({
                            'time': datetime.now(),
                            'service': 'backend',
                            'reason': f'Health check failures: {reason}',
                            'stderr': reason
                        })
                        restart_backend()
                        backend_consecutive_failures = 0
                else:
                    backend_consecutive_failures = 0
                    if check_count % 12 == 0:  # Every minute
                        memory = get_process_memory(backend_process.pid)
                        uptime = datetime.now() - start_time
                        log(f"✅ Backend healthy | Uptime: {str(uptime).split('.')[0]} | Memory: {memory:.1f}MB | Checks: {check_count}", "STATUS")
            
            # Check frontend
            if frontend_process is None or frontend_process.poll() is not None:
                log("❌ Frontend process died!", "ERROR")
                crash_history.append({
                    'time': datetime.now(),
                    'service': 'frontend',
                    'reason': 'Process died',
                    'stderr': 'Process not running'
                })
                restart_frontend()
                frontend_consecutive_failures = 0
            else:
                healthy, reason = check_frontend_health()
                if not healthy:
                    frontend_consecutive_failures += 1
                    log(f"⚠️  Frontend health check failed ({frontend_consecutive_failures}/{MAX_CONSECUTIVE_FAILURES}): {reason}", "WARNING")
                    
                    if frontend_consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                        log(f"❌ Frontend unhealthy after {MAX_CONSECUTIVE_FAILURES} checks. Restarting...", "ERROR")
                        crash_history.append({
                            'time': datetime.now(),
                            'service': 'frontend',
                            'reason': f'Health check failures: {reason}',
                            'stderr': reason
                        })
                        restart_frontend()
                        frontend_consecutive_failures = 0
                else:
                    frontend_consecutive_failures = 0
            
            # Print status every 5 minutes
            if check_count % 60 == 0:
                print(generate_status_report())
    
    except KeyboardInterrupt:
        log("\n\n🛑 Shutting down monitor...", "INFO")
        print(generate_status_report())
        
        # Cleanup
        if backend_process and backend_process.poll() is None:
            log("Stopping backend...", "INFO")
            backend_process.terminate()
        if frontend_process and frontend_process.poll() is None:
            log("Stopping frontend...", "INFO")
            frontend_process.terminate()
        
        log("✅ Monitor stopped", "SUCCESS")
        sys.exit(0)

if __name__ == "__main__":
    main()
