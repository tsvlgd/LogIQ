from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        return self.model.encode(texts)