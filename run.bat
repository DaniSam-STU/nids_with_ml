@echo off
echo ========================================
echo 🚀 NIDS Project - One Click Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Run the launcher
echo Starting setup...
python launch.py

REM If launcher exits, pause so user can see any errors
pause