# Guia de Desenvolvimento Local

## Requisitos

- Python 3.12+
- Node.js 18+
- Docker + Docker Compose
- AWS CLI (opcional)

## Inicialização

```bash
# Clonar
git clone https://github.com/guinatural/holocron-career-ai.git
cd holocron-career-ai

# Instalar dependências
./scripts/setup.ps1  # Windows
# ou
./scripts/setup.sh   # Linux/Mac

# Iniciar containers
docker-compose up -d
```

## Variáveis de Ambiente

Crie `.env.local` na raiz:

```bash
ENVIRONMENT=local
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/holocron
REDIS_URL=redis://localhost:6379
CHROMA_DB_PATH=http://localhost:8000

# Cognito (dev mode)
COGNITO_USER_POOL_ID=dev-pool
COGNITO_CLIENT_ID=dev-client
COGNITO_REGION=us-east-1

# Bedrock (opcional)
AWS_REGION=us-east-1
```

## Serviços Locais

| Serviço | Porta | URL |
|---|---|---|
| API | 8000 | http://localhost:8000/docs |
| PostgreSQL | 5432 | postgresql://localhost:5432 |
| Redis | 6379 | redis://localhost:6379 |
| ChromaDB | 8000 | http://localhost:8000 |

## Migrations

```bash
cd apps/api
alembic upgrade head
```

## Testes

```bash
# API tests
cd apps/api
pytest tests/ -v --cov=src

# Web tests
cd apps/web
npm test
```

## Debugging

```bash
# API debug
cd apps/api
uvicorn src.main:app --reload --debug

# Redis monitor
docker exec -it holocron-redis redis-cli MONITOR

# PostgreSQL logs
docker logs holocron-postgres
```