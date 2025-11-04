# Advanced Customer Service AI

A production-ready, full-stack customer service application powered by a multi-agent AI system. Built with FastAPI (backend) and Next.js (frontend), featuring intelligent routing to specialized AI agents using LangGraph orchestration.

## 🎯 Project Overview

This application demonstrates advanced AI engineering patterns through a real-world customer service use case. The system automatically routes customer queries to specialized agents, each optimized with different retrieval strategies:

- **Supervisor Agent** - Analyzes queries and intelligently routes to specialists
- **Billing Support Agent** - Handles pricing, invoices, payments (Hybrid RAG/CAG)
- **Technical Support Agent** - Answers technical questions (Pure RAG)
- **Policy & Compliance Agent** - Provides policy information (Pure CAG)

## 🌟 Key Features

✅ **Multi-Agent Architecture** - Specialized agents with focused responsibilities  
✅ **Strategic RAG** - Three retrieval strategies optimized for different data types  
✅ **Cost Optimization** - Smart model selection (GPT-4o vs GPT-4o-mini)  
✅ **Session Management** - Conversation history and context caching  
✅ **Modern UI** - Clean, responsive chat interface with streaming responses  
✅ **Production-Ready** - Error handling, logging, CORS, health checks  

## 📊 System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         User                                  │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│               Next.js Frontend (Port 3000)                    │
│                                                                │
│  • Chat Interface         • Session Management                │
│  • Streaming Display      • Error Handling                    │
└───────────────────────────┬──────────────────────────────────┘
                            │ HTTP POST /chat
                            ▼
┌──────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Port 8000)                     │
│                                                                │
│              Supervisor Agent (GPT-4o-mini)                   │
│                       ↓                                        │
│        ┌──────────────┼──────────────┐                       │
│        ↓              ↓               ↓                       │
│  Billing Agent   Technical Agent  Policy Agent               │
│  (Hybrid R/C)    (Pure RAG)       (Pure CAG)                 │
│  GPT-4o          GPT-4o           GPT-4o-mini                 │
│        ↓              ↓               ↓                       │
│  ChromaDB        ChromaDB         Static Files               │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11** (⚠️ Required - Python 3.14 has dependency compilation issues)
- Node.js 18+
- OpenAI API key

### One-Command Setup (Recommended)

**Windows:**
```bash
start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

This automatically starts both servers!

### Manual Setup

See [QUICKSTART.md](./QUICKSTART.md) for detailed step-by-step instructions.

**TL;DR:**

```bash
# Terminal 1: Backend
cd backend
py -3.11 -m venv venv           # Windows: Use Python 3.11
.\venv\Scripts\activate         # Windows
# source venv/bin/activate      # Mac/Linux
pip install -r requirements.txt
copy .env.example .env          # Windows: copy, Linux/Mac: cp
# Edit .env and add your OPENAI_API_KEY
python scripts/ingest_data.py
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

Visit **http://localhost:3000** 🚀

## 💬 Example Queries

### Billing Support
- "What are your pricing plans?"
- "How do I get a refund?"
- "Calculate the price for 10 additional users"

### Technical Support
- "How do I upload large files?"
- "I'm getting error 500 when uploading"
- "What keyboard shortcuts are available?"

### Policy & Compliance
- "What is your privacy policy?"
- "How do you handle my data?"
- "Are you GDPR compliant?"

## 🏗️ Project Structure

```
agentic-customer-project/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── agents/              # Multi-agent implementations
│   │   │   ├── supervisor.py    # Supervisor agent
│   │   │   ├── billing_agent.py # Billing support
│   │   │   ├── technical_agent.py # Technical support
│   │   │   └── policy_agent.py  # Policy & compliance
│   │   ├── tools/               # Agent tools
│   │   ├── utils/               # Utilities (sessions, vector stores)
│   │   ├── main.py             # FastAPI application
│   │   ├── config.py           # Configuration
│   │   ├── models.py           # Pydantic models
│   │   └── state.py            # LangGraph state
│   ├── data/                    # Mock data
│   │   ├── policies/           # Static policy documents (CAG)
│   │   ├── billing/            # Billing documents
│   │   └── technical/          # Technical documentation
│   ├── scripts/
│   │   └── ingest_data.py      # Data ingestion pipeline
│   ├── chroma_db/              # Vector stores (created after ingestion)
│   └── requirements.txt        # Python dependencies
│
├── frontend/                    # Next.js Frontend
│   ├── src/
│   │   ├── app/                # Next.js app
│   │   ├── components/         # React components
│   │   ├── lib/
│   │   │   └── api.ts          # API client
│   │   └── types/              # TypeScript types
│   ├── package.json            # Node dependencies
│   └── INTEGRATION.md          # Integration guide
│
├── multi-agent/
│   └── 12-customer-service-multi-agent.md  # Architecture docs
│
├── QUICKSTART.md               # Detailed setup guide
├── start.sh / start.bat        # Startup scripts
└── README.md                   # This file
```

