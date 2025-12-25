@echo off
title System Monitor
echo Starting System Monitor Tool...
py system_monitor.py
if errorlevel 1 (
    echo.
    echo Failed to start, please check if Python environment is properly installed.
    pause
)