# Customer Service Multi-Agent System

**LangChain Version:** v1.0+  
**Documentation:** https://docs.langchain.com/oss/python/langchain/multi-agent  
**Project Specification:** ../agentic-customer-specs.md  
**Last Updated:** November 3, 2025

Build an intelligent customer service system using a supervisor agent that routes queries to specialized worker agents, each optimized with different retrieval strategies.

---

## What is This System?

This is a **practical implementation of a multi-agent architecture** for customer service. A supervisor agent analyzes incoming customer queries and intelligently routes them to one of three specialized worker agents:

- **Billing Support Agent** - Handles pricing and invoice questions
- **Technical Support Agent** - Answers technical questions from a knowledge base
- **Policy & Compliance Agent** - Provides fast answers about terms, policies, and compliance

**Key Innovation:** Each agent uses a different **retrieval strategy** (RAG, CAG, or Hybrid) optimized for its specific domain and data characteristics.

---

## When to Use This Architecture

**Use this pattern when:**
- You have distinct customer service domains (billing, technical, policy)
- Different domains need different retrieval strategies
- You want to optimize cost vs. quality trade-offs across agents
- You need centralized routing with specialized expertise

**Benefits:**
- **Specialization** - Each agent focuses on one domain with optimized tools
- **Cost Optimization** - Use cheaper models for routing, premium models for complex responses
- **Scalability** - Easy to add new specialized agents
- **Strategic RAG** - Match retrieval strategy to data characteristics

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                         User Query                            │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│               Supervisor Agent                                 │
│         (OpenAI GPT-4o-mini)                                  │
│                                                                │
│  Analyzes query intent and routes to appropriate agent        │
└───────┬──────────────────┬────────────────────┬──────────────┘
        │                  │                    │
        ▼                  ▼                    ▼
┌───────────────┐  ┌───────────────┐  ┌────────────────────┐
│ Billing Agent │  │Technical Agent│  │ Policy Agent       │
│ (GPT-4o)      │  │ (GPT-4o)      │  │ (GPT-4o-mini)      │
│               │  │               │  │                    │
│ Hybrid        │  │ Pure RAG      │  │ Pure CAG           │
│ RAG/CAG       │  │               │  │                    │
└───────────────┘  └───────────────┘  └────────────────────┘
```

---

## Agent Comparison Table

| Agent | Model | Retrieval Strategy | Data Type | Use Case |
|-------|-------|-------------------|-----------|----------|
| **Supervisor** | OpenAI GPT-4o-mini | None | N/A | Fast, cost-effective routing |
| **Billing Support** | OpenAI GPT-4o | Hybrid RAG/CAG | Mixed (dynamic + static) | Pricing, invoices, billing policies |
| **Technical Support** | OpenAI GPT-4o | Pure RAG | Dynamic | Docs, bugs, forum posts |
| **Policy & Compliance** | OpenAI GPT-4o-mini | Pure CAG | Static | ToS, Privacy Policy, compliance |

---

## Supervisor Agent Implementation

The supervisor is the **entry point** for all customer queries. Its job is to analyze the query and route it to the appropriate specialist.

### Why OpenAI GPT-4o-mini for Supervisor?

- **Cost-effective** - Routing is a simple classification task, doesn't need full GPT-4o
- **Fast** - Lower latency for decision making
- **Sufficient** - GPT-4o-mini handles classification and routing well

### Supervisor Setup

```python
from langchain.agents import create_agent
from langchain.tools import tool

