@echo off
title Vira Assistant - Development Setup
color 0B

echo ====================================================
echo 🛠️ Vira Assistant - Development Environment
echo ====================================================
echo 📅 %date% %time%
echo.

echo 📋 Step 1: Navigate to project directory
cd /d c:\Users\HP\OneDrive\Desktop\mile_4
echo ✅ Current directory: %CD%

echo.
echo 📋 Step 2: Check Python installation
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)
echo ✅ Python is available

echo.
echo 📋 Step 3: Install/Update dependencies
echo 📦 Installing requirements...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)
echo ✅ Dependencies installed

echo.
echo 📋 Step 4: Install development tools
echo 📦 Installing development dependencies...
pip install pytest black flake8 autopep8
echo ✅ Development tools installed

echo.
echo 📋 Step 5: Create development environment
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.
echo 📋 Step 6: Activate virtual environment
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

echo.
echo 📋 Step 7: Start development server
echo 🚀 Starting Vira Assistant in development mode...
echo 🌐 Server will run on: http://localhost:5000
echo 📱 Mobile access: http://YOUR_PC_IP:5000
echo.
echo 🛑 Press Ctrl+C to stop the server
echo.

python app.py

echo.
echo 👋 Development server stopped
echo 📝 Changes made will be ready for git commit
pause
