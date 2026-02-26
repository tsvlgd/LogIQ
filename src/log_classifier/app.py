from log_classifier.services.regex_service import RegexService
from log_classifier.services.embedding_service import EmbeddingService
from log_classifier.services.classifier_service import ClassifierService
from log_classifier.services.llm_service import LLMService
from log_classifier.services.routing_service import RoutingService
from log_classifier.config import settings


# composition root / factory function for creating the router with all dependencies injected

def create_router() -> RoutingService:
    regex_service = RegexService()
    embedding_service = EmbeddingService(settings.embedding_model_name)
    classifier_service = ClassifierService(
        settings.classifier_path,
        settings.metadata_path,
    )
    llm_service = LLMService()

    return RoutingService(
        regex_service=regex_service,
        embedding_service=embedding_service,
        classifier_service=classifier_service,
        llm_service=llm_service,
        confidence_threshold=settings.confidence_threshold,
    )