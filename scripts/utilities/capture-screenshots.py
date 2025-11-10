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

# Screenshot definitions
SCREENSHOTS = [
    {
        "name": "01_dashboard_idle_state.png",
        "description": "Full dashboard in idle state",
        "action": "idle",
        "wait": 2,
        "full_page": True
    },
    {
        "name": "02_system_status_normal.png",
        "description": "System status panel - normal operation",
        "action": "focus_element",
        "selector": ".system-status-panel",
        "wait": 1,
        "full_page": False
    },
    {
        "name": "03_chaos_config_panel.png",
        "description": "Chaos testing configuration",
        "action": "open_chaos_config",
        "wait": 1,
        "full_page": False
    },
    {
        "name": "04_chaos_testing_started.png",
        "description": "Chaos testing - just started",
        "action": "start_chaos_test",
        "wait": 5,
        "full_page": True
    },
    {
        "name": "05_chaos_terminal_output.png",
        "description": "Chaos terminal output - active",
        "action": "focus_element",
        "selector": ".chaos-terminal",
        "wait": 10,
        "full_page": False
    },
    {
        "name": "06_response_time_chart_active.png",
        "description": "Response time chart with data",
        "action": "focus_element",
        "selector": ".response-time-chart",
        "wait": 15,
        "full_page": False
    },
    {
        "name": "07_success_rate_chart.png",
        "description": "Success rate chart showing degradation",
        "action": "focus_element",
        "selector": ".success-rate-chart",
        "wait": 20,
        "full_page": False
    },
    {
        "name": "08_circuit_breaker_closed.png",
        "description": "Circuit breaker - CLOSED state",
        "action": "focus_element",
        "selector": ".circuit-breaker-panel",
        "wait": 1,
        "full_page": False
    },
    {
        "name": "09_circuit_breaker_open.png",
        "description": "Circuit breaker - OPEN state",
        "action": "wait_for_circuit_open",
        "wait": 30,
        "full_page": False
    },
    {
        "name": "11_realtime_metrics_high_load.png",
        "description": "Real-time metrics under high load",
        "action": "focus_element",
        "selector": ".realtime-metrics-panel",
        "wait": 25,
        "full_page": False
    },
    {
        "name": "12_system_status_under_stress.png",
        "description": "System status during chaos testing",
        "action": "focus_element",
        "selector": ".system-status-panel",
        "wait": 30,
        "full_page": False
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
        print("AUTOMATED DASHBOARD SCREENSHOT CAPTURE")
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
        
        print("\nCapturing screenshots...")
        print("-"*70)
        
        chaos_started = False
        
        for i, screenshot in enumerate(SCREENSHOTS, 1):
            print(f"\n[{i}/{len(SCREENSHOTS)}] {screenshot['description']}")
            
            # Perform action
            action = screenshot.get('action', 'idle')
            
            if action == 'idle':
                time.sleep(screenshot['wait'])
            
            elif action == 'focus_element':
                selector = screenshot.get('selector')
                if selector:
                    self.focus_element(selector)
                time.sleep(screenshot['wait'])
            
            elif action == 'open_chaos_config':
                # Try to open chaos config panel
                try:
                    config_btn = self.driver.find_element(By.ID, "chaosConfigBtn")
                    config_btn.click()
                    time.sleep(screenshot['wait'])
                except:
                    print("  ⚠ Chaos config button not found, using default view")
            
            elif action == 'start_chaos_test':
                if not chaos_started:
                    self.start_chaos_test()
                    chaos_started = True
                time.sleep(screenshot['wait'])
            
            elif action == 'wait_for_circuit_open':
                self.wait_for_circuit_open()
                self.focus_element(screenshot.get('selector', '.circuit-breaker-panel'))
            
            # Take screenshot
            self.take_screenshot(screenshot['name'], screenshot.get('full_page', False))
            
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
║     📸 DASHBOARD SCREENSHOT AUTOMATION SCRIPT 📸            ║
╚══════════════════════════════════════════════════════════════╝

This script will automatically capture all dashboard states
for your research paper.

Prerequisites:
  ✓ Dashboard running on http://localhost:8080
  ✓ Backend running on http://localhost:3000
  ✓ Chrome browser installed
  ✓ ChromeDriver installed (pip install webdriver-manager)

The script will:
  1. Check if services are running
  2. Open Chrome browser
  3. Capture 12+ screenshots automatically
  4. Save to research-paper/figures/
  5. Close browser when done

Press Ctrl+C to cancel at any time.
""")
    
    input("Press Enter to start screenshot capture...")
    main()
