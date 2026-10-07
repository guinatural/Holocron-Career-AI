# OpenAPI / Contratos de API - Fase 1

## Endpoints

### Health
```yaml
GET /health
tags: [system]
responses:
  200:
    description: Health check
    content:
      application/json:
        schema:
          type: object
          properties:
            status: string
            service: string
            version: string
            environment: string
```

### Jobs

```yaml
GET /api/v1/jobs
tags: [jobs]
parameters:
  - name: skip
    in: query
    schema: { type: integer, default: 0 }
  - name: limit
    in: query
    schema: { type: integer, default: 10 }
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            items: { type: array, items: { $ref: '#/components/schemas/Job' } }
            total: integer
            page: integer
            pages: integer

POST /api/v1/jobs
tags: [jobs]
requestBody:
  content:
    application/json:
      schema: { $ref: '#/components/schemas/JobCreate' }
responses:
  201:
    content:
      application/json:
        schema: { $ref: '#/components/schemas/Job' }
```

### Applications

```yaml
POST /api/v1/applications
tags: [applications]
requestBody:
  content:
    application/json:
      schema: { $ref: '#/components/schemas/ApplicationCreate' }
responses:
  201:
    content:
      application/json:
        schema: { $ref: '#/components/schemas/Application' }

PUT /api/v1/applications/{id}
tags: [applications]
parameters:
  - name: id
    in: path
    required: true
    schema: { type: string, format: uuid }
requestBody:
  content:
    application/json:
      schema: { $ref: '#/components/schemas/ApplicationUpdate' }
responses:
  200:
    content:
      application/json:
        schema: { $ref: '#/components/schemas/Application' }
```

### Matching

```yaml
GET /api/v1/match/{id}
tags: [matching]
parameters:
  - name: id
    in: path
    required: true
    schema: { type: string, format: uuid }
responses:
  200:
    content:
      application/json:
        schema:
          type: object
          properties:
            score: number
            breakdown: { type: array, items: string }
```

### Resume

```yaml
POST /api/v1/resume/{id}
tags: [resume]
parameters:
  - name: id
    in: path
    required: true
    schema: { type: string, format: uuid }
responses:
  201:
    content:
      application/json:
        schema: { $ref: '#/components/schemas/ResumeVersion' }
```

## Schemas

```yaml
components:
  schemas:
    Job:
      type: object
      properties:
        id: { type: string, format: uuid }
        tenant_id: { type: string, format: uuid }
        title: { type: string }
        company_id: { type: string, format: uuid }
        description: { type: string }
        requirements: { type: array, items: string }
        benefits: { type: array, items: string }
        location: { type: string }
        remote: { type: boolean }
        salary_min: { type: number }
        salary_max: { type: number }
        currency: { type: string, default: BRL }
        level:
          type: string
          enum: [junior, pleno, senior, lead, manager, director]
        stack: { type: array, items: string }
        status: { type: string, default: active }
        created_at: { type: string, format: date-time }
        updated_at: { type: string, format: date-time }
        published_at: { type: string, format: date-time, nullable: true }

    JobCreate:
      type: object
      required: [title, company_id, description, requirements, benefits, location, level, stack]
      properties:
        title: { type: string }
        company_id: { type: string, format: uuid }
        description: { type: string }
        requirements: { type: array, items: string }
        benefits: { type: array, items: string }
        location: { type: string }
        remote: { type: boolean, default: false }
        salary_min: { type: number }
        salary_max: { type: number }
        level:
          type: string
          enum: [junior, pleno, senior, lead, manager, director]
        stack: { type: array, items: string }

    Application:
      type: object
      properties:
        id: { type: string, format: uuid }
        tenant_id: { type: string, format: uuid }
        job_id: { type: string, format: uuid }
        candidate_name: { type: string }
        candidate_email: { type: string, format: email }
        status:
          type: string
          enum: [draft, active, in_review, interview, offer, declined, hired, archived]
        score: { type: number }
        notes: { type: string, nullable: true }
        resume_url: { type: string, nullable: true }
        applied_at: { type: string, format: date-time }
        updated_at: { type: string, format: date-time }
        interview_date: { type: string, format: date-time, nullable: true }
        offer_letter_url: { type: string, nullable: true }

    ApplicationCreate:
      type: object
      required: [job_id, candidate_name, candidate_email]
      properties:
        job_id: { type: string, format: uuid }
        candidate_name: { type: string }
        candidate_email: { type: string, format: email }
        resume_text: { type: string, nullable: true }

    ApplicationUpdate:
      type: object
      properties:
        status:
          type: string
          enum: [draft, active, in_review, interview, offer, declined, hired, archived]
        notes: { type: string, nullable: true }
        interview_date: { type: string, format: date-time, nullable: true }
        offer_letter_url: { type: string, nullable: true }

    ResumeVersion:
      type: object
      properties:
        id: { type: string, format: uuid }
        tenant_id: { type: string, format: uuid }
        application_id: { type: string, format: uuid }
        content: { type: string }
        ats_score: { type: number, nullable: true }
        version: { type: integer }
        created_at: { type: string, format: date-time }
        created_by: { type: string }
```