# Create supervisor agent with OpenAI GPT-4o-mini
supervisor = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],  # Tools added after creating worker agents
    system_prompt=(
        "You are a customer service supervisor. Analyze incoming queries and route them to the appropriate specialist:\n\n"
        "- Billing Support: Questions about pricing, invoices, payments, refunds, billing cycles\n"
        "- Technical Support: Questions about features, bugs, troubleshooting, how-to, technical issues\n"
        "- Policy & Compliance: Questions about terms of service, privacy policy, data handling, compliance\n\n"
        "If the query spans multiple domains, choose the PRIMARY domain. "
        "Be decisive and route efficiently."
    ),
    name="supervisor"
)
```

### Key Points

1. **Clear routing criteria** - System prompt explicitly defines each agent's domain
2. **Fast model** - GPT-4o-mini is sufficient for classification
3. **Decisive routing** - Instructs supervisor to pick one agent, not multiple
4. **Cost optimization** - Uses mini model for simple routing tasks

---

## Billing Support Agent (Hybrid RAG/CAG)

### Strategy: Hybrid RAG/CAG

The Billing Support Agent uses a **hybrid approach**:
1. **First query in session**: RAG lookup for dynamic data (invoices, pricing)
2. **Session caching**: Store static billing policies in session state
3. **Subsequent queries**: Use cached policies (CAG) + fresh dynamic data if needed

### Why Hybrid?

- **Static policies** don't change (refund policy, billing terms) → Cache once
- **Dynamic data** changes frequently (customer invoices, current pricing) → Fetch each time
- **Best of both worlds**: Fast responses + up-to-date information

### Implementation

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import Annotated
from langchain.tools import ToolRuntime
from langchain.agents import AgentState

# Load billing vector store
billing_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
billing_vectorstore = Chroma(
    persist_directory="./chroma_db/billing",
    embedding_function=billing_embeddings,
    collection_name="billing"
)

# Session cache for static policies (initialized once per session)
SESSION_BILLING_POLICIES = None

@tool
def search_billing_info(
    query: str,
    runtime: ToolRuntime[None, AgentState]
) -> str:
    """
    Search for billing information including invoices, pricing, and policies.
    Uses hybrid RAG/CAG: fetches dynamic data, caches static policies.
    """
    global SESSION_BILLING_POLICIES
    
    # On first use, cache static policies
    if SESSION_BILLING_POLICIES is None:
        policy_docs = billing_vectorstore.similarity_search(
            "billing policies refund terms payment",
            k=3,
            filter={"type": "policy"}  # Filter for static policy documents
        )
        SESSION_BILLING_POLICIES = "\n\n".join(doc.page_content for doc in policy_docs)
    
    # Always fetch dynamic data (invoices, current pricing)
    dynamic_docs = billing_vectorstore.similarity_search(
        query,
        k=3,
        filter={"type": "dynamic"}  # Filter for dynamic documents
    )
    dynamic_context = "\n\n".join(doc.page_content for doc in dynamic_docs)
    
    # Combine cached policies + fresh dynamic data
    return f"BILLING POLICIES (cached):\n{SESSION_BILLING_POLICIES}\n\nCURRENT DATA:\n{dynamic_context}"

@tool
def calculate_price(product: str, quantity: int) -> str:
    """Calculate pricing for products and services."""
    # Mock implementation - replace with actual pricing logic
    pricing = {
        "basic_plan": 9.99,
        "pro_plan": 29.99,
        "enterprise_plan": 99.99
    }
    price = pricing.get(product, 0) * quantity
    return f"Price for {quantity}x {product}: ${price:.2f}"

# Create Billing Support Agent
billing_agent = create_agent(
    model="openai:gpt-4o",
    tools=[search_billing_info, calculate_price],
    system_prompt=(
        "You are a billing support specialist. Help customers with:\n"
        "- Invoice questions\n"
        "- Pricing information\n"
        "- Payment and refund inquiries\n"
        "- Billing policies\n\n"
        "Use search_billing_info for policy and invoice lookups. "
        "Use calculate_price for pricing calculations. "
        "Always include all relevant details in your final response."
    ),
    name="billing_agent"
)

# Wrap as tool for supervisor
@tool
def billing_support(request: str) -> str:
    """Handle billing, pricing, invoices, payments, and refund questions."""
    result = billing_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].content
```

### Key Features

1. **Session caching** - Policies loaded once, reused for session
2. **Metadata filtering** - Separates static vs. dynamic documents
3. **Hybrid context** - Combines cached + fresh information
4. **OpenAI GPT-4o** - High-quality responses for complex billing questions

