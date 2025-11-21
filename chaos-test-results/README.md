# Chaos Test Results

This directory contains the output of chaos engineering tests performed on the AI Resilience Monitor system.

## File Types

### Test Reports (*.txt)
- Final summary reports of chaos test runs
- Include resilience scores and circuit breaker behavior
- Generated after each test completion

### Request Logs (*.csv)
- Detailed logs of every request during testing
- Columns: timestamp, service, success, latency, error_type
- Used for detailed analysis

### Experiment Logs (*.csv)
- Chaos experiment execution details
- Tracks which experiments were run and when
- Includes experiment parameters and outcomes

### Service Comparisons (*.csv)
- Comparative analysis of service performance
- Shows success rates, latencies, and failure patterns
- Useful for provider selection decisions

## Sample Files

- `sample_chaos_test_report.txt` - Example test report format

## Running Tests

```bash
# Run validation test (quick)
python scripts/testing/chaos-test.py --validation

# Run full test (2 hours)
python scripts/testing/chaos-test.py --duration 120

# Run with custom output directory
python scripts/testing/chaos-test.py --output-dir custom-results
```

## Cleanup

Old test results can be safely deleted:
```bash
rm chaos-test-results/*.log
rm chaos-test-results/*.csv
rm chaos-test-results/*.txt
```

Keep only the most recent results for reference.
