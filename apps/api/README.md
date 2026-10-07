# Holocron Career AI - API

FastAPI backend for the Holocron Career AI platform.

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run with uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v --cov=src
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

- `GET /health` - Health check
- `GET /docs` - Swagger UI (local only)
- `GET /api/v1/jobs` - List jobs
- `POST /api/v1/jobs` - Create job
- `GET /api/v1/companies` - List companies
- `POST /api/v1/applications` - Create application