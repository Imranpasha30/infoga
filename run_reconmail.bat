@echo off
title ReconMail OSINT Dashboard
cd /d "%~dp0"
echo ==========================================================
echo   Launching ReconMail OSINT Dashboard...
echo   Target Port: 5050 ^| UI: http://localhost:5050
echo ==========================================================
start http://localhost:5050
py app.py
pause
