@echo off
setlocal

title Creative Studio MCP Installer

echo.
echo ============================================
echo Creative Studio MCP - Windows Installer
echo ============================================
echo.
echo This installer will:
echo 1. Check Python
echo 2. Create a local workspace
echo 3. Install required software
echo 4. Create your .env file
echo 5. Test the server file
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo.
    echo Install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo During installation, check "Add Python to PATH".
    echo Then close this window and run install.bat again.
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

if not exist requirements.txt (
    echo ERROR: requirements.txt was not found.
    echo Make sure install.bat is inside the creative-studio-mcp folder.
    echo.
    pause
    exit /b 1
)

echo [1/5] Creating local workspace...
if not exist .venv (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create the local workspace.
        echo Try reinstalling Python and make sure the venv feature is available.
        echo.
        pause
        exit /b 1
    )
) else (
    echo Local workspace already exists.
)
echo Done.
echo.

echo [2/5] Checking local Python...
if not exist .venv\Scripts\python.exe (
    echo ERROR: Local Python was not created.
    echo.
    pause
    exit /b 1
)
echo Done.
echo.

echo [3/5] Installing required software...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Could not install required software.
    echo Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)
echo Done.
echo.

echo [4/5] Creating environment file...
if not exist .env (
    copy .env.example .env >nul 2>nul
    if errorlevel 1 (
        (
            echo OPENAI_API_KEY=your_api_key_here
            echo MCP_SERVER_NAME=creative-studio
            echo MCP_SERVER_PATH=%CD%
        ) > .env
    )
    echo Created .env.
) else (
    echo .env already exists.
)
echo.

echo [5/5] Testing server startup...
.venv\Scripts\python.exe -m py_compile server.py
if errorlevel 1 (
    echo ERROR: server.py has a syntax problem.
    echo Please check the error above.
    echo.
    pause
    exit /b 1
)
echo Server file looks good.
echo.

echo ============================================
echo Installation complete
echo ============================================
echo.
echo Next steps:
echo 1. Open .env and add your API key if you plan to use API features.
echo 2. Run this command to test the server:
echo    .venv\Scripts\python.exe server.py
echo 3. Read QUICK_START.md for Claude or ChatGPT setup.
echo.
echo Note:
echo You do not need to run .venv\Scripts\Activate.ps1.
echo This avoids Windows PowerShell execution policy errors.
echo.
pause
