# Quick Start Guide - Advanced Customer Service AI

Complete integration guide for running the full-stack application with FastAPI backend and Next.js frontend.

## Prerequisites

- Python 3.10+ installed
- Node.js 18+ and npm installed
- OpenAI API key
- Git

## Project Structure

```
agentic-customer-project/
├── backend/           # FastAPI multi-agent backend
│   ├── app/          # Application code
│   ├── data/         # Mock data files
│   ├── scripts/      # Data ingestion
│   └── chroma_db/    # Vector stores (created after ingestion)
└── frontend/         # Next.js frontend
    └── src/          # Frontend source code
```

## Step-by-Step Setup

### Part 1: Backend Setup (15 minutes)

#### 1.1 Navigate to Backend

```bash
cd backend
```

#### 1.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

#### 1.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI, Uvicorn
- LangChain, LangGraph
- OpenAI client
- ChromaDB
- Pydantic and other utilities

#### 1.4 Configure Environment

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Edit `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

#### 1.5 Run Data Ingestion

```bash
python scripts/ingest_data.py
```

Expected output:
```
============================================================
ADVANCED CUSTOMER SERVICE AI - DATA INGESTION
============================================================

============================================================
Ingesting Billing Documents
============================================================
✓ Ingested 12 billing document chunks
  Saved to: ./chroma_db/billing

============================================================
Ingesting Technical Documents
============================================================
✓ Ingested 45 technical document chunks
  Saved to: ./chroma_db/technical

============================================================
Preparing Policy Documents
============================================================
✓ Found 4 policy documents
  Policy documents ready for CAG (no vector store needed)

============================================================
DATA INGESTION COMPLETE!
============================================================
```

#### 1.6 Start Backend Server

```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

✅ **Backend is now running at http://localhost:8000**

Test it: Visit http://localhost:8000/health in your browser

### Part 2: Frontend Setup (5 minutes)

Open a **new terminal window** (keep backend running).

#### 2.1 Navigate to Frontend

```bash
cd frontend
```

#### 2.2 Install Dependencies

```bash
npm install
```

This installs Next.js, React, Tailwind CSS, and other dependencies.

#### 2.3 Configure Environment

Create `.env.local` file:

**Windows:**
```bash
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
```

**Mac/Linux:**
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

#### 2.4 Start Frontend Server

```bash
npm run dev
```

Expected output:
```
  ▲ Next.js 15.0.3
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.5s
```

✅ **Frontend is now running at http://localhost:3000**

### Part 3: Test the Application (5 minutes)

#### 3.1 Open the Application

Visit http://localhost:3000 in your browser.

You should see:
- Clean chat interface
- Header: "Advanced Customer Service AI"
- Subtitle: "Multi-agent system: Billing Support • Technical Support • Policy & Compliance"
- Message input box at the bottom

#### 3.2 Test Billing Support Agent

Type: **"What are your pricing plans?"**

Expected response:
- Detailed pricing information for Basic, Pro, and Enterprise plans
- At the end: "_Handled by: Billing Support_"
- Smooth typewriter effect

#### 3.3 Test Technical Support Agent

Type: **"How do I upload large files?"**

Expected response:
- Step-by-step guide from the technical documentation
- At the end: "_Handled by: Technical Support_"

#### 3.4 Test Policy & Compliance Agent

Type: **"What is your privacy policy?"**

Expected response:
- Information from the privacy policy document
- At the end: "_Handled by: Policy & Compliance_"

#### 3.5 Test Session Persistence

1. Send a message
2. Refresh the page (F5)
3. Send another message
4. Your session should be maintained (conversation history persists)

Check browser cookies (F12 > Application > Cookies):
- You should see `chat_session_id` cookie

## Verification Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 3000
- [ ] Health check works: http://localhost:8000/health
- [ ] Chat interface loads successfully
- [ ] Billing questions route to Billing Support
- [ ] Technical questions route to Technical Support
- [ ] Policy questions route to Policy & Compliance
- [ ] Routing information displayed at end of responses
- [ ] Session persists after page refresh
- [ ] No errors in browser console (F12)
- [ ] No errors in backend terminal

## Architecture Overview

