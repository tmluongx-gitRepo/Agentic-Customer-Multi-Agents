"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Message(BaseModel):
    """Individual message structure."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Incoming chat request from frontend."""
    message: str = Field(..., min_length=1, description="User's message")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation continuity")
    customer_id: Optional[str] = Field(None, description="Optional customer identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What's your refund policy?",
                "session_id": "session_123",
                "customer_id": "customer_456"
            }
        }


class ChatResponse(BaseModel):
    """Outgoing chat response to frontend."""
    response: str = Field(..., description="AI assistant's response")
    routed_to: str = Field(..., description="Which agent handled the query")
    session_id: str = Field(..., description="Session ID for tracking conversation")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "Our refund policy allows returns within 30 days...",
                "routed_to": "Policy Support",
                "session_id": "session_123",
                "timestamp": "2025-11-03T10:30:00"
            }
        }


class SessionInfo(BaseModel):
    """Session metadata."""
    session_id: str
    customer_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    message_count: int = 0


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)

