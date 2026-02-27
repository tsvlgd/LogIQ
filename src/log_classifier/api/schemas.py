from pydantic import BaseModel


class LogRequest(BaseModel):
    message: str


class LogResponse(BaseModel):
    label: str
    confidence: float | None
    source: str