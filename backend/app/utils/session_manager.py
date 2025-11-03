"""
Session management for maintaining conversation state across requests.
Provides thread-safe in-memory session storage with automatic expiration.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
import threading
import uuid
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class SessionManager:
    """Thread-safe session manager for conversation state."""
    
    def __init__(self):
        self._sessions: Dict[str, dict] = {}
        self._lock = threading.Lock()
        self._session_timeout = timedelta(minutes=settings.session_timeout_minutes)
    
    def create_session(self, customer_id: Optional[str] = None) -> str:
        """Create a new session and return the session ID."""
        session_id = str(uuid.uuid4())
        
        with self._lock:
            self._sessions[session_id] = {
                "session_id": session_id,
                "customer_id": customer_id,
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "message_count": 0,
                "cached_billing_policies": None,
                "routing_history": []
            }
        
        logger.info(f"Created new session: {session_id}")
        return session_id
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session by ID, return None if not found or expired."""
        with self._lock:
            session = self._sessions.get(session_id)
            
            if session is None:
                return None
            
            # Check if session has expired
            if datetime.now() - session["last_activity"] > self._session_timeout:
                logger.info(f"Session {session_id} has expired, removing")
                del self._sessions[session_id]
                return None
            
            # Update last activity
            session["last_activity"] = datetime.now()
            return session
    
    def get_or_create_session(self, session_id: Optional[str] = None, 
                             customer_id: Optional[str] = None) -> dict:
        """Get existing session or create a new one."""
        if session_id:
            session = self.get_session(session_id)
            if session:
                return session
            logger.info(f"Session {session_id} not found, creating new session")
        
        # Create new session
        new_session_id = self.create_session(customer_id)
        return self.get_session(new_session_id)
    
    def update_session(self, session_id: str, **kwargs):
        """Update session data."""
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                session.update(kwargs)
                session["last_activity"] = datetime.now()
    
    def increment_message_count(self, session_id: str):
        """Increment message count for a session."""
        with self._lock:
            session = self._sessions.get(session_id)
            if session:
                session["message_count"] += 1
    
    def cleanup_expired_sessions(self):
        """Remove all expired sessions."""
        with self._lock:
            now = datetime.now()
            expired = [
                sid for sid, session in self._sessions.items()
                if now - session["last_activity"] > self._session_timeout
            ]
            
            for sid in expired:
                del self._sessions[sid]
                logger.info(f"Cleaned up expired session: {sid}")
            
            if expired:
                logger.info(f"Cleaned up {len(expired)} expired sessions")
    
    def get_session_count(self) -> int:
        """Get the number of active sessions."""
        with self._lock:
            return len(self._sessions)


# Global session manager instance
session_manager = SessionManager()

