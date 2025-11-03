# 🚀 How to Run the Backend Server

## Quick Answer

The **easiest way** to start the backend:

```powershell
cd backend
.\quickstart.bat
```

This script handles everything automatically!

---

## ⚠️ Important: Python Version Issue

**Your current Python 3.14 has compatibility issues** with AI/ML packages (ChromaDB, tiktoken, pydantic-core) that require Rust/C++ compilation.

### Solution: Install Python 3.11

1. **Download Python 3.11**: https://www.python.org/downloads/release/python-3119/
   - Choose "Windows installer (64-bit)"
   - ✅ Check "Add Python to PATH" during installation

2. **Verify installation**:
   ```powershell
   py -3.11 --version
   # Should show: Python 3.11.9
   ```

---

## Step-by-Step Setup (First Time)

### Option 1: Automated Setup (Recommended)

```powershell
cd C:\ASU_Project\project-specs\agentic-customer-project\backend

# Run the setup script
.\setup.bat

# Edit .env file with your OpenAI API key
notepad .env

# Ingest sample data
.\venv\Scripts\activate
python scripts\ingest_data.py

# Start the server
.\start-backend.bat
```

### Option 2: Manual Setup

```powershell
# 1. Navigate to backend directory
cd C:\ASU_Project\project-specs\agentic-customer-project\backend

# 2. Create virtual environment with Python 3.11
py -3.11 -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt

# 6. Setup environment variables
copy .env.example .env
notepad .env  # Add your OpenAI API key

# 7. Ingest sample data (first time only)
python scripts\ingest_data.py

# 8. Start the server
uvicorn app.main:app --reload --port 8000
```

---

## Starting the Server (After Setup)

Once setup is complete, just run:

```powershell
cd backend
.\start-backend.bat
```

Or manually:

```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

The server will start on: **http://localhost:8000**

---

## Verify It's Working

### 1. Check Health Endpoint

Open browser or use PowerShell:
```powershell
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-03T..."
}
```

### 2. View API Documentation

Open in browser: **http://localhost:8000/docs**

You'll see interactive Swagger UI with all endpoints.

### 3. Test Chat Endpoint

Using PowerShell:
```powershell
$body = @{
    message = "What are your refund policies?"
    session_id = "test123"
    customer_id = "customer1"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
```

Expected response:
```json
{
  "response": "Our refund policy...",
  "routed_to": "Policy Compliance Agent",
  "session_id": "test123",
  "timestamp": "..."
}
```

---

## Troubleshooting

### ❌ "Module not found" errors

**Solution**: Activate the virtual environment
```powershell
cd backend
.\venv\Scripts\activate
```

### ❌ "OpenAI API key not found"

**Solution**: Edit `.env` file
```powershell
notepad .env
# Add: OPENAI_API_KEY="sk-your-actual-key-here"
```

### ❌ "pip install" fails with compilation errors

**Solution**: You're using Python 3.14. Install Python 3.11 instead.

See [INSTALL.md](INSTALL.md) for detailed instructions.

### ❌ "Port 8000 already in use"

**Solution**: Use a different port
```powershell
uvicorn app.main:app --reload --port 8001
```

### ❌ ChromaDB errors

**Solution**: Delete and recreate the database
```powershell
Remove-Item -Recurse -Force chroma_db
python scripts\ingest_data.py
```

### ❌ Virtual environment activation fails

**Solution**: Fix PowerShell execution policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app (start here)
│   ├── config.py            # Environment configuration
│   ├── models.py            # API request/response models
│   ├── state.py             # LangGraph state definition
│   ├── agents/              # Agent implementations
│   │   ├── supervisor.py    # Routes queries to workers
│   │   ├── billing_agent.py # Handles billing questions
│   │   ├── technical_agent.py # Technical support
│   │   └── policy_agent.py  # Policy & compliance
│   ├── tools/               # Agent tools
│   └── utils/               # Utilities (session, vector store)
├── data/                    # Sample data
│   ├── policies/            # Static policy documents
│   ├── billing/             # Billing documents
│   └── technical/           # Technical docs
├── scripts/
│   └── ingest_data.py       # Load data into ChromaDB
├── chroma_db/               # Vector store (created by ingestion)
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── setup.bat                # Automated setup script
├── start-backend.bat        # Start server script
└── quickstart.bat           # All-in-one script
```

---

## API Endpoints

### POST /chat
Main endpoint for customer queries

**Request:**
```json
{
  "message": "How much is the pro plan?",
  "session_id": "optional-session-id",
  "customer_id": "customer123"
}
```

**Response:**
```json
{
  "response": "The Pro Plan is $29.99/month...",
  "routed_to": "Billing Support Agent",
  "session_id": "generated-or-provided-id",
  "timestamp": "2025-11-03T..."
}
```

### GET /health
Health check endpoint

### GET /sessions/count
Get active session count

### POST /sessions/cleanup
Force cleanup all sessions

---

## Environment Variables

Edit `.env` file:

```bash
# Required
OPENAI_API_KEY="sk-your-key-here"

# Optional (defaults shown)
FASTAPI_PORT=8000
LOG_LEVEL="INFO"
CHROMA_DB_PATH="./chroma_db"

# Model Configuration
SUPERVISOR_MODEL="openai:gpt-4o-mini"
BILLING_MODEL="openai:gpt-4o"
TECHNICAL_MODEL="openai:gpt-4o"
POLICY_MODEL="openai:gpt-4o-mini"
```

---

## Next Steps

1. ✅ **Setup backend** (you're here)
2. 📱 **Start frontend** (see `frontend/README.md`)
3. 🧪 **Test the integration** (both running together)

---

## Need Help?

- **Detailed setup instructions**: See [INSTALL.md](INSTALL.md)
- **Full documentation**: See [README.md](README.md)
- **Architecture details**: See `../multi-agent/12-customer-service-multi-agent.md`
- **Project overview**: See `../README.md`

---

## Summary

✅ **To start the backend server:**

```powershell
# First time:
cd backend
.\setup.bat
# Edit .env with your API key
python scripts\ingest_data.py
.\start-backend.bat

# Every time after:
cd backend
.\start-backend.bat
```

That's it! 🎉

