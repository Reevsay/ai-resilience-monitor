# 🎨 Dashboard Elements Visual Reference

**For Research Paper Screenshots**

This document describes the visual appearance and location of each dashboard element to help you identify what to capture.

---

## 📐 Dashboard Layout Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     AI RESILIENCE MONITOR                           │
│                   (Header / Navigation Bar)                         │
├───────────────────────────┬─────────────────────────────────────────┤
│                           │                                         │
│   SYSTEM STATUS PANEL     │    REAL-TIME METRICS PANEL             │
│   (Top Left)              │    (Top Right)                          │
│   - Total Requests        │    - Requests/sec                       │
│   - Successful            │    - Active Requests                    │
│   - Failed                │    - Error Rate                         │
│   - Avg Response Time     │    - Latency (p50, p95, p99)           │
│   - Success Rate %        │                                         │
│                           │                                         │
├───────────────────────────┴─────────────────────────────────────────┤
│                                                                     │
│              RESPONSE TIME CHART (Line Chart)                       │
│              - X-axis: Time                                         │
│              - Y-axis: Response Time (ms)                           │
│              - Multiple colored lines for different services        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│              SUCCESS RATE CHART (Line Chart)                        │
│              - X-axis: Time                                         │
│              - Y-axis: Success Rate (%)                             │
│              - Shows degradation during failures                    │
│                                                                     │
├───────────────────────────┬─────────────────────────────────────────┤
│                           │                                         │
│   CIRCUIT BREAKER STATUS  │    CHAOS TESTING CONTROLS              │
│   (Bottom Left)           │    (Bottom Right)                       │
│   - Service Names         │    - Start Chaos Test Button           │
│   - State (CLOSED/OPEN)   │    - Stop Test Button                  │
│   - Failure Count         │    - Test Configuration                │
│   - Color indicators      │    - Status: Running/Stopped           │
│                           │                                         │
├───────────────────────────┴─────────────────────────────────────────┤
│                                                                     │
│              CHAOS TESTING TERMINAL OUTPUT                          │
│              (Scrollable text area)                                 │
│              - Real-time logs from chaos test                       │
│              - Color-coded messages (success, errors, warnings)     │
│              - Timestamps and scenario descriptions                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Element Descriptions by Screenshot

### Screenshot 1: Dashboard Idle State
**Visual Characteristics:**
- All metrics show "0" or default values
- Charts are empty (no data points)
- Circuit breakers show "CLOSED" in GREEN
- Success rate: 100%
- Terminal output: Empty or showing "Ready to start testing..."

**What to Look For:**
✓ Clean, organized layout  
✓ All panels visible  
✓ No error messages  
✓ Green status indicators  

---

### Screenshot 2: System Status Panel - Normal
**Location:** Top-Left corner

**Visual Elements:**
```
┌─────────────────────────────┐
│    SYSTEM STATUS            │
├─────────────────────────────┤
│ Total Requests:      0      │
│ Successful:          0      │
│ Failed:              0      │
│ Avg Response Time:   0ms    │
│ Success Rate:        100%   │
└─────────────────────────────┘
```

**Colors:**
- Background: Light gray or white
- Text: Dark gray or black
- Success Rate: Green if 100%
- Border: Subtle shadow or border

---

### Screenshot 3: Chaos Config Panel
**Visual Characteristics:**
- Modal/Dialog box overlay
- Configuration options visible:
  - Test Type dropdown
  - Duration input field
  - Failure rate slider
  - Target service checkboxes

**What to Capture:**
✓ Modal centered on screen  
✓ Configuration options visible  
✓ "Start" and "Cancel" buttons  
✓ Background dimmed  

---

### Screenshot 4: Chaos Testing Started
**Visual Changes:**
- Status indicator changes to "Running" (Orange/Yellow)
- Terminal starts showing output
- First few log lines visible
- Metrics begin to update
- "Start" button disabled, "Stop" button enabled

**What to Look For:**
✓ Status: "Chaos Testing Active"  
✓ Terminal has 5-10 lines of output  
✓ Metrics still mostly at 0 (just started)  

---

### Screenshot 5: Chaos Terminal Output
**Location:** Bottom section of dashboard

