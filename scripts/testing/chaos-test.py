#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Resilience Monitor - Automated Chaos Testing & Data Collection Script
This script runs continuous chaos experiments to test AI services under various failure scenarios
and collects comprehensive data for analysis.
"""

import os
import sys
import time
import json
import requests
import csv
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import signal
from typing import Dict, List, Any
import random

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
BACKEND_URL = "http://localhost:3000"
FRONTEND_URL = "http://localhost:8080"

# Chaos experiment types
CHAOS_TYPES = {
    'latency': {
        'name': 'Network Latency',
        'intensities': [100, 500, 1000, 2000, 5000],  # milliseconds
        'description': 'Simulates slow network conditions'
    },
    'error': {
        'name': 'Error Injection',
        'intensities': [25, 50, 75, 100],  # percentage
        'description': 'Simulates random errors and failures'
    },
    'timeout': {
        'name': 'Timeout Simulation',
        'intensities': [1000, 3000, 5000, 10000],  # milliseconds
        'description': 'Simulates request timeouts'
    },
    'throttle': {
        'name': 'Rate Limiting',
        'intensities': [50, 75, 90, 100],  # percentage reduction
        'description': 'Simulates API rate limiting'
    }
}

# AI Services to test
SERVICES = ['gemini', 'cohere', 'huggingface']

# Test prompts
TEST_PROMPTS = [
    "What is artificial intelligence?",
    "Explain quantum computing briefly",
    "How does machine learning work?",
    "What are neural networks?",
    "Describe cloud computing",
    "What is blockchain technology?",
    "Explain data science",
    "What is cybersecurity?",
    "How does 5G work?",
    "What is the Internet of Things?"
]

class ChaosTestRunner:
    def __init__(self, duration_hours=24, requests_per_cycle=10, 
                 chaos_duration=300, normal_duration=180,
                 output_dir="chaos-test-results"):
        self.duration_hours = duration_hours
        self.requests_per_cycle = requests_per_cycle
        self.chaos_duration = chaos_duration  # seconds
        self.normal_duration = normal_duration  # seconds
        self.output_dir = Path(output_dir)
        self.running = True
        
        # Rate limiting to prevent overwhelming the backend
        self.min_request_delay = 2  # Minimum 2 seconds between requests
        self.request_timeout = 30  # Timeout for AI requests
        
        # Statistics
        self.total_requests = 0
        self.total_chaos_experiments = 0
        self.experiment_results = []
        self.service_performance = {service: [] for service in SERVICES}
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Initialize CSV files
        self.init_csv_files()
    
    def signal_handler(self, signum, frame):
        """Handle shutdown gracefully"""
        print("\n\n🛑 Shutting down chaos testing...")
        self.running = False
        self.generate_final_report()
        print("\n✅ Chaos testing stopped. Reports generated.")
        sys.exit(0)
    
    def init_csv_files(self):
        """Initialize CSV files for data collection"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Experiment log
        self.experiment_log_file = self.output_dir / f"experiment_log_{timestamp}.csv"
        with open(self.experiment_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp', 'Experiment_ID', 'Chaos_Type', 'Intensity', 
                'Service', 'Duration_Sec', 'Total_Requests', 'Successful_Requests',
                'Failed_Requests', 'Avg_Latency_Ms', 'Min_Latency_Ms', 'Max_Latency_Ms',
                'Success_Rate_%', 'Circuit_Breaker_Trips', 'Recovery_Time_Sec'
            ])
        
        # Request log
        self.request_log_file = self.output_dir / f"request_log_{timestamp}.csv"
        with open(self.request_log_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp', 'Experiment_ID', 'Service', 'Chaos_Type', 
                'Chaos_Active', 'Success', 'Latency_Ms', 'Error_Type',
                'Circuit_Breaker_State', 'Response_Size'
            ])
        
        # Service comparison log
        self.service_comparison_file = self.output_dir / f"service_comparison_{timestamp}.csv"
        with open(self.service_comparison_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Timestamp', 'Service', 'Total_Requests', 'Success_Rate_%',
                'Avg_Latency_Ms', 'Total_Failures', 'Circuit_Breaker_Trips',
                'Avg_Recovery_Time_Sec', 'Resilience_Score'
            ])
    
    def log(self, message, level='INFO'):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        color_codes = {
            'INFO': '\033[96m',     # Cyan
            'SUCCESS': '\033[92m',  # Green
            'WARNING': '\033[93m',  # Yellow
            'ERROR': '\033[91m',    # Red
            'CHAOS': '\033[95m',    # Magenta
            'RESET': '\033[0m'
        }
        
        color = color_codes.get(level, color_codes['INFO'])
        reset = color_codes['RESET']
        
        try:
            print(f"{color}[{timestamp}] [{level}] {message}{reset}", flush=True)
        except (UnicodeEncodeError, UnicodeError):
            # Fallback: Remove emojis and special characters for Windows console
            message_clean = message.encode('ascii', errors='ignore').decode('ascii')
            print(f"{color}[{timestamp}] [{level}] {message_clean}{reset}", flush=True)
    
    def check_backend_health(self):
        """Check if backend is running"""
        try:
            response = requests.get(f"{BACKEND_URL}/test", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def inject_chaos(self, service, chaos_type, intensity, duration):
        """Inject chaos into a service"""
        try:
            payload = {
                'service': service,
                'type': chaos_type,
                'intensity': intensity,
                'duration': duration
            }
            
            response = requests.post(f"{BACKEND_URL}/chaos/inject", json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"🔥 Chaos injected: {chaos_type.upper()} on {service.upper()} "
                        f"(intensity: {intensity}, duration: {duration}s)", level='CHAOS')
                return True
            else:
                self.log(f"Failed to inject chaos: {response.text}", level='ERROR')
                return False
        except Exception as e:
            self.log(f"Error injecting chaos: {e}", level='ERROR')
            return False
    
    def stop_chaos(self, service):
        """Stop chaos experiment"""
        try:
            payload = {'service': service}
            response = requests.post(f"{BACKEND_URL}/chaos/stop", json=payload, timeout=10)
            
            if response.status_code == 200:
                self.log(f"✅ Chaos stopped for {service.upper()}", level='SUCCESS')
                return True
            else:
                return False
        except Exception as e:
            self.log(f"Error stopping chaos: {e}", level='ERROR')
            return False
    
    def send_ai_request(self, service, prompt):
        """Send request to AI service via backend"""
        try:
            start_time = time.time()
            
            payload = {
                'service': service,
                'prompt': prompt
            }
            
            # Log the request
            print(f"🔵 Request #{self.total_requests + 1} → {service.upper()} | Prompt: '{prompt[:50]}...'", flush=True)
            
            response = requests.post(f"{BACKEND_URL}/ai", json=payload, timeout=self.request_timeout)
            
            latency = int((time.time() - start_time) * 1000)  # milliseconds
            
            success = response.status_code == 200
            error_type = None if success else response.json().get('error', 'Unknown')
            
            # Log the result
            if success:
                print(f"✅ SUCCESS | {service.upper()} | Latency: {latency}ms | Response: {len(response.content)} bytes", flush=True)
            else:
                print(f"❌ FAILED | {service.upper()} | Latency: {latency}ms | Error: {error_type}", flush=True)
            
            return {
                'success': success,
                'latency': latency,
                'error_type': error_type,
                'response_size': len(response.content) if success else 0
            }
            
        except requests.exceptions.Timeout:
            latency = self.request_timeout * 1000  # timeout value in ms
            print(f"⏱️ TIMEOUT | {service.upper()} | Request exceeded {self.request_timeout}s", flush=True)
            return {
                'success': False,
                'latency': latency,
                'error_type': 'Timeout',
                'response_size': 0
            }
        except Exception as e:
            print(f"❌ EXCEPTION | {service.upper()} | Error: {str(e)}", flush=True)
            return {
                'success': False,
                'latency': 0,
                'error_type': str(e),
                'response_size': 0
            }
    
    def get_circuit_breaker_status(self):
        """Get circuit breaker status for all services"""
        try:
            response = requests.get(f"{BACKEND_URL}/circuit-breaker/status", timeout=5)
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def run_experiment(self, experiment_id, chaos_type, intensity, service):
        """Run a single chaos experiment"""
        print(f"\n{'='*70}", flush=True)
        print(f"🧪 EXPERIMENT #{experiment_id} - {CHAOS_TYPES[chaos_type]['name']}", flush=True)
        print(f"{'='*70}", flush=True)
        print(f"   📍 Service: {service.upper()}", flush=True)
        print(f"   🔥 Chaos Type: {chaos_type.upper()}", flush=True)
        print(f"   💥 Intensity: {intensity}", flush=True)
        print(f"   ⏱️  Duration: {self.chaos_duration}s", flush=True)
        print(f"{'='*70}\n", flush=True)
        
        # Inject chaos
        print(f"🔥 Injecting chaos: {chaos_type} @ intensity {intensity}...", flush=True)
        if not self.inject_chaos(service, chaos_type, intensity, self.chaos_duration):
            print(f"❌ Failed to inject chaos. Skipping experiment.", flush=True)
            return
        
        print(f"✅ Chaos injected successfully! Starting requests...\n", flush=True)
        
        self.total_chaos_experiments += 1
        experiment_start = time.time()
        
        # Collect data during chaos
        requests_data = []
        circuit_breaker_trips = 0
        previous_cb_state = None
        
        # Run requests during chaos period
        chaos_end_time = time.time() + self.chaos_duration
        request_count = 0
        
        print(f"📊 Running requests under chaos conditions...", flush=True)
        print(f"", flush=True)
        
        while time.time() < chaos_end_time and self.running:
            prompt = random.choice(TEST_PROMPTS)
            
            # Send request
            result = self.send_ai_request(service, prompt)
            self.total_requests += 1
            request_count += 1
            
            # Get circuit breaker status
            cb_status = self.get_circuit_breaker_status()
            current_cb_state = cb_status.get(service, {}).get('state', 'UNKNOWN')
            
            # Detect circuit breaker trips
            if previous_cb_state == 'CLOSED' and current_cb_state == 'OPEN':
                circuit_breaker_trips += 1
                self.log(f"⚡ Circuit breaker OPENED for {service.upper()}", level='WARNING')
            
            previous_cb_state = current_cb_state
            
            # Log request
            request_data = {
                'timestamp': datetime.now().isoformat(),
                'experiment_id': experiment_id,
                'service': service,
                'chaos_type': chaos_type,
                'chaos_active': True,
                'success': result['success'],
                'latency': result['latency'],
                'error_type': result['error_type'],
                'circuit_breaker_state': current_cb_state,
                'response_size': result['response_size']
            }
            
            requests_data.append(request_data)
            
            # Write to CSV
            with open(self.request_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    request_data['timestamp'],
                    request_data['experiment_id'],
                    request_data['service'],
                    request_data['chaos_type'],
                    request_data['chaos_active'],
                    request_data['success'],
                    request_data['latency'],
                    request_data['error_type'],
                    request_data['circuit_breaker_state'],
                    request_data['response_size']
                ])
            
            # Status update
            if request_count % 5 == 0:
                success_count = sum(1 for r in requests_data if r['success'])
                success_rate = (success_count / len(requests_data)) * 100
                self.log(f"   Progress: {request_count} requests, "
                        f"{success_rate:.1f}% success rate", level='INFO')
            
            # Calculate dynamic delay based on actual request time and target rate
            # Target: requests_per_cycle requests over chaos_duration seconds
            target_delay = max(self.min_request_delay, self.chaos_duration / self.requests_per_cycle)
            actual_request_time = time.time() - experiment_start
            expected_time = request_count * target_delay
            
            # Adjust delay to stay on track
            if actual_request_time < expected_time:
                delay = expected_time - actual_request_time
                time.sleep(min(delay, target_delay))
            else:
                # We're behind schedule, use minimum delay
                time.sleep(self.min_request_delay)
        
        # Stop chaos
        self.stop_chaos(service)
        print(f"🛑 Chaos stopped. Monitoring recovery...\n", flush=True)
        
        # Wait for recovery
        print(f"⏳ Recovery Period: Waiting {self.normal_duration}s for service to stabilize...", flush=True)
        recovery_start = time.time()
        
        # Monitor recovery
        recovery_checks = 0
        while time.time() < recovery_start + self.normal_duration and self.running:
            time.sleep(5)
            recovery_checks += 1
            remaining = int((recovery_start + self.normal_duration) - time.time())
            print(f"   Recovery check #{recovery_checks} | {remaining}s remaining", flush=True)
        
        recovery_time = time.time() - recovery_start
        print(f"✅ Recovery period complete!\n", flush=True)
        
        # Calculate statistics
        successful_requests = sum(1 for r in requests_data if r['success'])
        failed_requests = len(requests_data) - successful_requests
        success_rate = (successful_requests / len(requests_data) * 100) if requests_data else 0
        
        latencies = [r['latency'] for r in requests_data if r['success']]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        min_latency = min(latencies) if latencies else 0
        max_latency = max(latencies) if latencies else 0
        
        # Log experiment results
        experiment_result = {
            'timestamp': datetime.now().isoformat(),
            'experiment_id': experiment_id,
            'chaos_type': chaos_type,
            'intensity': intensity,
            'service': service,
            'duration': self.chaos_duration,
            'total_requests': len(requests_data),
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'avg_latency': avg_latency,
            'min_latency': min_latency,
            'max_latency': max_latency,
            'success_rate': success_rate,
            'circuit_breaker_trips': circuit_breaker_trips,
            'recovery_time': recovery_time
        }
        
        self.experiment_results.append(experiment_result)
        
        # Write to experiment log
        with open(self.experiment_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                experiment_result['timestamp'],
                experiment_result['experiment_id'],
                experiment_result['chaos_type'],
                experiment_result['intensity'],
                experiment_result['service'],
                experiment_result['duration'],
                experiment_result['total_requests'],
                experiment_result['successful_requests'],
                experiment_result['failed_requests'],
                f"{experiment_result['avg_latency']:.2f}",
                experiment_result['min_latency'],
                experiment_result['max_latency'],
                f"{experiment_result['success_rate']:.2f}",
                experiment_result['circuit_breaker_trips'],
                f"{experiment_result['recovery_time']:.2f}"
            ])
        
        # Print detailed summary
        print(f"\n{'='*70}", flush=True)
        print(f"📊 EXPERIMENT #{experiment_id} RESULTS", flush=True)
        print(f"{'='*70}", flush=True)
        print(f"   📝 Service: {service.upper()}", flush=True)
        print(f"   🔥 Chaos: {chaos_type.upper()} @ {intensity}", flush=True)
        print(f"   📈 Total Requests: {len(requests_data)}", flush=True)
        print(f"   ✅ Successful: {successful_requests} ({success_rate:.1f}%)", flush=True)
        print(f"   ❌ Failed: {failed_requests} ({100-success_rate:.1f}%)", flush=True)
        print(f"   ⚡ Avg Latency: {avg_latency:.0f}ms", flush=True)
        print(f"   📊 Latency Range: {min_latency}ms - {max_latency}ms", flush=True)
        print(f"   🔌 Circuit Breaker Trips: {circuit_breaker_trips}", flush=True)
        self.log(f"   Recovery Time: {recovery_time:.1f}s", level='INFO')
        self.log(f"{'='*60}\n", level='INFO')
    
    def run_load_test_normal(self, duration=300):
        """Test Scenario 1: Normal Load - 1 request every 5 seconds"""
        print(f"\n{'='*70}", flush=True)
        print(f"📊 SCENARIO 1: Normal Load Test", flush=True)
        print(f"{'='*70}", flush=True)
        print(f"   ⚙️  Mode: Baseline performance measurement", flush=True)
        print(f"   📈 Rate: 1 request every 5 seconds", flush=True)
        print(f"   ⏱️  Duration: {duration}s ({duration//60} minutes)", flush=True)
        print(f"   🎯 Purpose: Establish baseline metrics", flush=True)
        print(f"{'='*70}\n", flush=True)
        
        end_time = time.time() + duration
        request_count = 0
        
        while time.time() < end_time and self.running:
            service = random.choice(SERVICES)
            prompt = random.choice(TEST_PROMPTS)
            
            print(f"[Normal Load] Request {request_count + 1} in {int(end_time - time.time())}s remaining...", flush=True)
            result = self.send_ai_request(service, prompt)
            self.total_requests += 1
            request_count += 1
            
            # Log request
            with open(self.request_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    'LOAD_NORMAL',
                    service,
                    'NONE',
                    False,
                    result['success'],
                    result['latency'],
                    result['error_type'],
                    'UNKNOWN',
                    result['response_size']
                ])
            
            time.sleep(5)  # 1 request every 5 seconds
        
        print(f"\n✅ Normal load test COMPLETE | Requests: {request_count} | Time: {duration}s\n", flush=True)
    
    def run_load_test_high(self, duration=300):
        """Test Scenario 2: High Load - 1 request every 2 seconds"""
        print(f"\n{'='*70}", flush=True)
        print(f"📊 SCENARIO 2: High Load Test", flush=True)
        print(f"{'='*70}", flush=True)
        print(f"   ⚙️  Mode: Sustained high load", flush=True)
        print(f"   📈 Rate: 1 request every 2 seconds (2.5x normal)", flush=True)
        print(f"   ⏱️  Duration: {duration}s ({duration//60} minutes)", flush=True)
        print(f"   🎯 Purpose: Test sustained performance under load", flush=True)
        print(f"{'='*70}\n", flush=True)
        
        end_time = time.time() + duration
        request_count = 0
        
        while time.time() < end_time and self.running:
            service = random.choice(SERVICES)
            prompt = random.choice(TEST_PROMPTS)
            
            print(f"[High Load] Request {request_count + 1} in {int(end_time - time.time())}s remaining...", flush=True)
            result = self.send_ai_request(service, prompt)
            self.total_requests += 1
            request_count += 1
            
            # Log request
            with open(self.request_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    'LOAD_HIGH',
                    service,
                    'NONE',
                    False,
                    result['success'],
                    result['latency'],
                    result['error_type'],
                    'UNKNOWN',
                    result['response_size']
                ])
            
            time.sleep(2)  # 1 request every 2 seconds
        
        print(f"\n✅ High load test COMPLETE | Requests: {request_count} | Time: {duration}s\n", flush=True)
    
    def run_load_test_burst(self, bursts=5, burst_size=10):
        """Test Scenario 3: Burst Load - 10 requests simultaneously"""
        self.log(f"\n📊 LOAD TEST: Burst Load ({bursts} bursts of {burst_size} requests)", level='INFO')
        
        import concurrent.futures
        from threading import Lock
        
        request_lock = Lock()
        total_burst_requests = 0
        
        def send_burst_request(service, prompt, burst_id, request_id):
            nonlocal total_burst_requests
            result = self.send_ai_request(service, prompt)
            
            with request_lock:
                self.total_requests += 1
                total_burst_requests += 1
                
                # Log request
                with open(self.request_log_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.now().isoformat(),
                        f'LOAD_BURST_{burst_id}',
                        service,
                        'NONE',
                        False,
                        result['success'],
                        result['latency'],
                        result['error_type'],
                        'UNKNOWN',
                        result['response_size']
                    ])
            
            return result
        
        for burst_num in range(bursts):
            if not self.running:
                break
                
            self.log(f"   Burst {burst_num + 1}/{bursts}: Sending {burst_size} simultaneous requests...", level='INFO')
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=burst_size) as executor:
                futures = []
                for i in range(burst_size):
                    service = random.choice(SERVICES)
                    prompt = random.choice(TEST_PROMPTS)
                    future = executor.submit(send_burst_request, service, prompt, burst_num + 1, i + 1)
                    futures.append(future)
                
                # Wait for all requests to complete
                concurrent.futures.wait(futures)
            
            # Wait between bursts
            if burst_num < bursts - 1:
                time.sleep(10)
        
        self.log(f"✅ Burst load test complete ({total_burst_requests} total requests)", level='SUCCESS')
    
    def run_load_test_mixed_providers(self, duration=300):
        """Test Scenario 4: Mixed Providers - Round-robin across all services"""
        self.log(f"\n📊 LOAD TEST: Mixed Providers (Round-robin for {duration}s)", level='INFO')
        
        end_time = time.time() + duration
        request_count = 0
        service_index = 0
        
        while time.time() < end_time and self.running:
            # Round-robin through services
            service = SERVICES[service_index % len(SERVICES)]
            service_index += 1
            
            prompt = random.choice(TEST_PROMPTS)
            
            result = self.send_ai_request(service, prompt)
            self.total_requests += 1
            request_count += 1
            
            # Log request
            with open(self.request_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    'LOAD_MIXED',
                    service,
                    'NONE',
                    False,
                    result['success'],
                    result['latency'],
                    result['error_type'],
                    'UNKNOWN',
                    result['response_size']
                ])
            
            time.sleep(3)  # Even distribution
        
        self.log(f"✅ Mixed provider test complete ({request_count} requests across all services)", level='SUCCESS')
    
    def run_chaos_continuous_load(self, chaos_type, intensity, service, duration=300):
        """Test Scenario 5: Chaos Testing - Continuous requests during active chaos"""
        self.log(f"\n📊 CHAOS LOAD TEST: Continuous requests under {chaos_type.upper()} chaos", level='CHAOS')
        
        # Inject chaos
        if not self.inject_chaos(service, chaos_type, intensity, duration):
            self.log("Failed to inject chaos for load test", level='ERROR')
            return
        
        end_time = time.time() + duration
        request_count = 0
        successes = 0
        failures = 0
        latencies = []
        
        while time.time() < end_time and self.running:
            prompt = random.choice(TEST_PROMPTS)
            
            result = self.send_ai_request(service, prompt)
            self.total_requests += 1
            request_count += 1
            
            if result['success']:
                successes += 1
                latencies.append(result['latency'])
            else:
                failures += 1
            
            # Log request
            with open(self.request_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    'CHAOS_CONTINUOUS',
                    service,
                    chaos_type,
                    True,
                    result['success'],
                    result['latency'],
                    result['error_type'],
                    'UNKNOWN',
                    result['response_size']
                ])
            
            time.sleep(2)  # Continuous load
        
        # Stop chaos
        self.stop_chaos(service)
        
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        success_rate = (successes / request_count * 100) if request_count else 0
        
        self.log(f"✅ Chaos continuous load complete:", level='SUCCESS')
        self.log(f"   Total: {request_count} | Success: {successes} | Failed: {failures}", level='INFO')
        self.log(f"   Success Rate: {success_rate:.1f}% | Avg Latency: {avg_latency:.0f}ms", level='INFO')
    
    def run_empirical_validation_suite(self):
        """Run comprehensive empirical validation test suite"""
        self.log("\n" + "="*80, level='INFO')
        self.log("🔬 EMPIRICAL VALIDATION TEST SUITE", level='INFO')
        self.log("="*80, level='INFO')
        
        # Test Scenario 1: Normal Load
        if self.running:
            self.run_load_test_normal(duration=180)
        
        # Test Scenario 2: High Load
        if self.running:
            time.sleep(30)  # Cooldown
            self.run_load_test_high(duration=180)
        
        # Test Scenario 3: Burst Load
        if self.running:
            time.sleep(30)  # Cooldown
            self.run_load_test_burst(bursts=3, burst_size=10)
        
        # Test Scenario 4: Mixed Providers
        if self.running:
            time.sleep(30)  # Cooldown
            self.run_load_test_mixed_providers(duration=180)
        
        # Test Scenario 5: Chaos Testing with different scenarios
        chaos_scenarios = [
            ('latency', 500, 'gemini'),
            ('error', 50, 'cohere'),
            ('timeout', 3000, 'huggingface'),
        ]
        
        for chaos_type, intensity, service in chaos_scenarios:
            if self.running:
                time.sleep(30)  # Cooldown
                self.run_chaos_continuous_load(chaos_type, intensity, service, duration=180)
        
        self.log("\n" + "="*80, level='SUCCESS')
        self.log("✅ EMPIRICAL VALIDATION SUITE COMPLETE", level='SUCCESS')
        self.log("="*80 + "\n", level='SUCCESS')
    
    def run_normal_period(self, duration):
        """Run normal testing without chaos"""
        self.log(f"\n✅ Running normal period ({duration}s)...", level='SUCCESS')
        
        end_time = time.time() + duration
        request_count = 0
        
        while time.time() < end_time and self.running:
            service = random.choice(SERVICES)
            prompt = random.choice(TEST_PROMPTS)
            
            result = self.send_ai_request(service, prompt)
            self.total_requests += 1
            request_count += 1
            
            # Log request
            with open(self.request_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    'NORMAL',
                    service,
                    'NONE',
                    False,
                    result['success'],
                    result['latency'],
                    result['error_type'],
                    'UNKNOWN',
                    result['response_size']
                ])
            
            time.sleep(duration / 20)  # Spread requests evenly
        
        self.log(f"✅ Normal period complete ({request_count} requests)", level='SUCCESS')
    
    def generate_final_report(self):
        """Generate comprehensive final analysis report"""
        self.log("\n\n" + "="*80, level='INFO')
        self.log("📊 GENERATING FINAL REPORT", level='INFO')
        self.log("="*80, level='INFO')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"final_report_{timestamp}.txt"
        
        with open(report_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("AI RESILIENCE MONITOR - CHAOS TESTING FINAL REPORT\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Test Duration: {self.duration_hours} hours\n")
            f.write(f"Total Requests: {self.total_requests}\n")
            f.write(f"Total Chaos Experiments: {self.total_chaos_experiments}\n")
            f.write(f"Report Generated: {datetime.now().isoformat()}\n\n")
            
            # Service comparison
            f.write("\n" + "="*80 + "\n")
            f.write("SERVICE PERFORMANCE COMPARISON\n")
            f.write("="*80 + "\n\n")
            
            for service in SERVICES:
                service_experiments = [e for e in self.experiment_results if e['service'] == service]
                
                if service_experiments:
                    total_requests = sum(e['total_requests'] for e in service_experiments)
                    total_successes = sum(e['successful_requests'] for e in service_experiments)
                    avg_success_rate = (total_successes / total_requests * 100) if total_requests else 0
                    avg_latency = sum(e['avg_latency'] for e in service_experiments) / len(service_experiments)
                    total_cb_trips = sum(e['circuit_breaker_trips'] for e in service_experiments)
                    avg_recovery = sum(e['recovery_time'] for e in service_experiments) / len(service_experiments)
                    
                    # Calculate resilience score (0-100)
                    resilience_score = (
                        (avg_success_rate * 0.4) +  # 40% weight on success rate
                        ((100 - min(avg_latency / 50, 100)) * 0.3) +  # 30% weight on speed
                        ((100 - min(total_cb_trips * 10, 100)) * 0.2) +  # 20% weight on stability
                        ((100 - min(avg_recovery / 10, 100)) * 0.1)  # 10% weight on recovery
                    )
                    
                    f.write(f"{service.upper()}\n")
                    f.write(f"  Total Requests: {total_requests}\n")
                    f.write(f"  Success Rate: {avg_success_rate:.2f}%\n")
                    f.write(f"  Avg Latency: {avg_latency:.0f}ms\n")
                    f.write(f"  Circuit Breaker Trips: {total_cb_trips}\n")
                    f.write(f"  Avg Recovery Time: {avg_recovery:.1f}s\n")
                    f.write(f"  Resilience Score: {resilience_score:.2f}/100\n\n")
            
            # Chaos type analysis
            f.write("\n" + "="*80 + "\n")
            f.write("CHAOS TYPE IMPACT ANALYSIS\n")
            f.write("="*80 + "\n\n")
            
            for chaos_type in CHAOS_TYPES.keys():
                chaos_experiments = [e for e in self.experiment_results if e['chaos_type'] == chaos_type]
                
                if chaos_experiments:
                    avg_success_rate = sum(e['success_rate'] for e in chaos_experiments) / len(chaos_experiments)
                    avg_cb_trips = sum(e['circuit_breaker_trips'] for e in chaos_experiments) / len(chaos_experiments)
                    
                    f.write(f"{CHAOS_TYPES[chaos_type]['name'].upper()}\n")
                    f.write(f"  Experiments Run: {len(chaos_experiments)}\n")
                    f.write(f"  Avg Success Rate: {avg_success_rate:.2f}%\n")
                    f.write(f"  Avg Circuit Breaker Trips: {avg_cb_trips:.1f}\n")
                    f.write(f"  Impact Level: {'High' if avg_success_rate < 50 else 'Medium' if avg_success_rate < 75 else 'Low'}\n\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("DATA FILES GENERATED\n")
            f.write("="*80 + "\n\n")
            f.write(f"Experiment Log: {self.experiment_log_file.name}\n")
            f.write(f"Request Log: {self.request_log_file.name}\n")
            f.write(f"Service Comparison: {self.service_comparison_file.name}\n")
            f.write(f"Final Report: {report_file.name}\n\n")
        
        self.log(f"\n✅ Final report saved to: {report_file}", level='SUCCESS')
        self.log(f"📁 All data files in: {self.output_dir}", level='SUCCESS')
    
    def run(self):
        """Main test execution loop"""
        self.log("="*80, level='INFO')
        self.log("🔥 AI RESILIENCE CHAOS TESTING STARTED", level='INFO')
        self.log("="*80, level='INFO')
        self.log(f"Duration: {self.duration_hours} hours", level='INFO')
        self.log(f"Requests per cycle: {self.requests_per_cycle}", level='INFO')
        self.log(f"Chaos duration: {self.chaos_duration}s", level='INFO')
        self.log(f"Normal period: {self.normal_duration}s", level='INFO')
        self.log(f"Output directory: {self.output_dir}", level='INFO')
        self.log("="*80 + "\n", level='INFO')
        
        # Check backend health
        if not self.check_backend_health():
            self.log("❌ Backend is not running! Please start the backend first.", level='ERROR')
            return
        
        start_time = time.time()
        end_time = start_time + (self.duration_hours * 3600)
        
        experiment_id = 1
        
        # Main testing loop
        while time.time() < end_time and self.running:
            # Round-robin through all chaos types
            for chaos_type in CHAOS_TYPES.keys():
                if not self.running or time.time() >= end_time:
                    break
                
                # Test each intensity level
                for intensity in CHAOS_TYPES[chaos_type]['intensities']:
                    if not self.running or time.time() >= end_time:
                        break
                    
                    # Test each service
                    for service in SERVICES:
                        if not self.running or time.time() >= end_time:
                            break
                        
                        # Run chaos experiment
                        self.run_experiment(experiment_id, chaos_type, intensity, service)
                        experiment_id += 1
                        
                        # Normal period between experiments
                        if self.running and time.time() < end_time:
                            self.run_normal_period(self.normal_duration)
        
        # Generate final report
        self.log("\n\n⏰ Test duration completed!", level='SUCCESS')
        self.generate_final_report()
        
        self.log("\n" + "="*80, level='INFO')
        self.log("🎉 CHAOS TESTING COMPLETE!", level='SUCCESS')
        self.log("="*80, level='INFO')

def main():
    parser = argparse.ArgumentParser(
        description='AI Resilience Monitor - Automated Chaos Testing & Empirical Validation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run empirical validation suite (recommended for research)
  python chaos-test.py --validation
  
  # Run 24-hour test with default settings
  python chaos-test.py
  
  # Run 4-hour test with custom parameters
  python chaos-test.py --duration 4 --requests 20 --chaos-duration 600
  
  # Quick test (1 hour)
  python chaos-test.py --duration 1 --requests 5 --chaos-duration 120
  
  # Run validation suite with custom output
  python chaos-test.py --validation --output-dir validation-results
        """
    )
    
    parser.add_argument('--validation', action='store_true',
                       help='Run empirical validation suite with all test scenarios')
    parser.add_argument('--duration', type=int, default=24,
                       help='Test duration in hours (default: 24)')
    parser.add_argument('--requests', type=int, default=10,
                       help='Requests per chaos cycle (default: 10)')
    parser.add_argument('--chaos-duration', type=int, default=300,
                       help='Chaos experiment duration in seconds (default: 300)')
    parser.add_argument('--normal-duration', type=int, default=180,
                       help='Normal period duration in seconds (default: 180)')
    parser.add_argument('--output-dir', type=str, default='chaos-test-results',
                       help='Output directory for results (default: chaos-test-results)')
    
    args = parser.parse_args()
    
    # Create test runner
    runner = ChaosTestRunner(
        duration_hours=args.duration,
        requests_per_cycle=args.requests,
        chaos_duration=args.chaos_duration,
        normal_duration=args.normal_duration,
        output_dir=args.output_dir
    )
    
    try:
        if args.validation:
            # Run empirical validation suite
            if not runner.check_backend_health():
                runner.log("❌ Backend is not running! Please start the backend first.", level='ERROR')
                return
            
            runner.log("="*80, level='INFO')
            runner.log("🔬 STARTING EMPIRICAL VALIDATION MODE", level='INFO')
            runner.log("="*80, level='INFO')
            runner.log("This will run comprehensive load tests and chaos experiments", level='INFO')
            runner.log("to demonstrate effectiveness through empirical validation.", level='INFO')
            runner.log("="*80 + "\n", level='INFO')
            
            # Run validation suite
            runner.run_empirical_validation_suite()
            
            # Generate report
            runner.generate_final_report()
            
            runner.log("\n" + "="*80, level='INFO')
            runner.log("🎉 EMPIRICAL VALIDATION COMPLETE!", level='SUCCESS')
            runner.log("="*80, level='INFO')
        else:
            # Run standard chaos testing
            runner.run()
            
    except KeyboardInterrupt:
        try:
            print("\n\n[STOP] Test interrupted by user", flush=True)
        except:
            print("\n\nTest interrupted by user", flush=True)
        runner.generate_final_report()
    except Exception as e:
        try:
            print(f"\n[ERROR] Fatal error: {e}", flush=True)
        except:
            print(f"\nFatal error: {str(e).encode('ascii', errors='ignore').decode('ascii')}", flush=True)
        import traceback
        traceback.print_exc()
        runner.generate_final_report()

if __name__ == '__main__':
    main()
