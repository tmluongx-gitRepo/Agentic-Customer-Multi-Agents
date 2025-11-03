"""
LangGraph state definitions for the multi-agent customer service system.
"""
from typing import Annotated, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class CustomerServiceState(TypedDict):
    """
    State for the customer service multi-agent system.
    
    This state is passed through the LangGraph workflow and maintains
    conversation context, session information, and routing history.
    """
    # Messages using LangGraph's message handling
    messages: Annotated[list[BaseMessage], add_messages]
    
    # Session information
    session_id: str
    customer_id: Optional[str]
    
    # Caching for Hybrid RAG/CAG
    cached_billing_policies: Optional[str]
    
    # Routing history for debugging and analytics
    routing_history: list[str]
    
    # Current agent being invoked
    current_agent: Optional[str]

