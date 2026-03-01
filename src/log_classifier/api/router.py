# log_classifier/api/router.py
from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Request
from log_classifier.api.schemas import (
    RawLogRequest,
    LogRequest,
    BatchLogRequest,
    LogResponse,
    LogInput,
)
from log_classifier.api.utils import norm
from log_classifier.services.routing_service import RoutingService

router = APIRouter()

def get_router(request: Request) -> RoutingService:
    return request.app.state.router

@router.post(
    "/classify",
    response_model=Union[LogResponse, List[LogResponse]],
)
def classify(
    request: LogInput,
    routing_service: RoutingService = Depends(get_router),
):
    # Normalize to List[LogRequest]
    if isinstance(request, LogRequest):
        logs = [request]

    elif isinstance(request, BatchLogRequest):
        logs = request.logs

    elif isinstance(request, RawLogRequest):
        logs = norm(request.raw)

    else:
        raise HTTPException(status_code=400, detail="Unsupported input")

    if not logs:
        raise HTTPException(status_code=400, detail="No valid logs found")

    responses = []
    for log in logs:
        result = routing_service.route(log.message)
        responses.append(
            LogResponse(
                label=result.label,
                confidence=result.confidence,
                source=result.source,
            )
        )

    return responses[0] if len(responses) == 1 else responses