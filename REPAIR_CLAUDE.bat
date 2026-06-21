@echo off
setlocal

title Repair Creative Studio MCP for Claude

echo.
echo ============================================
echo Creative Studio MCP - Claude Repair
echo ============================================
echo.

pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo Could not open the project folder.
    echo.
    pause
    exit /b 1
)

if not exist ".\.venv\Scripts\python.exe" (
    echo Setup is not complete yet.
    echo.
    echo Double-click install.bat first.
    echo.
    pause
    exit /b 1
)

call ".\.venv\Scripts\python.exe" ".\repair_claude.py"
if errorlevel 1 (
    echo.
    echo Repair did not finish.
    echo.
    pause
    exit /b 1
)

echo.
echo Done.
echo.
pause
