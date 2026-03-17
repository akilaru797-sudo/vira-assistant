@echo off
title Vira Assistant - Dual Launcher
color 0A

echo ====================================================
echo 🤖 Vira Assistant - Dual Launcher
echo ====================================================
echo 📅 %date% %time%
echo.

echo 🔍 Checking dependencies...

REM Check Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)
echo ✅ Python is available

REM Check required packages
echo 📦 Checking Python packages...
pip show flask >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 📦 Installing Flask...
    pip install flask
)

pip show streamlit >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 📦 Installing Streamlit...
    pip install streamlit
)

echo ✅ Dependencies checked
echo.

echo 🚀 Starting both applications...
echo.

REM Start Flask Web App
echo 🌐 Starting Flask Web App...
start "Vira Web App" cmd /k "cd /d c:\Users\HP\OneDrive\Desktop\mile_4 && python app.py"
timeout /t 3 >nul

REM Start Streamlit Dashboard
echo 📊 Starting Streamlit Dashboard...
start "Streamlit Dashboard" cmd /k "cd /d c:\Users\HP\OneDrive\Desktop/mile_4 && streamlit run streamlit_deploy.py --server.port 8501"
timeout /t 5 >nul

echo.
echo ====================================================
echo 🌐 Both applications are running!
echo ====================================================
echo 📱 Flask Web App:   http://localhost:5000
echo 📊 Streamlit Dashboard: http://localhost:8501
echo.
echo 🔧 Features:
echo    • Flask Web App - Full Vira Assistant with voice commands
echo    • Streamlit Dashboard - Deployment controls and monitoring
echo    • Mobile Compatible - Both work on phones/tablets
echo.
echo ⚡ Quick Access:
echo    • Main Assistant: http://localhost:5000
echo    • Admin Panel: http://localhost:5000/admin
echo    • Deployment: http://localhost:8501
echo.
echo 🌐 Opening browsers...
timeout /t 2 >nul
start http://localhost:5000
start http://localhost:8501

echo.
echo ====================================================
echo ✅ Both applications started successfully!
echo ====================================================
echo 📱 Open your browsers to access both applications
echo 🛑 Close this window to stop both applications
echo ====================================================
echo.

REM Wait for user to close
echo Press any key to stop both applications...
pause >nul

echo.
echo 🛑 Stopping applications...

REM Kill processes
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1

echo ✅ Applications stopped
echo 👋 Goodbye!
timeout /t 2 >nul
