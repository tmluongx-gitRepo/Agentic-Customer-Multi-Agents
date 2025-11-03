"""
Technical support tools for Pure RAG approach.
Retrieves information from dynamic technical knowledge base.
"""
from langchain.tools import tool
from app.utils.vector_store import vector_store_manager
import logging

logger = logging.getLogger(__name__)


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search technical documentation, bug reports, and forum discussions.
    Use this for troubleshooting, how-to questions, and feature information.
    
    Args:
        query: The technical question or search query
    
    Returns:
        Relevant technical documentation with source attribution
    """
    vectorstore = vector_store_manager.get_technical_store()
    
    if vectorstore is None:
        return "Technical knowledge base is currently unavailable. Please try again later."
    
    try:
        # Use MMR for diverse results (avoid duplicate similar docs)
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 5,              # Return 5 documents
                "fetch_k": 20,       # Consider top 20 candidates
                "lambda_mult": 0.7   # Balance relevance vs. diversity
            }
        )
        
        docs = retriever.invoke(query)
        
        if not docs:
            return "No relevant technical documentation found for your query."
        
        # Format with source attribution
        formatted_results = []
        for doc in docs:
            source = doc.metadata.get("source", "Unknown")
            content = doc.page_content
            formatted_results.append(f"[Source: {source}]\n{content}")
        
        return "\n\n---\n\n".join(formatted_results)
        
    except Exception as e:
        logger.error(f"Error in search_knowledge_base: {e}")
        return f"Error searching knowledge base: {str(e)}"


@tool
def search_bug_reports(query: str) -> str:
    """
    Search known bugs and their status. Use for error messages and bug-related questions.
    
    Args:
        query: Error message or bug description
    
    Returns:
        Matching bug reports with status
    """
    vectorstore = vector_store_manager.get_technical_store()
    
    if vectorstore is None:
        return "Bug report database is currently unavailable. Please try again later."
    
    try:
        # Search specifically in bug report documents
        docs = vectorstore.similarity_search(
            query,
            k=3,
            filter={"doc_type": "bug_report"}
        )
        
        if not docs:
            # Try without filter if no filtered results
            docs = vectorstore.similarity_search(query, k=3)
            if not docs:
                return "No matching bug reports found."
        
        formatted_bugs = []
        for doc in docs:
            bug_id = doc.metadata.get("bug_id", "Unknown")
            status = doc.metadata.get("status", "Unknown")
            formatted_bugs.append(
                f"Bug ID: {bug_id} | Status: {status}\n{doc.page_content}"
            )
        
        return "\n\n".join(formatted_bugs)
        
    except Exception as e:
        logger.error(f"Error in search_bug_reports: {e}")
        # Fall back to general search
        try:
            docs = vectorstore.similarity_search(query, k=3)
            return "\n\n".join(f"Bug: {doc.page_content}" for doc in docs)
        except:
            return f"Error searching bug reports: {str(e)}"

