@echo off
setlocal

title Creative Studio MCP Start

echo.
echo ============================================
echo Creative Studio MCP
echo ============================================
echo.
echo This will open the simple start page.
echo.
echo If you downloaded a ZIP file, make sure you extracted it first.
echo.

pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo ERROR: Could not open this folder.
    echo.
    echo Put START_WINDOWS.bat inside the creative-studio-mcp folder and try again.
    echo.
    pause
    exit /b 1
)

if not exist "START_HERE.html" (
    echo ERROR: START_HERE.html was not found.
    echo.
    echo Please open the extracted creative-studio-mcp folder and try again.
    echo.
    pause
    exit /b 1
)

start "" "START_HERE.html"

echo The start page is open in your browser.
echo.
echo Follow the 3 steps there:
echo 1. Install
echo 2. Check
echo 3. Connect
echo.
pause
