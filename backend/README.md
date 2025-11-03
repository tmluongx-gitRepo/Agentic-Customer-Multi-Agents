# Advanced Customer Service AI - Backend

A production-ready FastAPI backend with LangGraph-based multi-agent orchestration for intelligent customer service.

## Overview

This backend implements a sophisticated multi-agent system that routes customer queries to specialized AI agents:

- **Supervisor Agent** (GPT-4o-mini) - Analyzes queries and routes to appropriate specialists
- **Billing Support Agent** (GPT-4o) - Handles pricing, invoices, payments using Hybrid RAG/CAG
- **Technical Support Agent** (GPT-4o) - Answers technical questions using Pure RAG
- **Policy & Compliance Agent** (GPT-4o-mini) - Provides policy information using Pure CAG

## Architecture

```
User Query → FastAPI /chat Endpoint → Supervisor Agent
                                            ↓
                        ┌──────────────────┼──────────────────┐
                        ↓                  ↓                   ↓
                Billing Agent      Technical Agent      Policy Agent
                (Hybrid RAG/CAG)   (Pure RAG)           (Pure CAG)
                        ↓                  ↓                   ↓
                    Response           Response            Response
```

## Features

✅ Multi-agent orchestration with LangGraph  
✅ Three specialized worker agents with optimized retrieval strategies  
✅ Session management with conversation history  
✅ Vector stores (ChromaDB) for dynamic content retrieval  
✅ Context-augmented generation for static policies  
✅ RESTful API with FastAPI  
✅ CORS enabled for frontend integration  
✅ Comprehensive error handling and logging  
✅ Cost-optimized model selection (GPT-4o vs GPT-4o-mini)  

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration management
│   ├── models.py                  # Pydantic models
│   ├── state.py                   # LangGraph state definitions
│   ├── agents/                    # Agent implementations
│   │   ├── supervisor.py
│   │   ├── billing_agent.py
│   │   ├── technical_agent.py
│   │   └── policy_agent.py
│   ├── tools/                     # Agent tools
│   │   ├── billing_tools.py
│   │   ├── technical_tools.py
│   │   └── policy_tools.py
│   └── utils/                     # Utilities
│       ├── session_manager.py
│       └── vector_store.py
├── data/                          # Sample data
│   ├── policies/                  # Static policy documents
│   ├── billing/                   # Billing documents
│   └── technical/                 # Technical documentation
├── chroma_db/                     # Vector store (created after ingestion)
├── scripts/
│   └── ingest_data.py            # Data ingestion script
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## Prerequisites

- **Python 3.11** (⚠️ **Required** - Python 3.14 has dependency compilation issues, see [INSTALL.md](INSTALL.md))
- OpenAI API key
- pip (Python package manager)

