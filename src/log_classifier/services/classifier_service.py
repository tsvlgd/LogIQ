import joblib

class ClassifierService:
    def __init__(self, model_path: str):
        self.model = joblib.load(model_path)

    def predict(self, embeddings):
        probs = self.model.predict_proba(embeddings)
        idx = probs.argmax(axis=1)[0]
        label = self.model.classes_[idx]
        confidence = probs[0][idx]
        return label, float(confidence)