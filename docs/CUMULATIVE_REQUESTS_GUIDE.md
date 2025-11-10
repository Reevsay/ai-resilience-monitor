# Cumulative Request Counting - Implementation Guide

## Problem
The dashboard's **Total Requests** counter was **not accurate** because:
1. ❌ Requests were stored **in-memory** only
2. ❌ Counter **reset to 0** every time backend restarted
3. ❌ Did **not persist** across sessions
4. ❌ Lost all historical data on crash/restart

## Solution
Implemented **database-backed cumulative request tracking** using SQLite.

## Changes Made

### 1. Database Schema (`src/index.js`)
```javascript
// New table for persistent counters
CREATE TABLE IF NOT EXISTS cumulative_metrics (
  key TEXT PRIMARY KEY,
  value INTEGER DEFAULT 0,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### 2. Database Helper Functions
```javascript
// Get cumulative metric from database
async function getCumulativeMetric(key)

// Increment cumulative metric (for each request)
async function incrementCumulativeMetric(key, amount = 1)

// Reset cumulative metric (for "Clear All Data" button)
async function resetCumulativeMetric(key)
```

### 3. Modified Endpoints

#### `/metrics` - Now returns database count
```javascript
app.get('/metrics', async (req, res) => {
  // Get cumulative total from database (persists across restarts)
  const cumulativeTotalRequests = await getCumulativeMetric('totalRequests');
  
  const metrics = calculateMetrics();
  metrics.totalRequests = cumulativeTotalRequests;  // Override with DB count
  
  res.json(metrics);
});
```

#### `/ai` - Increments database counter
```javascript
app.post('/ai', async (req, res) => {
  // Increment both in-memory AND database counter
  metricsHistory.totalRequests++;
  await incrementCumulativeMetric('totalRequests');  // PERSIST TO DB
  
  // ... process request ...
});
```

#### `/metrics/reset` - Resets database counter
```javascript
app.post('/metrics/reset', async (req, res) => {
  // Reset in-memory counters
  metricsHistory.totalRequests = 0;
  
  // ALSO reset database counter
  await resetCumulativeMetric('totalRequests');  // CLEAR PERSISTENT DATA
  
  // ... reset other metrics ...
});
```

## How It Works

### Flow Diagram
```
┌─────────────────────────────────────────────────────────────┐
│  REQUEST FLOW                                               │
└─────────────────────────────────────────────────────────────┘

1. User/Test sends request → POST /ai
                               ↓
2. Backend increments counter → metricsHistory.totalRequests++ (in-memory)
                               ↓
3. Backend persists to DB     → incrementCumulativeMetric('totalRequests')
                               ↓
4. SQLite stores count        → UPDATE cumulative_metrics SET value = value + 1


┌─────────────────────────────────────────────────────────────┐
│  DASHBOARD DISPLAY FLOW                                     │
└─────────────────────────────────────────────────────────────┘

1. Dashboard polls           → GET /metrics (every 5 seconds)
                               ↓
2. Backend queries database  → getCumulativeMetric('totalRequests')
                               ↓
3. Returns persistent count  → { totalRequests: 42 }  (from DB)
                               ↓
4. Dashboard displays        → "Total Requests: 42"


┌─────────────────────────────────────────────────────────────┐
│  RESET FLOW                                                 │
└─────────────────────────────────────────────────────────────┘

1. User clicks "Clear All Data" → POST /metrics/reset
                                   ↓
2. Backend resets memory         → metricsHistory.totalRequests = 0
                                   ↓
3. Backend resets database       → resetCumulativeMetric('totalRequests')
                                   ↓
4. SQLite updates                → UPDATE cumulative_metrics SET value = 0
                                   ↓
5. Dashboard shows 0             → "Total Requests: 0"
```

## Benefits

### ✅ Accurate Cumulative Tracking
- Counts **all requests** from session start
- Includes manual requests, automated tests, and chaos experiments
- Shows true total across **all sources**

### ✅ Persistence Across Restarts
- **Backend crashes** → Count preserved ✅
- **Manual restart** → Count preserved ✅
- **System reboot** → Count preserved ✅
- Data survives **ANY interruption**

### ✅ Proper Reset Functionality
- "Clear All Data" button **actually clears** cumulative count
- Resets to **0** (not just in-memory, but in database)
- Fresh start when needed

### ✅ No Data Loss
- SQLite database (`data/monitoring.db`) stores persistent data
- Even if backend crashes 100 times, count is never lost
- Historical accuracy maintained

## Testing

### Run the test script:
```bash
python test-cumulative-requests.py
```

### Expected Output:
```
🧪 CUMULATIVE REQUEST COUNTING TEST
====================================================

