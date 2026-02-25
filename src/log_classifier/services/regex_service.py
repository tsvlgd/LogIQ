"""Regex-based log classification service."""

from typing import Optional


def classify_by_regex(text: str) -> Optional[tuple[str, float]]:
    """
    Classify a log message using regex patterns.

    Args:
        text: Log text to classify.

    Returns:
        Tuple of (category, confidence) or None if no match.
    """
    # TODO: Implement regex-based classification
    pass
