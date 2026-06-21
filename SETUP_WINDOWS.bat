@echo off
setlocal

title Creative Studio MCP Setup

echo.
echo ============================================
echo Creative Studio MCP
echo One-click Windows setup
echo ============================================
echo.

pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo Could not open the setup folder.
    echo Put this file inside the creative-studio-mcp folder and try again.
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
    echo Could not find requirements.txt.
    echo.
    echo Make sure this file is inside the creative-studio-mcp folder.
    echo If you downloaded a ZIP file, right-click it and choose Extract All first.
    echo.
    pause
    exit /b 1
)

:project_found
pushd "%PROJECT_DIR%" >nul 2>nul
if errorlevel 1 (
    echo Could not open the project folder.
    echo.
    pause
    exit /b 1
)

echo Project folder:
echo %CD%
echo.

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

echo Step 1 of 4: Creating local Python setup...
if not exist ".\.venv\Scripts\python.exe" (
    %PYTHON_CMD% -m venv ".venv"
    if errorlevel 1 (
        echo Could not create the local Python setup.
        echo.
        pause
        exit /b 1
    )
) else (
    echo Local Python setup already exists.
)

echo.
echo Step 2 of 4: Installing required files...
call ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 (
    echo Could not update pip.
    echo Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

call ".\.venv\Scripts\python.exe" -m pip install -r "requirements.txt"
if errorlevel 1 (
    echo Could not install project requirements.
    echo Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo Step 3 of 4: Checking the tool...
call ".\.venv\Scripts\python.exe" -c "import server"
if errorlevel 1 (
    echo The tool could not load.
    echo.
    pause
    exit /b 1
)

echo.
echo Step 4 of 4: Connecting Claude Desktop...
if exist ".\setup_claude.py" (
    call ".\.venv\Scripts\python.exe" ".\setup_claude.py"
    if errorlevel 1 (
        echo.
        echo Claude was not connected yet.
        echo Open Claude Desktop once, then double-click CONNECT_CLAUDE.bat.
        echo.
        pause
        exit /b 1
    )
) else (
    echo setup_claude.py is missing.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup complete
echo ============================================
echo.
echo Next:
echo 1. Fully quit Claude Desktop.
echo 2. Open Claude Desktop again.
echo 3. Start a new chat.
echo 4. Ask: Use the Creative Studio MCP tool to list our services.
echo.
pause
