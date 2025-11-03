"""
Supervisor Agent - Routes queries to specialized worker agents.
Uses GPT-4o-mini for fast, cost-effective routing decisions.
"""
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings
from app.agents.billing_agent import get_billing_agent
from app.agents.technical_agent import get_technical_agent
from app.agents.policy_agent import get_policy_agent
import logging

logger = logging.getLogger(__name__)


@tool
def billing_support(request: str) -> str:
    """Handle billing, pricing, invoices, payments, and refund questions."""
    logger.info("Routing to Billing Support Agent")
    agent = get_billing_agent()
    try:
        result = agent.invoke({"messages": [("user", request)]})
        # Extract last AI message
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            if hasattr(last_msg, 'content'):
                return last_msg.content
        return "No response from billing agent"
    except Exception as e:
        logger.error(f"Error in billing_support: {e}", exc_info=True)
        return f"I encountered an error processing your billing question. Please try rephrasing or contact support."


@tool
def technical_support(request: str) -> str:
    """Handle technical issues, troubleshooting, features, and how-to questions."""
    logger.info("Routing to Technical Support Agent")
    agent = get_technical_agent()
    try:
        result = agent.invoke({"messages": [("user", request)]})
        # Extract last AI message
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            if hasattr(last_msg, 'content'):
                return last_msg.content
        return "No response from technical agent"
    except Exception as e:
        logger.error(f"Error in technical_support: {e}", exc_info=True)
        return f"I encountered an error processing your technical question. Please try rephrasing or contact support."


@tool
def policy_support(request: str) -> str:
    """Handle questions about terms of service, privacy policy, data handling, and compliance."""
    logger.info("Routing to Policy & Compliance Agent")
    agent = get_policy_agent()
    try:
        result = agent.invoke({"messages": [("user", request)]})
        # Extract last AI message
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            if hasattr(last_msg, 'content'):
                return last_msg.content
        return "No response from policy agent"
    except Exception as e:
        logger.error(f"Error in policy_support: {e}", exc_info=True)
        return f"I encountered an error processing your policy question. Please try rephrasing or contact support."


def create_supervisor_agent():
    """
    Create the Supervisor agent that routes to specialized workers.
    Returns a CompiledGraph that can be invoked.
    """
    logger.info("Creating Supervisor Agent")
    
    # Create LLM
    llm = ChatOpenAI(
        model=settings.supervisor_model,
        temperature=0.0  # Deterministic routing
    )
    
    # Create system prompt
    system_prompt = """You are a customer service supervisor. Analyze incoming queries and route them to the appropriate specialist:

- billing_support: Questions about pricing, invoices, payments, refunds, billing cycles
- technical_support: Questions about features, bugs, troubleshooting, how-to, technical issues
- policy_support: Questions about terms of service, privacy policy, data handling, compliance

If the query spans multiple domains, choose the PRIMARY domain.
Be decisive and route efficiently.

After routing to a specialist and receiving their response, provide that response to the user.
Do not add unnecessary commentary - just ensure the customer gets the specialist's answer."""
    
    # Create agent with routing tools
    tools = [billing_support, technical_support, policy_support]
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    
    logger.info("Supervisor Agent created successfully")
    return agent


# Global agent instance
supervisor_agent = None


def get_supervisor_agent():
    """Get or create the supervisor agent instance."""
    global supervisor_agent
    if supervisor_agent is None:
        supervisor_agent = create_supervisor_agent()
    return supervisor_agent

