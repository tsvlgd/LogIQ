from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # Model configuration
    embedding_model_name: str = Field(
        default="all-MiniLM-L6-v2",
        description="SentenceTransformer model name"
    )

    classifier_path: str = Field(
        default="models/log_classifier.joblib",
        description="Path to trained sklearn classifier"
    )

    metadata_path: str = Field(
        default="models/metadata.json",
        description="Path to model metadata file"
    )

    confidence_threshold: float = Field(
        default=0.6,
        description="Minimum probability required before LLM fallback"
    )

    # LLM configuration
    llm_model_name: str = Field(
        default="deepseek-r1-distill-llama-70b",
        description="LLM model identifier"
    )

    llm_timeout_seconds: int = Field(
        default=10,
        description="Timeout for LLM calls"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()