# Modelo de Dados - Holocron Career AI

## Schema PostgreSQL

### Entidades Principais

```
tenants (multi-tenancy)
├── jobs
├── companies
├── applications
└── recruiters

applications
├── resume_versions (history)
└── application_events (timeline)

recruiters
└── application_recruiters (assignment)
```

---

## Tabelas

### tenants
```sql
CREATE TABLE tenants (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### jobs
```sql
CREATE TABLE jobs (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements JSONB NOT NULL,
    benefits JSONB NOT NULL,
    location VARCHAR(255) NOT NULL,
    remote BOOLEAN DEFAULT FALSE,
    salary_min NUMERIC,
    salary_max NUMERIC,
    currency VARCHAR(3) DEFAULT 'BRL',
    level VARCHAR(20) NOT NULL CHECK (level IN ('junior', 'pleno', 'senior', 'lead', 'manager', 'director')),
    stack JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_jobs_tenant_status ON jobs(tenant_id, status);
CREATE INDEX idx_jobs_tenant_level ON jobs(tenant_id, level);
CREATE INDEX idx_jobs_title ON jobs(title);
```

### companies
```sql
CREATE TABLE companies (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(255),
    logo_url VARCHAR(500),
    size VARCHAR(50),
    industry VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### applications
```sql
CREATE TABLE applications (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    job_id UUID NOT NULL REFERENCES jobs(id),
    candidate_name VARCHAR(255) NOT NULL,
    candidate_email VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN (
        'draft', 'active', 'in_review', 'interview', 'offer', 'declined', 'hired', 'archived'
    )),
    score NUMERIC(5,2),
    notes TEXT,
    resume_url VARCHAR(500),
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    interview_date TIMESTAMP WITH TIME ZONE,
    offer_letter_url VARCHAR(500)
);

CREATE INDEX idx_applications_tenant ON applications(tenant_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_applications_job ON applications(job_id);
```

### resume_versions
```sql
CREATE TABLE resume_versions (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    application_id UUID NOT NULL REFERENCES applications(id),
    content TEXT NOT NULL,
    ats_score NUMERIC(5,2),
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(50) NOT NULL  -- Agent ID
);
```

### application_events
```sql
CREATE TABLE application_events (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    application_id UUID NOT NULL REFERENCES applications(id),
    event_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES tenants(id)
);
```

### recruiters
```sql
CREATE TABLE recruiters (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    team VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### application_recruiters
```sql
CREATE TABLE application_recruiters (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL,
    application_id UUID NOT NULL REFERENCES applications(id),
    recruiter_id UUID NOT NULL REFERENCES recruiters(id),
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## Índices para Performance

```sql
-- Multi-tenant queries
CREATE INDEX idx_jobs_tenant_id ON jobs(tenant_id);
CREATE INDEX idx_companies_tenant_id ON companies(tenant_id);
CREATE INDEX idx_applications_tenant_id ON applications(tenant_id);
CREATE INDEX idx_recruiters_tenant_id ON recruiters(tenant_id);

-- Common filters
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_level ON jobs(level);
CREATE INDEX idx_jobs_remote ON jobs(remote);

-- Date ordering
CREATE INDEX idx_applications_applied_at ON applications(applied_at DESC);
CREATE INDEX idx_events_created_at ON application_events(created_at);

-- Composite for pagination
CREATE INDEX idx_applications_tenant_applied ON applications(tenant_id, applied_at DESC);
```

---

## RLS (Row Level Security) - Fase 8

```sql
-- Enable RLS
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE companies ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY tenant_isolation ON jobs
    USING (tenant_id = current_setting('app.tenant_id')::UUID);

CREATE POLICY tenant_isolation ON applications
    USING (tenant_id = current_setting('app.tenant_id')::UUID);
```

---

## Vector Store (ChromaDB) - RAG

### Collections

| Collection | Conteúdo | Embeddings |
|---|---|---|
| `jobs` | Vagas publicadas | Title + description + stack |
| `resumes` | Currículos (hashed) | Content |
| `documents` | Artigos, guias | Full text |

### Metadata por item
```json
{
    "job_id": "uuid",
    "tenant_id": "uuid",
    "created_at": "iso8601",
    "source": "manual|rss|api"
}
```