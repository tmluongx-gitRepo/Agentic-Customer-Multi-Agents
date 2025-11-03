"""
FastAPI Application - Advanced Customer Service AI Backend
Main entry point for the multi-agent customer service system.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from app.config import settings
from app.models import ChatRequest, ChatResponse, HealthResponse
from app.agents.supervisor import get_supervisor_agent
from app.utils.session_manager import session_manager
from app.utils.vector_store import vector_store_manager
from app.tools.policy_tools import load_policy_documents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown events."""
    # Startup
    logger.info("Starting Advanced Customer Service AI Backend...")
    
    try:
        # Load policy documents
        logger.info("Loading policy documents...")
        load_policy_documents()
        
        # Initialize vector stores
        logger.info("Initializing vector stores...")
        vector_store_manager.get_billing_store()
        vector_store_manager.get_technical_store()
        
        # Pre-initialize supervisor agent
        logger.info("Initializing supervisor agent...")
        get_supervisor_agent()
        
        logger.info("✓ Application startup complete!")
        
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        logger.warning("Application started with limited functionality")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Advanced Customer Service AI Backend...")
    session_manager.cleanup_expired_sessions()
    logger.info("✓ Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Advanced Customer Service AI",
    description="Multi-agent customer service system with LangGraph orchestration",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now()
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now()
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for customer service queries.
    
    Accepts a customer message and routes it through the multi-agent system.
    Returns the response along with routing information.
    """
    try:
        logger.info(f"Received chat request: {request.message[:100]}...")
        
        # Get or create session
        session = session_manager.get_or_create_session(
            session_id=request.session_id,
            customer_id=request.customer_id
        )
        session_id = session["session_id"]
        
        logger.info(f"Using session: {session_id}")
        
        # Get supervisor agent
        supervisor = get_supervisor_agent()
        
        # Invoke supervisor with the query
        # New LangGraph API expects messages format
        logger.info(f"Invoking supervisor with message: {request.message}")
        try:
            result = supervisor.invoke({
                "messages": [("user", request.message)]
            })
            logger.info(f"Supervisor result keys: {result.keys()}")
            logger.info(f"Supervisor result: {result}")
        except Exception as e:
            logger.error(f"Error invoking supervisor: {e}", exc_info=True)
            raise
        
        # Extract response from the messages
        # The last message should be the AI's response
        messages = result.get("messages", [])
        if messages:
            last_message = messages[-1]
            # Handle different message types
            if hasattr(last_message, 'content'):
                response_text = last_message.content
            else:
                response_text = str(last_message)
        else:
            response_text = "I apologize, but I couldn't process your request."
        
        # Determine which agent was routed to by checking tool calls in messages
        routed_to = "Supervisor"
        for msg in messages:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                tool_name = msg.tool_calls[0].get('name', '')
                if "billing" in tool_name.lower():
                    routed_to = "Billing Support"
                elif "technical" in tool_name.lower():
                    routed_to = "Technical Support"
                elif "policy" in tool_name.lower():
                    routed_to = "Policy & Compliance"
                break
        
        # Update session
        session_manager.increment_message_count(session_id)
        session_manager.update_session(
            session_id,
            routing_history=session.get("routing_history", []) + [routed_to]
        )
        
        logger.info(f"Request processed successfully. Routed to: {routed_to}")
        
        return ChatResponse(
            response=response_text,
            routed_to=routed_to,
            session_id=session_id,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing your request: {str(e)}"
        )


@app.get("/sessions/count")
async def get_session_count():
    """Get the number of active sessions."""
    count = session_manager.get_session_count()
    return {"active_sessions": count}


@app.post("/sessions/cleanup")
async def cleanup_sessions():
    """Manually trigger cleanup of expired sessions."""
    session_manager.cleanup_expired_sessions()
    count = session_manager.get_session_count()
    return {
        "message": "Expired sessions cleaned up",
        "active_sessions": count
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )

