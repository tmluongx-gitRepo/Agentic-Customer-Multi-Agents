# Backend Installation Guide

## ⚠️ Important: Python Version

**This project requires Python 3.11** due to dependency compatibility issues with Python 3.14.

If you're using Python 3.14, please install Python 3.11 from: https://www.python.org/downloads/

---

## Installation Steps

### 1. Install Python 3.11 (if needed)

Download from: https://www.python.org/downloads/release/python-3119/
- Choose "Windows installer (64-bit)"
- During installation, check "Add Python to PATH"

### 2. Create Virtual Environment

```powershell
cd backend

# Use Python 3.11 explicitly
py -3.11 -m venv venv

# Or if Python 3.11 is your default
python -m venv venv
```

### 3. Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you get a PowerShell execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

This should install without compilation errors on Python 3.11.

### 5. Set Up Environment Variables

```powershell
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY="sk-your-actual-key-here"
```

### 6. Run Data Ingestion (First Time Only)

```powershell
python scripts\ingest_data.py
```

This loads mock data into the ChromaDB vector stores.

### 7. Start the Server

```powershell
uvicorn app.main:app --reload --port 8000
```

The backend will be available at: **http://localhost:8000**

---

## Verify Installation

Test the health endpoint:
```powershell
curl http://localhost:8000/health
```

You should see:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-..."
}
```

---

## Troubleshooting

### "Module not found" errors
Make sure you activated the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

### "OpenAI API key not found"
Check your `.env` file has:
```
OPENAI_API_KEY="sk-..."
```

### Port already in use
Change the port:
```powershell
uvicorn app.main:app --reload --port 8001
```

### ChromaDB errors
Delete and recreate the database:
```powershell
Remove-Item -Recurse -Force chroma_db
python scripts\ingest_data.py
```

---

## Quick Start (All-in-One)

```powershell
# Navigate to backend
cd C:\ASU_Project\project-specs\agentic-customer-project\backend

# Create and activate venv (Python 3.11)
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Ingest data
python scripts\ingest_data.py

# Start server
uvicorn app.main:app --reload --port 8000
```

---

## Alternative: Use Current Python 3.14 (Advanced)

If you must use Python 3.14, you'll need to install build tools:

1. **Install Visual Studio Build Tools**: https://visualstudio.microsoft.com/downloads/
   - Select "Desktop development with C++"
   - This is ~7GB download

2. **Install Rust**: https://rustup.rs/
   - Download and run `rustup-init.exe`
   - Restart your terminal

3. Then try `pip install -r requirements.txt` again

However, **Python 3.11 is strongly recommended** for AI/ML projects.

