# Logs Directory

This directory contains runtime logs from the AI Resilience Monitor system.

## Log Files

### `monitor.log`
- General monitoring logs
- Service health checks
- System events

### `frontend-monitor.log`
- Flask frontend server logs
- HTTP request logs
- Database operation logs

### `all-services-monitor.log`
- Combined logs from all services
- Useful for debugging multi-service issues

## Log Rotation

Logs are not automatically rotated. To clean old logs:

```bash
# Remove all logs
rm logs/*.log

# Or keep only recent logs
find logs -name "*.log" -mtime +7 -delete
```

## Viewing Logs

```bash
# Tail logs in real-time
tail -f logs/monitor.log

# Search logs
grep "ERROR" logs/*.log

# View last 100 lines
tail -n 100 logs/monitor.log
```

## Log Levels

- **INFO**: Normal operations
- **WARNING**: Potential issues
- **ERROR**: Errors that need attention
- **CRITICAL**: System failures

Logs are automatically created when services start.
