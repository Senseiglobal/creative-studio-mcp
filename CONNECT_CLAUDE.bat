@echo off
setlocal

title Connect Creative Studio MCP to Claude

echo.
echo ============================================
echo Creative Studio MCP - Connect to Claude
echo ============================================
echo.

pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo Could not open the project folder.
    echo.
    echo Put CONNECT_CLAUDE.bat inside the creative-studio-mcp folder and try again.
    echo.
    pause
    exit /b 1
)

if not exist ".\.venv\Scripts\python.exe" (
    echo Setup is not complete yet.
    echo.
    echo Step 1: Double-click install.bat
    echo Step 2: Double-click CHECK_INSTALL.bat
    echo Step 3: Double-click CONNECT_CLAUDE.bat again
    echo.
    pause
    exit /b 1
)

if not exist ".\setup_claude.py" (
    echo setup_claude.py is missing.
    echo.
    echo Please make sure all project files are in this folder.
    echo.
    pause
    exit /b 1
)

call ".\.venv\Scripts\python.exe" ".\setup_claude.py"
if errorlevel 1 (
    echo.
    echo Claude connection could not be completed.
    echo.
    pause
    exit /b 1
)

echo.
echo Done.
echo.
pause
