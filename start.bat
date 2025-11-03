@echo off
REM Start script for Advanced Customer Service AI (Windows)
REM This script starts both backend and frontend servers

echo ==================================================
echo Advanced Customer Service AI - Startup Script
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.10+ from https://www.python.org/
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed
    echo Please install Node.js 18+ from https://nodejs.org/
    exit /b 1
)

echo ✓ Python found
python --version
echo ✓ Node.js found
node --version
echo.

echo ==================================================
echo Starting Backend Server...
echo ==================================================
cd backend

REM Check if virtual environment exists
if not exist "venv\" (
    echo Error: Virtual environment not found
    echo Please run setup first:
    echo   cd backend
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

REM Check if .env exists
if not exist ".env" (
    echo Error: .env file not found
    echo Please copy .env.example to .env and add your OPENAI_API_KEY
    exit /b 1
)

echo ✓ Environment configured
echo.
echo Starting backend server...
start /B uvicorn app.main:app --reload
echo ✓ Backend started
echo   URL: http://localhost:8000
echo.

REM Wait for backend to be ready
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul
echo ✓ Backend should be ready!

cd ..

echo.
echo ==================================================
echo Starting Frontend Server...
echo ==================================================
cd frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Error: node_modules not found
    echo Please run: npm install
    exit /b 1
)

echo ✓ Dependencies installed
echo.
echo Starting frontend server...
start /B npm run dev
echo ✓ Frontend started
echo   URL: http://localhost:3000
echo.

echo ==================================================
echo ✅ All servers started successfully!
echo ==================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo To stop the servers, close this window or press Ctrl+C
echo.
echo Opening frontend in browser...
timeout /t 3 /nobreak >nul
start http://localhost:3000

pause

