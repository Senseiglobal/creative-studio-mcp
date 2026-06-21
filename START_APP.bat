@echo off
setlocal

title Creative Studio MCP App

echo.
echo ============================================
echo Creative Studio MCP
echo Local browser app
echo ============================================
echo.

pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo Could not open the project folder.
    echo.
    pause
    exit /b 1
)

set "PYTHON_CMD="
where py >nul 2>nul
if not errorlevel 1 (
    py -3 --version >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
    where python >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo Python is not installed or cannot be found.
    echo.
    echo Install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo During install, tick: Add Python to PATH
    echo.
    pause
    exit /b 1
)

if not exist "local_app.py" (
    echo local_app.py is missing.
    echo Make sure you extracted the full project ZIP.
    echo.
    pause
    exit /b 1
)

echo Starting the app...
echo.
%PYTHON_CMD% "local_app.py"
echo.
pause
