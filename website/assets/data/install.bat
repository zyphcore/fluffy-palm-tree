@echo off
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed.
    echo Redirecting to the Python installation page...
    start https://www.python.org/downloads/
    echo Please install Python, add it to PATH, and then rerun this script.
    pause
    exit /b
)

echo Python is installed. Checking version...
python --version

echo Checking if pip is installed...
pip --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Pip is not installed. Attempting to install pip...
    python -m ensurepip --upgrade
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to install pip. Please install pip manually.
        pause
        exit /b
    )
    echo Pip installed successfully.
)

if exist requirements.txt (
    echo Installing packages from requirements.txt...
    pip install -r requirements.txt
    if %ERRORLEVEL% EQU 0 (
        echo All packages installed successfully.
    ) else (
        echo Failed to install one or more packages. Check the error messages for details.
    )
) else (
    echo requirements.txt not found in the current directory.
    echo Please ensure the file exists and rerun this script.
)

echo Setup completed.
pause