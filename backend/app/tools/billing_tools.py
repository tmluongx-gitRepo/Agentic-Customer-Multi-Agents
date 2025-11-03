"""
Billing support tools for Hybrid RAG/CAG approach.
Combines session-cached static policies with dynamic billing data retrieval.
"""
from langchain.tools import tool
from app.utils.vector_store import vector_store_manager
import logging

logger = logging.getLogger(__name__)


# Session-based cache for static billing policies
SESSION_BILLING_POLICIES = {}


@tool
def search_billing_info(query: str, session_id: str = "default") -> str:
    """
    Search for billing information including invoices, pricing, and policies.
    Uses hybrid RAG/CAG: fetches dynamic data, caches static policies per session.
    
    Args:
        query: The billing question or search query
        session_id: Session ID for caching policies
    
    Returns:
        Combined static policies and dynamic billing data
    """
    global SESSION_BILLING_POLICIES
    
    vectorstore = vector_store_manager.get_billing_store()
    
    if vectorstore is None:
        return "Billing information is currently unavailable. Please try again later or contact support."
    
    try:
        # Check if we need to cache static policies for this session
        if session_id not in SESSION_BILLING_POLICIES:
            logger.info(f"Caching billing policies for session: {session_id}")
            try:
                policy_docs = vectorstore.similarity_search(
                    "billing policies refund terms payment",
                    k=3,
                    filter={"type": "static"}
                )
                SESSION_BILLING_POLICIES[session_id] = "\n\n".join(
                    doc.page_content for doc in policy_docs
                )
            except Exception as e:
                logger.warning(f"Could not fetch static policies: {e}")
                SESSION_BILLING_POLICIES[session_id] = ""
        
        # Always fetch dynamic data (invoices, current pricing)
        try:
            dynamic_docs = vectorstore.similarity_search(
                query,
                k=3,
                filter={"type": "dynamic"}
            )
            dynamic_context = "\n\n".join(doc.page_content for doc in dynamic_docs)
        except Exception as e:
            logger.warning(f"Could not fetch dynamic billing data: {e}")
            # Fall back to general search without filter
            dynamic_docs = vectorstore.similarity_search(query, k=3)
            dynamic_context = "\n\n".join(doc.page_content for doc in dynamic_docs)
        
        # Combine cached policies + fresh dynamic data
        result = ""
        if SESSION_BILLING_POLICIES[session_id]:
            result += f"BILLING POLICIES (cached):\n{SESSION_BILLING_POLICIES[session_id]}\n\n"
        
        if dynamic_context:
            result += f"CURRENT BILLING DATA:\n{dynamic_context}"
        
        return result if result else "No relevant billing information found."
        
    except Exception as e:
        logger.error(f"Error in search_billing_info: {e}")
        return f"Error retrieving billing information: {str(e)}"


@tool
def calculate_price(product: str, quantity: int = 1) -> str:
    """
    Calculate pricing for products and services.
    
    Args:
        product: Product name (e.g., 'basic_plan', 'pro_plan', 'enterprise_plan')
        quantity: Quantity to calculate (default: 1)
    
    Returns:
        Formatted price calculation
    """
    # Mock pricing data - replace with actual pricing logic/database
    pricing = {
        "basic_plan": 9.99,
        "pro_plan": 29.99,
        "enterprise_plan": 99.99,
        "addon_storage": 5.00,
        "addon_users": 10.00,
    }
    
    product_lower = product.lower().replace(" ", "_")
    
    if product_lower in pricing:
        unit_price = pricing[product_lower]
        total_price = unit_price * quantity
        return f"Price for {quantity}x {product}: ${total_price:.2f} (${unit_price:.2f} per unit)"
    else:
        available = ", ".join(pricing.keys())
        return f"Product '{product}' not found. Available products: {available}"

