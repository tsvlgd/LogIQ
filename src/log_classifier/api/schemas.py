from pydantic import BaseModel
from typing import List, Union

class RawLogRequest(BaseModel):
    raw: str

class LogRequest(BaseModel):
    message: str

class BatchLogRequest(BaseModel):
    logs: List[LogRequest]

class LogResponse(BaseModel):
    label: str
    confidence: float | None
    source: str

LogInput = Union[RawLogRequest, LogRequest, BatchLogRequest]