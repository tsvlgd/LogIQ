"""Configuration management for log-classifier."""

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Embedding Configuration
    embedding_model_name: str = "all-MiniLM-L6-v2"

    # Model Configuration
    classifier_path: str = "models/classifier.pkl"
    confidence_threshold: float = 0.5

    # LLM Configuration
    llm_model_name: str = "gpt-3.5-turbo"

    # Server Configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    debug: bool = False

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
