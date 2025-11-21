#!/usr/bin/env python3
"""
Automated Dashboard Screenshot Script
Captures all dashboard states for research paper documentation
"""

import time
import os
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests

# Configuration
DASHBOARD_URL = "http://localhost:8080"
BACKEND_URL = "http://localhost:3000"
OUTPUT_DIR = Path(__file__).parent.parent / "research-paper" / "figures"
SCREENSHOT_WIDTH = 1920
SCREENSHOT_HEIGHT = 1080

# Screenshot definitions - Individual Components (Every component on the page)
SCREENSHOTS = [
    # Top Section
    {
        "name": "01_top_metrics_cards.png",
        "description": "Top Metrics Cards (Total Requests, Success Rate, Avg Response Time)",
        "selector": ".stats-grid",
        "wait": 2
    },
    
    # AI Services Section
    {
        "name": "02_ai_service_status_section.png",
        "description": "AI Service Status Section (All Services)",
        "selector": ".services-section",
        "wait": 2
    },
    
    # Chaos Engineering Section
    {
        "name": "03_chaos_engineering_section.png",
        "description": "Chaos Engineering Section (Complete)",
        "selector": ".chaos-section",
        "wait": 2
    },
    {
        "name": "04_chaos_controls.png",
        "description": "Chaos Engineering Controls Panel",
        "selector": ".chaos-controls",
        "wait": 2
    },
    {
        "name": "05_active_experiments.png",
        "description": "Active Chaos Experiments List",
        "selector": ".active-experiments",
        "wait": 2
    },
    
    # Analytics Section
    {
        "name": "06_analytics_section.png",
        "description": "Complete Analytics & Insights Section",
        "selector": ".analytics-section",
        "wait": 2
    },
    {
        "name": "07_analytics_controls.png",
        "description": "Analytics Controls (Auto Requests, Target Service, Interval)",
        "selector": ".analytics-controls",
        "wait": 2
    },
    {
        "name": "08_real_time_performance_chart.png",
        "description": "Real-Time Performance Chart",
        "selector": "#performanceChart",
        "wait": 3
    },
    {
        "name": "09_service_response_time_trends.png",
        "description": "Service Response Time Trends Chart",
        "selector": "#latencyChart",
        "wait": 3
    },
    {
        "name": "10_service_performance_leaderboard.png",
        "description": "Service Performance Leaderboard",
        "selector": "#serviceLeaderboard",
        "wait": 2
    },
    {
        "name": "11_circuit_breaker_status.png",
        "description": "Circuit Breaker Status Panel",
        "selector": "#circuitBreakerStatus",
        "wait": 2
    },
    {
        "name": "12_key_insights.png",
        "description": "Key Insights Summary",
        "selector": ".metrics-summary",
        "wait": 2
    },
    {
        "name": "13_advanced_analytics.png",
        "description": "Advanced Analytics Section",
        "selector": ".analytics-card.full-width:nth-of-type(1)",
        "wait": 2
    },
    {
        "name": "14_failure_recovery_analysis.png",
        "description": "Failure Recovery Analysis",
        "selector": ".recovery-section",
        "wait": 2
    },
    {
        "name": "15_error_patterns_leaderboard.png",
        "description": "Error Patterns Leaderboard",
        "selector": ".error-patterns-section",
        "wait": 2
    },
    {
        "name": "16_performance_trends_analysis.png",
        "description": "Performance Trends Analysis",
        "selector": ".trends-section",
        "wait": 2
    },
    {
        "name": "17_historical_request_log.png",
        "description": "Historical Request Log Table",
        "selector": "#historyTable",
        "wait": 2
    },
    
    # Long-Term Chaos Testing Section
    {
        "name": "18_chaos_testing_section.png",
        "description": "Long-Term Chaos Testing Section",
        "selector": ".chaos-testing-section",
        "wait": 2
    },
    {
        "name": "19_chaos_test_status.png",
        "description": "Chaos Test Status Card",
        "selector": ".testing-status-card",
        "wait": 2
    },
    {
        "name": "20_chaos_testing_actions.png",
        "description": "Chaos Testing Action Buttons",
        "selector": ".testing-actions",
        "wait": 2
    },
]


