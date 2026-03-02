FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen

ARG UID=10001

RUN adduser \
    --disabled-password \
    --gecos "" \
    --uid "${UID}" \
    appuser

COPY src/ src/
COPY web/ web/
COPY models-artifacts/ models-artifacts/

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000", "--workers", "1"]