---

## Technical Support Agent (Pure RAG)

### Strategy: Pure RAG

The Technical Support Agent uses **pure RAG** because technical documentation is:
- **Frequently updated** (bug fixes, new features, forum discussions)
- **Query-specific** (need different docs for different problems)
- **Large and diverse** (can't cache everything efficiently)

### Why Pure RAG?

- Technical knowledge base changes frequently
- Each query needs different, specific documentation
- Vector search finds the most relevant docs for each question
- No benefit from caching (too much content, too dynamic)

### Implementation

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Load technical knowledge base
tech_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
tech_vectorstore = Chroma(
    persist_directory="./chroma_db/technical",
    embedding_function=tech_embeddings,
    collection_name="technical"
)

@tool
def search_knowledge_base(query: str) -> str:
    """
    Search technical documentation, bug reports, and forum discussions.
    Use this for troubleshooting, how-to questions, and feature information.
    """
    # Use MMR for diverse results (avoid duplicate similar docs)
    retriever = tech_vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 5,              # Return 5 documents
            "fetch_k": 20,       # Consider top 20 candidates
            "lambda_mult": 0.7   # Balance relevance vs. diversity
        }
    )
    
    docs = retriever.invoke(query)
    
    # Format with source attribution
    formatted_results = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        content = doc.page_content
        formatted_results.append(f"[Source: {source}]\n{content}")
    
    return "\n\n---\n\n".join(formatted_results)

@tool
def search_bug_reports(query: str) -> str:
    """Search known bugs and their status. Use for error messages and bug-related questions."""
    # Search specifically in bug report documents
    docs = tech_vectorstore.similarity_search(
        query,
        k=3,
        filter={"doc_type": "bug_report"}
    )
    
    if not docs:
        return "No matching bug reports found."
    
    return "\n\n".join(f"Bug: {doc.page_content}" for doc in docs)

# Create Technical Support Agent
technical_agent = create_agent(
    model="openai:gpt-4o",
    tools=[search_knowledge_base, search_bug_reports],
    system_prompt=(
        "You are a technical support specialist. Help customers with:\n"
        "- Troubleshooting technical issues\n"
        "- Feature explanations and how-to guides\n"
        "- Bug reports and known issues\n"
        "- Technical questions about the product\n\n"
        "Use search_knowledge_base for general technical questions. "
        "Use search_bug_reports when customers report errors or bugs. "
        "Provide clear, step-by-step solutions. "
        "Include all relevant technical details in your final response."
    ),
    name="technical_agent"
)

# Wrap as tool for supervisor
@tool
def technical_support(request: str) -> str:
    """Handle technical issues, troubleshooting, features, and how-to questions."""
    result = technical_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].content
```

### Key Features

1. **MMR retrieval** - Diverse results avoid redundant similar docs
2. **Source attribution** - Shows which doc each answer comes from
3. **Multiple search tools** - General knowledge base + specific bug reports
4. **Fresh every time** - Always queries vector store for latest info
5. **OpenAI GPT-4o** - Complex technical reasoning capability

---

## Policy & Compliance Agent (Pure CAG)

### Strategy: Pure CAG (Context-Augmented Generation)

The Policy & Compliance Agent uses **pure CAG** because:
- **Static documents** - Terms of Service and Privacy Policy rarely change
- **Small corpus** - Can load entire policy docs into context
- **Fast responses** - No vector search latency
- **Consistency** - Same context every time ensures consistent answers

### Why Pure CAG?

- Policy documents are static (change infrequently)
- Small enough to fit in context window
- No need for vector search overhead
- Faster responses for common policy questions
- More cost-effective with Bedrock

### Implementation

```python
from langchain.agents import create_agent
from langchain.tools import tool
import os

