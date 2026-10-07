# Guia de Variáveis de Ambiente

## Variáveis de Aplicação

| Variável | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `ENVIRONMENT` | Sim | Ambiente: local, staging, production | `local` |
| `APP_NAME` | Não | Nome da aplicação | `Holocron Career AI` |
| `APP_VERSION` | Não | Versão da aplicação | `0.1.0` |
| `DEBUG` | Não | Modo debug | `false` |

## Database

| Variável | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `DATABASE_URL` | Sim | Connection string PostgreSQL | `postgresql://user:pass@host:5432/db` |
| `DATABASE_POOL_SIZE` | Não | Pool size | `10` |
| `DATABASE_MAX_OVERFLOW` | Não | Max overflow | `20` |

## Redis

| Variável | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `REDIS_URL` | Sim | Connection string Redis | `redis://localhost:6379` |
| `REDIS_CACHE_TTL` | Não | TTL em segundos | `3600` |

## Cognito (Auth)

| Variável | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `COGNITO_USER_POOL_ID` | Sim | Pool ID | `us-east-1_XXXXX` |
| `COGNITO_CLIENT_ID` | Sim | Client ID | `XXXXX` |
| `COGNITO_REGION` | Sim | AWS Region | `us-east-1` |
| `COGNITO_DEV_BYPASS` | Não | Bypass auth (dev only) | `true` |

## Bedrock (IA)

| Variável | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `BEDROCK_REGION` | Sim | AWS Region | `us-east-1` |
| `BEDROCK_HAIKU_MODEL` | Não | Model ID Haiku | `anthropic.claude-3-5-haiku-20241022-v1:0` |
| `BEDROCK_SONNET_MODEL` | Não | Model ID Sonnet | `anthropic.claude-3-5-sonnet-20241022-v2:0` |

## ChromaDB (RAG)

| Variável | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `CHROMA_DB_PATH` | Sim | Path ou URL | `http://localhost:8000` |
| `CHROMA_DB_COLLECTION` | Não | Collection name | `career_jobs` |

## Budget

| Variável | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `DAILY_TOKEN_BUDGET` | Sim | Tokens/dia | `100000` |
| `COST_LIMIT_USD` | Sim | Limite diário USD | `10.00` |

## CORS

| Variável | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `CORS_ORIGINS` | Sim | Origins permitidos | `http://localhost:3000` |

## Segurança

| Variável | Obrigatório | Descrição | Exemplo |
|---|---|---|---|
| `SESSION_KEY` | Sim | Chave de criptografia (32 bytes) | `...` |
| `JWT_SECRET` | Sim | Secret para JWT | `...` |
| `JWT_EXPIRY_HOURS` | Não | Tempo de expiração | `24` |

## Exemplo - Local

```bash
# .env.local
ENVIRONMENT=local
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/holocron
REDIS_URL=redis://localhost:6379
CHROMA_DB_PATH=http://localhost:8000
COGNITO_DEV_BYPASS=true
DAILY_TOKEN_BUDGET=100000
COST_LIMIT_USD=10.00
CORS_ORIGINS=http://localhost:3000
SESSION_KEY=your_32_byte_key_here
JWT_SECRET=your_jwt_secret_here
```

## Exemplo - Production

```bash
# .env.production
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@rds.amazonaws.com:5432/prod
REDIS_URL=redis://redis.amazonaws.com:6379
CHROMA_DB_PATH=http://chromadb.amazonaws.com:8000
COGNITO_USER_POOL_ID=us-east-1_XXXXX
COGNITO_CLIENT_ID=XXXXX
COGNITO_REGION=us-east-1
BEDROCK_REGION=us-east-1
DAILY_TOKEN_BUDGET=500000
COST_LIMIT_USD=50.00
CORS_ORIGINS=https://yourdomain.com
```