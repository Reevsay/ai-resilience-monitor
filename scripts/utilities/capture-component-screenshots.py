#!/usr/bin/env python3
"""
Detailed Component Screenshot Script
Captures individual dashboard components in all their visual states
Each screenshot shows ONLY the component (cropped), not the full page
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
from PIL import Image
import requests

# Configuration
DASHBOARD_URL = "http://localhost:8080"
BACKEND_URL = "http://localhost:3000"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "research-paper" / "component-screenshots"
SCREENSHOT_WIDTH = 1920
SCREENSHOT_HEIGHT = 1080

# Component definitions with their CSS selectors
COMPONENTS = {
    'header': {
        'name': 'Dashboard Header',
        'selector': 'header, .header, .navbar, .top-bar, h1',
        'states': ['normal']
    },
    'system_status': {
        'name': 'System Status Panel',
        'selector': '.card, .panel, [class*="status"], .metrics-card',
        'states': ['idle', 'normal', 'stressed', 'critical']
    },
    'metrics_panel': {
        'name': 'Real-time Metrics Panel',
        'selector': '.metrics, .real-time, [class*="metric"]',
        'states': ['idle', 'active', 'high_load']
    },
    'response_chart': {
        'name': 'Response Time Chart',
        'selector': 'canvas, .chart, [id*="chart"], .graph',
        'states': ['empty', 'normal_load', 'high_load', 'degraded']
    },
    'success_chart': {
        'name': 'Success Rate Chart',
        'selector': 'canvas, .chart, [id*="success"]',
        'states': ['baseline', 'degrading', 'degraded', 'recovering', 'recovered']
    },
    'circuit_breaker': {
        'name': 'Circuit Breaker Status',
        'selector': '.circuit, [class*="breaker"], .status-indicator',
        'states': ['closed', 'open', 'half_open']
    },
    'chaos_controls': {
        'name': 'Chaos Testing Controls',
        'selector': '.controls, .buttons, [class*="chaos-control"]',
        'states': ['idle', 'running', 'stopped']
    },
    'terminal_output': {
        'name': 'Chaos Terminal Output',
        'selector': '.terminal, .console, .output, pre, code',
        'states': ['empty', 'starting', 'running', 'completed']
    },
    'alerts': {
        'name': 'Alerts/Notifications',
        'selector': '.alert, .notification, .toast, .message',
        'states': ['none', 'info', 'warning', 'error', 'critical']
    }
}


class ComponentScreenshotter:
    def __init__(self):
        self.driver = None
        self.output_dir = OUTPUT_DIR
        self.setup_output_directory()
        
    def setup_output_directory(self):
        """Create output directory structure"""
        for component_key in COMPONENTS.keys():
            component_dir = self.output_dir / component_key
            component_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory created: {self.output_dir}")
    
    def setup_driver(self):
        """Setup Chrome driver"""
        chrome_options = Options()
        chrome_options.add_argument(f"--window-size={SCREENSHOT_WIDTH},{SCREENSHOT_HEIGHT}")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--force-device-scale-factor=1")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✓ Chrome driver initialized")
            return True
        except Exception as e:
            print(f"✗ Error initializing Chrome driver: {e}")
            return False
    
    def check_services(self):
        """Check if services are running"""
        try:
            response = requests.get(DASHBOARD_URL, timeout=5)
            if response.status_code == 200:
                print(f"✓ Dashboard running at {DASHBOARD_URL}")
                return True
        except:
            print(f"✗ Dashboard not accessible at {DASHBOARD_URL}")
            return False
    
    def find_all_elements(self, selector_list):
        """Find elements using multiple selectors"""
        for selector in selector_list.split(','):
            selector = selector.strip()
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return elements
            except:
                continue
        return []
    
    def capture_element(self, element, filename):
        """Capture screenshot of a specific element only"""
        try:
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            
            # Get element location and size
            location = element.location
            size = element.size
            
            # Take full page screenshot
            temp_file = self.output_dir / "temp_full.png"
            self.driver.save_screenshot(str(temp_file))
            
            # Crop to element
            image = Image.open(temp_file)
            
            # Calculate coordinates with padding
            padding = 10
            left = max(0, location['x'] - padding)
            top = max(0, location['y'] - padding)
            right = min(image.width, location['x'] + size['width'] + padding)
            bottom = min(image.height, location['y'] + size['height'] + padding)
            
            # Crop image
            cropped = image.crop((left, top, right, bottom))
            cropped.save(filename)
            
            # Clean up temp file
            if temp_file.exists():
                temp_file.unlink()
            
            return True
        except Exception as e:
            print(f"  ✗ Error capturing element: {e}")
            return False
    
    def wait_for_state(self, state_name, duration):
        """Wait for a specific state to be achieved"""
        print(f"  ⏳ Waiting for state: {state_name} ({duration}s)")
        time.sleep(duration)
    
    def start_chaos_test(self):
        """Start chaos testing"""
        try:
            response = requests.post(f"{BACKEND_URL}/chaos-testing/start",
                                   json={"duration": 120, "mode": "validation"})
            if response.status_code == 200:
                print("  ✓ Chaos test started")
                return True
        except Exception as e:
            print(f"  ⚠ Could not start chaos test: {e}")
        return False
    
    def capture_all_components(self):
        """Capture all components in all states"""
        print("\n" + "="*70)
        print("COMPONENT-BY-COMPONENT SCREENSHOT CAPTURE")
        print("="*70)
        
        if not self.check_services():
            return False
        
        if not self.setup_driver():
            return False
        
        print(f"\nLoading dashboard: {DASHBOARD_URL}")
        self.driver.get(DASHBOARD_URL)
        time.sleep(5)
        
        total_screenshots = 0
        
        # PHASE 1: Capture IDLE state components
        print("\n" + "="*70)
        print("PHASE 1: IDLE STATE - All components at rest")
        print("="*70)
        
        self.capture_phase_components('idle', total_screenshots)
        
        # PHASE 2: Start chaos test and capture ACTIVE states
        print("\n" + "="*70)
        print("PHASE 2: STARTING CHAOS TEST")
        print("="*70)
        
        chaos_started = self.start_chaos_test()
        if chaos_started:
            time.sleep(3)
            self.capture_phase_components('starting', total_screenshots)
        
        # PHASE 3: Capture during active testing (normal load)
        print("\n" + "="*70)
        print("PHASE 3: NORMAL LOAD - 15 seconds into test")
        print("="*70)
        time.sleep(12)
        self.capture_phase_components('normal_load', total_screenshots)
        
        # PHASE 4: High load / stressed state
        print("\n" + "="*70)
        print("PHASE 4: HIGH LOAD / STRESSED - 30 seconds into test")
        print("="*70)
        time.sleep(15)
        self.capture_phase_components('stressed', total_screenshots)
        
        # PHASE 5: Degraded / Circuit breaker open
        print("\n" + "="*70)
        print("PHASE 5: DEGRADED / CIRCUIT OPEN - 45 seconds into test")
        print("="*70)
        time.sleep(15)
        self.capture_phase_components('degraded', total_screenshots)
        
        # PHASE 6: Recovery phase
        print("\n" + "="*70)
        print("PHASE 6: RECOVERY - Test completing")
        print("="*70)
        time.sleep(30)
        self.capture_phase_components('recovering', total_screenshots)
        
        print("\n" + "="*70)
        print("CAPTURE COMPLETE!")
        print("="*70)
        print(f"\nTotal screenshots captured: Check {self.output_dir}")
        
        return True
    
    def capture_phase_components(self, phase_name, counter):
        """Capture all visible components in current phase"""
        print(f"\n📸 Capturing components in {phase_name} state...")
        
        # Find all visible cards/panels/components
        element_selectors = [
            'div.card',
            'div.panel',
            'div[class*="container"]',
            'section',
            'canvas',
            'pre',
            '.terminal',
            '.metrics',
            '.status',
            'table'
        ]
        
        captured_elements = set()
        screenshot_count = 0
        
        for selector in element_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for idx, element in enumerate(elements):
                    try:
                        # Check if element is visible and has size
                        if element.is_displayed() and element.size['width'] > 50 and element.size['height'] > 50:
                            # Get unique identifier
                            element_id = f"{selector}_{idx}"
                            
                            if element_id not in captured_elements:
                                # Generate filename
                                component_name = selector.replace('.', '').replace('[', '').replace(']', '').replace('*', '').replace('=', '')[:20]
                                filename = self.output_dir / f"{phase_name}_{component_name}_{idx:02d}.png"
                                
                                if self.capture_element(element, filename):
                                    print(f"  ✓ Captured: {filename.name} ({element.size['width']}x{element.size['height']}px)")
                                    captured_elements.add(element_id)
                                    screenshot_count += 1
                    except:
                        continue
            except:
                continue
        
        print(f"  📊 Total components captured in {phase_name}: {screenshot_count}")
        return screenshot_count
    
    def cleanup(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("\n✓ Browser closed")


def main():
    """Main function"""
    screenshotter = ComponentScreenshotter()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║   📸 DETAILED COMPONENT SCREENSHOT CAPTURE 📸               ║
╚══════════════════════════════════════════════════════════════╝

This script will capture INDIVIDUAL components (not full page):
  • Each component cropped to its actual size
  • Multiple states: idle, active, stressed, degraded, recovering
  • Organized by component type and state

Prerequisites:
  ✓ Dashboard running on http://localhost:8080
  ✓ Backend running on http://localhost:3000
  ✓ Chrome browser installed

Output:
  research-paper/component-screenshots/
    ├── idle_*.png
    ├── starting_*.png
    ├── normal_load_*.png
    ├── stressed_*.png
    ├── degraded_*.png
    └── recovering_*.png

Press Ctrl+C to cancel at any time.
""")
    
    input("Press Enter to start component screenshot capture...")
    
    try:
        success = screenshotter.capture_all_components()
        
        if success:
            print("\n✅ All component screenshots captured!")
            print(f"\nScreenshots saved to: {screenshotter.output_dir}")
            print("\nOrganized by state:")
            print("  • idle_* - Components at rest")
            print("  • starting_* - Test just started")
            print("  • normal_load_* - Normal test load")
            print("  • stressed_* - High load/stress")
            print("  • degraded_* - Circuit breakers open")
            print("  • recovering_* - System recovering")
    
    except KeyboardInterrupt:
        print("\n\n⚠ Screenshot capture cancelled by user")
    
    except Exception as e:
        print(f"\n✗ Error during capture: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        screenshotter.cleanup()


if __name__ == '__main__':
    main()
