@echo off
REM Vira Assistant Deployment Script for Windows
REM Usage: deploy.bat [docker|streamlit|local|stop|status]

set DEPLOYMENT_TYPE=%1
if "%DEPLOYMENT_TYPE%"=="" set DEPLOYMENT_TYPE=docker

echo 🚀 Vira Assistant Deployment Script
echo ==================================
echo Deployment Type: %DEPLOYMENT_TYPE%
echo Project Directory: c:\Users\HP\OneDrive\Desktop\mile_4
echo.

REM Navigate to project directory
cd /d "c:\Users\HP\OneDrive\Desktop\mile_4"
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Could not navigate to project directory
    pause
    exit /b 1
)

echo 📁 Current directory: %CD%
echo.

if "%DEPLOYMENT_TYPE%"=="docker" (
    echo 🐳 Docker Deployment
    echo -------------------
    
    REM Check if Docker is running
    docker info >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Docker is not running. Please start Docker Desktop first.
        pause
        exit /b 1
    )
    
    echo ✅ Docker is running
    
    REM Build and start container
    echo 🔨 Building and starting container...
    docker-compose up -d --build
    
    REM Check if container is running
    docker ps | findstr "vira-assistant" >nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Container started successfully!
        echo 🌐 Access at: http://localhost:5000
        echo 📊 Container status:
        docker ps | findstr "vira-assistant"
    ) else (
        echo ❌ Container failed to start
        echo 📋 Logs:
        docker-compose logs vira-assistant
        pause
        exit /b 1
    )
    
) else if "%DEPLOYMENT_TYPE%"=="streamlit" (
    echo ☁️ Streamlit Deployment
    echo ---------------------
    
    REM Check if Streamlit is installed
    streamlit --version >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo 📦 Installing Streamlit...
        pip install streamlit
    )
    
    echo ✅ Streamlit is available
    
    REM Create Streamlit requirements if needed
    if not exist "requirements_streamlit.txt" (
        echo 📝 Creating Streamlit requirements...
        (
            echo streamlit==1.28.1
            echo psutil==5.9.5
            echo requests==2.31.0
            echo flask==2.3.3
            echo flask-socketio==5.3.6
            echo pyttsx3==2.90
            echo pywhatkit==5.4
            echo google-api-python-client==2.100.0
            echo google-auth-httplib2==0.1.1
            echo google-auth-oauthlib==1.0.0
        ) > requirements_streamlit.txt
    )
    
    echo 🚀 Starting Streamlit app...
    streamlit run streamlit_deploy.py --server.port 8501 --server.headless true
    
) else if "%DEPLOYMENT_TYPE%"=="local" (
    echo 💻 Local Deployment
    echo ------------------
    
    REM Check Python version
    python --version
    echo 🐍 Python version checked
    
    REM Install requirements
    echo 📦 Installing requirements...
    pip install -r requirements.txt
    
    echo 🚀 Starting local server...
    python app.py
    
) else if "%DEPLOYMENT_TYPE%"=="stop" (
    echo 🛑 Stop Services
    echo ---------------
    
    REM Stop Docker container
    docker ps | findstr "vira-assistant" >nul
    if %ERRORLEVEL% EQU 0 (
        echo 🛑 Stopping Docker container...
        docker-compose down
        echo ✅ Container stopped
    ) else (
        echo ℹ️ No running Docker container found
    )
    
    REM Kill any running Python processes
    echo 🛑 Stopping Python processes...
    taskkill /f /im python.exe 2>nul
    taskkill /f /im streamlit.exe 2>nul
    echo ✅ Processes stopped
    
) else if "%DEPLOYMENT_TYPE%"=="status" (
    echo 📊 Service Status
    echo ----------------
    
    REM Docker status
    echo 🐳 Docker Status:
    docker ps | findstr "vira-assistant" >nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Container is running
        docker ps | findstr "vira-assistant"
    ) else (
        echo ❌ Container is not running
    )
    
    echo.
    
    REM Port status
    echo 🌐 Port Status:
    netstat -an | findstr ":5000" >nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Port 5000 is in use
    ) else (
        echo ❌ Port 5000 is free
    )
    
    netstat -an | findstr ":8501" >nul
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Port 8501 is in use ^(Streamlit^)
    ) else (
        echo ❌ Port 8501 is free
    )
    
    echo.
    
    REM File status
    echo 📁 File Status:
    if exist "app.py" (
        echo ✅ app.py exists
    ) else (
        echo ❌ app.py missing
    )
    
    if exist "requirements.txt" (
        echo ✅ requirements.txt exists
    ) else (
        echo ❌ requirements.txt missing
    )
    
    if exist "Dockerfile" (
        echo ✅ Dockerfile exists
    ) else (
        echo ❌ Dockerfile missing
    )
    
    if exist "docker-compose.yml" (
        echo ✅ docker-compose.yml exists
    ) else (
        echo ❌ docker-compose.yml missing
    )
    
) else (
    echo ❌ Unknown deployment type: %DEPLOYMENT_TYPE%
    echo.
    echo Usage: deploy.bat [docker^|streamlit^|local^|stop^|status]
    echo.
    echo Options:
    echo   docker    - Deploy with Docker ^(recommended^)
    echo   streamlit - Deploy with Streamlit
    echo   local     - Deploy locally
    echo   stop      - Stop all services
    echo   status    - Show service status
    pause
    exit /b 1
)

echo.
echo ✅ Deployment completed!
echo 🌐 Access your Vira Assistant:
echo    Docker: http://localhost:5000
echo    Streamlit: http://localhost:8501
echo.
echo 📚 For more help, see DEPLOYMENT_GUIDE.md
pause
