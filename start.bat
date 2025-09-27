@echo off
echo 🚀 AI Resilience Monitor Startup Script
echo =====================================

echo Installing Node.js dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo Installing Python dependencies...
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!
echo.
echo Starting services...
echo ==================

echo Starting Node.js backend server...
start "AI Monitor Backend" cmd /k "node src/index.js"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo Starting Python dashboard...
start "AI Monitor Dashboard" cmd /k "python app.py"

echo.
echo ✅ Both services are starting!
echo.
echo 📊 Dashboard: http://localhost:8080
echo 🔧 Backend API: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul