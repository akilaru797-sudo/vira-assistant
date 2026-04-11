@echo off
title Vira AI Voice Portal
color 0A

echo ====================================================
echo 🤖 Vira AI Voice Portal - Starting
echo ====================================================
echo 📅 %date% %time%
echo.

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python first.
    echo 📦 Download from: https://python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python is available

echo.
echo 📦 Checking dependencies...
pip show flask >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 📦 Installing Flask...
    pip install flask
)

pip show flask-socketio >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 📦 Installing Flask-SocketIO...
    pip install flask-socketio
)

echo ✅ Dependencies checked
echo.

echo 🚀 Starting Vira AI Server...
echo 📍 Location: c:\Users\HP\OneDrive\Desktop\mile_4
echo 🌐 URL: http://localhost:5000
echo.

REM Start the server in background
start "Vira Server" cmd /k "cd /d c:\Users\HP\OneDrive\Desktop\mile_4 && python app.py"

REM Wait for server to start
echo ⏳ Waiting for server to start...
timeout /t 5 >nul

REM Check if server is running
curl -s http://localhost:5000/test >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Server is running successfully!
) else (
    echo ⚠️ Server might still be starting...
)

echo.
echo 🌐 Opening browser...
start http://localhost:5000

echo.
echo ====================================================
echo ✅ Vira AI is running!
echo ====================================================
echo 🌐 Web Interface: http://localhost:5000
echo 👤 Login: Use your credentials
echo 🎤 Voice Commands: Click microphone button
echo 📱 Mobile: Access from your phone too
echo.
echo 🛑 To stop: Close the server window
echo ====================================================
echo.
echo 💡 Tips:
echo    • Allow microphone access when prompted
echo    • Speak clearly for voice commands
echo    • Use "hello", "time", "weather", "whatsapp"
echo    • Admin access: http://localhost:5000/admin
echo.

REM Keep this window open for user to read
echo Press any key to exit this launcher (server will keep running)...
pause >nul

echo.
echo 👋 Launcher closed. Server is still running in background.
echo 🛑 To stop server, close the "Vira Server" window.
timeout /t 3 >nul
