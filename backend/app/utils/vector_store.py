"""
Vector store initialization and management.
Provides singleton instances of ChromaDB for billing and technical support.
"""
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Singleton manager for vector stores."""
    
    _instance = None
    _billing_store = None
    _technical_store = None
    _embeddings = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize embeddings model (shared across stores)."""
        if self._embeddings is None:
            logger.info(f"Initializing embeddings with model: {settings.embedding_model}")
            self._embeddings = OpenAIEmbeddings(model=settings.embedding_model)
    
    def get_billing_store(self) -> Chroma:
        """Get or create billing vector store."""
        if self._billing_store is None:
            logger.info(f"Loading billing vector store from {settings.billing_vectorstore_path}")
            try:
                self._billing_store = Chroma(
                    persist_directory=settings.billing_vectorstore_path,
                    embedding_function=self._embeddings,
                    collection_name="billing"
                )
                logger.info("Billing vector store loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load billing vector store: {e}")
                logger.warning("Billing vector store not available - run data ingestion first")
                self._billing_store = None
        return self._billing_store
    
    def get_technical_store(self) -> Chroma:
        """Get or create technical vector store."""
        if self._technical_store is None:
            logger.info(f"Loading technical vector store from {settings.technical_vectorstore_path}")
            try:
                self._technical_store = Chroma(
                    persist_directory=settings.technical_vectorstore_path,
                    embedding_function=self._embeddings,
                    collection_name="technical"
                )
                logger.info("Technical vector store loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load technical vector store: {e}")
                logger.warning("Technical vector store not available - run data ingestion first")
                self._technical_store = None
        return self._technical_store
    
    def get_embeddings(self) -> OpenAIEmbeddings:
        """Get embeddings model."""
        return self._embeddings


# Global vector store manager instance
vector_store_manager = VectorStoreManager()

