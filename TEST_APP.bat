@echo off
setlocal

title Creative Studio MCP Test

echo.
echo ============================================
echo Creative Studio MCP
echo App test
echo ============================================
echo.

pushd "%~dp0" >nul 2>nul
if errorlevel 1 (
    echo Could not open the project folder.
    echo.
    pause
    exit /b 1
)

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
    pause
    exit /b 1
)

%PYTHON_CMD% -m py_compile business_tools.py local_app.py server.py
if errorlevel 1 (
    echo Test failed.
    echo.
    pause
    exit /b 1
)

%PYTHON_CMD% -c "from business_tools import list_services, calculate_payment, create_quote; assert 'Brand Identity Design' in list_services(); assert calculate_payment(5000)['upfront_payment'] == '$3,500'; assert 'John' in create_quote('John','Brand Identity Design',3000); print('Success. The local app tools work.')"
if errorlevel 1 (
    echo Test failed.
    echo.
    pause
    exit /b 1
)

echo.
echo Success. The app is ready.
echo.
pause
