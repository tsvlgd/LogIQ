# NLP-project
=======
# Log Classifier

A production-ready hybrid ML inference API for log classification, combining regex patterns, embeddings, logistic regression, and LLM-based fallback strategies.

## Overview

**Log Classifier** is a FastAPI-based service that classifies log messages using a multi-stage pipeline:

1. **Regex Matching** - Fast pattern-based classification
2. **Embedding + Logistic Regression** - ML-based classification using sentence embeddings
3. **LLM Fallback** - High-confidence classification for edge cases

This hybrid approach ensures both speed and accuracy across diverse log formats and types.

## Architecture

```
Request
   ↓
[Regex Classifier] → Match? → Return (fast)
   ↓ No Match
[Embedding + LogReg] → High Confidence? → Return
   ↓ Low Confidence
[LLM Classifier] → Return (fallback)
```

### Components

- **domain/** - Core business models (schemas, types)
- **services/** - Classification logic (regex, embedding, LLM, orchestration)
- **infrastructure/** - ML model loading and registry (SentenceTransformer, scikit-learn)
- **api/** - FastAPI HTTP endpoints
- **config.py** - Environment-based configuration
- **logging_config.py** - Structured logging setup

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd log-classifier

# Install dependencies using uv
uv sync

# Create .env file from example
cp .env.example .env
```

### Running the Server

```bash
# Development server (with auto-reload)
uv run uvicorn log_classifier.api.server:app --reload --host 0.0.0.0 --port 8000

# Production server
uv run uvicorn log_classifier.api.server:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testing

```bash
# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/log_classifier
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "models_ready": true
}
```

### Classify Log
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "text": "ERROR: Database connection timeout",
    "metadata": {"source": "production", "timestamp": "2025-02-25T10:30:00Z"}
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

## Configuration

All configuration is managed through environment variables (see `.env.example`):

```env
# Embedding Model
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

# Classifier Model
CLASSIFIER_PATH=models/classifier.pkl
CONFIDENCE_THRESHOLD=0.5

# LLM Configuration
LLM_MODEL_NAME=gpt-3.5-turbo

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=false
```

## Project Structure

```
log-classifier/
├── src/log_classifier/          # Main source code (src layout)
│   ├── __init__.py
│   ├── config.py               # Settings & environment loading
│   ├── logging_config.py       # Structured logging
│   ├── domain/                 # Core business models
│   │   ├── schemas.py          # Pydantic models
│   │   └── types.py            # Type definitions
│   ├── services/               # Business logic
│   │   ├── regex_service.py
│   │   ├── embedding_service.py
│   │   ├── classifier_service.py
│   │   ├── llm_service.py
│   │   └── routing_service.py
│   ├── infrastructure/         # External integrations
│   │   └── model_registry.py
│   └── api/                    # HTTP layer
│       └── server.py           # FastAPI app
├── models/                      # ML models (gitignored for large files)
│   ├── .gitkeep
│   └── metadata.json
├── tests/                       # Test suite
├── pyproject.toml              # Project config & dependencies
├── uv.lock                     # Locked dependencies
├── README.md                   # This file
└── .env.example                # Environment template
```

## Dependencies

### Production
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sentence-transformers** - Embedding models
- **scikit-learn** - ML models & utilities
- **joblib** - Model persistence
- **pydantic** - Data validation
- **python-dotenv** - Environment loading
- **numpy** - Numerical computing

### Development
- **pytest** - Testing framework
- **httpx** - HTTP client for testing

## Development Workflow

### Setting Up Development Environment

```bash
# Install dependencies (including dev)
uv sync

# Run tests
uv run pytest tests/

# Run specific test
uv run pytest tests/test_service.py::test_function
```

### Adding Dependencies

```bash
# Add production dependency
uv add package-name

# Add dev dependency
uv add --dev package-name
```

### Code Structure Guidelines

- **No business logic in `__init__.py`** - Modules should be clear imports only
- **Minimal abstractions** - Use functions/classes only when needed
- **Type hints everywhere** - For IDE support and documentation
- **Docstrings** - Every module, function, and class
- **src layout** - Prevents import issues and test isolation

## Future Roadmap

- [ ] Regex pattern library & configuration
- [ ] SentenceTransformer model fine-tuning
- [ ] LogisticRegression classifier training pipeline
- [ ] LLM integration (OpenAI API)
- [ ] Batch classification endpoint
- [ ] Model versioning & A/B testing
- [ ] Metrics & monitoring (Prometheus)
- [ ] Docker containerization
- [ ] Kubernetes deployment manifests
- [ ] Comprehensive test suite


