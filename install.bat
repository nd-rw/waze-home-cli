@echo off
echo === Waze Home CLI Installer ===
echo This script will install the Waze Home CLI tool.

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found. Please install Python 3.10 or higher.
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%I in ('python -c "import sys; print(sys.version.split()[0])"') do set PYTHON_VERSION=%%I
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

if %PYTHON_MAJOR% LSS 3 (
    echo Error: Python 3.10 or higher is required. Found Python %PYTHON_VERSION%
    exit /b 1
)

if %PYTHON_MAJOR% EQU 3 (
    if %PYTHON_MINOR% LSS 10 (
        echo Error: Python 3.10 or higher is required. Found Python %PYTHON_VERSION%
        exit /b 1
    )
)

echo Found Python %PYTHON_VERSION%

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install the package
echo Installing Waze Home CLI...
pip install -e .

REM Verify installation
echo Verifying installation...
where waze-home >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Installation successful!
    echo.
    echo You can now use the 'waze-home' command while the virtual environment is active.
    echo To activate the virtual environment in the future, run:
    echo   venv\Scripts\activate.bat
    echo.
    echo Try running 'waze-home --help' to see available commands.
) else (
    echo Installation failed. The 'waze-home' command was not found.
    exit /b 1
) 