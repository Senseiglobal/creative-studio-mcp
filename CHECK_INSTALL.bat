@echo off
setlocal

title Creative Studio MCP Check

echo.
echo ============================================
echo Creative Studio MCP - Setup Check
echo ============================================
echo.

pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo ERROR: Could not open the folder where CHECK_INSTALL.bat is located.
    echo.
    echo Put CHECK_INSTALL.bat inside the creative-studio-mcp folder and try again.
    echo.
    pause
    exit /b 1
)

set "PROJECT_DIR="

if exist "requirements.txt" (
    set "PROJECT_DIR=."
    goto project_found
)

if exist "..\requirements.txt" (
    set "PROJECT_DIR=.."
    goto project_found
)

for /d %%D in (*) do (
    if not defined PROJECT_DIR (
        if exist "%%D\requirements.txt" (
            set "PROJECT_DIR=%%D"
        )
    )
)

if not defined PROJECT_DIR (
    echo ERROR: Could not find the project folder.
    echo.
    echo Open the creative-studio-mcp folder and double-click CHECK_INSTALL.bat from there.
    echo.
    pause
    exit /b 1
)

:project_found
pushd "%PROJECT_DIR%" >nul 2>nul
if errorlevel 1 (
    echo ERROR: Could not open the project folder.
    echo.
    pause
    exit /b 1
)

echo Project folder:
echo %CD%
echo.

if not exist ".venv\Scripts\python.exe" (
    echo Setup is not complete yet.
    echo.
    echo Please double-click install.bat first.
    echo.
    pause
    exit /b 1
)

echo Checking the tool...
".venv\Scripts\python.exe" -c "import server"
if errorlevel 1 (
    echo.
    echo The setup check failed.
    echo.
    echo Please run install.bat again. If the error continues, ask for help in GitHub Discussions.
    echo.
    pause
    exit /b 1
)

echo.
echo Success. Creative Studio MCP is installed correctly.
echo.
echo Next:
echo 1. Open QUICK_START.md
echo 2. Follow the connection steps for Claude Desktop
echo 3. Start asking for quotes, payment breakdowns, and checklists
echo.
pause
