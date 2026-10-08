# Holocron Career AI

> **Plataforma SaaS multi-tenant de gestão de carreira com agentes de IA**

[![CI](https://github.com/guinatural/holocron-career-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/guinatural/holocron-career-ai/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/guinatural/holocron-career-ai/branch/main/graph/badge.svg)](https://codecov.io/gh/guinatural/holocron-career-ai)

---

## Visão Geral

O Holocron Career AI é o produto principal do ecossistema Holocron: uma plataforma SaaS multi-tenant focada na gestão automatizada de carreiras. Ao invés de operações tradicionais de CRUD, a aplicação é construída sobre uma arquitetura orientada a eventos (Event-Driven) e serverless, utilizando o Amazon Bedrock (GenAI) para correspondência semântica de currículos e operação de agentes autônomos.

---

## Arquitetura de Produção (AWS Native)

A arquitetura foi desenhada com foco nos pilares do **AWS Well-Architected Framework**, garantindo Observabilidade (O11y), Controle de Custos (FinOps) e Segurança (Zero Trust).

```mermaid
flowchart TD
    subgraph "Frontend Layer (Vercel / AWS Amplify)"
        UI[Next.js 15 UI - Dashboard]
    end

    subgraph "API Layer (AWS ECS Fargate / App Runner)"
        API[FastAPI Backend]
        O11y[OpenTelemetry / AWS X-Ray]
        API --- O11y
    end

    subgraph "State & Vector Store"
        PG[(PostgreSQL / RDS)]
        Redis[(Redis Cache)]
        Chroma[(ChromaDB)]
    end

    subgraph "AWS AI & Event Core"
        Bedrock[Amazon Bedrock\nClaude 3.5 / Titan Embeddings]
        EventBus{Amazon EventBridge}
        Worker[AWS Step Functions\nAgent Workflows]
        FinOps[AWS Budgets\nCost Alerts]
    end

    UI -->|REST API + JWT| API
    API -->|Read/Write| PG
    API -->|Cache| Redis
    API -->|RAG Query| Chroma
    API -->|Emit Event| EventBus
    
    EventBus -->|Trigger| Worker
    Worker -->|Invoke LLM| Bedrock
    Chroma <-->|Embeddings| Bedrock
    
    FinOps -.->|Monitor| Bedrock
```

### Padrões Enterprise Implementados
1. **FinOps & Cost Control:** AWS Budgets integrados via **AWS CDK** para matar execuções caso o custo de tokens passe do limite diário estabelecido.
2. **Observabilidade Total:** Logs estruturados e *traces* de execução de IA injetados em todas as chamadas do Bedrock.
3. **Infraestrutura como Código (IaC):** Stack definida integralmente em **AWS CDK (TypeScript/Python)**.
┌──────────────────────▼──────────────────────────────────┐
│                  8 Agentes de IA                        │
│  Search  │ Matching │ Resume │ Cover │ Application     │
│  CRM     │ Interview  │ Learning                          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Model (Amazon Bedrock)                     │
│         Claude 3.5 Haiku / Sonnet (AWS)                 │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                    Data Layer                           │
│  PostgreSQL │ ChromaDB (RAG) │ Redis (Cache)            │
└─────────────────────────────────────────────────────────┘
```

---

## Stack Tecnológica

| Camada | Tecnologia |
|---|---|
| **Frontend** | Next.js 15, Tailwind, shadcn/ui |
| **Backend** | FastAPI, Uvicorn, Pydantic v2 |
| **Auth** | Amazon Cognito + JWT |
| **Database** | PostgreSQL 16 + Alembic |
| **Vector Store** | ChromaDB (local) → Bedrock KB (prod) |
| **Cache** | Redis |
| **Agentes** | Strands Agents SDK + LangGraph |
| **IA** | Amazon Bedrock (Claude 3.5) |
| **Infra** | Docker Compose (dev) → ECS Fargate (prod) |
| **CI/CD** | GitHub Actions |

---

## Estrutura do Projeto

```
holocron-career-ai/
├── apps/
│   ├── api/                    # FastAPI backend
│   │   ├── src/
│   │   │   ├── domain/         # Entities, ports
│   │   │   ├── application/    # Use cases, services
│   │   │   ├── infrastructure/ # DB, external APIs
│   │   │   └── presentation/   # Controllers, routes
│   │   ├── alembic/            # Database migrations
│   │   └── tests/
│   └── web/                    # Next.js frontend
│       ├── src/
│       │   ├── app/
│       │   ├── components/
│       │   └── lib/
├── packages/
│   ├── core/                   # Shared types, DTOs
│   ├── agents/                 # Strands agent definitions
│   └── rag/                    # RAG pipeline
├── infra/
│   ├── docker/
│   │   └── docker-compose.yml  # Local development
│   └── terraform/              # AWS production (Fase 8+)
├── docs/
│   ├── adr/                    # Architecture Decision Records
│   └── openapi/                # API specification
├── scripts/
│   └── import-candidaturas.py  # Data import utility
├── .github/workflows/          # CI/CD pipelines
├── .cursorrules                # Prompt engineering rules
├── README.md
└── requirements.txt            # Python dependencies
```

---

## Fases de Implementação

| Fase | Objetivo | Status |
|---|---|---|
| 0 | Documentação e arquitetura | |
| 1 | Fundação (CRM funcional) | Planejado |
| 2 | Search Agent + RSS ingestion | Planejado |
| 3 | Matching Agent + RAG | Planejado |
| 4 | Resume Agent | Planejado |
| 5 | Cover Letter + Mensagens | Planejado |
| 6 | CRM Completo + Kanban | Planejado |
| 7 | Interview Agent | Planejado |
| 8 | Aprendizado + AWS Deploy | Planejado |

---

## Começando (Desenvolvimento Local)

### Requisitos

- Python 3.12+
- Node.js 18+ (para frontend)
- Docker + Docker Compose
- AWS Account (opcional para Bedrock)

### Instalação

```bash
# Clonar o repositório
git clone https://github.com/guinatural/holocron-career-ai.git
cd holocron-career-ai

# Iniciar ambiente local
docker compose up -d

# Acessar
# API: http://localhost:8000/docs
# Frontend: http://localhost:3000
```

### Variáveis de Ambiente (local)

```bash
# .env.local
ENVIRONMENT=local
DATABASE_URL=postgresql://user:pass@localhost:5432/holocron
REDIS_URL=redis://localhost:6379

# Cognito (desenvolvimento)
COGNITO_USER_POOL_ID=dev-pool
COGNITO_CLIENT_ID=dev-client

# Bedrock (opcional)
AWS_REGION=us-east-1
```

---

## Documentação

- [Roadmap Completo](docs/ROADMAP.md)
- [Arquitetura Técnica](docs/ARQUITETURA.md)
- [Modelo de Dados](docs/MODELO-DE-DADOS.md)
- [ADR - Decisões](docs/adr/)
- [OpenAPI Spec](docs/openapi/)

---

## Autoria

Desenvolvido por **Guilherme Barreto Gomes**

- GitHub: [@guinatural](https://github.com/guinatural)
- LinkedIn: [linkedin.com/in/guinatural](https://linkedin.com/in/guinatural)

---

## Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## Relacionado

- [Holocron Sentinel](https://github.com/guinatural/Holocron-Sentinel-AWS-AgentCore) - Agente de auditoria AWS
- [Wayfinder Cloud](https://github.com/guinatural/wayfinder-cloud) -Governança contínua AWS

---
