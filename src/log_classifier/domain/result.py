from dataclasses import dataclass


@dataclass(frozen=True)
class ClassificationResult:
    label: str
    confidence: float | None
    source: str