# Load static policy documents at startup (one-time operation)
def load_policy_documents():
    """Load all static policy documents into memory."""
    policies = {}
    
    # Load Terms of Service
    with open("./data/policies/terms_of_service.txt", "r") as f:
        policies["terms"] = f.read()
    
    # Load Privacy Policy
    with open("./data/policies/privacy_policy.txt", "r") as f:
        policies["privacy"] = f.read()
    
    # Load Compliance Guidelines
    with open("./data/policies/compliance_guidelines.txt", "r") as f:
        policies["compliance"] = f.read()
    
    # Load Data Handling Policy
    with open("./data/policies/data_handling.txt", "r") as f:
        policies["data_handling"] = f.read()
    
    return policies

# Load once at startup
POLICY_DOCUMENTS = load_policy_documents()

# Create combined context for agent
POLICY_CONTEXT = f"""
TERMS OF SERVICE:
{POLICY_DOCUMENTS['terms']}

PRIVACY POLICY:
{POLICY_DOCUMENTS['privacy']}

COMPLIANCE GUIDELINES:
{POLICY_DOCUMENTS['compliance']}

DATA HANDLING POLICY:
{POLICY_DOCUMENTS['data_handling']}
"""

@tool
def get_policy_info(question: str) -> str:
    """
    Get information about company policies, terms, privacy, and compliance.
    This tool provides access to all static policy documents.
    """
    # Note: The actual policy content is in the agent's system prompt
    # This tool exists to make the agent "aware" it should use policy info
    return "Policy documents are available in your context. Answer based on the policies provided."

# Create Policy & Compliance Agent with CAG
policy_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_policy_info],
    system_prompt=(
        f"You are a policy and compliance specialist. Help customers understand:\n"
        f"- Terms of Service\n"
        f"- Privacy Policy\n"
        f"- Data handling practices\n"
        f"- Compliance requirements\n\n"
        f"IMPORTANT: You have access to the complete policy documents below. "
        f"Use them to provide accurate, authoritative answers.\n\n"
        f"{POLICY_CONTEXT}\n\n"
        f"Always cite the specific policy section when answering. "
        f"Be precise and quote relevant sections directly."
    ),
    name="policy_agent"
)

# Wrap as tool for supervisor
@tool
def policy_support(request: str) -> str:
    """Handle questions about terms of service, privacy policy, data handling, and compliance."""
    result = policy_agent.invoke({
        "messages": [{"role": "user", "content": request}]
    })
    return result["messages"][-1].content
```

### Key Features

1. **No vector search** - Documents loaded directly into context
2. **Fast responses** - No retrieval latency
3. **Consistent answers** - Same context every time
4. **OpenAI GPT-4o-mini** - Cost-effective for simple policy queries
5. **Direct quotes** - Agent instructed to cite specific policy sections

### CAG vs RAG Trade-offs

| Aspect | CAG (This Agent) | RAG |
|--------|------------------|-----|
| **Speed** | Faster (no search) | Slower (vector search) |
| **Cost** | Lower (GPT-4o-mini) | Higher (GPT-4o + embeddings) |
| **Consistency** | Perfect | Depends on retrieval |
| **Context size** | Limited by LLM | Unlimited corpus |
| **Best for** | Static, small docs | Dynamic, large docs |

---

## Retrieval Strategy Deep Dive

### Pure RAG (Technical Support)

**When to use:**
- Frequently updated content (docs, bug reports, forums)
- Large corpus that can't fit in context
- Query-specific information needs
- Content changes regularly

**Implementation pattern:**
```python
@tool
def search_tool(query: str) -> str:
    docs = vectorstore.similarity_search(query, k=5)
    return "\n\n".join(doc.page_content for doc in docs)
```

**Benefits:**
- Always up-to-date
- Scales to large knowledge bases
- Retrieves only relevant information

**Trade-offs:**
- Vector search latency
- Embedding costs
- Query quality affects results

---

### Pure CAG (Policy & Compliance)

**When to use:**
- Static documents that rarely change
- Small corpus that fits in context window
- Need consistent responses
- Speed is critical

**Implementation pattern:**
```python
# Load once at startup
STATIC_DOCS = load_documents()

