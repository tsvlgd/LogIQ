"""LLM-based log classification service (fallback)."""

from typing import Optional


def classify_by_llm(text: str, model_name: str) -> Optional[tuple[str, float]]:
    """
    Classify a log message using an LLM (fallback method).

    Args:
        text: Log text to classify.
        model_name: LLM model name (e.g., gpt-3.5-turbo).

    Returns:
        Tuple of (category, confidence) or None if LLM call fails.
    """
    # TODO: Implement LLM-based classification
    pass
