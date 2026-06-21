@echo off
setlocal

title Creative Studio MCP Security Check

echo.
echo ============================================
echo Creative Studio MCP
echo Security check
echo ============================================
echo.

pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo Could not open the project folder.
    echo.
    pause
    exit /b 1
)

echo Project folder:
echo %CD%
echo.

echo Checking important files...

set "FAILED=0"

for %%F in (START_APP.bat local_app.py business_tools.py server.py README.md) do (
    if not exist "%%F" (
        echo Missing: %%F
        set "FAILED=1"
    ) else (
        echo Found: %%F
    )
)

echo.
echo Checking for private local files...

if exist ".env" (
    echo Private file found: .env
    echo Do not share this file.
) else (
    echo No .env file found.
)

if exist "brand_profile.json" (
    echo Private file found: brand_profile.json
    echo Do not upload screenshots or copies if it contains business details.
)

if exist "projects.json" (
    echo Private file found: projects.json
    echo Do not upload screenshots or copies if it contains client details.
)

echo.
echo Checking for risky install behavior...

findstr /S /I /M "Invoke-WebRequest curl.exe bitsadmin certutil -decode Remove-Item -Recurse Set-ExecutionPolicy -Scope LocalMachine Start-Process -Verb RunAs" *.bat *.py > "%TEMP%\creative_studio_security_findings.txt" 2>nul

for %%A in ("%TEMP%\creative_studio_security_findings.txt") do set "SIZE=%%~zA"

if "%SIZE%"=="0" (
    echo No common risky command patterns found.
) else (
    echo Review these files before running:
    type "%TEMP%\creative_studio_security_findings.txt"
)

del "%TEMP%\creative_studio_security_findings.txt" >nul 2>nul

echo.
echo Creating file fingerprints...
echo This helps advanced users compare files after download.
echo.

if exist "checksums.txt" del "checksums.txt"

for %%F in (START_APP.bat TEST_APP.bat SETUP_WINDOWS.bat CONNECT_CLAUDE.bat local_app.py business_tools.py server.py README.md SECURITY.md) do (
    if exist "%%F" (
        certutil -hashfile "%%F" SHA256 | findstr /V /I "hash CertUtil" >> "checksums.txt"
        echo %%F >> "checksums.txt"
        echo. >> "checksums.txt"
    )
)

echo Saved: checksums.txt

echo.
if "%FAILED%"=="1" (
    echo Security check finished, but important files are missing.
    echo Download a fresh copy from the official GitHub repository.
    echo.
    pause
    exit /b 1
)

echo Security check finished.
echo If you downloaded this from the official GitHub repo, you can now run START_APP.bat.
echo.
pause
