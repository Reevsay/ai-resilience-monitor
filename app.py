#!/usr/bin/env python3
"""
AI Resilience Monitor Dashboard
A Flask web application serving a real-time dashboard for AI service monitoring.
"""

import sys
import argparse
from flask import Flask, render_template, jsonify, request
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    
    try:
        app.run(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        logger.info("🛑 Dashboard stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start dashboard: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()