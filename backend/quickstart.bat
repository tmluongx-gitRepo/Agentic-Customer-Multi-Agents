@echo off
echo ============================================================
echo Advanced Customer Service AI - Quick Start
echo ============================================================
echo.

REM Run setup if venv doesn't exist
if not exist venv (
    echo Running setup...
    call setup.bat
    if errorlevel 1 exit /b 1
    echo.
)

REM Check .env
if not exist .env (
    echo [ERROR] Please edit .env file with your OpenAI API key first!
    echo.
    echo 1. Open .env file
    echo 2. Add your OpenAI API key
    echo 3. Run this script again
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Ingest data if not done
if not exist chroma_db\billing (
    echo.
    echo Running data ingestion...
    python scripts\ingest_data.py
    if errorlevel 1 (
        echo [ERROR] Data ingestion failed!
        pause
        exit /b 1
    )
)

echo.
echo ============================================================
echo Starting Backend Server
echo ============================================================
echo.
echo Server: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

uvicorn app.main:app --reload --port 8000

