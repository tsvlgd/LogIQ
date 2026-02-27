from fastapi import APIRouter, Depends, Request
from log_classifier.api.schemas import LogRequest, LogResponse
from log_classifier.services.routing_service import RoutingService

router = APIRouter()


def get_router(request: Request) -> RoutingService:
    return request.app.state.router

@router.post("/classify", response_model=LogResponse)
def classify(
    request: LogRequest,
    routing_service: RoutingService = Depends(get_router), # Depennds -> this will call get_router to get the router instance with all dependencies injected
):
    result = routing_service.route(request.message)

    return LogResponse(
        label=result.label,
        confidence=result.confidence,
        source=result.source,
    )