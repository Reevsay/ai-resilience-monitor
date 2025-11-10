# Scripts

This folder contains all operational scripts for the project.

## Structure

### `monitoring/`
Auto-recovery and monitoring scripts that keep services running:
- `monitor-backend-enhanced.py` - Backend auto-restart monitor
- `monitor-frontend-continuous.py` - Frontend crash monitor

### `testing/`
Chaos engineering and validation scripts:
- `chaos-test.py` - Comprehensive chaos testing engine

### `setup/`
Startup and initialization scripts:
- `START_MONITOR_ENHANCED.bat` - Windows batch startup
- `start-monitor-enhanced.ps1` - PowerShell startup script

### `utilities/`
Maintenance and utility scripts:
- `cleanup-project.py` - Project cleanup script
- `reorganize-project.py` - Project reorganization script

## Usage

Start the monitoring system:
```bash
# Windows (Batch)
START_MONITOR_ENHANCED.bat

# Windows (PowerShell)
.\start-monitor-enhanced.ps1
```

Run chaos testing:
```bash
python chaos-test.py
```
