@echo off
REM Creative Studio MCP - One-Click Installation (Windows)
REM This script sets up everything needed to run the project

echo.
echo ============================================
echo Creative Studio MCP - Installation
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [1/4] Creating workspace...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Workspace created

echo.
echo [2/4] Activating workspace...
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Workspace activated

echo.
echo [3/4] Installing software...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)
echo ✓ Software installed

echo.
echo [4/4] Creating environment file...
if not exist .env (
    (
        echo # Creative Studio MCP Configuration
        echo # Get your OpenAI API Key from: https://platform.openai.com/api-keys
        echo OPENAI_API_KEY=your_api_key_here
        echo.
        echo # Server Configuration
        echo MCP_SERVER_NAME=creative-studio
        echo MCP_SERVER_PATH=%CD%
    ) > .env
    echo ✓ Environment file created (.env)
) else (
    echo ✓ Environment file already exists
)

echo.
echo ============================================
echo ✓ Installation Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Open .env file and add your OpenAI API Key
echo 2. Read QUICK_START.md for next steps
echo 3. Run: python server.py (to test)
echo.
pause
