@echo off
title Vira Assistant - Git Setup with MIT License
color 0A

echo ====================================================
echo 🤖 Vira Assistant - Git Setup with MIT License
echo ====================================================
echo 📅 %date% %time%
echo.

REM Navigate to project directory
cd /d c:\Users\HP\OneDrive\Desktop\mile_4

REM Step 1: Initialize Git repository
echo 📋 Step 1: Initializing Git repository...
git init
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to initialize Git repository
    pause
    exit /b 1
)
echo ✅ Git repository initialized successfully

REM Step 2: Configure Git (if not configured)
echo 📋 Step 2: Checking Git configuration...
git config user.name >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Git user not configured. Please set your name:
    set /p GIT_NAME=Enter your name: 
    git config --global user.name "%GIT_NAME%"
)

git config user.email >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ Git email not configured. Please set your email:
    set /p GIT_EMAIL=Enter your email: 
    git config --global user.email "%GIT_EMAIL%"
)

echo ✅ Git configuration complete
echo    Name: 
git config user.name
echo    Email: 
git config user.email

REM Step 3: Add all files
echo 📋 Step 3: Adding files to Git...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to add files to Git
    pause
    exit /b 1
)
echo ✅ Files added to staging area

REM Step 4: Commit files
echo 📋 Step 4: Creating initial commit...
git commit -m "Initial commit - Vira Assistant with MIT License

Features:
- Voice commands with location-based processing
- WhatsApp and email integration with PIN security
- Weather information for Vijayawada, India
- Admin panel with API usage tracking
- Google OAuth authentication
- Mobile-responsive interface
- MIT License compliance

Technology Stack:
- Flask with SocketIO
- HTML5, TailwindCSS, JavaScript
- pyttsx3 for text-to-speech
- Gmail API and Weather API integration"
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to create initial commit
    pause
    exit /b 1
)
echo ✅ Initial commit created successfully

REM Step 5: GitHub repository instructions
echo 📋 Step 5: GitHub Repository Setup
echo ==================================
echo.
echo To complete the setup, follow these steps:
echo.
echo 1. 🌐 Go to GitHub: https://github.com
echo 2. ➕ Click 'New repository'
echo 3. 📝 Repository name: vira-assistant
echo 4. 📄 Description: Vira Voice Assistant - Location-based AI with WhatsApp, Email, Weather
echo 5. 🔓 Visibility: Public (or Private)
echo 6. ✅ Click 'Create repository'
echo.
echo 7. 📋 Copy the repository URL (HTTPS)
echo 8. 🔄 Run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/vira-assistant.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 9. 🎉 Your repository is now on GitHub!
echo.

REM Step 6: Show repository status
echo 📊 Repository Status:
echo ====================
echo 📁 Files committed:
git log --oneline -1
echo.
echo 📋 Files in repository:
git ls-files | more
echo.
echo 📄 License: MIT License
echo 📍 Location: Vijayawada, India
echo 🔐 Security: PIN protection enabled
echo 🌐 Mobile: Responsive design
echo.

echo ✅ Git setup completed successfully!
echo 🚀 Ready to push to GitHub!
echo.
echo 📝 Don't forget to:
echo    1. Create GitHub repository
echo    2. Add remote origin
echo    3. Push to main branch
echo.
echo 🎯 Your Vira Assistant is now MIT licensed and ready for sharing!
pause
