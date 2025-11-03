"""
Configuration management for the Advanced Customer Service AI backend.
Loads environment variables and provides configuration constants.
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str
    
    # Model Configuration
    supervisor_model: str = "gpt-4o-mini"
    billing_model: str = "gpt-4o"
    technical_model: str = "gpt-4o"
    policy_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    
    # Vector Store Paths
    billing_vectorstore_path: str = "./chroma_db/billing"
    technical_vectorstore_path: str = "./chroma_db/technical"
    
    # Data Paths
    policies_path: str = "./data/policies"
    billing_data_path: str = "./data/billing"
    technical_data_path: str = "./data/technical"
    
    # Session Configuration
    session_timeout_minutes: int = 30
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS Origins
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def base_path(self) -> Path:
        """Get the backend base path."""
        return Path(__file__).parent.parent


# Global settings instance
settings = Settings()

# Ensure OpenAI API key is set
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

