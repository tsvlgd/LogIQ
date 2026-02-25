"""Model registry for managing loaded ML models."""

from typing import Optional

import numpy as np


class ModelRegistry:
    """
    Registry for managing ML model instances.

    Handles loading and caching of:
    - SentenceTransformer for embeddings
    - LogisticRegression classifier
    """

    def __init__(self):
        """Initialize the model registry."""
        self._embedding_model = None
        self._classifier_model = None

    def get_embedding_model(self):
        """
        Load or retrieve cached embedding model.

        Returns:
            SentenceTransformer instance or None if loading fails.
        """
        # TODO: Load SentenceTransformer model
        return self._embedding_model

    def get_classifier_model(self):
        """
        Load or retrieve cached classifier model.

        Returns:
            LogisticRegression instance or None if loading fails.
        """
        # TODO: Load LogisticRegression model from joblib pickle
        return self._classifier_model

    def is_ready(self) -> bool:
        """
        Check if all required models are loaded.

        Returns:
            True if both models are available, False otherwise.
        """
        return self._embedding_model is not None and self._classifier_model is not None


# Global registry instance
_registry: Optional[ModelRegistry] = None


def get_model_registry() -> ModelRegistry:
    """
    Get or create the global model registry.

    Returns:
        ModelRegistry instance.
    """
    global _registry
    if _registry is None:
        _registry = ModelRegistry()
    return _registry
