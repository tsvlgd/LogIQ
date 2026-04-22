import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from log_classifier.app import create_router
from log_classifier.api.router import router as api_router


BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"

# HF warnings desabled
os.environ["TOKENIZERS_PARALLELISM"] = "false"


# lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.router = create_router()
    yield
    print("Application shutdown: cleaning up resources if needed")



app = FastAPI(lifespan=lifespan)


app.include_router(api_router, prefix="/api")

templates = Jinja2Templates(directory=str(WEB_DIR / "templates"))

app.mount(
    "/static",
    StaticFiles(directory=str(WEB_DIR / "static")),
    name="static",
)



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
