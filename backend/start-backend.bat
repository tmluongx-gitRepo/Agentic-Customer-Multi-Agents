@echo off
echo ============================================================
echo Advanced Customer Service AI - Backend Startup
echo ============================================================
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please copy .env.example to .env and add your OpenAI API key.
    echo.
    echo Run: copy .env.example .env
    echo Then edit .env with your API key.
    pause
    exit /b 1
)

REM Check if venv exists
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup first:
    echo   1. py -3.11 -m venv venv
    echo   2. venv\Scripts\activate
    echo   3. pip install -r requirements.txt
    echo   4. python scripts\ingest_data.py
    echo.
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Checking if data is ingested...
if not exist chroma_db\billing (
    echo.
    echo [WARNING] ChromaDB not found. Running data ingestion...
    python scripts\ingest_data.py
    echo.
)

echo [3/3] Starting FastAPI server...
echo.
echo Server will start on: http://localhost:8000
echo API docs available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --reload --port 8000

