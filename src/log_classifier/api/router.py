# log_classifier/api/router.py
import io 
import pandas as pd
from typing import List, Union
from fastapi import UploadFile, File 
from log_classifier.api.utils import norm
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, Request
from log_classifier.api.schemas import (
    RawLogRequest,
    LogRequest,
    BatchLogRequest,
    LogResponse,
    LogInput,
)
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
    


@router.post("/classify-file")
async def classify_file(
    file: UploadFile = File(...),
    routing_service: RoutingService = Depends(get_router),
):
    # 1. Read file contents
    contents = await file.read()

    # 2. Load into pandas
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(contents))
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file format")

    # 3. Validate required column
    if "log" not in df.columns:
        raise HTTPException(status_code=400, detail="File must contain 'log' column")

    # 4. Apply existing routing logic
    df["predicted_label"] = df["log"].apply(
        lambda msg: routing_service.route(msg).label
    )

    # 5. Convert back to CSV
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # 6. Return downloadable response
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv"
    )
