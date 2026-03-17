@echo off
title Vira AI Voice Portal
echo Starting Vira AI...

:: Run the Python script first
python app.py

:: Wait for server to start, then open browser
timeout /t 3 >nul
start http://127.0.0.1:5000

pause