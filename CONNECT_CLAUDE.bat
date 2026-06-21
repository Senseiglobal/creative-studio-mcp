@echo off
setlocal

title Connect Creative Studio MCP to Claude

echo.
echo ============================================
echo Creative Studio MCP
echo Connect Claude Desktop
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
    echo Double-click SETUP_WINDOWS.bat first.
    echo.
    pause
    exit /b 1
)

call ".\.venv\Scripts\python.exe" ".\setup_claude.py"
if errorlevel 1 (
    echo.
    echo Claude connection did not finish.
    echo.
    pause
    exit /b 1
)

echo.
echo Done.
echo Fully quit Claude Desktop, then open it again.
echo.
pause
