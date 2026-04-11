@echo off
title Vira Assistant - Railway Deployment
color 0A

echo 🚂 Vira Assistant - Railway Deployment
echo =======================================

REM Check if Node.js is installed
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js not found. Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Railway CLI not found. Installing...
    npm install -g @railway/cli
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to install Railway CLI
        pause
        exit /b 1
    )
)

echo ✅ Railway CLI is installed

REM Check if user is logged in
railway whoami >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 🔐 Please login to Railway...
    railway login
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ Failed to login to Railway
        pause
        exit /b 1
    )
)

echo ✅ Logged in to Railway

REM Deploy to Railway
echo 🚀 Deploying to Railway...
railway up
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to deploy to Railway
    pause
    exit /b 1
)

echo ⏳ Waiting for deployment...
timeout /t 10 >nul

echo.
echo 🎉 Deployment completed successfully!
echo =======================================
echo 🌐 Your app is being deployed...
echo 👤 Login: admin / admin123
echo 📊 Admin Panel: Available at your app URL /admin
echo 📱 Mobile: Works on all devices
echo.
echo 💡 Next steps:
echo 1. Wait for deployment to complete (2-3 minutes)
echo 2. Railway will show your app URL
echo 3. Visit your app URL
echo 4. Login with admin / admin123
echo 5. Change the default password
echo 6. Test all features
echo.
echo 🔧 To view logs: railway logs
echo 🔧 To open app: railway open
echo.
echo 🌐 Opening Railway dashboard...
railway open

pause
