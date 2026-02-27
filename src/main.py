import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI
from contextlib import asynccontextmanager # For managing application lifespan
from log_classifier.app import create_router
from log_classifier.services.routing_service import RoutingService
from log_classifier.api.router import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.router = create_router()
    yield
    print("Application shutdown: cleaning up resources if needed")


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api") # this is the main router for the API endpoints we'll define in api/router.py
