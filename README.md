# NLP-project: Log Classifier

A production-ready hybrid ML inference API for log classification combining regex patterns, sentence embeddings, logistic regression, and LLM-based fallback (Groq/Llama).

## What's Implemented

**Core Services** (all complete & optimized)
- `regex_service.py` - Fast pattern-based classification
- `embedding_service.py` - SentenceTransformer embeddings (all-MiniLM-L6-v2)
- `classifier_service.py` - Pre-trained logistic regression model
- `llm_service.py` - Groq API integration for fallback (optimized & fully tested)
- `routing_service.py` - Multi-stage pipeline orchestration

**Model Artifacts** (trained & ready)
- `log_classifier.joblib` - Logistic regression classifier
- `metadata.json` - Model config: embedding dimension (384), 7 label categories, 1910 training samples

**Training Pipeline** (complete ML workflow)
- `training/log_classification.ipynb` - Full ML pipeline:
  - Data loading from synthetic dataset (1910 samples)
  - DBSCAN clustering for pattern discovery
  - Regex classification (Stage 1)
  - Embedding + logistic regression (Stage 2)
  - Label inference & validation

**Testing** (LLM service fully tested)
- `tests/test_llm.py` - 6 comprehensive test cases covering all label categories

## Setup & Running

**Requirements:** Python 3.10+, [uv](https://docs.astral.sh/uv/)

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with: GROQ_API_KEY, CLASSIFIER_PATH, CONFIDENCE_THRESHOLD, etc.
```

**Development server:**
```bash
uv run uvicorn log_classifier.api.server:app --reload --host 0.0.0.0 --port 8000
```

**Production server:**
```bash
uv run uvicorn log_classifier.api.server:app --host 0.0.0.0 --port 8000 --workers 4
```

**Run tests:**
```bash
uv run pytest tests/test_llm.py -v
```

## API Endpoints

**Health Check**
```bash
curl http://localhost:8000/health
```

**Classify Log**
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "text": "ERROR: Database connection timeout",
    "metadata": {"source": "production"}
  }'
```

Response:
```json
{
  "category": "database_error",
  "confidence": 0.92,
  "method": "embedding",
  "metadata": {"processing_time_ms": 45}
}
```

## Classification Pipeline

```
Log Input
   ↓
[Regex] → Pattern match found? → Return result (fastest)
   ↓ No match
[Embedding + LogReg] → Confidence ≥ threshold? → Return result
   ↓ Low confidence
[LLM (Groq)] → Return classification (fallback)
```

## Project Structure

```
src/log_classifier/
├── api/
│   └── server.py           # FastAPI app & endpoints
├── config.py               # Settings & environment loading
├── domain/
│   ├── schemas.py          # Pydantic models
│   └── types.py            # Type definitions
└── services/
    ├── regex_service.py
    ├── embedding_service.py
    ├── classifier_service.py
    ├── llm_service.py      # Groq integration (optimized)
    └── routing_service.py  # Pipeline orchestration

models-artifacts/
├── log_classifier.joblib   # Trained classifier
└── metadata.json           # Model metadata

training/
├── log_classification.ipynb # ML workflow notebook
└── dataset/
    └── synthetic_logs.csv  # Training data (1910 samples)

tests/
└── test_llm.py            # LLM service tests

pyproject.toml              # Project config & dependencies
```

## Supported Labels

- Critical Error
- Error
- HTTP Status
- Resource Usage
- Security Alert
- Workflow Error
- Deprecation Warning
- System Notification
- User Action

## Configuration

Environment variables (see `.env.example`):

| Variable | Default | Purpose |
|----------|---------|---------|
| `EMBEDDING_MODEL_NAME` | `all-MiniLM-L6-v2` | SentenceTransformer model |
| `CLASSIFIER_PATH` | `models-artifacts/log_classifier.joblib` | Pre-trained classifier location |
| `CONFIDENCE_THRESHOLD` | `0.6` | Min confidence before LLM fallback |
| `GROQ_API_KEY` | - | Groq API key (required for LLM) |
| `LLM_MODEL_NAME` | `llama-3.1-8b-instant` | Groq model ID |
| `SERVER_HOST` | `0.0.0.0` | Server bind address |
| `SERVER_PORT` | `8000` | Server port |

## Dependencies

**Production:**
- fastapi, uvicorn - Web framework
- sentence-transformers - Embeddings
- scikit-learn - ML models
- joblib - Model serialization
- pydantic, python-dotenv - Config
- torch, numpy - ML backend
- groq - LLM API client

**Development:**
- pytest - Testing
- httpx - HTTP testing

## Implementation Status

✅ All services implemented and tested  
✅ Model training pipeline complete  
✅ Pre-trained artifacts generated  
✅ LLM integration (Groq) optimized  
✅ Comprehensive test suite  
✅ API endpoints defined  
✅ Configuration system ready