📝 TEST 1: Making initial requests...
✅ Request 1 sent
✅ Request 2 sent
...
📊 Total requests after batch 1: 5

📝 TEST 2: Testing persistence across restart...
🔄 Stopping backend...
✅ Killed Node process
🚀 Starting backend...
✅ Backend started
📊 Total requests after restart: 5
✅ PASS: Count persisted across restart!

📝 TEST 3: Adding more requests after restart...
✅ Request 1 sent
...
📊 Total requests after batch 2: 8
✅ PASS: Cumulative count correct (8)!

📝 TEST 4: Testing reset button...
✅ Metrics reset
📊 Total requests after reset: 0
✅ PASS: Reset worked correctly!

📝 TEST 5: Adding requests after reset...
✅ Request 1 sent
...
📊 Total requests after reset batch: 2
✅ PASS: Count started fresh from 0!

🎉 TEST SUMMARY
====================================================
✅ Initial requests: 5
✅ Persisted after restart: True
✅ Cumulative counting works: True
✅ Reset to 0: True
✅ Fresh count after reset: True
```

## Database Location
```
📁 data/monitoring.db
   └── Table: cumulative_metrics
       └── Row: { key: 'totalRequests', value: <count> }
```

## Package Requirements
Added to `package.json`:
```json
{
  "dependencies": {
    "sqlite3": "^5.x.x"
  }
}
```

## Installation
```bash
npm install sqlite3
```

## Verification Steps

### 1. Check current count:
```bash
curl http://localhost:3000/metrics
# Look for "totalRequests": <number>
```

### 2. Send test requests:
```bash
curl -X POST http://localhost:3000/ai \
  -H "Content-Type: application/json" \
  -d '{"service":"gemini","prompt":"test"}'
```

### 3. Restart backend:
```bash
# Kill: taskkill /F /IM node.exe
# Start: node src/index.js
# Check metrics again - count should be preserved!
```

### 4. Reset counters:
```bash
curl -X POST http://localhost:3000/metrics/reset
# Check metrics - totalRequests should be 0
```

## Troubleshooting

### Problem: Database not found
**Solution:** Backend automatically creates `data/monitoring.db` on startup

### Problem: Count still resets on restart
**Solution:** Check console for "✅ Connected to SQLite database" message

### Problem: Reset not working
**Solution:** Verify `/metrics/reset` endpoint calls `resetCumulativeMetric()`

### Problem: Count inconsistent
**Solution:** Clear browser cache and refresh dashboard

## Architecture Notes

### Why separate in-memory and database?
- **In-memory (`metricsHistory`)**: Fast access for current session stats
- **Database (`cumulative_metrics`)**: Persistent storage for cumulative totals
- **Hybrid approach**: Best of both worlds - speed + persistence

### Why not query database on every request?
- Database queries add latency
- In-memory increments are instant
- Database writes are async (don't block request processing)

### Why SQLite instead of JSON file?
- **Atomic operations** (no race conditions)
- **ACID compliance** (data integrity guaranteed)
- **Concurrent access** (multiple processes can access safely)
- **SQL queries** (easy to extend with analytics)

## Future Enhancements

### Possible Additions:
1. Track cumulative success/failure counts
2. Store per-service request totals
3. Historical data analytics (requests per day/week)
4. Export cumulative statistics to CSV
5. Grafana integration with persistent metrics

## Summary

**Before:**
- ❌ In-memory storage only
- ❌ Resets on every restart
- ❌ No historical data
- ❌ Inaccurate counts

**After:**
- ✅ SQLite database persistence
- ✅ Survives restarts/crashes
- ✅ Accurate cumulative tracking
- ✅ Proper reset functionality
- ✅ Production-ready reliability

**Impact:**
- Dashboard now shows **true cumulative total** from start
- Data **never lost** even with backend crashes
- "Clear All Data" button **properly resets** everything
- **Accurate metrics** for analysis and reporting
