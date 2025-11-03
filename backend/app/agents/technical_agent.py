"""
Technical Support Agent - Pure RAG approach.
Uses GPT-4o with vector retrieval from dynamic technical knowledge base.
"""
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from app.config import settings
from app.tools.technical_tools import search_knowledge_base, search_bug_reports
import logging

logger = logging.getLogger(__name__)


def create_technical_agent():
    """
    Create the Technical Support agent with Pure RAG.
    Returns a CompiledGraph that can be invoked.
    """
    logger.info("Creating Technical Support Agent")
    
    # Create LLM
    llm = ChatOpenAI(
        model=settings.technical_model,
        temperature=0.1  # Slightly creative for explanations
    )
    
    # Create system prompt
    system_prompt = """You are a technical support specialist. Help customers with:
- Troubleshooting technical issues
- Feature explanations and how-to guides
- Bug reports and known issues
- Technical questions about the product

Use search_knowledge_base for general technical questions.
Use search_bug_reports when customers report errors or bugs.
Provide clear, step-by-step solutions.
Include all relevant technical details in your final response.

Be patient, thorough, and technical when needed, but explain things clearly.
Always check the knowledge base before answering."""
    
    # Create agent with tools
    tools = [search_knowledge_base, search_bug_reports]
    agent = create_react_agent(llm, tools, prompt=system_prompt)
    
    logger.info("Technical Support Agent created successfully")
    return agent


# Global agent instance
technical_agent = None


def get_technical_agent():
    """Get or create the technical agent instance."""
    global technical_agent
    if technical_agent is None:
        technical_agent = create_technical_agent()
    return technical_agent

