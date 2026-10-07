# Fluxos de Agentes - Holocron Career AI

## Visão Geral

8 Agentes especializados coordenados pelo Strands Agent SDK.

---

## Agentes

### 1. Search Agent (Fase 2)

**Responsabilidade:** Ingestão de vagas e busca inteligente

**Fontes:**
- RSS feeds (RemoteOK, Remotive)
- APIs (Adzuna, Indeed)
- Import manual (URL/paste)

**Tools:**
```python
@agent.tool
def fetch_rss_jobs(feed_url: str) -> List[Job]:
    """Fetch jobs from RSS feed."""

@agent.tool
def search_api_jobs(api_key: str, query: str) -> List[Job]:
    """Search jobs via API."""

@agent.tool
def deduplicate_jobs(jobs: List[Job]) -> List[Job]:
    """Remove duplicates by hash(title+company)."""
```

**Workflow:**
```
Schedule (15min) → Fetch RSS → Parse → Deduplicate → Store → RAG Ingest
                 → Fetch API → Parse → Deduplicate → Store → RAG Ingest
```

---

### 2. Matching Agent (Fase 3)

**Responsabilidade:** Score 0-100 com explicação RAG

**Inputs:**
- Candidate resume (text)
- Job requirements (structured)

**Process:**
```
Resume → Extract skills/experience → RAG retrieve relevant jobs
       → Compare → Score → Breakdown explanation
```

**Tools:**
```python
@agent.tool
def extract_skills_from_resume(text: str) -> List[str]:
    """Extract skills from resume text."""

@agent.tool
def retrieve_relevant_jobs(candidate_skills: List[str]) -> List[Job]:
    """Retrieve jobs matching candidate skills."""

@agent.tool
def calculate_match_score(resume_skills: List[str], job_requirements: List[str]) -> float:
    """Calculate 0-100 match score."""
```

**Output:**
```json
{
    "score": 87.5,
    "breakdown": [
        "Skills match: 90% (Python, AWS, Docker)",
        "Experience level match: 85% (3+ years required, 4 years candidate)",
        "Location match: 100% (Remote accepted)"
    ],
    "missing_skills": ["Kubernetes"],
    "recommended_skills": ["Kubernetes", "Terraform"]
}
```

---

### 3. Resume Agent (Fase 4)

**Responsabilidade:** ATS-optimized resume generation

**Inputs:**
- Original resume text
- Target job requirements

**Process:**
```
Resume → Keyword optimization → ATS score → Version → Store
       → Generate ATS-compliant PDF
```

**Tools:**
```python
@agent.tool
def optimize_for_ats(text: str, job_requirements: List[str]) -> str:
    """Optimize resume with ATS keywords."""

@agent.tool
def calculate_ats_score(text: str) -> float:
    """Calculate ATS compatibility score (0-100)."""

@agent.tool
def generate_pdf(text: str) -> str:
    """Generate PDF from text (WeasyPrint)."""
```

**Versioning:**
- Version 1: Original
- Version 2: ATS-optimized
- Version N: Iterations based on feedback

---

### 4. Cover Letter Agent (Fase 5)

**Responsabilidade:** Personalized cover letter generation

**Inputs:**
- Job description
- Candidate background
- Company info

**Process:**
```
Job + Background → Draft → Personalization score → Anti-generic check → Store
```

**Tools:**
```python
@agent.tool
def generate_cover_letter(job: Job, background: str) -> str:
    """Generate personalized cover letter."""

@agent.tool
def check_generic_score(text: str) -> float:
    """Check if text is too generic (0-100, higher is worse)."""

@agent.tool
def personalize_with_company_info(text: str, company: Company) -> str:
    """Add company-specific personalization."""
```

**Formats:**
- Email subject
- Email body
- PDF attachment

---

### 5. CRM Agent (Fase 6)

**Responsabilidade:** Pipeline management and automation

**Tools:**
```python
@agent.tool
def update_application_status(app_id: str, new_status: str, notes: str):
    """Update application status with audit trail."""

@agent.tool
def assign_recruiter(app_id: str, recruiter_id: str):
    """Assign recruiter to application."""

@agent.tool
def suggest_next_steps(app: Application) -> List[str]:
    """Suggest next steps based on current status."""
```

**Workflow:**
```
Application status change → CRM Agent → Update timeline → Suggest action
```

---

### 6. Interview Agent (Fase 7)

**Responsabilidade:** Interview preparation pack generation

**Inputs:**
- Job requirements
- Candidate resume
- Interview stage (tech/HR)

**Process:**
```
Job + Resume → Technical questions → STAR questions → Prep pack
```

**Tools:**
```python
@agent.tool
def generate_technical_questions(job: Job, count: int = 10) -> List[Question]:
    """Generate technical interview questions."""

@agent.tool
def generate_star_questions(resume: str, count: int = 5) -> List[Question]:
    """Generate behavioral STAR questions."""

@agent.tool
def generate_preparation_plan(job: Job, level: str) -> str:
    """Generate interview preparation plan."""
```

**Output:**
```json
{
    "tech_questions": [
        {"question": "...", "expected_answer": "...", "difficulty": "medium"}
    ],
    "star_questions": [
        {"question": "Tell me about a time...", "scenario": "conflict"}
    ],
    "company_research": ["Research their AWS usage...", "Check their tech stack..."],
    "questions_to_ask": ["What is your tech stack?", "How do you handle compliance?"]
}
```

---

### 7. Learning Agent (Fase 8)

**Responsabilidade:** Insights and recommendations

**Process:**
```
Batch processing (nightly) → Correlate data → Generate insights → Notify
```

**Tools:**
```python
@agent.tool
def analyze_application_patterns(tenant_id: str) -> dict:
    """Analyze application patterns for the tenant."""

@agent.tool
def generate_insights(tenant_id: str) -> List[Insight]:
    """Generate weekly insights."""

@agent.tool
def recommend_actions(tenant_id: str) -> List[Action]:
    """Recommend actions based on insights."""
```

**Insights:**
- Top skills in demand (by market)
- Best performing resume keywords
- Common rejection reasons
- Salary range recommendations

---

## Agent Orchestration

### Strands Agent SDK Pattern

```python
from strands import Agent, tool

class MatchingAgent(Agent):
    name = "matching_agent"
    model = "claude-3-5-sonnet"
    
    @tool
    def calculate_score(self, resume: str, job: str) -> float:
        """Calculate match score 0-100."""
        pass
    
    @tool
    def explain_breakdown(self, score: float, resume: str, job: str) -> str:
        """Explain scoring breakdown."""
        pass

# Usage
agent = MatchingAgent()
result = agent.run("Calculate score for John's resume against Senior AWS role")
```

### Agent Coordinator

```python
class AgentCoordinator:
    def __init__(self):
        self.agents = {
            'search': SearchAgent(),
            'matching': MatchingAgent(),
            'resume': ResumeAgent(),
            'cover_letter': CoverLetterAgent(),
            'crm': CRMAgent(),
            'interview': InterviewAgent(),
            'learning': LearningAgent()
        }
    
    def route(self, user_request: str) -> Tuple[Agent, dict]:
        """Route request to appropriate agent."""
        # Use LLM to classify request
        agent_name = classify_request(user_request)
        agent = self.agents[agent_name]
        return agent, parse_params(user_request)
```