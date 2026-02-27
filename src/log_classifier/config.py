from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.
    Values are loaded from environment variables and `.env` file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ======================
    # Paths
    # ======================

    classifier_path: Path = Field(
        default=Path("models-artifacts/log_classifier.joblib"),
        description="Path to trained sklearn classifier",
    )

    metadata_path: Path = Field(
        default=Path("models-artifacts/metadata.json"),
        description="Path to model metadata file",
    )

    # ======================
    # ML Configuration
    # ======================

    embedding_model_name: str = Field(
        default="all-MiniLM-L6-v2",
        description="SentenceTransformer model name",
    )

    confidence_threshold: float = Field(
        default=0.7,
        description="Minimum probability required before LLM fallback",
        ge=0.0,
        le=1.0,
    )

    # ======================
    # LLM Configuration
    # ======================

    groq_api_key: str = Field(
        ...,
        description="Groq API key (must be set via environment variable)",
    )

    llm_model_name: str = Field(
        default="llama-3.1-8b-instant",
        description="LLM model name to use for classification fallback",
    )

    llm_timeout_seconds: int = Field(
        default=10,
        description="Timeout for LLM calls",
        gt=0,
    )


settings = Settings()