@echo off
echo ============================================================
echo Advanced Customer Service AI - Backend Setup
echo ============================================================
echo.

REM Check Python 3.11
echo [1/6] Checking Python version...
py -3.11 --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.11 not found!
    echo.
    echo Please install Python 3.11 from:
    echo https://www.python.org/downloads/release/python-3119/
    echo.
    echo Make sure to:
    echo   - Choose "Windows installer (64-bit)"
    echo   - Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
py -3.11 --version

REM Create virtual environment
echo.
echo [2/6] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)
py -3.11 -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)

REM Activate virtual environment
echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment!
    pause
    exit /b 1
)

REM Upgrade pip
echo.
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo [5/6] Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies!
    echo.
    echo If you see compilation errors, you need Python 3.11 (not 3.14).
    echo See INSTALL.md for detailed troubleshooting.
    pause
    exit /b 1
)

REM Setup environment file
echo.
echo [6/6] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo.
    echo ============================================================
    echo IMPORTANT: Edit .env file and add your OpenAI API key!
    echo ============================================================
    echo.
    echo 1. Open .env file
    echo 2. Replace "your_openai_api_key_here" with your actual key
    echo 3. Save the file
    echo.
    echo Get your API key from: https://platform.openai.com/api-keys
    echo.
) else (
    echo .env file already exists. Skipping...
)

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Edit .env file with your OpenAI API key (if not done)
echo   2. Run: python scripts\ingest_data.py  (ingest sample data)
echo   3. Run: start-backend.bat  (start the server)
echo.
echo Or use the quick start script: quickstart.bat
echo.
pause

