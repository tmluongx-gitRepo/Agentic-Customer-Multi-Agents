"""
Data Ingestion Pipeline
Processes documents and loads them into ChromaDB with proper metadata.
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ingest_billing_data():
    """Ingest billing documents with metadata tagging."""
    logger.info("=" * 60)
    logger.info("Ingesting Billing Documents")
    logger.info("=" * 60)
    
    billing_path = Path(settings.billing_data_path)
    
    if not billing_path.exists():
        logger.warning(f"Billing data path does not exist: {billing_path}")
        logger.info("Creating sample billing directory structure...")
        billing_path.mkdir(parents=True, exist_ok=True)
        return
    
    try:
        # Load documents
        loader = DirectoryLoader(
            str(billing_path),
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        documents = loader.load()
        
        if not documents:
            logger.warning("No billing documents found")
            return
        
        logger.info(f"Loaded {len(documents)} billing documents")
        
        # Add metadata to distinguish static vs dynamic
        for doc in documents:
            source = doc.metadata.get("source", "").lower()
            # Tag static policy documents
            if "policy" in source or "terms" in source:
                doc.metadata["type"] = "static"
            else:
                doc.metadata["type"] = "dynamic"
        
        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(documents)
        
        logger.info(f"Created {len(chunks)} chunks")
        
        # Create embeddings and store
        embeddings = OpenAIEmbeddings(model=settings.embedding_model)
        vectorstore_path = Path(settings.billing_vectorstore_path)
        vectorstore_path.parent.mkdir(parents=True, exist_ok=True)
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(vectorstore_path),
            collection_name="billing"
        )
        
        logger.info(f"✓ Ingested {len(chunks)} billing document chunks")
        logger.info(f"  Saved to: {vectorstore_path}")
        
    except Exception as e:
        logger.error(f"Error ingesting billing data: {e}")


def ingest_technical_data():
    """Ingest technical documentation."""
    logger.info("=" * 60)
    logger.info("Ingesting Technical Documents")
    logger.info("=" * 60)
    
    technical_path = Path(settings.technical_data_path)
    
    if not technical_path.exists():
        logger.warning(f"Technical data path does not exist: {technical_path}")
        logger.info("Creating sample technical directory structure...")
        technical_path.mkdir(parents=True, exist_ok=True)
        return
    
    try:
        # Load documents (support both .txt and .md)
        loader = DirectoryLoader(
            str(technical_path),
            glob="**/*.*",
            loader_cls=TextLoader
        )
        documents = loader.load()
        
        if not documents:
            logger.warning("No technical documents found")
            return
        
        logger.info(f"Loaded {len(documents)} technical documents")
        
        # Add doc_type metadata
        for doc in documents:
            source = doc.metadata.get("source", "").lower()
            if "bug" in source:
                doc.metadata["doc_type"] = "bug_report"
            elif "forum" in source:
                doc.metadata["doc_type"] = "forum"
            else:
                doc.metadata["doc_type"] = "documentation"
        
        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_documents(documents)
        
        logger.info(f"Created {len(chunks)} chunks")
        
        # Create embeddings and store
        embeddings = OpenAIEmbeddings(model=settings.embedding_model)
        vectorstore_path = Path(settings.technical_vectorstore_path)
        vectorstore_path.parent.mkdir(parents=True, exist_ok=True)
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(vectorstore_path),
            collection_name="technical"
        )
        
        logger.info(f"✓ Ingested {len(chunks)} technical document chunks")
        logger.info(f"  Saved to: {vectorstore_path}")
        
    except Exception as e:
        logger.error(f"Error ingesting technical data: {e}")


def prepare_policy_documents():
    """Prepare static policy documents (no vector store needed for CAG)."""
    logger.info("=" * 60)
    logger.info("Preparing Policy Documents")
    logger.info("=" * 60)
    
    policies_path = Path(settings.policies_path)
    
    if not policies_path.exists():
        logger.warning(f"Policies path does not exist: {policies_path}")
        logger.info("Creating sample policies directory structure...")
        policies_path.mkdir(parents=True, exist_ok=True)
        return
    
    policy_files = [
        "terms_of_service.txt",
        "privacy_policy.txt",
        "compliance_guidelines.txt",
        "data_handling.txt"
    ]
    
    found_files = []
    for policy_file in policy_files:
        if (policies_path / policy_file).exists():
            found_files.append(policy_file)
    
    if found_files:
        logger.info(f"✓ Found {len(found_files)} policy documents:")
        for filename in found_files:
            logger.info(f"  - {filename}")
        logger.info("  Policy documents ready for CAG (no vector store needed)")
    else:
        logger.warning("No policy documents found")


if __name__ == "__main__":
    logger.info("\n" + "=" * 60)
    logger.info("ADVANCED CUSTOMER SERVICE AI - DATA INGESTION")
    logger.info("=" * 60 + "\n")
    
    try:
        ingest_billing_data()
        print()
        ingest_technical_data()
        print()
        prepare_policy_documents()
        
        logger.info("\n" + "=" * 60)
        logger.info("DATA INGESTION COMPLETE!")
        logger.info("=" * 60)
        logger.info("\nYou can now start the FastAPI server with:")
        logger.info("  cd backend")
        logger.info("  uvicorn app.main:app --reload")
        
    except Exception as e:
        logger.error(f"\nFatal error during data ingestion: {e}")
        sys.exit(1)

