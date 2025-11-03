"""
Policy & Compliance tools for Pure CAG (Context-Augmented Generation).
Loads static policy documents directly into context.
"""
from pathlib import Path
from app.config import settings
import logging

logger = logging.getLogger(__name__)


# Global storage for policy documents
POLICY_DOCUMENTS = {}
POLICY_CONTEXT = ""


def load_policy_documents() -> dict:
    """
    Load all static policy documents into memory.
    This is done once at startup for Pure CAG approach.
    """
    global POLICY_DOCUMENTS, POLICY_CONTEXT
    
    policies = {}
    policies_path = Path(settings.policies_path)
    
    logger.info(f"Loading policy documents from {policies_path}")
    
    # Define policy files
    policy_files = {
        "terms": "terms_of_service.txt",
        "privacy": "privacy_policy.txt",
        "compliance": "compliance_guidelines.txt",
        "data_handling": "data_handling.txt"
    }
    
    for key, filename in policy_files.items():
        file_path = policies_path / filename
        try:
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    policies[key] = f.read()
                logger.info(f"Loaded policy: {filename}")
            else:
                logger.warning(f"Policy file not found: {file_path}")
                policies[key] = f"[{filename} not available]"
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            policies[key] = f"[Error loading {filename}]"
    
    POLICY_DOCUMENTS = policies
    
    # Create combined context for agent
    POLICY_CONTEXT = f"""
TERMS OF SERVICE:
{policies['terms']}

PRIVACY POLICY:
{policies['privacy']}

COMPLIANCE GUIDELINES:
{policies['compliance']}

DATA HANDLING POLICY:
{policies['data_handling']}
"""
    
    logger.info("Policy documents loaded successfully")
    return policies


def get_policy_context() -> str:
    """Get the combined policy context for the agent."""
    return POLICY_CONTEXT


def get_policy_documents() -> dict:
    """Get individual policy documents."""
    return POLICY_DOCUMENTS

