from log_classifier.services.regex_service import RegexService
from log_classifier.services.embedding_service import EmbeddingService
from log_classifier.services.classifier_service import ClassifierService
from log_classifier.services.llm_service import LLMService


import warnings
warnings.simplefilter("ignore", FutureWarning)

class RoutingService:
"""
Dependency Injection (DI)
Specifically: Constructor Injection
"""

    def __init__(
        self,
        regex_service: RegexService,
        embedding_service: EmbeddingService,
        classifier_service: ClassifierService,
        llm_service: LLMService,
        confidence_threshold: float,
    ) -> None:
        self.regex_service = regex_service
        self.embedding_service = embedding_service
        self.classifier_service = classifier_service
        self.llm_service = llm_service
        self.confidence_threshold = confidence_threshold

    def route(self, log_message: str) -> str:
        label: str | None = self.regex_service.classify(log_message)

        if label:
            return label

        embeddings = self.embedding_service.embed([log_message])
        label, confidence = self.classifier_service.predict(embeddings)

        if confidence >= self.confidence_threshold:
            return label

        return self.llm_service.classify(log_message)