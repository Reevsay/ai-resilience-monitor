# Data Directory

This directory stores persistent data for the AI Resilience Monitor.

## Files

### `monitoring.db`
SQLite database containing all historical monitoring data:
- **requests** - Every AI service request with full details
- **metrics_snapshots** - Periodic system metrics snapshots
- **circuit_breaker_events** - Circuit breaker state transitions
- **chaos_experiments** - Chaos engineering experiment logs
- **service_health** - Historical service health data

### Export Files
JSON exports are saved here with format: `export_YYYYMMDD_HHMMSS.json`

## Database Schema

### requests table
Stores every AI service request made through the system.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | DATETIME | When request was made |
| service | TEXT | AI service (gemini/cohere/huggingface) |
| prompt | TEXT | Input prompt (optional) |
| success | BOOLEAN | Whether request succeeded |
| latency | INTEGER | Response time in milliseconds |
| response_size | INTEGER | Size of response in characters |
| error_type | TEXT | Type of error if failed |
| error_message | TEXT | Full error message |
| circuit_breaker_state | TEXT | Circuit breaker state during request |
| chaos_active | BOOLEAN | Whether chaos was active |
| automated | BOOLEAN | Whether request was automated |

### circuit_breaker_events table
Tracks all circuit breaker state transitions.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| timestamp | DATETIME | When transition occurred |
| service | TEXT | Which service's circuit breaker |
| from_state | TEXT | Previous state |
| to_state | TEXT | New state |
| reason | TEXT | Why transition occurred |
| failure_count | INTEGER | Number of failures |
| success_count | INTEGER | Number of successes |

### chaos_experiments table
Records chaos engineering experiments.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| start_time | DATETIME | When experiment started |
| end_time | DATETIME | When experiment ended |
| chaos_type | TEXT | Type of chaos (latency/error/corruption) |
| intensity | REAL | Chaos intensity (0-100) |
| duration | INTEGER | Duration in seconds |
| affected_services | TEXT | JSON array of affected services |
| total_requests | INTEGER | Requests during experiment |
| failed_requests | INTEGER | Failed requests during experiment |
| notes | TEXT | Additional notes |

## API Endpoints

### Get Historical Requests
```
GET /api/history/requests?limit=100&service=gemini
```

### Get Statistics
```
GET /api/history/statistics?hours=24&service=gemini
```

### Get Error Patterns
```
GET /api/history/errors?hours=24
```

### Get Circuit Breaker History
```
GET /api/history/circuit-breaker?limit=50&service=gemini
```

### Get Chaos Experiments
```
GET /api/history/chaos?limit=20
```

### Get Performance Trends
```
GET /api/history/trends?hours=24&interval=30&service=gemini
```

### Export Data
```
GET /api/history/export?hours=24
```

### Database Statistics
```
GET /api/database/stats
```

## Data Retention

By default, data is kept indefinitely. To clean up old data:

```python
from database import get_datastore

db = get_datastore()
db.cleanup_old_data(days=30)  # Remove data older than 30 days
```

## Analysis Examples

### Find patterns in errors
```python
from database import get_datastore

db = get_datastore()
patterns = db.get_error_patterns(hours=24)
print(patterns)
# Output: {'TimeoutError': 15, 'APIKeyError': 3, 'NetworkError': 8}
```

### Get service performance
```python
stats = db.get_service_statistics(service='gemini', hours=24)
print(f"Success rate: {stats['success_rate']}%")
print(f"Average latency: {stats['avg_latency']}ms")
```

### Export for research
```python
db.export_to_json('data/research_export.json', hours=168)  # Last 7 days
```

## Backup

To backup your data:
1. Copy `monitoring.db` to a safe location
2. Or use the export feature to create JSON backups

## Notes

- Database is SQLite for simplicity and portability
- All timestamps are in UTC
- Database grows over time - use cleanup_old_data() periodically
- Indexes are created for common queries (timestamp, service, success)