**Visual Characteristics:**
```
┌─────────────────────────────────────────────────────────┐
│ CHAOS TESTING OUTPUT                         [Clear]    │
├─────────────────────────────────────────────────────────┤
│ [21:45:32] 🔬 Starting Scenario 1: Normal Load Test    │
│ [21:45:33] ✅ Request #1 - Status: 200 - Time: 145ms   │
│ [21:45:34] ✅ Request #2 - Status: 200 - Time: 152ms   │
│ [21:45:35] ❌ Request #3 - Status: 500 - Time: 1250ms  │
│ [21:45:36] ⚠️  Warning: High response time detected    │
│ [21:45:37] ✅ Request #4 - Status: 200 - Time: 148ms   │
│ ...                                                      │
│ [Scrollable content]                                     │
└─────────────────────────────────────────────────────────┘
```

**Colors:**
- ✅ Green for successful requests
- ❌ Red for failed requests
- ⚠️ Yellow/Orange for warnings
- Black/white background with contrasting text

---

### Screenshot 6: Response Time Chart - Active
**Visual Characteristics:**
- Line chart with fluctuating data
- X-axis: Time labels (e.g., "21:45:00", "21:45:30")
- Y-axis: Milliseconds (0ms - 2000ms)
- Multiple colored lines (different services)
- Peaks during failure injection
- Tooltip on hover showing exact values

**What to Look For:**
✓ At least 20-30 data points  
✓ Visible spikes (high response times)  
✓ Legend showing service names  
✓ Grid lines for readability  

**Typical Pattern:**
```
Response Time (ms)
2000 ─              ●  ●
     │             ●    ●
1500 ─            ●      ●
     │           ●        ●
1000 ─          ●          ●
     │         ●            ●
 500 ─    ● ● ●              ● ● ●
     │  ●                          ●
   0 ─●────────────────────────────────●─
     Time →
```

---

### Screenshot 7: Success Rate Chart
**Visual Characteristics:**
- Line chart showing percentage (0% - 100%)
- Starts at 100%
- Dips during chaos injection
- Recovers back to 100%

**What to Look For:**
✓ Clear degradation visible  
✓ Recovery curve back to 100%  
✓ Time duration visible  

**Typical Pattern:**
```
Success Rate (%)
100% ─●●●●          ●●●●●●●●●●
     │     ●        ●
 80% ─      ●      ●
     │       ●    ●
 60% ─        ●  ●
     │         ●●
 40% ─
     │
  0% ─────────────────────────────────
     Time →
     │←Injection→│←Recovery→│
```

---

### Screenshot 8: Circuit Breaker - CLOSED
**Visual Characteristics:**
```
┌─────────────────────────────┐
│  CIRCUIT BREAKER STATUS     │
├─────────────────────────────┤
│  🟢 OpenAI Service          │
│     State: CLOSED           │
│     Failures: 0             │
│     Success Rate: 100%      │
├─────────────────────────────┤
│  🟢 Anthropic Service       │
│     State: CLOSED           │
│     Failures: 0             │
│     Success Rate: 100%      │
└─────────────────────────────┘
```

**Colors:**
- 🟢 Green circle/indicator
- Black text on white/light background
- Clean, healthy appearance

---

### Screenshot 9: Circuit Breaker - OPEN
**Visual Characteristics:**
```
┌─────────────────────────────┐
│  CIRCUIT BREAKER STATUS     │
├─────────────────────────────┤
│  🔴 OpenAI Service          │
│     State: OPEN             │
│     Failures: 15            │
│     Success Rate: 45%       │
│     Retry in: 30s           │
├─────────────────────────────┤
│  🟢 Anthropic Service       │
│     State: CLOSED           │
│     Failures: 2             │
│     Success Rate: 95%       │
└─────────────────────────────┘
```

**Colors:**
- 🔴 Red circle/indicator for OPEN
- Red text for "OPEN" state
- Warning color for low success rate
- Countdown timer visible

---

### Screenshot 10: Circuit Breaker - HALF_OPEN
**Visual Characteristics:**
```
┌─────────────────────────────┐
│  CIRCUIT BREAKER STATUS     │
├─────────────────────────────┤
│  🟡 OpenAI Service          │
│     State: HALF_OPEN        │
│     Failures: 15            │
│     Testing recovery...     │
└─────────────────────────────┘
```

