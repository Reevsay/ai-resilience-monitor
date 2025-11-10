# 📸 Screenshot Capture Instructions

## Quick Setup for Automated Screenshots

### 1. Install Required Packages

```bash
# Install Selenium for automated screenshots
pip install selenium webdriver-manager

# Or add to requirements.txt
echo selenium >> requirements.txt
echo webdriver-manager >> requirements.txt
pip install -r requirements.txt
```

### 2. Make Sure Services are Running

```bash
# Terminal 1: Start backend monitor (auto-starts backend)
python scripts/monitoring/monitor-backend-enhanced.py

# Terminal 2: Start frontend
python app.py

# OR use the enhanced startup script:
.\scripts\setup\start-monitor-enhanced.ps1
```

### 3. Run Automated Screenshot Script

```bash
# Navigate to project root
cd "c:\Users\yashv\OneDrive - BML MUNJAL UNIVERSITY\Documents\Work\Projects\AI related Projects\Devops try-2\ai-resilience-monitor"

# Run the screenshot script
python scripts/utilities/capture-screenshots.py
```

The script will:
- ✅ Open Chrome browser automatically
- ✅ Load the dashboard
- ✅ Start chaos testing
- ✅ Capture screenshots at different states
- ✅ Save everything to `research-paper/figures/`

---

## Manual Screenshot Capture (If Automated Doesn't Work)

### Phase 1: Idle State (3 screenshots)

1. **Open Dashboard:**
   ```
   http://localhost:8080
   ```

2. **Screenshot 1 - Full Dashboard Idle**
   - Press `Windows + Shift + S`
   - Capture full browser window
   - Save as: `01_dashboard_idle_state.png`

3. **Screenshot 2 - System Status Normal**
   - Locate "System Status" panel (usually top-left)
   - Capture just that panel
   - Save as: `02_system_status_normal.png`

4. **Screenshot 8 - Circuit Breaker Closed**
   - Find "Circuit Breaker Status" panel
   - Capture the panel showing "CLOSED" state (green)
   - Save as: `08_circuit_breaker_closed.png`

---

### Phase 2: Start Chaos Testing (2 screenshots)

5. **Screenshot 3 - Chaos Configuration**
   - Click "Start Chaos Test" button (don't confirm yet)
   - If config modal appears, capture it
   - Save as: `03_chaos_config_panel.png`

6. **Screenshot 4 - Testing Started**
   - Confirm/start the chaos test
   - Wait 5 seconds
   - Capture full dashboard
   - Save as: `04_chaos_testing_started.png`

---

### Phase 3: During Active Chaos Testing (6 screenshots)

**⏱ Wait 10-15 seconds after starting chaos test**

7. **Screenshot 5 - Terminal Output**
   - Scroll to chaos testing terminal/output section
   - Capture the terminal showing active logs
   - Save as: `05_chaos_terminal_output.png`

**⏱ Wait 20 seconds (let test run)**

8. **Screenshot 6 - Response Time Chart**
   - Locate "Response Time" chart
   - Should show fluctuating line with data points
   - Save as: `06_response_time_chart_active.png`

9. **Screenshot 7 - Success Rate Chart**
   - Find "Success Rate" chart
   - Should show degradation during failures
   - Save as: `07_success_rate_chart.png`

**⏱ Wait 30 seconds (circuit breaker should trip)**

10. **Screenshot 9 - Circuit Breaker OPEN**
    - Check "Circuit Breaker Status" panel
    - Should show "OPEN" state in RED
    - Save as: `09_circuit_breaker_open.png`

11. **Screenshot 11 - High Load Metrics**
    - Capture "Real-time Metrics" panel
    - Should show elevated request counts
    - Save as: `11_realtime_metrics_high_load.png`

12. **Screenshot 12 - System Under Stress**
    - Go back to "System Status" panel
    - Should show failed requests, lower success rate
    - Save as: `12_system_status_under_stress.png`

---

### Phase 4: After Test Completes (2 screenshots)

**⏱ Wait for test to complete (1-2 minutes)**

13. **Screenshot 13 - Test Results**
    - Look for test completion summary
    - Capture results panel or notification
    - Save as: `13_chaos_test_results.png`

14. **Screenshot 15 - Service Health**
    - Find "Service Health" or "AI Services Status"
    - Shows individual service statuses
    - Save as: `15_service_health_status.png`

---

## Screenshot Checklist

Use this to track what you've captured:

```
□ 01_dashboard_idle_state.png        - Full dashboard idle
□ 02_system_status_normal.png        - System status normal
□ 03_chaos_config_panel.png          - Chaos configuration
□ 04_chaos_testing_started.png       - Test just started
□ 05_chaos_terminal_output.png       - Terminal with logs
□ 06_response_time_chart_active.png  - Response time chart
□ 07_success_rate_chart.png          - Success rate chart
□ 08_circuit_breaker_closed.png      - CB closed (green)
□ 09_circuit_breaker_open.png        - CB open (red)
□ 10_circuit_breaker_half_open.png   - CB half-open (yellow) [OPTIONAL]
□ 11_realtime_metrics_high_load.png  - Metrics under load
□ 12_system_status_under_stress.png  - System stressed
□ 13_chaos_test_results.png          - Test results summary
□ 14_alerts_notifications.png        - Alerts panel [OPTIONAL]
□ 15_service_health_status.png       - Service health
□ 16_historical_data_view.png        - Historical view [OPTIONAL]
```

---

## Tips for Best Screenshots

### ✅ Do:
- Use 1920x1080 or higher resolution
- Maximize browser window
- Set browser zoom to 100%
- Wait for data to load before capturing
- Capture panels separately for clarity
- Use consistent timing

### ❌ Don't:
- Don't use compressed JPEG (use PNG)
- Don't capture with browser extensions visible
- Don't capture with low resolution
- Don't rush - wait for animations to complete
- Don't capture with partial data loading

---

## Organizing Screenshots

Create this folder structure:

```
research-paper/
└── figures/
    ├── dashboard-states/
    │   ├── 01_dashboard_idle_state.png
    │   └── 04_chaos_testing_started.png
    ├── metrics/
    │   ├── 06_response_time_chart_active.png
    │   ├── 07_success_rate_chart.png
    │   └── 11_realtime_metrics_high_load.png
    ├── circuit-breaker/
    │   ├── 08_circuit_breaker_closed.png
    │   ├── 09_circuit_breaker_open.png
    │   └── 10_circuit_breaker_half_open.png
    └── chaos-testing/
        ├── 03_chaos_config_panel.png
        ├── 05_chaos_terminal_output.png
        └── 13_chaos_test_results.png
```

---

## For Your Research Paper

### Sample Figure Caption Format:

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.8\textwidth]{figures/01_dashboard_idle_state.png}
\caption{AI Resilience Monitor Dashboard - Idle State. The dashboard shows 
all system metrics at baseline levels with 100\% success rate and minimal 
response times.}
\label{fig:dashboard_idle}
\end{figure}
```

### Reference in Text:

```
As shown in Figure~\ref{fig:dashboard_idle}, the monitoring dashboard provides 
real-time visibility into system performance...
```

---

## Need Help?

If automated script doesn't work:
1. Check if Chrome is installed
2. Install Selenium: `pip install selenium webdriver-manager`
3. Make sure dashboard is accessible at http://localhost:8080
4. Try manual screenshot method above

If manual screenshots are unclear:
- Check `docs/SCREENSHOT_GUIDE.md` for detailed element descriptions
- Adjust browser zoom for better visibility
- Use browser DevTools (F12) to highlight specific elements

---

**Good luck with your research paper!** 📸📊📝