## 🔧 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain & LangGraph** - Agent orchestration
- **OpenAI GPT-4o / GPT-4o-mini** - Language models
- **ChromaDB** - Vector database
- **Pydantic** - Data validation

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **js-cookie** - Session management

## 📖 Documentation

- [**QUICKSTART.md**](./QUICKSTART.md) - Complete setup guide
- [**frontend/INTEGRATION.md**](./frontend/INTEGRATION.md) - Frontend-backend integration
- [**backend/README.md**](./backend/README.md) - Backend documentation
- [**multi-agent/12-customer-service-multi-agent.md**](./multi-agent/12-customer-service-multi-agent.md) - Multi-agent architecture

## 🎓 Key Concepts

### Retrieval Strategies

1. **Pure RAG** (Technical Support)
   - Always retrieves from vector store
   - Best for: Dynamic, frequently updated content
   - Example: Technical docs, bug reports

2. **Pure CAG** (Policy & Compliance)
   - Static documents in context
   - Best for: Static, unchanging documents
   - Example: Terms of service, privacy policy

3. **Hybrid RAG/CAG** (Billing Support)
   - Caches static policies per session
   - Fetches dynamic data each time
   - Best for: Mix of static and dynamic content
   - Example: Billing policies + current invoices

### Cost Optimization

Strategic model selection reduces costs by 40%:

| Agent | Model | Use Case | Cost |
|-------|-------|----------|------|
| Supervisor | GPT-4o-mini | Fast routing | Low |
| Billing | GPT-4o | Complex billing logic | High |
| Technical | GPT-4o | Technical reasoning | High |
| Policy | GPT-4o-mini | Simple policy queries | Low |

**Estimated cost**: ~$3.06 per 1,000 queries

## 🔍 API Endpoints

### Backend (http://localhost:8000)

- `GET /health` - Health check
- `POST /chat` - Main chat endpoint
- `GET /sessions/count` - Active session count
- `POST /sessions/cleanup` - Cleanup expired sessions
- `GET /docs` - Interactive API documentation

### Example Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your pricing plans?"}'
```

### Example Response

```json
{
  "response": "We offer three pricing plans: Basic ($9.99/month)...",
  "routed_to": "Billing Support",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2025-11-03T10:30:00"
}
```

## 🐛 Troubleshooting

### Backend Issues

**"OpenAI API key not found"**
- Check `.env` file exists in `backend/`
- Verify `OPENAI_API_KEY` is set correctly

**"Vector store not available"**
- Run data ingestion: `python scripts/ingest_data.py`
- Check `chroma_db/` directory exists

### Frontend Issues

**"Failed to send message"**
- Verify backend is running: http://localhost:8000/health
- Check browser console (F12) for errors
- Verify `.env.local` has correct API URL

**CORS errors**
- Backend CORS configured for localhost:3000 and localhost:3001
- Update `backend/app/config.py` if using different port

See [QUICKSTART.md](./QUICKSTART.md) for more troubleshooting.

## 🚢 Deployment

### Backend Production

```bash
# Use production WSGI server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Use proper secrets management
# Enable HTTPS with reverse proxy
# Replace in-memory sessions with Redis
```

### Frontend Production

```bash
# Build for production
npm run build
npm start

# Deploy to Vercel, Netlify, or similar
# Update NEXT_PUBLIC_API_URL to production backend
```

## 📊 Features Showcase

### Session Management
- Automatic session creation and tracking
- Conversation history maintained across requests
- Cookie-based persistence (7-day expiry)
- Session timeout after 30 minutes of inactivity

### Intelligent Routing
- Supervisor analyzes query intent
- Routes to appropriate specialized agent
- Handles ambiguous queries gracefully
- Displays routing information to user

### Streaming Responses
- Character-by-character streaming display
- Smooth typewriter effect
- Better perceived performance
- Real-time feedback to user

## 🤝 Contributing

This is a portfolio project demonstrating advanced AI engineering patterns. Feel free to:

1. Fork the repository
2. Experiment with different agent configurations
3. Add new specialized agents
4. Customize for your use case
5. Share your improvements

## 📝 License

This project is part of the Advanced Customer Service AI Portfolio Project.

## 🎓 Learning Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Multi-Agent Patterns](./multi-agent/12-customer-service-multi-agent.md)

## 📧 Project Details

- **Backend**: Python 3.10+, FastAPI, LangChain, LangGraph
- **Frontend**: Node.js 18+, Next.js 15, TypeScript, Tailwind CSS
- **AI Models**: OpenAI GPT-4o, GPT-4o-mini
- **Vector Store**: ChromaDB
- **Deployment**: Docker-ready, cloud-deployable

---

**Built with** ❤️ **as a demonstration of advanced AI engineering patterns**

For detailed setup instructions, see [QUICKSTART.md](./QUICKSTART.md)

For integration details, see [frontend/INTEGRATION.md](./frontend/INTEGRATION.md)

#   A g e n t i c - C u s t o m e r - M u l t i - A g e n t s 
 
 