agent = create_agent(
    model="openai:gpt-4o-mini",
    system_prompt=f"Use this context:\n\n{STATIC_DOCS}\n\nAnswer questions based on it."
)
```

**Benefits:**
- No search latency
- Lower cost (no embeddings)
- Perfectly consistent
- Simple implementation

**Trade-offs:**
- Limited by context window size
- Not suitable for dynamic content
- Manual updates needed

---

### Hybrid RAG/CAG (Billing Support)

**When to use:**
- Mix of static and dynamic content
- Some information rarely changes (policies, terms)
- Other information changes frequently (invoices, pricing)
- Want to optimize for both speed and freshness

**Implementation pattern:**
```python
# Cache static content once per session
SESSION_CACHE = None

@tool
def hybrid_search(query: str) -> str:
    global SESSION_CACHE
    
    # Load static content once
    if SESSION_CACHE is None:
        static_docs = vectorstore.similarity_search(
            "policies terms",
            filter={"type": "static"}
        )
        SESSION_CACHE = "\n\n".join(doc.page_content for doc in static_docs)
    
    # Always fetch dynamic content
    dynamic_docs = vectorstore.similarity_search(
        query,
        filter={"type": "dynamic"}
    )
    dynamic_context = "\n\n".join(doc.page_content for doc in dynamic_docs)
    
    return f"STATIC:\n{SESSION_CACHE}\n\nDYNAMIC:\n{dynamic_context}"
```

**Benefits:**
- Best of both worlds
- Fast for cached content
- Fresh for dynamic data
- Efficient resource usage

**Trade-offs:**
- More complex implementation
- Requires metadata tagging (static vs dynamic)
- Cache management overhead

---

## Data Ingestion Pipeline

The multi-agent system requires properly structured data in ChromaDB. Here's how to set it up:

### Pipeline Overview

```python
"""
ingest_data.py - Data Ingestion Pipeline
Processes documents and loads them into ChromaDB with proper metadata
"""
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os

def ingest_billing_data():
    """Ingest billing documents with metadata tagging."""
    # Load documents
    loader = DirectoryLoader(
        "./data/billing/",
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    documents = loader.load()
    
    # Add metadata to distinguish static vs dynamic
    for doc in documents:
        # Tag static policy documents
        if "policy" in doc.metadata["source"].lower():
            doc.metadata["type"] = "static"
        else:
            doc.metadata["type"] = "dynamic"
    
    # Split documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    
    # Create embeddings and store
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db/billing",
        collection_name="billing"
    )
    
    print(f"Ingested {len(chunks)} billing document chunks")

def ingest_technical_data():
    """Ingest technical documentation."""
    loader = DirectoryLoader(
        "./data/technical/",
        glob="**/*.md",
        loader_cls=TextLoader
    )
    documents = loader.load()
    
    # Add doc_type metadata
    for doc in documents:
        if "bug" in doc.metadata["source"].lower():
            doc.metadata["doc_type"] = "bug_report"
        elif "forum" in doc.metadata["source"].lower():
            doc.metadata["doc_type"] = "forum"
        else:
            doc.metadata["doc_type"] = "documentation"
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db/technical",
        collection_name="technical"
    )
    
    print(f"Ingested {len(chunks)} technical document chunks")

def prepare_policy_documents():
    """Prepare static policy documents (no vector store needed)."""
    # Policy documents are loaded directly as plain text
    # No embeddings or vector store required
    print("Policy documents ready for CAG (no vector store needed)")

if __name__ == "__main__":
    print("Starting data ingestion...")
    ingest_billing_data()
    ingest_technical_data()
    prepare_policy_documents()
    print("Data ingestion complete!")
```

### Key Points

1. **Metadata tagging** - Essential for filtering (static vs dynamic, doc types)
2. **Separate collections** - Each agent has its own ChromaDB collection
3. **Consistent embedding model** - Use same model for ingestion and retrieval
4. **Policy documents** - Don't need vector store (CAG approach)

---

## Complete System Integration

Now let's put it all together into a working customer service system:

```python
"""
customer_service_system.py - Complete Multi-Agent Customer Service
"""
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import Annotated
from langchain.tools import InjectedToolCallId
from langgraph.types import Command
from langchain_core.messages import ToolMessage