**Colors:**
- 🟡 Yellow/Orange circle
- Yellow text for "HALF_OPEN"
- "Testing" message visible

---

### Screenshot 11: Real-time Metrics - High Load
**Location:** Top-Right corner

**Visual Characteristics:**
```
┌─────────────────────────────┐
│  REAL-TIME METRICS          │
├─────────────────────────────┤
│  Requests/sec:     25       │
│  Active Requests:  8        │
│  Error Rate:       12%      │
│                             │
│  Latency:                   │
│    p50:  250ms              │
│    p95:  850ms              │
│    p99:  1450ms             │
└─────────────────────────────┘
```

**Visual Indicators:**
- Animated counters/gauges
- Error rate highlighted in red if >10%
- High latency values in orange/yellow

---

### Screenshot 12: System Status - Under Stress
**Visual Changes from Normal:**
```
┌─────────────────────────────┐
│    SYSTEM STATUS            │
├─────────────────────────────┤
│ Total Requests:      450    │
│ Successful:          382    │ ← Lower %
│ Failed:              68     │ ← Visible failures
│ Avg Response Time:   650ms  │ ← Elevated
│ Success Rate:        84.9%  │ ← RED/ORANGE
└─────────────────────────────┘
```

**Color Changes:**
- Success Rate: Changes from green to yellow/orange/red
- Failed Requests: Highlighted in red
- Response Time: Yellow if >500ms, red if >1000ms

---

### Screenshot 13: Test Results Summary
**Visual Characteristics:**
- Modal or panel showing summary
- Test completion notification
- Statistics table or cards

**Elements to Show:**
```
┌─────────────────────────────────────┐
│  CHAOS TEST RESULTS                 │
├─────────────────────────────────────┤
│  Duration:        120 seconds       │
│  Total Requests:  500               │
│  Successful:      425 (85%)         │
│  Failed:          75 (15%)          │
│  Avg Response:    425ms             │
│  Circuit Breaks:  3 times           │
│  Recovery Time:   45 seconds        │
├─────────────────────────────────────┤
│         [Save Report]   [Close]     │
└─────────────────────────────────────┘
```

---

## 🎨 Color Coding Reference

### Status Indicators:
- 🟢 **Green** - Normal/Healthy/Closed/Success
- 🔴 **Red** - Error/Failed/Open/Critical
- 🟡 **Yellow/Orange** - Warning/Half-Open/Degraded
- 🔵 **Blue** - Info/Running/Active
- ⚪ **Gray** - Idle/Disabled/Unknown

### Text Colors:
- **Black** - Normal text
- **Green** - Success messages, good metrics
- **Red** - Error messages, failures
- **Orange** - Warnings, elevated metrics
- **Blue** - Informational messages

---

## 📏 Screenshot Dimensions

### Recommended Sizes:
- **Full Dashboard:** 1920x1080 (Full HD)
- **Individual Panels:** 800x600 minimum
- **Charts:** 1200x600 minimum
- **Terminal Output:** 1000x400 minimum

### For Research Paper:
- **DPI:** 300 (for print)
- **Format:** PNG (lossless)
- **Color Mode:** RGB
- **Compression:** None or minimal

---

## 💡 Tips for Clear Screenshots

1. **Wait for Animations** - Let transitions complete
2. **Scroll Carefully** - Ensure entire element is visible
3. **Clean Background** - Hide unnecessary browser UI
4. **Consistent Zoom** - Always use 100% browser zoom
5. **Good Contrast** - Use light theme for better print quality
6. **Highlight Important** - Use annotations after capture

---

## ✅ Quality Checklist

Before submitting screenshots to your paper:

- [ ] All text is readable
- [ ] Charts show clear data
- [ ] Colors are distinct
- [ ] No cut-off elements
- [ ] Consistent resolution
- [ ] No browser chrome visible (unless needed)
- [ ] Proper aspect ratio maintained
- [ ] File size appropriate (<5MB)

---

**Use this guide along with `SCREENSHOT_INSTRUCTIONS.md` for best results!**
