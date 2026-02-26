class RoutingService:
    def __init__(
            self,
            regex_service,
            embedding_service,
            classifier_service,
            llm_service,
            confidence_threshold
    ):
        self.regex_service = regex_service
        self.embedding_service = embedding_service
        self.classifier_service = classifier_service
        self.llm_service = llm_service
        self.confidence_threshold = confidence_threshold


    def route(self, log_message: str) -> str:
        
        label = self.regex_service.classify(log_message)
        if label:
            return label
        
        embeddings = self.embedding_service.embed([log_message])
        label, confidence = self.classifier_service.predict(embeddings)

        if confidence >= self.confidence_threshold: 
            return label
        return self.llm_service.classify(log_message)