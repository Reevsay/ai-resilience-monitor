"""
Enhanced Backend Monitor with Auto-Recovery
Monitors the Node.js backend and automatically restarts it if it crashes
Features:
- Health checks every 5 seconds
- Automatic restart on crash
- Detailed logging
- Process management
- Memory usage monitoring
"""

import subprocess
import time
import requests
import sys
import os
from datetime import datetime
import psutil

# Configuration
BACKEND_PORT = 3000
BACKEND_URL = f"http://localhost:{BACKEND_PORT}/test"
CHECK_INTERVAL = 5  # seconds
MAX_RESTART_ATTEMPTS = 100  # Maximum restart attempts before giving up
RESTART_DELAY = 3  # seconds to wait before restarting
HEALTH_CHECK_TIMEOUT = 15  # Increased timeout for chaos testing scenarios (was 5)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..", "..")  # Go up to project root from scripts/monitoring
BACKEND_SCRIPT = os.path.join(PROJECT_ROOT, "src", "index.js")
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "monitor.log")

# Global state
backend_process = None
restart_count = 0
last_restart_time = None
consecutive_failures = 0

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

def check_health():
    """Check if backend is responding"""
    try:
        response = requests.get(BACKEND_URL, timeout=HEALTH_CHECK_TIMEOUT)
        if response.status_code == 200:
            # Check if chaos is active - log but don't fail
            try:
                data = response.json()
                if data.get('chaos_active', False):
                    log("Backend healthy (chaos testing active)", "INFO")
            except:
                pass
            return True
        else:
            log(f"Backend returned status code {response.status_code}", "WARNING")
            return False
    except requests.exceptions.ConnectionError:
        log("Backend not responding (connection refused)", "WARNING")
        return False
    except requests.exceptions.Timeout:
        log(f"Backend health check timed out (>{HEALTH_CHECK_TIMEOUT}s)", "WARNING")
        return False
    except Exception as e:
        log(f"Health check error: {e}", "ERROR")
        return False

def kill_existing_backend():
    """Kill any existing Node.js backend processes"""
    killed = False
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Check if it's a node process running index.js
                if proc.info['name'] and 'node' in proc.info['name'].lower():
                    cmdline = proc.info['cmdline']
                    if cmdline and any('index.js' in str(cmd) for cmd in cmdline):
                        log(f"Killing existing backend process (PID: {proc.info['pid']})", "INFO")
                        proc.kill()
                        proc.wait(timeout=5)
                        killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except Exception as e:
        log(f"Error killing existing processes: {e}", "ERROR")
    
    if killed:
        time.sleep(2)  # Wait for process to fully terminate
    
    return killed