# Initialize all agents (using code from previous sections)
# ... [Billing agent setup] ...
# ... [Technical agent setup] ...
# ... [Policy agent setup] ...

# Create supervisor with all worker agents as tools
supervisor = create_agent(
    model="openai:gpt-4o-mini",
    tools=[billing_support, technical_support, policy_support],
    system_prompt=(
        "You are a customer service supervisor. Analyze queries and route to specialists:\n\n"
        "- billing_support: Pricing, invoices, payments, refunds, billing\n"
        "- technical_support: Features, bugs, troubleshooting, how-to, technical issues\n"
        "- policy_support: Terms, privacy, data handling, compliance\n\n"
        "Route decisively to ONE specialist. If unclear, make your best judgment."
    ),
    name="supervisor"
)

def handle_customer_query(query: str, session_id: str = None) -> dict:
    """
    Main entry point for customer service queries.
    
    Args:
        query: Customer question
        session_id: Optional session ID for maintaining conversation history
    
    Returns:
        dict with response and routing information
    """
    # Invoke supervisor
    result = supervisor.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    # Extract response
    response = result["messages"][-1].content
    
    # Determine which agent was called (from tool calls in messages)
    routed_to = "unknown"
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tool_name = msg.tool_calls[0]["name"]
            routed_to = tool_name.replace("_", " ").title()
    
    return {
        "query": query,
        "response": response,
        "routed_to": routed_to,
        "session_id": session_id
    }

# Example usage
if __name__ == "__main__":
    # Test different types of queries
    test_queries = [
        "What's the refund policy?",
        "How do I reset my password?",
        "What data do you collect about users?",
        "Why was I charged twice this month?",
        "I'm getting error code 500 when uploading files"
    ]
    
    print("=== Customer Service Multi-Agent System ===\n")
    
    for query in test_queries:
        print(f"Customer: {query}")
        result = handle_customer_query(query)
        print(f"Routed to: {result['routed_to']}")
        print(f"Response: {result['response']}\n")
        print("-" * 80 + "\n")
```

---

## Multi-Provider LLM Strategy

One of the key optimizations in this system is the **strategic use of different OpenAI models** to balance cost and performance.

### Model Selection Rationale

| Component | Model | Why |
|-----------|-------|-----|
| **Supervisor** | GPT-4o-mini | Fast, cheap routing decisions - classification is simple |
| **Billing Agent** | GPT-4o | Complex billing logic and calculations require advanced reasoning |
| **Technical Agent** | GPT-4o | Advanced technical reasoning and problem-solving |
| **Policy Agent** | GPT-4o-mini | Simple policy questions from static content - doesn't need full power |

### Cost-Performance Trade-offs

**OpenAI GPT-4o-mini:**
- **Cost:** ~$0.15 per 1M input tokens / $0.60 per 1M output tokens
- **Speed:** Very fast (low latency)
- **Best for:** Classification, routing, simple questions from known content
- **Use in system:** Supervisor routing, policy questions

**OpenAI GPT-4o:**
- **Cost:** ~$2.50 per 1M input tokens / $10.00 per 1M output tokens
- **Speed:** Moderate
- **Best for:** Complex reasoning, technical analysis, calculations
- **Use in system:** Billing and technical support

### Estimated Cost Breakdown

For 1,000 customer queries (assuming average query length):

```
Supervisor (routing): 1,000 queries × 200 tokens × $0.15/1M = $0.03
Billing queries (30%): 300 × 1,500 tokens × $2.50/1M = $1.13
Technical queries (50%): 500 × 1,500 tokens × $2.50/1M = $1.88
Policy queries (20%): 200 × 500 tokens × $0.15/1M = $0.02

Total: ~$3.06 for 1,000 queries
```

**Compared to all-GPT-4o approach:** ~$5.00 (40% more expensive)

### Setup Configuration

```python
import os

