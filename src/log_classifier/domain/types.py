"""Type definitions for the domain layer."""

from typing import Literal

# Classification methods
ClassificationMethod = Literal["regex", "embedding", "llm"]

# Log severity levels
SeverityLevel = Literal["debug", "info", "warning", "error", "critical"]