> **Note**: If you're using Python 3.14, you'll encounter errors with packages like `tiktoken`, `chromadb`, and `pydantic-core` that require Rust/C++ compilation. Please install Python 3.11 from [python.org](https://www.python.org/downloads/).

## Installation

### 1. Clone the repository

```bash
cd backend
```

### 2. Create and activate virtual environment

**Windows (PowerShell):**
```powershell
# Use Python 3.11 specifically
py -3.11 -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mac/Linux:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

> **Note**: Installation may take 2-3 minutes. The packages include FastAPI, LangChain, LangGraph, ChromaDB, and the OpenAI SDK.

### 4. Set up environment variables

**Windows:**
```powershell
copy .env.example .env
notepad .env  # Add your OpenAI API key
```

**Mac/Linux:**
```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

**Required environment variables:**
- `OPENAI_API_KEY` - Your OpenAI API key (**required**)

**Optional environment variables** (defaults provided):
- `SUPERVISOR_MODEL` - Model for supervisor agent (default: openai:gpt-4o-mini)
- `BILLING_MODEL` - Model for billing agent (default: openai:gpt-4o)
- `TECHNICAL_MODEL` - Model for technical agent (default: openai:gpt-4o)
- `POLICY_MODEL` - Model for policy agent (default: openai:gpt-4o-mini)
- `FASTAPI_PORT` - Server port (default: 8000)
- `CHROMA_DB_PATH` - ChromaDB storage path (default: ./chroma_db)

### 5. Run data ingestion

This step creates vector stores from the sample data:

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

## Running the Server

### Development mode (with auto-reload)

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Production mode

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server will start at **http://localhost:8000**

✅ **Verify it's working:**
- Health check: http://localhost:8000/health  
- Interactive API docs: http://localhost:8000/docs  
- Alternative API docs: http://localhost:8000/redoc

You should see output like:
```
INFO:     Starting Advanced Customer Service AI Backend...
INFO:     Loading policy documents...
INFO:     Initializing vector stores...
INFO:     ✓ Application startup complete!
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## API Endpoints

### Health Check

```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-03T10:30:00"
}
```

### Chat Endpoint

```bash
POST /chat
```

Request body:
```json
{
  "message": "What's your refund policy?",
  "session_id": "optional-session-id",
  "customer_id": "optional-customer-id"
}
```

Response:
```json
{
  "response": "Our refund policy allows returns within 30 days...",
  "routed_to": "Policy & Compliance",
  "session_id": "generated-session-id",
  "timestamp": "2025-11-03T10:30:00"
}
```

### Session Management

Get active session count:
```bash
GET /sessions/count
```

Cleanup expired sessions:
```bash
POST /sessions/cleanup
```

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Chat request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your pricing plans?"}'
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "How do I reset my password?"}
)

print(response.json())
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## Example Queries

**Billing Questions** (routes to Billing Support Agent):
- "What are your pricing plans?"
- "How do I get a refund?"
- "Why was I charged twice?"
- "Calculate the price for 10 additional users"

**Technical Questions** (routes to Technical Support Agent):
- "How do I upload large files?"
- "I'm getting error 500 when uploading"
- "How do I integrate with Slack?"
- "What keyboard shortcuts are available?"

**Policy Questions** (routes to Policy & Compliance Agent):
- "What is your privacy policy?"
- "How do you handle my data?"
- "What are your terms of service?"
- "Are you GDPR compliant?"

## Agent Retrieval Strategies

### Billing Support Agent - Hybrid RAG/CAG
- **Static policies** cached per session (refund policy, billing terms)
- **Dynamic data** fetched each time (invoices, current pricing)
- **Benefit**: Fast + up-to-date information

### Technical Support Agent - Pure RAG
- **Always retrieves** from vector store
- **MMR (Maximum Marginal Relevance)** for diverse results
- **Benefit**: Always current technical information

### Policy & Compliance Agent - Pure CAG
- **Static documents** loaded into context at startup
- **No vector search** overhead
- **Benefit**: Fastest responses, perfectly consistent

## Cost Optimization

The system uses different models strategically:

| Agent | Model | Cost per 1M tokens | Use Case |
|-------|-------|-------------------|----------|
| Supervisor | GPT-4o-mini | $0.15 | Fast routing |
| Billing | GPT-4o | $2.50 | Complex billing logic |
| Technical | GPT-4o | $2.50 | Technical reasoning |
| Policy | GPT-4o-mini | $0.15 | Simple policy queries |

**Estimated cost**: ~$3.06 per 1,000 queries (40% cheaper than all-GPT-4o)

## Troubleshooting

### Vector stores not loading

**Problem**: "Billing vector store not available" warning

**Solution**:
1. Make sure you ran `python scripts/ingest_data.py`
2. Check that `chroma_db/` directory exists
3. Verify OpenAI API key is set correctly
4. Check data files exist in `data/billing/` and `data/technical/`

### OpenAI API errors

**Problem**: "401 Unauthorized" or "Invalid API key"

**Solution**:
1. Verify your API key in `.env` file
2. Ensure no extra spaces or quotes around the key
3. Check that your API key has sufficient credits
4. Verify the key starts with `sk-`

### Import errors

**Problem**: `ModuleNotFoundError` when running the server

**Solution**:
1. Activate virtual environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure you're in the `backend` directory

### Port already in use

**Problem**: "Address already in use" error

**Solution**:
1. Change port in `.env`: `PORT=8001`
2. Or kill the process using port 8000
3. Run with custom port: `uvicorn app.main:app --port 8001`

## Development

### Adding new agents

1. Create agent file in `app/agents/`
2. Create corresponding tools in `app/tools/`
3. Add tool to supervisor in `app/agents/supervisor.py`
4. Update routing logic and system prompt

### Adding new data

1. Add documents to appropriate `data/` subdirectory
2. Run ingestion script: `python scripts/ingest_data.py`
3. Restart the server

### Logging

Logs are printed to console with INFO level by default. To change log level:

```python
# In app/main.py
logging.basicConfig(level=logging.DEBUG)
```

## Production Deployment

### Recommended settings for production:

1. **Use production WSGI server**:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Set environment variables**:
   - Use proper secrets management (AWS Secrets Manager, Azure Key Vault, etc.)
   - Never commit `.env` file to version control

3. **Enable HTTPS**:
   - Use reverse proxy (Nginx, Traefik)
   - Obtain SSL certificate (Let's Encrypt)

4. **Database for sessions**:
   - Replace in-memory session manager with Redis or database
   - Enables horizontal scaling

5. **Monitoring**:
   - Set up application monitoring (DataDog, New Relic)
   - Monitor API usage and costs
   - Set up alerts for errors

## License

This project is part of the Advanced Customer Service AI Portfolio Project.

## Support

For questions or issues:
- Check documentation in `/docs`
- Review example queries above
- Check the project specification: `../agentic-customer-specs.md`
- Review multi-agent architecture: `../multi-agent/12-customer-service-multi-agent.md`

## Related Documentation

- [Multi-Agent Architecture](../multi-agent/12-customer-service-multi-agent.md)
- [Project Specification](../agentic-customer-specs.md)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

