#!/bin/bash

# Start script for Advanced Customer Service AI
# This script starts both backend and frontend servers

echo "=================================================="
echo "Advanced Customer Service AI - Startup Script"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Error: Python is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

echo "✓ Python found: $(python3 --version 2>/dev/null || python --version)"
echo "✓ Node.js found: $(node --version)"
echo ""

# Start backend
echo "=================================================="
echo "Starting Backend Server..."
echo "=================================================="
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found"
    echo "Please run setup first:"
    echo "  cd backend"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment and start backend
source venv/bin/activate
echo "✓ Virtual environment activated"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found"
    echo "Please copy .env.example to .env and add your OPENAI_API_KEY"
    exit 1
fi

echo "✓ Environment configured"
echo ""
echo "Starting backend server..."
uvicorn app.main:app --reload &
BACKEND_PID=$!
echo "✓ Backend started (PID: $BACKEND_PID)"
echo "  URL: http://localhost:8000"
echo ""

# Wait for backend to be ready
echo "Waiting for backend to start..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ Backend is ready!"
        break
    fi
    sleep 1
    if [ $i -eq 30 ]; then
        echo "❌ Backend failed to start within 30 seconds"
        kill $BACKEND_PID
        exit 1
    fi
done

cd ..

# Start frontend
echo ""
echo "=================================================="
echo "Starting Frontend Server..."
echo "=================================================="
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules not found"
    echo "Please run: npm install"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""
echo "Starting frontend server..."
npm run dev &
FRONTEND_PID=$!
echo "✓ Frontend started (PID: $FRONTEND_PID)"
echo "  URL: http://localhost:3000"
echo ""

echo "=================================================="
echo "✅ All servers started successfully!"
echo "=================================================="
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "To stop the servers, press Ctrl+C"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