# Configure OpenAI
os.environ["OPENAI_API_KEY"] = "your-openai-key"

# Model selection by role
MODELS = {
    "supervisor": "openai:gpt-4o-mini",
    "billing": "openai:gpt-4o",
    "technical": "openai:gpt-4o",
    "policy": "openai:gpt-4o-mini"
}
```

---

## Context Engineering for Customer Service

Controlling information flow between supervisor and workers is critical for quality responses.

### Session State Management

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, MessagesState
from langgraph.graph.message import add_messages

class CustomerServiceState(MessagesState):
    """Extended state for customer service conversations."""
    session_id: str
    customer_id: str
    conversation_history: Annotated[list, add_messages]
    cached_billing_policies: str | None
    routing_history: list[str]

# Initialize state
def create_session_state(customer_id: str) -> CustomerServiceState:
    return {
        "messages": [],
        "session_id": f"session_{customer_id}_{int(time.time())}",
        "customer_id": customer_id,
        "conversation_history": [],
        "cached_billing_policies": None,
        "routing_history": []
    }
```

### Passing Context to Workers

```python
from langchain.tools import ToolRuntime
from langchain.agents import AgentState

@tool
def billing_support(
    request: str,
    runtime: ToolRuntime[None, AgentState]
) -> str:
    """Handle billing questions with full conversation context."""
    
    # Access conversation history from state
    history = runtime.state.get("messages", [])
    
    # Build context for worker agent
    context = f"Customer request: {request}\n\n"
    
    if len(history) > 1:
        context += "Previous conversation:\n"
        for msg in history[-5:]:  # Last 5 messages
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            context += f"{role}: {content}\n"
    
    # Invoke worker with full context
    result = billing_agent.invoke({
        "messages": [{"role": "user", "content": context}]
    })
    
    return result["messages"][-1].content
```

### Best Practices

1. **Conversation history** - Pass last N messages for context
2. **Session caching** - Store frequently used data (policies) per session
3. **Customer metadata** - Include customer ID for personalized responses
4. **Routing history** - Track which agents were called to avoid loops

---

## Implementation Best Practices

### 1. Clear Agent Boundaries

**Do:**
```python
# Clear, non-overlapping domains
billing_agent: "pricing, invoices, payments, refunds"
technical_agent: "features, bugs, troubleshooting, how-to"
policy_agent: "terms, privacy, data handling, compliance"
```

**Avoid:**
```python
# Overlapping or vague domains
agent1: "customer questions"
agent2: "support issues"
agent3: "general help"
```

### 2. Test Agents Independently

```python
def test_agent(agent, test_cases):
    """Test an agent independently before integration."""
    results = []
    for query in test_cases:
        result = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        results.append({
            "query": query,
            "response": result["messages"][-1].content
        })
    return results

# Test each agent separately
billing_tests = [
    "What's the price of the pro plan?",
    "How do I get a refund?",
    "When will I be charged?"
]

billing_results = test_agent(billing_agent, billing_tests)
```

### 3. Handle Edge Cases

```python
@tool
def billing_support(request: str) -> str:
    """Handle billing questions with error handling."""
    try:
        result = billing_agent.invoke({
            "messages": [{"role": "user", "content": request}]
        })
        return result["messages"][-1].content
    except Exception as e:
        # Fallback response
        return (
            "I apologize, but I'm having trouble accessing billing information right now. "
            "Please try again in a moment or contact our billing team directly at billing@company.com."
        )
```

### 4. Ambiguous Queries

```python
# Update supervisor prompt to handle ambiguity
supervisor_prompt = (
    "...route to appropriate specialist.\n\n"
    "If query spans multiple domains, choose PRIMARY domain:\n"
    "- 'Why was I charged?' → Billing (payment issue)\n"
    "- 'Feature X not working' → Technical (technical issue)\n"
    "- 'Is my data safe?' → Policy (privacy question)\n\n"
    "If truly ambiguous, default to Technical Support."
)
```

