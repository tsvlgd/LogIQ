"""FastAPI application and endpoint definitions."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from log_classifier.config import get_settings
from log_classifier.domain.schemas import LogRequest, LogResponse
from log_classifier.infrastructure.model_registry import get_model_registry
from log_classifier.logging_config import get_logger

logger = get_logger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle (startup and shutdown).

    Args:
        app: FastAPI application instance.
    """
    # Startup
    logger.info("Starting log-classifier service")
    registry = get_model_registry()
    if not registry.is_ready():
        logger.warning("Models not fully loaded at startup")
    yield

    # Shutdown
    logger.info("Shutting down log-classifier service")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        Configured FastAPI application.
    """
    app = FastAPI(
        title="Log Classifier API",
        description="Hybrid log classification system (Regex + Embedding + Logistic Regression + LLM)",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health_check() -> dict:
        """
        Health check endpoint.

        Returns:
            Health status.
        """
        registry = get_model_registry()
        return {
            "status": "healthy",
            "models_ready": registry.is_ready(),
        }

    @app.post("/classify", response_model=LogResponse)
    async def classify_log(request: LogRequest) -> LogResponse:
        """
        Classify a log message.

        Args:
            request: Log request containing text and optional metadata.

        Returns:
            Classification result with category and confidence.

        Raises:
            HTTPException: If classification fails.
        """
        try:
            # TODO: Call routing_service.route_classification_request(request.text, request.metadata)
            raise HTTPException(
                status_code=501, detail="Classification not yet implemented"
            )
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Invalid request: {e}")
        except Exception as e:
            logger.error(f"Classification error: {e}")
            raise HTTPException(
                status_code=500, detail="Classification failed"
            ) from e

    return app


# Application instance
app = create_app()