def start_backend():
    """Start the Node.js backend"""
    global backend_process, restart_count, last_restart_time
    
    try:
        # Kill any existing backend first
        kill_existing_backend()
        
        log("Starting backend server...", "INFO")
        
        # Start new process
        backend_process = subprocess.Popen(
            ["node", BACKEND_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=SCRIPT_DIR,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
        )
        
        restart_count += 1
        last_restart_time = datetime.now()
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Check if process is still running
        if backend_process.poll() is not None:
            # Process already died
            stdout, stderr = backend_process.communicate()
            log(f"Backend failed to start!", "ERROR")
            log(f"STDOUT: {stdout.decode('utf-8', errors='ignore')}", "ERROR")
            log(f"STDERR: {stderr.decode('utf-8', errors='ignore')}", "ERROR")
            return False
        
        log(f"✅ Backend started successfully (PID: {backend_process.pid})", "SUCCESS")
        return True
        
    except FileNotFoundError:
        log(f"❌ Backend script not found: {BACKEND_SCRIPT}", "ERROR")
        return False
    except Exception as e:
        log(f"❌ Failed to start backend: {e}", "ERROR")
        return False

def restart_backend():
    """Restart the backend server"""
    global backend_process, consecutive_failures
    
    if restart_count >= MAX_RESTART_ATTEMPTS:
        log(f"❌ Maximum restart attempts ({MAX_RESTART_ATTEMPTS}) reached. Giving up.", "ERROR")
        return False
    
    log(f"🔄 Restarting backend (attempt {restart_count + 1})...", "INFO")
    
    # Stop existing process if running
    if backend_process and backend_process.poll() is None:
        try:
            log("Stopping existing backend process...", "INFO")
            backend_process.terminate()
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            log("Force killing backend process...", "WARNING")
            backend_process.kill()
        except Exception as e:
            log(f"Error stopping process: {e}", "ERROR")
    
    # Wait before restarting
    time.sleep(RESTART_DELAY)
    
    # Start backend
    if start_backend():
        consecutive_failures = 0
        return True
    else:
        consecutive_failures += 1
        return False

def get_process_info():
    """Get process information for monitoring"""
    try:
        if backend_process and backend_process.poll() is None:
            proc = psutil.Process(backend_process.pid)
            cpu_percent = proc.cpu_percent(interval=1)
            memory_mb = proc.memory_info().rss / 1024 / 1024
            return f"CPU: {cpu_percent:.1f}%, Memory: {memory_mb:.1f}MB"
        return "Process not running"
    except Exception as e:
        return f"Error getting info: {e}"

def main():
    """Main monitoring loop"""
    global consecutive_failures
    
    log("=" * 60, "INFO")
    log("🚀 Backend Monitor Started", "INFO")
    log(f"Monitoring: {BACKEND_URL}", "INFO")
    log(f"Check interval: {CHECK_INTERVAL} seconds", "INFO")
    log(f"Log file: {LOG_FILE}", "INFO")
    log("=" * 60, "INFO")
    
    # Initial start
    if not start_backend():
        log("❌ Failed to start backend initially. Retrying...", "ERROR")
        time.sleep(5)
        if not start_backend():
            log("❌ Cannot start backend after retry. Exiting.", "ERROR")
            return
    
    last_status_log = time.time()
    health_check_count = 0
    
    try:
        while True:
            health_check_count += 1
            
            # Check if process is still running
            if backend_process.poll() is not None:
                log("❌ Backend process died!", "ERROR")
                consecutive_failures += 1
                
                # Try to get exit code and output
                try:
                    stdout, stderr = backend_process.communicate(timeout=1)
                    log(f"Exit code: {backend_process.returncode}", "ERROR")
                    if stdout:
                        log(f"STDOUT: {stdout.decode('utf-8', errors='ignore')[:500]}", "ERROR")
                    if stderr:
                        log(f"STDERR: {stderr.decode('utf-8', errors='ignore')[:500]}", "ERROR")
                except:
                    pass
                
                if not restart_backend():
                    log("❌ Failed to restart backend", "ERROR")
                    if consecutive_failures >= 5:
                        log("❌ Too many consecutive failures. Exiting.", "ERROR")
                        break
                    time.sleep(10)
                continue
            
            # Health check
            is_healthy = check_health()
            
            if is_healthy:
                consecutive_failures = 0
                
                # Log status every minute
                if time.time() - last_status_log >= 60:
                    process_info = get_process_info()
                    uptime = (datetime.now() - last_restart_time).total_seconds() if last_restart_time else 0
                    uptime_str = f"{int(uptime // 60)}m {int(uptime % 60)}s"
                    log(f"✅ Backend healthy | Uptime: {uptime_str} | {process_info} | Checks: {health_check_count}", "STATUS")
                    last_status_log = time.time()
            else:
                consecutive_failures += 1
                log(f"⚠️  Health check failed ({consecutive_failures} consecutive failures)", "WARNING")
                
                if consecutive_failures >= 3:
                    log("❌ Backend unhealthy after 3 checks. Restarting...", "ERROR")
                    if not restart_backend():
                        log("❌ Failed to restart backend", "ERROR")
                        if consecutive_failures >= 5:
                            log("❌ Too many consecutive failures. Exiting.", "ERROR")
                            break
                        time.sleep(10)
            
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        log("\n🛑 Monitor stopped by user", "INFO")
    except Exception as e:
        log(f"❌ Monitor error: {e}", "ERROR")
        import traceback
        log(traceback.format_exc(), "ERROR")
    finally:
        # Cleanup
        if backend_process and backend_process.poll() is None:
            log("Stopping backend process...", "INFO")
            try:
                backend_process.terminate()
                backend_process.wait(timeout=5)
            except:
                backend_process.kill()
        
        log("=" * 60, "INFO")
        log(f"Monitor stopped. Total restarts: {restart_count}", "INFO")
        log("=" * 60, "INFO")

if __name__ == "__main__":
    main()
