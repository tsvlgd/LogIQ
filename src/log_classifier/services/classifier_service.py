"""Main classifier orchestration service."""

from typing import Optional


def classify(text: str) -> Optional[tuple[str, float]]:
    """
    Classify a log message using the hybrid approach.

    Uses fallback strategy:
    1. Try regex classification
    2. Try embedding + logistic regression
    3. Fall back to LLM if confidence is low

    Args:
        text: Log text to classify.

    Returns:
        Tuple of (category, confidence) or None if all methods fail.
    """
    # TODO: Implement hybrid classification strategy
    pass
