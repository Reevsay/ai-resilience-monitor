# 🚀 Quick Start: Capturing Screenshots for Your Research Paper

**Goal:** Get all dashboard screenshots in different states for your research paper

---

## ⚡ Fastest Method (Automated)

### 1. Install Selenium
```bash
pip install selenium webdriver-manager
```

### 2. Make Sure Everything is Running
```bash
# Start the enhanced monitoring system
.\scripts\setup\start-monitor-enhanced.ps1
```

### 3. Run the Screenshot Script
```bash
python scripts/utilities/capture-screenshots.py
```

**Done!** Screenshots will be saved to `research-paper/figures/`

---

## 📋 Manual Method (If Automated Fails)

### Quick 4-Phase Process:

#### **Phase 1: Idle State (3 min)**
1. Open: `http://localhost:8080`
2. Capture full dashboard → `01_dashboard_idle_state.png`
3. Capture system status panel → `02_system_status_normal.png`
4. Capture circuit breaker panel → `08_circuit_breaker_closed.png`

#### **Phase 2: Start Test (1 min)**
5. Click "Start Chaos Test"
6. Capture configuration → `03_chaos_config_panel.png`
7. Confirm start, wait 5 sec
8. Capture full dashboard → `04_chaos_testing_started.png`

#### **Phase 3: During Test (2 min)**
9. Wait 15 seconds, capture terminal → `05_chaos_terminal_output.png`
10. Wait 25 seconds, capture response chart → `06_response_time_chart_active.png`
11. Capture success rate chart → `07_success_rate_chart.png`
12. Wait 35 seconds, capture circuit breaker (red) → `09_circuit_breaker_open.png`
13. Capture metrics panel → `11_realtime_metrics_high_load.png`
14. Capture system status → `12_system_status_under_stress.png`

#### **Phase 4: Results (1 min)**
15. Wait for test to complete
16. Capture results summary → `13_chaos_test_results.png`
17. Capture service health → `15_service_health_status.png`

**Total Time: ~7 minutes**

---

## 📚 Guides Available

| Guide | Purpose | Location |
|-------|---------|----------|
| **Screenshot Guide** | List of all screenshots needed | `docs/SCREENSHOT_GUIDE.md` |
| **Instructions** | Step-by-step manual process | `docs/SCREENSHOT_INSTRUCTIONS.md` |
| **Visual Reference** | Dashboard layout & elements | `docs/VISUAL_REFERENCE_GUIDE.md` |

---

## ✅ Minimum Required Screenshots (for Paper)

If short on time, get at least these **8 core screenshots**:

1. ✅ **Dashboard Idle** - Shows initial state
2. ✅ **Chaos Testing Active** - Shows test running
3. ✅ **Terminal Output** - Shows live logging
4. ✅ **Response Time Chart** - Shows performance impact
5. ✅ **Success Rate Chart** - Shows degradation/recovery
6. ✅ **Circuit Breaker Closed** - Shows normal state
7. ✅ **Circuit Breaker Open** - Shows failure protection
8. ✅ **Test Results** - Shows final metrics

---

## 🎯 Screenshot Quality Checklist

Before using in paper:
- [ ] 1920x1080 or higher resolution
- [ ] PNG format (not JPG)
- [ ] All text is readable
- [ ] No browser UI visible (unless needed)
- [ ] Proper file naming (01_, 02_, etc.)

---

## 💡 Pro Tips

1. **Timing is Key** - Wait for data to populate before capturing
2. **Use Fullscreen** - Press F11 for clean dashboard view
3. **Consistency** - Use same browser zoom (100%) for all
4. **Annotations** - Add arrows/boxes AFTER capturing (use PowerPoint or Paint)
5. **Backup** - Keep originals, edit copies

---

## 🆘 Troubleshooting

### Dashboard not loading?
```bash
# Check if services are running
python app.py
# In another terminal
cd src
node index.js
```

### Automated script fails?
- Make sure Chrome is installed
- Install selenium: `pip install selenium webdriver-manager`
- Use manual method instead

### Screenshots are blurry?
- Use PNG format (not JPG)
- Ensure browser zoom is 100%
- Capture at higher resolution (2560x1440)

---

## 📊 For Your Research Paper

### Sample LaTeX Code:
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/01_dashboard_idle_state.png}
    \caption{AI Resilience Monitor Dashboard in idle state showing baseline metrics.}
    \label{fig:dashboard_idle}
\end{figure}
```

### Sample Word/Docs:
1. Insert → Picture → Choose screenshot
2. Right-click → Add Caption
3. Reference as "Figure 1", "Figure 2", etc.

---

## 🎉 Ready to Go!

Everything you need is set up. Choose your method:

- **Fast & Automated:** Run `python scripts/utilities/capture-screenshots.py`
- **Manual Control:** Follow `docs/SCREENSHOT_INSTRUCTIONS.md`
- **Visual Guide:** Reference `docs/VISUAL_REFERENCE_GUIDE.md`

**Good luck with your research paper!** 🎓📸