class DashboardScreenshotter:
    def __init__(self):
        self.driver = None
        self.output_dir = OUTPUT_DIR
        self.setup_output_directory()
        
    def setup_output_directory(self):
        """Create output directory structure"""
        subdirs = ['dashboard-states', 'metrics', 'circuit-breaker', 'chaos-testing']
        for subdir in subdirs:
            (self.output_dir / subdir).mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory created: {self.output_dir}")
    
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument(f"--window-size={SCREENSHOT_WIDTH},{SCREENSHOT_HEIGHT}")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--force-device-scale-factor=1")
        chrome_options.add_argument("--high-dpi-support=1")
        
        # Uncomment for headless mode (no browser window)
        # chrome_options.add_argument("--headless")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✓ Chrome driver initialized")
            return True
        except Exception as e:
            print(f"✗ Error initializing Chrome driver: {e}")
            print("\nPlease install ChromeDriver:")
            print("  pip install webdriver-manager")
            print("  or download from: https://chromedriver.chromium.org/")
            return False
    
    def check_services(self):
        """Check if dashboard and backend are running"""
        try:
            response = requests.get(DASHBOARD_URL, timeout=5)
            if response.status_code == 200:
                print(f"✓ Dashboard is running at {DASHBOARD_URL}")
            else:
                print(f"✗ Dashboard returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Cannot connect to dashboard: {e}")
            print(f"\nPlease start the dashboard first:")
            print(f"  python app.py")
            return False
        
        try:
            response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
            if response.status_code == 200:
                print(f"✓ Backend is running at {BACKEND_URL}")
                return True
            else:
                print(f"⚠ Backend returned status {response.status_code}")
                return True  # Continue anyway
        except requests.exceptions.RequestException as e:
            print(f"⚠ Cannot connect to backend: {e}")
            return True  # Continue anyway
    
    def take_screenshot(self, filename, full_page=False):
        """Take a screenshot and save it"""
        filepath = self.output_dir / filename
        
        try:
            if full_page:
                # Get full page height
                total_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.set_window_size(SCREENSHOT_WIDTH, total_height)
                time.sleep(0.5)
            
            self.driver.save_screenshot(str(filepath))
            
            # Reset window size if full page
            if full_page:
                self.driver.set_window_size(SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT)
            
            print(f"  ✓ Saved: {filename}")
            return True
        except Exception as e:
            print(f"  ✗ Error saving {filename}: {e}")
            return False
    
    def take_element_screenshot(self, selector, filename):
        """Take a screenshot of a specific element only"""
        filepath = self.output_dir / filename
        
        try:
            # Find the element
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(1)
            
            # Take screenshot of just this element
            element.screenshot(str(filepath))
            
            print(f"  ✓ Saved: {filename}")
            return True
        except Exception as e:
            print(f"  ⚠ Could not capture {selector}: {e}")
            print(f"  ℹ Taking full page screenshot instead...")
            # Fallback to full page screenshot
            return self.take_screenshot(filename, full_page=False)
            return False
    
    def focus_element(self, selector):
        """Scroll to and focus on a specific element"""
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(1)
            return True
        except Exception as e:
            print(f"  ⚠ Could not find element {selector}: {e}")
            return False
    
    def start_chaos_test(self):
        """Start chaos testing via API"""
        try:
            # Find and click start button
            start_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "startChaosTestBtn"))
            )
            start_button.click()
            print("  ✓ Chaos test started")
            return True
        except Exception as e:
            print(f"  ⚠ Could not start chaos test: {e}")
            # Try API fallback
            try:
                response = requests.post(f"{BACKEND_URL}/chaos-testing/start", 
                                       json={"duration": 60, "mode": "validation"})
                if response.status_code == 200:
                    print("  ✓ Chaos test started via API")
                    return True
            except:
                pass
            return False
    
    def wait_for_circuit_open(self):
        """Wait for circuit breaker to open"""
        print("  Waiting for circuit breaker to open...")
        max_wait = 60
        waited = 0
        
        while waited < max_wait:
            try:
                # Check if any circuit breaker shows OPEN state
                open_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'OPEN')]")
                if open_elements:
                    print(f"  ✓ Circuit breaker opened after {waited}s")
                    return True
            except:
                pass
            
            time.sleep(2)
            waited += 2
        
        print("  ⚠ Circuit breaker did not open within timeout")
        return False
    
    def capture_all(self):
        """Capture all screenshots according to the plan"""
        print("\n" + "="*70)
        print("INDIVIDUAL COMPONENT SCREENSHOT CAPTURE")
        print("="*70)
        
        # Check services
        if not self.check_services():
            return False
        
        # Setup driver
        if not self.setup_driver():
            return False
        
        # Load dashboard
        print(f"\nLoading dashboard: {DASHBOARD_URL}")
        self.driver.get(DASHBOARD_URL)
        time.sleep(3)
        
        print("\nCapturing individual component screenshots...")
        print("-"*70)
        
        for i, screenshot in enumerate(SCREENSHOTS, 1):
            print(f"\n[{i}/{len(SCREENSHOTS)}] {screenshot['description']}")
            
            # Wait before capturing
            time.sleep(screenshot.get('wait', 1))
            
            # Capture element screenshot
            selector = screenshot.get('selector')
            if selector:
                self.take_element_screenshot(selector, screenshot['name'])
            else:
                self.take_screenshot(screenshot['name'], full_page=False)
            
            # Small delay between screenshots
            time.sleep(0.5)
        
        print("\n" + "="*70)
        print("SCREENSHOT CAPTURE COMPLETE!")
        print("="*70)
        print(f"\nScreenshots saved to: {self.output_dir}")
        print(f"Total screenshots: {len(SCREENSHOTS)}")
        
        return True
    
    def cleanup(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("\n✓ Browser closed")


def main():
    """Main function"""
    screenshotter = DashboardScreenshotter()
    
    try:
        success = screenshotter.capture_all()
        
        if success:
            print("\n✅ All screenshots captured successfully!")
            print("\nNext steps:")
            print("  1. Review screenshots in: research-paper/figures/")
            print("  2. Organize into subfolders as needed")
            print("  3. Add annotations using image editing software")
            print("  4. Insert into research paper with captions")
        else:
            print("\n⚠ Screenshot capture incomplete")
    
    except KeyboardInterrupt:
        print("\n\n⚠ Screenshot capture cancelled by user")
    
    except Exception as e:
        print(f"\n✗ Error during screenshot capture: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        screenshotter.cleanup()


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║     📸 COMPONENT SCREENSHOT AUTOMATION SCRIPT 📸           ║
╚══════════════════════════════════════════════════════════════╝

This script will capture individual dashboard components
as separate screenshots with proper naming.

Prerequisites:
  ✓ Dashboard running on http://localhost:8080
  ✓ Backend running on http://localhost:3000
  ✓ Chrome browser installed
  ✓ ChromeDriver installed (pip install webdriver-manager)

The script will capture:
  • Top Metrics Cards
  • AI Service Status
  • Chaos Engineering Panel
  • Service Performance Leaderboard
  • Real-Time Performance Chart
  • Service Response Time Trends
  • Circuit Breaker Status
  • Error Rate Monitoring
  • System Health Overview
  • And more...

Each component will be saved with its actual size and named
appropriately for easy identification.

Press Ctrl+C to cancel at any time.
""")
    
    input("Press Enter to start screenshot capture...")
    main()
