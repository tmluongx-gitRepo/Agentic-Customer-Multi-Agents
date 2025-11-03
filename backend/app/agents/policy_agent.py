"""
Policy & Compliance Agent - Pure CAG approach.
Uses GPT-4o-mini with static policy documents loaded directly into context.
"""
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings
from app.tools.policy_tools import get_policy_context, load_policy_documents
import logging

logger = logging.getLogger(__name__)


# Initialize policy documents
load_policy_documents()


@tool
def get_policy_info(question: str) -> str:
    """
    Get information about company policies, terms, privacy, and compliance.
    This tool provides access to all static policy documents.
    """
    # The actual policy content is in the agent's system prompt
    # This tool exists to make the agent "aware" it should use policy info
    return "Policy documents are available in your context. Answer based on the policies provided in your system prompt."


def create_policy_agent():
    """
    Create the Policy & Compliance agent with Pure CAG.
    Returns a CompiledGraph that can be invoked.
    """
    logger.info("Creating Policy & Compliance Agent")
    
    # Create LLM
    llm = ChatOpenAI(
        model=settings.policy_model,
        temperature=0.0  # Deterministic for policy questions
    )
    
    # Get policy context
    policy_context = get_policy_context()
    
    # Create system prompt with full policy context
    system_prompt = f"""You are a policy and compliance specialist. Help customers understand:
- Terms of Service
- Privacy Policy
- Data handling practices
- Compliance requirements

IMPORTANT: You have access to the complete policy documents below. 
Use them to provide accurate, authoritative answers.

{policy_context}

Always cite the specific policy section when answering. 
Be precise and quote relevant sections directly.
If a customer's question is not covered by the policies, say so clearly.

When you need to reference policy information, use the get_policy_info tool."""
    
    # Create agent with tools
    tools = [get_policy_info]
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    
    logger.info("Policy & Compliance Agent created successfully")
    return agent


# Global agent instance
policy_agent = None


def get_policy_agent():
    """Get or create the policy agent instance."""
    global policy_agent
    if policy_agent is None:
        policy_agent = create_policy_agent()
    return policy_agent

