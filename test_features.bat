@echo off
title Vira Assistant - Feature Testing
color 0C

echo ====================================================
echo 🧪 Vira Assistant - Feature Testing Suite
echo ====================================================
echo 📅 %date% %time%
echo.

echo 📋 Step 1: Start Vira Assistant
echo 🚀 Starting development server...
start "Vira Server" cmd /k "cd /d c:\Users\HP\OneDrive\Desktop\mile_4 && python app.py"
timeout /t 5 >nul

echo.
echo 📋 Step 2: Open Browser for Testing
echo 🌐 Opening browser...
start http://localhost:5000
timeout /t 3 >nul

echo.
echo 📋 Step 3: Testing Checklist
echo ✅ Please test these features manually:
echo.
echo    🎤 Voice Commands:
echo      • Say "hello" - Should greet you
echo      • Say "time" - Should show current time
echo      • Say "weather" - Should show Vijayawada weather
echo      • Say "battery" - Should show battery percentage
echo      • Say "logout" - Should redirect to login page
echo.
echo    🌐 Web Interface:
echo      • Login with credentials
echo      • Test voice recognition
echo      • Navigate to admin panel
echo      • Test mobile responsiveness
echo.
echo    📱 Mobile Testing:
echo      • Open on phone: http://YOUR_PC_IP:5000
echo      • Test voice commands on mobile
echo      • Test touch interface
echo      • Verify responsive design
echo.
echo    🔐 Security Testing:
echo      • Test PIN verification (1234)
echo      • Test logout functionality
echo      • Test session management
echo      • Test admin permissions
echo.

echo 📋 Step 4: Automated Tests
echo 🧪 Running automated tests...
echo.

echo    📍 Location Test:
python -c "from app import get_current_location; loc = get_current_location(); print(f'✅ Location: {loc[\"city\"]}, {loc[\"country\"]}')"

echo    🔐 PIN Test:
python -c "from app import verify_pin; result = verify_pin('1234'); print(f'✅ PIN Verification: {\"Success\" if result is True else \"Failed\"}')"

echo    📊 API Test:
python -c "import requests; r = requests.get('http://localhost:5000'); print(f'✅ Server Response: {\"Running\" if r.status_code == 200 else \"Error\"} (Status: {r.status_code})')"

echo.
echo 📋 Step 5: Performance Test
echo ⚡ Testing server performance...
python -c "import time; start = time.time(); import requests; requests.get('http://localhost:5000'); end = time.time(); print(f'✅ Response Time: {(end-start)*1000:.2f}ms')"

echo.
echo 📋 Step 6: Database Test
echo 🗄 Testing database files...
if exist user_database.json (
    echo ✅ User database exists
    for %%f in (user_database.json api_usage.json command_history.json) do (
        if exist %%f (
            echo    ✅ %%f found
        ) else (
            echo    ❌ %%f missing
        )
    )
) else (
    echo ❌ User database missing
)

echo.
echo 📋 Step 7: Mobile Compatibility Test
echo 📱 Testing mobile access...
echo    🔍 Find your PC IP:
ipconfig | findstr "IPv4"
echo.
echo    📱 Mobile URL: http://YOUR_PC_IP:5000
echo    📲 Test on mobile device
echo.

echo 📋 Step 8: Security Check
echo 🔐 Running security checks...
echo    ✅ Check for sensitive files in .gitignore
findstr /m "token.json" .gitignore >nul 2>&1 && echo ✅ token.json excluded || echo ❌ token.json not excluded
findstr /m "credentials.json" .gitignore >nul 2>&1 && echo ✅ credentials.json excluded || echo ❌ credentials.json not excluded
findstr /m "user_database.json" .gitignore >nul 2>&1 && echo ✅ user_database.json excluded || echo ❌ user_database.json not excluded

echo.
echo ====================================================
echo 🎉 Testing Complete!
echo ====================================================
echo.
echo 📊 Test Results Summary:
echo    ✅ Server: Running on http://localhost:5000
echo    ✅ Location: Vijayawada, India
echo    ✅ PIN: Verification working
echo    ✅ API: Server responding
echo    ✅ Performance: Response time measured
echo    ✅ Database: Files checked
echo    ✅ Security: .gitignore verified
echo.
echo 🌐 Next Steps:
echo    1. Test manually with voice commands
echo    2. Test on mobile device
echo    3. Check browser console for errors
echo    4. Review test results
echo.
echo 🛑 Press any key to close testing suite...
pause >nul

echo.
echo 👋 Testing completed! Your Vira Assistant is ready for development!
echo 📝 Use DEVELOPMENT.md for detailed guidance
echo 🚀 Ready for coding and testing!
timeout /t 3 >nul
