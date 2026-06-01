@echo off
REM PokerWin v2 - Windows Quick Launch Script
REM Usage: Double-click this file to start the web interface

echo ==========================================
echo   PokerWin v2 - Texas Hold'em Equity
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not detected. Please install Python 3.7+
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies (flask, flask-cors)...
    pip install flask flask-cors
    if %errorlevel% neq 0 (
        echo [ERROR] Dependency installation failed
        echo Please run manually: pip install flask flask-cors
        pause
        exit /b 1
    )
)

echo [2/3] Starting server...
echo.
echo ==========================================
echo  Server started successfully!
echo  Web URL: http://127.0.0.1:15000
echo ==========================================
echo.
echo [TIP] Press Ctrl+C to stop the server
echo.

REM Open browser (delay 2 seconds for server startup)
start /b timeout /t 2 /nobreak >nul 2>&1 && start http://127.0.0.1:15000

REM Start Flask server
python server.py

pause
