@echo off
setlocal

title Creative Studio MCP Installer

echo.
echo ============================================
echo Creative Studio MCP - Windows Installer
echo ============================================
echo.
echo This installer will:
echo 1. Set up the project
echo 2. Check that it works
echo 3. Show you what to do next
echo.

echo [Setup] Finding the project folder...
pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo ERROR: Could not open the folder where install.bat is located.
    echo.
    echo Move install.bat into the creative-studio-mcp folder and try again.
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

if defined PROJECT_DIR goto project_found

echo ERROR: requirements.txt was not found.
echo.
echo The installer looked in:
echo - The folder where install.bat is located
echo - One folder above install.bat
echo - One folder below install.bat
echo.
echo Please place install.bat inside the creative-studio-mcp project folder.
echo That folder should contain files like:
echo - requirements.txt
echo - server.py
echo - README.md
echo.
popd >nul 2>nul
pause
exit /b 1

:project_found
pushd "%PROJECT_DIR%" >nul 2>nul
if errorlevel 1 (
    echo ERROR: The project folder was found, but could not be opened.
    echo.
    echo Move install.bat into the creative-studio-mcp folder and try again.
    echo.
    popd >nul 2>nul
    pause
    exit /b 1
)

echo Project folder:
echo %CD%
echo.

if not exist "requirements.txt" (
    echo ERROR: requirements.txt is missing from the selected project folder.
    echo.
    echo The installer must be run from the creative-studio-mcp project folder.
    echo.
    popd >nul 2>nul
    popd >nul 2>nul
    pause
    exit /b 1
)

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

echo [1/3] Setting up the project...
echo Creating the project workspace...
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

echo Checking the project Python...
if not exist .venv\Scripts\python.exe (
    echo ERROR: Local Python was not created.
    echo.
    pause
    exit /b 1
)
echo Done.
echo.

echo Installing the required files...
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

echo Creating the settings file...
if not exist .env (
    copy .env.example .env >nul 2>nul
    if errorlevel 1 (
        (
            echo OPENAI_API_KEY=your_api_key_here
            echo MCP_SERVER_NAME=creative-studio
            echo MCP_SERVER_PATH=server.py
        ) > .env
    )
    echo Created .env.
) else (
    echo .env already exists.
)
echo.

echo [2/3] Checking that everything works...
.venv\Scripts\python.exe -c "import server"
if errorlevel 1 (
    echo ERROR: The tool could not be checked.
    echo Please check the error above.
    echo.
    pause
    exit /b 1
)
echo Setup check passed.
echo.

echo ============================================
echo Installation complete
echo ============================================
echo.
echo [3/3] What to do next
echo.
echo Step 1:
echo Double-click CHECK_INSTALL.bat any time you want to confirm the setup.
echo.
echo Step 2:
echo Open QUICK_START.md for the short connection steps.
echo.
echo Step 3:
echo Connect the tool to Claude Desktop or your AI assistant.
echo.
echo Important:
echo Do not open or run Activate.ps1. It is not needed.
echo.
if exist START_HERE.html (
    echo Opening the visual start page now...
    start "" "START_HERE.html"
    echo.
)
pause
