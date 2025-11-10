#!/usr/bin/env python3
"""
AI Resilience Monitor Dashboard
A Flask web application serving a real-time dashboard for AI service monitoring.
"""
import sys
import os
import argparse
from flask import Flask, render_template, jsonify, request
import requests
import logging
from datetime import datetime

# Add backend directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from database import get_datastore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
db = get_datastore()

app = Flask(__name__)

# Configuration
BACKEND_URL = "http://localhost:3000"
DEFAULT_PORT = 8080

class DashboardAPI:
    """Handle all backend API interactions with error handling."""
    
    def __init__(self, backend_url):
        self.backend_url = backend_url
        self.session = requests.Session()
        self.timeout = 10
    
    def get_metrics(self):
        """Fetch metrics from the backend API."""
        try:
            response = self.session.get(f"{self.backend_url}/metrics", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch metrics: {e}")
            return self._get_fallback_metrics()
    
    def get_health_status(self):
        """Fetch AI services health status."""
        try:
            response = self.session.get(f"{self.backend_url}/ai/health", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch health status: {e}")
            return self._get_fallback_health()
    
    def _get_fallback_metrics(self):
        """Return fallback metrics when backend is unavailable."""
        return {
            "totalRequests": 0,
            "successfulRequests": 0,
            "failedRequests": 0,
            "successRate": 0,
            "avgLatency": 0,
            "uptime": 0,
            "aiServices": {
                "gemini": {"requests": 0, "failures": 0, "successRate": 0, "avgLatency": 0, "status": "unknown"},
                "cohere": {"requests": 0, "failures": 0, "successRate": 0, "avgLatency": 0, "status": "unknown"},
                "huggingface": {"requests": 0, "failures": 0, "successRate": 0, "avgLatency": 0, "status": "unknown"}
            },
            "error": "Backend unavailable"
        }
    
    def _get_fallback_health(self):
        """Return fallback health status when backend is unavailable."""
        return {
            "overall": "unknown",
            "services": {
                "gemini": {"status": "unknown", "lastCheck": None},
                "cohere": {"status": "unknown", "lastCheck": None},
                "huggingface": {"status": "unknown", "lastCheck": None}
            },
            "error": "Backend unavailable"
        }

# Initialize API client
api_client = DashboardAPI(BACKEND_URL)

@app.route('/')
def dashboard():
    """Serve the main dashboard page."""
    # Disable caching to ensure fresh content
    response = app.make_response(render_template('dashboard.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/metrics')
def api_metrics():
    """API endpoint to get current metrics."""
    metrics = api_client.get_metrics()
    return jsonify(metrics)

@app.route('/api/health')
def api_health():
    """API endpoint to get health status."""
    health = api_client.get_health_status()
    return jsonify(health)

@app.route('/api/status')
def api_status():
    """Get dashboard status including backend connectivity."""
    try:
        # Test backend connectivity
        response = requests.get(f"{BACKEND_URL}/test", timeout=5)
        backend_status = "connected" if response.status_code == 200 else "error"
    except requests.exceptions.RequestException:
        backend_status = "disconnected"
    
    return jsonify({
        "status": "running",
        "backend_status": backend_status,
        "timestamp": datetime.now().isoformat(),
        "backend_url": BACKEND_URL
    })

@app.route('/metrics')
def proxy_metrics():
    """Proxy metrics request to backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/metrics", timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to proxy metrics: {e}")
        return jsonify({"error": "Backend unavailable"}), 503

@app.route('/ai', methods=['POST'])
def proxy_ai():
    """Proxy AI request to backend."""
    try:
        data = request.get_json()
        response = requests.post(f"{BACKEND_URL}/ai", json=data, timeout=30)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to proxy AI request: {e}")
        return jsonify({"error": "Backend unavailable"}), 503

@app.route('/chaos/inject', methods=['POST'])
def proxy_chaos_inject():
    """Proxy chaos injection request to backend."""
    try:
        data = request.get_json()
        response = requests.post(f"{BACKEND_URL}/chaos/inject", json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to inject chaos: {e}")
        return jsonify({"error": "Backend unavailable", "success": False}), 503

@app.route('/chaos/stop', methods=['POST'])
def proxy_chaos_stop():
    """Proxy chaos stop request to backend."""
    try:
        data = request.get_json()
        response = requests.post(f"{BACKEND_URL}/chaos/stop", json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to stop chaos: {e}")
        return jsonify({"error": "Backend unavailable", "success": False}), 503

@app.route('/chaos/status', methods=['GET'])
def proxy_chaos_status():
    """Proxy chaos status request to backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/chaos/status", timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get chaos status: {e}")
        return jsonify({"experiments": []}), 503

@app.route('/circuit-breaker/status', methods=['GET'])
def proxy_circuit_breaker_status():
    """Proxy circuit breaker status request to backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/circuit-breaker/status", timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get circuit breaker status: {e}")
        return jsonify({"error": str(e)}), 503

@app.route('/circuit-breaker/reset', methods=['POST'])
def proxy_circuit_breaker_reset():
    """Proxy circuit breaker reset request to backend."""
    try:
        data = request.get_json() or {}
        response = requests.post(f"{BACKEND_URL}/circuit-breaker/reset", json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to reset circuit breaker: {e}")
        return jsonify({"error": str(e)}), 503

# ============================================================================
# HISTORICAL DATA & ANALYTICS ENDPOINTS
# ============================================================================

@app.route('/api/history/requests', methods=['GET'])
def get_request_history():
    """Get historical request logs."""
    try:
        limit = int(request.args.get('limit', 100))
        service = request.args.get('service', None)
        
        requests_data = db.get_recent_requests(limit=limit, service=service)
        
        return jsonify({
            "success": True,
            "count": len(requests_data),
            "requests": requests_data
        })
    except Exception as e:
        logger.error(f"Failed to get request history: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/history/statistics', methods=['GET'])
def get_statistics():
    """Get aggregated statistics."""
    try:
        hours = int(request.args.get('hours', 24))
        service = request.args.get('service', None)
        
        stats = db.get_service_statistics(service=service, hours=hours)
        
        return jsonify({
            "success": True,
            "time_range_hours": hours,
            "statistics": stats
        })
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/history/errors', methods=['GET'])
def get_error_patterns():
    """Get error pattern analysis."""
    try:
        hours = int(request.args.get('hours', 24))
        
        patterns = db.get_error_patterns(hours=hours)
        
        return jsonify({
            "success": True,
            "time_range_hours": hours,
            "error_patterns": patterns
        })
    except Exception as e:
        logger.error(f"Failed to get error patterns: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/history/circuit-breaker', methods=['GET'])
def get_circuit_breaker_history():
    """Get circuit breaker event history."""
    try:
        limit = int(request.args.get('limit', 50))
        service = request.args.get('service', None)
        
        events = db.get_circuit_breaker_history(service=service, limit=limit)
        
        return jsonify({
            "success": True,
            "count": len(events),
            "events": events
        })
    except Exception as e:
        logger.error(f"Failed to get circuit breaker history: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/history/chaos', methods=['GET'])
def get_chaos_history():
    """Get chaos experiment history."""
    try:
        limit = int(request.args.get('limit', 20))
        
        experiments = db.get_chaos_experiments(limit=limit)
        
        return jsonify({
            "success": True,
            "count": len(experiments),
            "experiments": experiments
        })
    except Exception as e:
        logger.error(f"Failed to get chaos history: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/history/trends', methods=['GET'])
def get_performance_trends():
    """Get performance trends over time."""
    try:
        hours = int(request.args.get('hours', 24))
        interval = int(request.args.get('interval', 30))
        service = request.args.get('service', None)
        
        trends = db.get_performance_trends(service=service, hours=hours, interval_minutes=interval)
        
        return jsonify({
            "success": True,
            "time_range_hours": hours,
            "interval_minutes": interval,
            "trends": trends
        })
    except Exception as e:
        logger.error(f"Failed to get performance trends: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/history/export', methods=['GET'])
def export_data():
    """Export historical data to JSON."""
    try:
        hours = int(request.args.get('hours', 24))
        output_file = f'data/export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        file_path = db.export_to_json(output_file, hours=hours)
        
        return jsonify({
            "success": True,
            "file": file_path,
            "message": f"Data exported to {file_path}"
        })
    except Exception as e:
        logger.error(f"Failed to export data: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/database/stats', methods=['GET'])
def get_database_stats():
    """Get database statistics."""
    try:
        stats = db.get_database_stats()
        
        return jsonify({
            "success": True,
            "statistics": stats
        })
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.route('/api/log-request', methods=['POST'])
def log_request_to_db():
    """Log a request to the database."""
    try:
        data = request.get_json()
        
        request_id = db.log_request(
            service=data.get('service'),
            success=data.get('success'),
            latency=data.get('latency'),
            response_size=data.get('responseSize', 0),
            error_type=data.get('errorType'),
            error_message=data.get('errorMessage'),
            prompt=data.get('prompt'),
            circuit_breaker_state=data.get('circuitBreakerState'),
            chaos_active=data.get('chaosActive', False),
            automated=data.get('automated', False)
        )
        
        return jsonify({
            "success": True,
            "request_id": request_id,
            "message": "Request logged successfully"
        })
    except Exception as e:
        logger.error(f"Failed to log request: {e}")
        return jsonify({"error": str(e), "success": False}), 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

def main():
    """Main function to run the Flask app."""
    parser = argparse.ArgumentParser(description='AI Resilience Monitor Dashboard')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, 
                       help=f'Port to run the dashboard on (default: {DEFAULT_PORT})')
    parser.add_argument('--host', default='localhost',
                       help='Host to run the dashboard on (default: localhost)')
    parser.add_argument('--debug', action='store_true',
                       help='Run in debug mode')
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Starting AI Resilience Dashboard on http://{args.host}:{args.port}")
    logger.info(f"📊 Backend URL: {BACKEND_URL}")

    # Helper: check if a TCP port is open
    import socket, subprocess, atexit, os, time

    def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            return False

    backend_process = None

    # If backend not listening on expected port, try to start it from repo
    try:
        host = 'localhost'
        backend_port = 3000
        project_dir = os.path.dirname(__file__)

        if not is_port_open(host, backend_port):
            logger.info('Backend not detected on port %s — attempting to start Node.js backend...', backend_port)

            node_cmd = [
                'node',
                os.path.join('src', 'index.js')
            ]

            # Start Node.js backend as a child process
            try:
                backend_process = subprocess.Popen(
                    node_cmd,
                    cwd=project_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )

                logger.info('Started Node.js backend (pid=%s), waiting for it to listen on port %s...', backend_process.pid, backend_port)

                # Wait up to 12 seconds for backend to come up
                wait_until = time.time() + 12
                while time.time() < wait_until:
                    if is_port_open(host, backend_port):
                        logger.info('Backend is now listening on port %s', backend_port)
                        break
                    # drain any available stdout lines to log
                    if backend_process.stdout:
                        try:
                            line = backend_process.stdout.readline()
                            if line:
                                logger.info('[node] %s', line.rstrip())
                        except Exception:
                            pass
                    time.sleep(0.25)
                else:
                    logger.warning('Backend did not start within timeout; continuing to launch dashboard frontend only.')

            except FileNotFoundError:
                logger.error('Node.js executable not found. Ensure Node is installed and available in PATH.')
            except Exception as e:
                logger.error('Failed to start Node.js backend: %s', e)
        else:
            logger.info('Backend already running on port %s — will not start a new Node process.', backend_port)

        # Ensure child backend_process is cleaned up when this process exits
        def _cleanup_child():
            nonlocal backend_process
            try:
                if backend_process and backend_process.poll() is None:
                    logger.info('Terminating child Node.js backend (pid=%s)...', backend_process.pid)
                    backend_process.terminate()
                    time.sleep(1)
                    if backend_process.poll() is None:
                        logger.info('Killing child Node.js backend (pid=%s)...', backend_process.pid)
                        backend_process.kill()
            except Exception as ex:
                logger.debug('Error while cleaning up backend process: %s', ex)

        atexit.register(_cleanup_child)

        # Run Flask app (blocking). When it stops, cleanup will run via atexit.
        app.run(host=args.host, port=args.port, debug=args.debug)

    except KeyboardInterrupt:
        logger.info('🛑 Dashboard stopped by user')
    except Exception as e:
        logger.error(f'❌ Failed to start dashboard: {e}')
        # Attempt to clean up backend process if it was created
        try:
            if backend_process and backend_process.poll() is None:
                backend_process.terminate()
        except Exception:
            pass
        sys.exit(1)

if __name__ == '__main__':
    main()