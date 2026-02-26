from log_classifier.config import settings
from log_classifier.services.regex_service import RegexService
from log_classifier.services.embedding_service import EmbeddingService
from log_classifier.services.classifier_service import ClassifierService
from log_classifier.services.llm_service import LLMService
from log_classifier.services.routing_service import RoutingService


def test_routing():
    # Instantiate real services
    regex_service = RegexService()
    embedding_service = EmbeddingService(
        model_name=settings.embedding_model_name
    )
    classifier_service = ClassifierService(
        settings.classifier_path, # inpalce args
        settings.metadata_path, 
    )
    llm_service = LLMService()

    routing_service = RoutingService(
        regex_service=regex_service,
        embedding_service=embedding_service,
        classifier_service=classifier_service,
        llm_service=llm_service,
        confidence_threshold=settings.confidence_threshold,
    )

    test_logs = [
    # 1️⃣ HTTP Status (Regex should catch)
    "500 Internal Server Error: Upstream service unavailable at /api/payments.",

    # 2️⃣ Resource Usage (Regex should catch)
    "Memory usage exceeded 95% on node-3. Automatic restart initiated.",

    # 3️⃣ Security Alert (Regex or classifier)
    "Unauthorized access attempt detected for admin endpoint from IP 10.0.0.12.",

    # 4️⃣ Critical Error (Classifier likely)
    "Database primary shard corrupted. Failover unsuccessful. Service entering degraded mode.",

    # 5️⃣ Ambiguous / Likely LLM fallbpython -m tests.test_routingack
    "System instability observed after configuration update; dependent services intermittently failing.",

    "Post-deployment anomaly detected affecting user-facing latency but without observable resource saturation."
]
    

    for log in test_logs:
        label = routing_service.route(log)
        print("Log:", log)
        print("Predicted:", label)
        print("-" * 60)


if __name__ == "__main__":
    test_routing()