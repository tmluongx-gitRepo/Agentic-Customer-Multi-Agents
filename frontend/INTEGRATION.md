# Frontend-Backend Integration Guide

## Overview

This guide explains how the Next.js frontend integrates with the FastAPI backend for the Advanced Customer Service AI system.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js Frontend                         │
│                  (Port 3000)                                 │
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ ChatInterface │ -> │  API Client  │ -> │    Cookies   │  │
│  │  Component    │    │  (api.ts)    │    │  (Session)   │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │
                             │ HTTP POST /chat
                             │ { message, session_id }
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│                  (Port 8000)                                 │
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ /chat        │ -> │  Supervisor   │ -> │  Specialized │  │
│  │  Endpoint    │    │    Agent      │    │   Agents     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                               │
│  Billing Agent (Hybrid RAG/CAG) | Technical Agent (Pure RAG) │
│  Policy Agent (Pure CAG)                                     │
└─────────────────────────────────────────────────────────────┘
```

## Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run data ingestion
python scripts/ingest_data.py

# Start the backend server
uvicorn app.main:app --reload
```

Backend will run at `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start the development server
npm run dev
```

Frontend will run at `http://localhost:3000`

## API Integration

### Request Format

The frontend sends POST requests to `/chat`:

```typescript
interface ChatRequest {
  message: string;           // User's message
  session_id?: string;       // Optional session ID from cookie
  customer_id?: string;      // Optional customer identifier
}
```

Example:
```json
{
  "message": "What's your refund policy?",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Response Format

The backend returns:

```typescript
interface ChatResponse {
  response: string;          // AI agent's response
  routed_to: string;        // Which agent handled it (Billing Support, Technical Support, Policy & Compliance)
  session_id: string;       // Session ID for tracking
  timestamp: string;        // ISO timestamp
}
```

Example:
```json
{
  "response": "Our refund policy allows returns within 30 days of purchase...",
  "routed_to": "Policy & Compliance",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2025-11-03T10:30:00"
}
```

## Session Management

### Cookie-Based Sessions

The frontend uses `js-cookie` to manage session IDs:

1. **First Request**: No session_id sent
2. **Backend Creates Session**: Returns new session_id
3. **Frontend Stores**: Saves session_id in cookie (7-day expiry)
4. **Subsequent Requests**: Includes session_id in requests
5. **Backend Maintains State**: Conversation history and cached data

### Session Features

- **Conversation History**: Full message history maintained per session
- **Hybrid RAG/CAG Caching**: Billing policies cached per session
- **Automatic Expiry**: Sessions expire after 30 minutes of inactivity
- **Persistent**: Survives page refreshes (cookie-based)

## Streaming Response

The frontend implements **simulated streaming** for better UX:

1. Backend returns complete response immediately
2. Frontend receives full response
3. Frontend streams it character-by-character to the UI
4. Creates typewriter effect (15ms per character)
5. Appends routing information at the end

```typescript
// Simulated streaming
for (const char of fullText) {
  yield char;
  await new Promise(resolve => setTimeout(resolve, 15));
}
```

## Error Handling

### Frontend Error Handling

```typescript
try {
  // Make API request
  for await (const chunk of streamChatMessage(content)) {
    // Handle streaming chunks
  }
} catch (err) {
  console.error('Error sending message:', err);
  setError('Failed to send message. Please try again.');
  // Remove placeholder message
}
```

### Backend Error Responses

The backend returns appropriate HTTP status codes:

- `200 OK`: Successful response
- `500 Internal Server Error`: Server error with details
- `422 Unprocessable Entity`: Invalid request format

## Agent Routing

The supervisor agent automatically routes queries:

| Query Type | Example | Routes To |
|------------|---------|-----------|
| **Billing** | "What are your pricing plans?" | Billing Support |
| **Technical** | "How do I upload files?" | Technical Support |
| **Policy** | "What is your privacy policy?" | Policy & Compliance |

The frontend displays which agent handled each query in italics at the end of the response:

```
_Handled by: Billing Support_
```

## Health Monitoring

### Health Check Endpoint

```typescript
// Frontend can check backend health
const health = await healthCheck();
// Returns: { status: "healthy", version: "1.0.0", timestamp: "..." }
```

### Session Count (Monitoring)

```typescript
// Get active session count
const count = await getSessionCount();
// Returns: { active_sessions: 5 }
```

## CORS Configuration

The backend is configured to allow requests from the frontend:

```python
# backend/app/config.py
cors_origins: str = "http://localhost:3000,http://localhost:3001"

# backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing the Integration

### 1. Start Both Servers

```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 2. Test Example Queries

Visit `http://localhost:3000` and try:

**Billing Questions:**
- "What are your pricing plans?"
- "How do I get a refund?"
- "Calculate the price for 10 additional users"

**Technical Questions:**
- "How do I upload large files?"
- "I'm getting error 500 when uploading"
- "What keyboard shortcuts are available?"

**Policy Questions:**
- "What is your privacy policy?"
- "How do you handle my data?"
- "Are you GDPR compliant?"

### 3. Verify Session Persistence

1. Send a message
2. Refresh the page
3. Send another message
4. Session should be maintained (check browser cookies)

### 4. Check Developer Console

Open browser DevTools (F12) and check:
- **Network Tab**: See API requests to `http://localhost:8000/chat`
- **Console Tab**: Check for any errors
- **Application Tab > Cookies**: Verify `chat_session_id` cookie

## Troubleshooting

### Backend Not Responding

**Problem**: Frontend shows "Failed to send message"

**Solutions**:
1. Verify backend is running: Visit `http://localhost:8000/health`
2. Check for CORS errors in browser console
3. Verify `.env` has `OPENAI_API_KEY`
4. Check backend terminal for errors

### Session Not Persisting

**Problem**: Session resets after refresh

**Solutions**:
1. Check browser cookies are enabled
2. Verify `chat_session_id` cookie exists
3. Check cookie expiration (7 days default)
4. Ensure same domain for frontend/backend

### Slow Responses

**Problem**: Long wait times for responses

**Solutions**:
1. OpenAI API might be slow - check status
2. Vector stores not loaded - run data ingestion
3. Reduce streaming delay in `api.ts` (change from 15ms to 5ms)

### Agent Not Routing Correctly

**Problem**: Wrong agent handles query

**Solutions**:
1. Check backend logs for routing decisions
2. Supervisor prompt may need tuning
3. Query might be ambiguous - try more specific wording

## Production Deployment

### Backend Deployment

1. Use production WSGI server:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. Set proper environment variables
3. Use HTTPS with reverse proxy (Nginx)
4. Replace in-memory sessions with Redis
5. Enable monitoring and logging

### Frontend Deployment

1. Update `NEXT_PUBLIC_API_URL` to production backend URL
2. Build for production:
   ```bash
   npm run build
   npm start
   ```

3. Deploy to Vercel, Netlify, or similar
4. Ensure CORS allows production domain
5. Use environment variables for API URL

## Additional Resources

- [Backend README](../backend/README.md)
- [Frontend README](./README.md)
- [Multi-Agent Architecture](../multi-agent/12-customer-service-multi-agent.md)
- [Project Specification](../agentic-customer-specs.md)

## Support

For integration issues:
1. Check both backend and frontend logs
2. Verify environment variables
3. Test endpoints with curl or Postman
4. Review browser network tab for API calls

