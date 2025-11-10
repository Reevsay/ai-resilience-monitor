@echo off
title Backend Monitor - Enhanced Auto-Recovery
color 0B

echo ========================================
echo  Backend Monitor - Enhanced Version
echo ========================================
echo.
echo Starting monitoring with auto-recovery...
echo.

REM Run PowerShell script
powershell -ExecutionPolicy Bypass -File "%~dp0start-monitor-enhanced.ps1"

pause
