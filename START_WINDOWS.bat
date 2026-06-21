@echo off
setlocal

title Creative Studio MCP Start

pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo Could not open the project folder.
    pause
    exit /b 1
)

if exist "START_HERE.html" (
    start "" "START_HERE.html"
)

echo.
echo Main app:
echo START_APP.bat
echo.
pause
