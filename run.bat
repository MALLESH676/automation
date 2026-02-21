@echo off
setlocal

echo ==================================================
echo   Employee Lifecycle Automation System - Launcher
echo ==================================================

:: Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

:: Create virtual environment if missing
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate virtual environment
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Upgrade pip (optional but good practice)
python -m pip install --upgrade pip >nul 2>&1

:: Install dependencies
if exist "requirements.txt" (
    echo [INFO] Installing/Updating dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo [WARNING] requirements.txt not found! Skipping dependency install.
)

:: Set PYTHONPATH to current directory to ensure module imports work
set PYTHONPATH=%CD%

:: Run the Flask Application
echo.
echo [INFO] Starting Application...
echo [INFO] Access the UI at http://localhost:5000
echo.
python -m src.app.server

pause
