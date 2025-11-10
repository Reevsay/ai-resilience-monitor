#!/usr/bin/env python3
"""
Continuous Frontend Monitor with Detailed Output Logging
Monitors Flask frontend for crashes and logs all output in real-time
"""

import subprocess
import time
import psutil
import os
import signal
import sys
from datetime import datetime
from pathlib import Path

# Configuration
FRONTEND_PORT = 8080
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..", "..")  # Go up to project root
FRONTEND_SCRIPT = os.path.join(PROJECT_ROOT, "app.py")
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "frontend-monitor.log")
MAX_RESTARTS = 100
HEALTH_CHECK_INTERVAL = 5  # seconds

class FrontendMonitor:
    def __init__(self):
        self.process = None
        self.restart_count = 0
        self.start_time = datetime.now()
        self.last_crash_time = None
        self.log_file = open(LOG_FILE, 'a', buffering=1, encoding='utf-8')
        
    def log(self, message, level="INFO"):
        """Log message to both console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        self.log_file.write(log_entry + "\n")
        self.log_file.flush()
    
    def is_port_in_use(self, port):
        """Check if port is in use"""
        try:
            for conn in psutil.net_connections():
                if hasattr(conn, 'laddr') and conn.laddr.port == port:
                    return True
        except:
            pass
        return False
    
    def kill_port(self, port):
        """Kill process using specified port"""
        killed = False
        try:
            for conn in psutil.net_connections():
                if hasattr(conn, 'laddr') and conn.laddr.port == port:
                    try:
                        proc = psutil.Process(conn.pid)
                        self.log(f"Killing zombie process on port {port} (PID: {conn.pid})", "WARN")
                        proc.kill()
                        killed = True
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
        except:
            pass
        
        if killed:
            time.sleep(2)
        return killed
    
    def start_frontend(self):
        """Start the Flask frontend"""
        try:
            # Kill any existing process on the port
            if self.is_port_in_use(FRONTEND_PORT):
                self.log(f"Port {FRONTEND_PORT} is in use, cleaning up...", "WARN")
                self.kill_port(FRONTEND_PORT)
            
            self.log("=" * 80)
            self.log(f"Starting Flask frontend (Attempt {self.restart_count + 1})", "START")
            self.log("=" * 80)
            
            # Start Flask with full output logging
            self.process = subprocess.Popen(
                [sys.executable, FRONTEND_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
                cwd=os.getcwd()
            )
            
            self.restart_count += 1
            self.log(f"✅ Frontend started (PID: {self.process.pid})", "SUCCESS")
            
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to start frontend: {e}", "ERROR")
            return False
    
    def read_output(self):
        """Read and log frontend output in real-time"""
        try:
            if self.process and self.process.stdout:
                for line in iter(self.process.stdout.readline, ''):
                    if line:
                        # Remove trailing newline
                        line = line.rstrip()
                        
                        # Categorize output
                        if "ERROR" in line.upper() or "EXCEPTION" in line.upper():
                            self.log(f"🔴 {line}", "ERROR")
                        elif "WARNING" in line.upper() or "WARN" in line.upper():
                            self.log(f"🟡 {line}", "WARN")
                        elif "CRASH" in line.upper() or "FATAL" in line.upper():
                            self.log(f"💥 {line}", "FATAL")
                        elif "Running on" in line or "http://" in line:
                            self.log(f"🚀 {line}", "INFO")
                        elif "GET" in line or "POST" in line:
                            self.log(f"📡 {line}", "REQUEST")
                        else:
                            self.log(f"📝 {line}", "OUTPUT")
        except Exception as e:
            self.log(f"Error reading output: {e}", "ERROR")
    
    def is_frontend_alive(self):
        """Check if frontend process is running"""
        if self.process is None:
            return False
        
        # Check if process is still running
        if self.process.poll() is not None:
            return False
        
        # Check if it's responsive on the port
        try:
            return self.is_port_in_use(FRONTEND_PORT)
        except:
            return False
    
    def handle_crash(self):
        """Handle frontend crash"""
        self.last_crash_time = datetime.now()
        crash_duration = (self.last_crash_time - self.start_time).total_seconds()
        
        self.log("=" * 80, "CRASH")
        self.log("💥 FRONTEND CRASHED!", "CRASH")
        self.log(f"Crash time: {self.last_crash_time.strftime('%Y-%m-%d %H:%M:%S')}", "CRASH")
        self.log(f"Uptime before crash: {crash_duration:.2f} seconds", "CRASH")
        self.log(f"Total restarts so far: {self.restart_count}", "CRASH")
        
        # Get exit code if available
        if self.process:
            exit_code = self.process.poll()
            self.log(f"Exit code: {exit_code}", "CRASH")
            
            # Read any remaining output
            try:
                remaining = self.process.stdout.read()
                if remaining:
                    self.log(f"Final output:\n{remaining}", "CRASH")
            except:
                pass
        
        self.log("=" * 80, "CRASH")
        
        # Clean up
        if self.process:
            try:
                self.process.kill()
            except:
                pass
        
        self.kill_port(FRONTEND_PORT)
    
    def monitor(self):
        """Main monitoring loop"""
        self.log("=" * 80)
        self.log("🔍 CONTINUOUS FRONTEND MONITOR STARTED", "START")
        self.log(f"Frontend script: {FRONTEND_SCRIPT}")
        self.log(f"Port: {FRONTEND_PORT}")
        self.log(f"Health check interval: {HEALTH_CHECK_INTERVAL}s")
        self.log(f"Max restarts: {MAX_RESTARTS}")
        self.log(f"Log file: {LOG_FILE}")
        self.log("=" * 80)
        
        try:
            while self.restart_count < MAX_RESTARTS:
                # Start frontend if not running
                if not self.is_frontend_alive():
                    if self.process is not None:
                        # It was running but crashed
                        self.handle_crash()
                        
                        if self.restart_count >= MAX_RESTARTS:
                            self.log(f"❌ Max restarts ({MAX_RESTARTS}) reached. Giving up.", "FATAL")
                            break
                        
                        self.log(f"⏳ Waiting 3 seconds before restart...", "INFO")
                        time.sleep(3)
                    
                    # Start the frontend
                    if not self.start_frontend():
                        self.log("❌ Failed to start frontend, waiting 5 seconds...", "ERROR")
                        time.sleep(5)
                        continue
                    
                    # Wait for startup
                    time.sleep(2)
                    self.start_time = datetime.now()
                
                # Read output continuously
                self.read_output()
                
                # Small delay to prevent CPU spinning
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.log("\n⚠️  Monitor interrupted by user", "INFO")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        self.log("🧹 Cleaning up...", "INFO")
        
        if self.process:
            try:
                self.process.kill()
                self.log(f"Killed frontend process (PID: {self.process.pid})", "INFO")
            except:
                pass
        
        self.kill_port(FRONTEND_PORT)
        
        uptime = (datetime.now() - self.start_time).total_seconds()
        self.log("=" * 80)
        self.log("📊 MONITOR STATISTICS", "INFO")
        self.log(f"Total restarts: {self.restart_count}", "INFO")
        self.log(f"Last uptime: {uptime:.2f} seconds", "INFO")
        if self.last_crash_time:
            self.log(f"Last crash: {self.last_crash_time.strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
        self.log("=" * 80)
        
        self.log_file.close()
        self.log("✅ Monitor stopped")

def main():
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Stopping monitor...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create monitor and start
    monitor = FrontendMonitor()
    monitor.monitor()

if __name__ == '__main__':
    main()
