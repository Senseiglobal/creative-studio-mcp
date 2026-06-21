@echo off
setlocal

title Creative Studio MCP Check

echo.
echo ============================================
echo Creative Studio MCP
echo Setup check
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
    echo Setup is not complete.
    echo Double-click SETUP_WINDOWS.bat first.
    echo.
    pause
    exit /b 1
)

echo Checking the tool...
call ".\.venv\Scripts\python.exe" -c "import server"
if errorlevel 1 (
    echo The tool could not load.
    echo Double-click SETUP_WINDOWS.bat again.
    echo.
    pause
    exit /b 1
)

echo.
echo Success. The tool is installed.
echo.
echo If Claude still cannot see it:
echo 1. Double-click CONNECT_CLAUDE.bat
echo 2. Fully quit Claude Desktop
echo 3. Open Claude Desktop again
echo.
pause
