"""
Billing Support Agent - Hybrid RAG/CAG approach.
Uses GPT-4o with session-cached policies and dynamic billing data.
"""
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings
from app.tools.billing_tools import search_billing_info, calculate_price
import logging

logger = logging.getLogger(__name__)


def create_billing_agent():
    """
    Create the Billing Support agent with Hybrid RAG/CAG.
    Returns a CompiledGraph that can be invoked.
    """
    logger.info("Creating Billing Support Agent")
    
    # Create LLM
    llm = ChatOpenAI(
        model=settings.billing_model,
        temperature=0.1  # Slightly creative for explanations
    )
    
    # Create system prompt
    system_prompt = """You are a billing support specialist. Help customers with:
- Invoice questions
- Pricing information
- Payment and refund inquiries
- Billing policies

Use search_billing_info for policy and invoice lookups. 
Use calculate_price for pricing calculations.
Always include all relevant details in your final response.

Be friendly, professional, and clear in your explanations.
If you need to look up information, use the appropriate tool."""
    
    # Create agent with tools
    tools = [search_billing_info, calculate_price]
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    
    logger.info("Billing Support Agent created successfully")
    return agent


# Global agent instance
billing_agent = None


def get_billing_agent():
    """Get or create the billing agent instance."""
    global billing_agent
    if billing_agent is None:
        billing_agent = create_billing_agent()
    return billing_agent