```
User → Next.js Frontend (Port 3000)
         ↓
     HTTP POST /chat
         ↓
    FastAPI Backend (Port 8000)
         ↓
    Supervisor Agent (GPT-4o-mini)
         ↓
    ┌────┴────┬──────────┐
    ↓         ↓          ↓
Billing   Technical   Policy
(GPT-4o)  (GPT-4o)    (GPT-4o-mini)
```

### Agent Strategies

1. **Billing Support** - Hybrid RAG/CAG
   - Caches static billing policies per session
   - Fetches dynamic data (invoices, pricing) each time

2. **Technical Support** - Pure RAG
   - Always retrieves from vector store
   - Uses MMR for diverse results

3. **Policy & Compliance** - Pure CAG
   - Static documents loaded in context
   - Fastest responses, no vector search

## Example Queries

### Billing Questions
- "What's your refund policy?"
- "How much does the Pro plan cost?"
- "Calculate the price for 5 additional users"
- "When will I be charged?"
- "What payment methods do you accept?"

### Technical Questions
- "How do I get started?"
- "What keyboard shortcuts are available?"
- "I'm getting error 500 when uploading"
- "How do I integrate with Slack?"
- "What's the maximum file upload size?"

### Policy Questions
- "What is your privacy policy?"
- "How do you handle my data?"
- "Are you GDPR compliant?"
- "What are your terms of service?"
- "Do you sell my personal information?"

## Troubleshooting

### Backend Won't Start

**Error: "ModuleNotFoundError"**
```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

**Error: "OpenAI API key not found"**
```bash
# Check .env file exists
# Verify OPENAI_API_KEY is set correctly
# No spaces, no quotes around the key
```

**Error: "Vector store not available"**
```bash
# Run data ingestion
python scripts/ingest_data.py

# Verify chroma_db/ directory was created
```

### Frontend Won't Start

**Error: "Cannot find module"**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 3000 already in use"**
```bash
# Use different port
npm run dev -- -p 3001

# Update backend CORS in backend/app/config.py
# Add http://localhost:3001 to cors_origins
```

### Connection Issues

**Error: "Failed to send message"**

1. Check backend is running: http://localhost:8000/health
2. Check browser console (F12) for CORS errors
3. Verify `.env.local` has correct API URL
4. Check both terminals for error messages

**Error: "CORS policy"**

Backend CORS is configured for:
- http://localhost:3000
- http://localhost:3001

If using different port, update `backend/app/config.py`:
```python
cors_origins: str = "http://localhost:3000,http://localhost:YOUR_PORT"
```

### Slow Responses

**Problem: Long wait for AI response**

This is normal for first query (loading models):
- First query: ~10-15 seconds
- Subsequent queries: ~3-5 seconds

To speed up:
1. Reduce character streaming delay in `frontend/src/lib/api.ts`:
   ```typescript
   await new Promise(resolve => setTimeout(resolve, 5)); // Change from 15 to 5
   ```

## Stopping the Servers

### Stop Backend
In backend terminal: `Ctrl+C`

### Stop Frontend
In frontend terminal: `Ctrl+C`

### Deactivate Virtual Environment
```bash
deactivate
```

## Next Steps

1. **Explore the Code**
   - Backend: `backend/app/agents/` - Agent implementations
   - Frontend: `frontend/src/components/` - UI components

2. **Customize**
   - Add your own data to `backend/data/`
   - Re-run data ingestion
   - Modify agent prompts in `backend/app/agents/`

3. **Deploy**
   - See `backend/README.md` for production deployment
   - See `frontend/INTEGRATION.md` for deployment guide

## Additional Resources

- [Backend Documentation](../backend/README.md)
- [Integration Guide](./INTEGRATION.md)
- [Multi-Agent Architecture](../multi-agent/12-customer-service-multi-agent.md)
- [Project Specification](../agentic-customer-specs.md)

## Support

If you encounter issues:
1. Check both terminal windows for errors
2. Verify all prerequisites are installed
3. Review the troubleshooting section above
4. Check browser DevTools (F12) console

---

**🎉 Congratulations!** You now have a fully functional multi-agent customer service AI system running locally!

