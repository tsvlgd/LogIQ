"""Pydantic schemas for request/response models."""

from typing import Optional

from pydantic import BaseModel, Field


class LogRequest(BaseModel):
    """Log entry for classification."""

    text: str = Field(..., description="Log text to classify", min_length=1)
    metadata: Optional[dict] = Field(
        default=None, description="Additional metadata for the log"
    )


class LogResponse(BaseModel):
    """Classification result for a log entry."""

    category: str = Field(..., description="Predicted log category")
    confidence: float = Field(
        ..., description="Confidence score (0.0 to 1.0)", ge=0.0, le=1.0
    )
    method: str = Field(..., description="Classification method used")
    metadata: Optional[dict] = Field(
        default=None, description="Additional result metadata"
    )