### 5. Monitoring and Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_customer_query(query: str) -> dict:
    """Handle query with comprehensive logging."""
    
    logger.info(f"Received query: {query}")
    
    # Invoke supervisor
    result = supervisor.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    
    # Log routing decision
    routed_to = extract_routed_agent(result)
    logger.info(f"Routed to: {routed_to}")
    
    # Log response
    response = result["messages"][-1].content
    logger.info(f"Response length: {len(response)} characters")
    
    return {"response": response, "routed_to": routed_to}
```

---

## Quick Reference

### Complete System Setup

```python
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 1. Load vector stores
billing_vectorstore = Chroma(
    persist_directory="./chroma_db/billing",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
)

technical_vectorstore = Chroma(
    persist_directory="./chroma_db/technical",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-small")
)

# 2. Create worker agents
@tool
def billing_support(request: str) -> str:
    """Handle billing, pricing, and payment questions."""
    # Billing agent implementation with Hybrid RAG/CAG
    pass

@tool
def technical_support(request: str) -> str:
    """Handle technical issues and troubleshooting."""
    # Technical agent implementation with Pure RAG
    pass

@tool
def policy_support(request: str) -> str:
    """Handle policy, privacy, and compliance questions."""
    # Policy agent implementation with Pure CAG
    pass

# 3. Create supervisor
supervisor = create_agent(
    model="openai:gpt-4o-mini",
    tools=[billing_support, technical_support, policy_support],
    system_prompt="Route queries to appropriate specialists...",
    name="supervisor"
)

# 4. Handle queries
def handle_query(query: str) -> str:
    result = supervisor.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].content
```

---

## Key Takeaways

- **Multi-agent architecture** with supervisor routing to specialized workers
- **Three retrieval strategies** matched to data characteristics:
  - Pure RAG for dynamic, frequently updated content (Technical)
  - Pure CAG for static, small documents (Policy)
  - Hybrid RAG/CAG for mixed content (Billing)
- **Model optimization** - GPT-4o-mini for routing/simple tasks, GPT-4o for complex reasoning
- **Cost-effective** - 40% cheaper than all-GPT-4o approach
- **Scalable** - Easy to add new specialized agents
- **Context engineering** - Session state, conversation history, and smart caching
- **Production-ready** - Error handling, logging, and monitoring built in

---

## Connection to Full-Stack Application

This multi-agent system is designed to integrate with a FastAPI backend and Next.js frontend:

### Backend Integration (FastAPI)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    routed_to: str
    session_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for customer service."""
    try:
        result = handle_customer_query(
            query=request.message,
            session_id=request.session_id
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Frontend Integration (Next.js)

```typescript
// API call from Next.js frontend
async function sendMessage(message: string, sessionId?: string) {
  const response = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId })
  });
  
  const data = await response.json();
  return data; // { response, routed_to, session_id }
}
```

---

## Resources

- [Multi-Agent Documentation](https://docs.langchain.com/oss/python/langchain/multi-agent)
- [LangGraph Documentation](https://docs.langchain.com/oss/python/langgraph)
- [Previous: Multi-Agent Systems](./11-multi-agent.md)
- [RAG Documentation](../rag/10-agentic-rag.md)
- [Retrieval Strategies](../rag/8-retrieval.md)
- [Project Specification](../agentic-customer-specs.md)
- [OpenAI Models](https://platform.openai.com/docs/models)
- [OpenAI Pricing](https://openai.com/api/pricing/)

---

## Next Steps

1. **Run the data ingestion pipeline** - Process and load your documents
2. **Test each agent independently** - Verify retrieval strategies work correctly
3. **Test supervisor routing** - Ensure queries route to correct agents
4. **Integrate with FastAPI** - Build the backend API
5. **Build the frontend** - Create the chat interface with Next.js
6. **Deploy** - Set up production environment with proper API keys
7. **Monitor** - Track agent performance and routing decisions

**Remember:** This is a proof-of-concept demonstrating advanced AI engineering patterns. Customize the agents, models, and retrieval strategies for your specific use case.

