"""Application layer use cases (business logic)."""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from datetime import datetime
from ..domain.models import (
    Job, JobCreate, Company, CompanyCreate,
    Application, ApplicationCreate, ApplicationUpdate,
    ResumeVersion, ApplicationEvent
)
from ..domain.ports import (
    JobRepository, CompanyRepository, ApplicationRepository,
    ResumeRepository, EventRepository, RAGRepository
)
from ..security.anonymization import lgpd_anonymize


class JobService(ABC):
    """Job domain service interface."""
    
    @abstractmethod
    def list_jobs(
        self, tenant_id: str, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Job], int]:
        """Get paginated job list for tenant."""
        pass
    
    @abstractmethod
    def search_jobs(
        self, tenant_id: str, query: str, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Job], int]:
        """Search jobs by text query."""
        pass
    
    @abstractmethod
    def create_job(self, tenant_id: str, job: JobCreate) -> Job:
        """Create new job posting."""
        pass
    
    @abstractmethod
    def update_job(self, tenant_id: str, job: Job) -> Job:
        """Update job posting."""
        pass
    
    @abstractmethod
    def delete_job(self, tenant_id: str, job_id: str) -> bool:
        """Soft delete job."""
        pass


class CompanyService(ABC):
    """Company domain service interface."""
    
    @abstractmethod
    def list_companies(self, tenant_id: str) -> List[Company]:
        """Get companies for tenant."""
        pass
    
    @abstractmethod
    def create_company(self, tenant_id: str, company: CompanyCreate) -> Company:
        """Create new company."""
        pass
    
    @abstractmethod
    def update_company(self, tenant_id: str, company: Company) -> Company:
        """Update company."""
        pass


class ApplicationService(ABC):
    """Application domain service interface."""
    
    @abstractmethod
    def list_applications(
        self, tenant_id: str, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Application], int]:
        """Get paginated application list."""
        pass
    
    @abstractmethod
    def create_application(
        self, tenant_id: str, application: ApplicationCreate
    ) -> Application:
        """Create new application."""
        pass
    
    @abstractmethod
    def update_application(
        self, tenant_id: str, application_id: str, updates: ApplicationUpdate
    ) -> Application:
        """Update application."""
        pass
    
    @abstractmethod
    def delete_application(self, tenant_id: str, application_id: str) -> bool:
        """Soft delete application."""
        pass
    
    @abstractmethod
    def match_application(
        self, tenant_id: str, application_id: str
    ) -> Tuple[float, List[str]]:
        """Run AI matching and return score + breakdown."""
        pass
    
    @abstractmethod
    def generate_resume(
        self, tenant_id: str, application_id: str, original_text: str
    ) -> ResumeVersion:
        """Generate optimized resume version."""
        pass
    
    @abstractmethod
    def add_event(
        self, tenant_id: str, application_id: str, event_type: str,
        description: str, created_by: Optional[str] = None
    ) -> ApplicationEvent:
        """Add audit event for application."""
        pass


class RAGService(ABC):
    """RAG pipeline service interface."""
    
    @abstractmethod
    def ingest_job(self, tenant_id: str, job: Job) -> str:
        """Ingest job into RAG vector store."""
        pass
    
    @abstractmethod
    def ingest_document(
        self, tenant_id: str, content: str, doc_type: str
    ) -> str:
        """Ingest arbitrary document into RAG."""
        pass
    
    @abstractmethod
    def search_jobs_rag(
        self, tenant_id: str, query: str, limit: int = 5
    ) -> List[dict]:
        """Search jobs using RAG."""
        pass
    
    @abstractmethod
    def get_relevant_docs(
        self, tenant_id: str, job_id: str, limit: int = 3
    ) -> List[dict]:
        """Get relevant documents for job matching."""
        pass


# Implementation base classes
class BaseJobService(JobService):
    """Base implementation for JobService."""
    
    def __init__(
        self, job_repo: JobRepository, rag_repo: Optional[RAGRepository] = None
    ):
        self.job_repo = job_repo
        self.rag_repo = rag_repo
    
    def list_jobs(self, tenant_id: str, skip: int = 0, limit: int = 10) -> Tuple[List[Job], int]:
        return self.job_repo.get_by_tenant(tenant_id, skip, limit)
    
    def search_jobs(self, tenant_id: str, query: str, skip: int = 0, limit: int = 10) -> Tuple[List[Job], int]:
        # In production, this would use RAG for semantic search
        return self.job_repo.search(tenant_id, query, skip, limit)
    
    def create_job(self, tenant_id: str, job: JobCreate) -> Job:
        job_dict = job.model_dump()
        job_dict["id"] = f"job_{datetime.now().timestamp()}"
        job_dict["created_at"] = datetime.now()
        job_dict["updated_at"] = datetime.now()
        
        new_job = Job(**job_dict)
        return self.job_repo.create(tenant_id, new_job)
    
    def update_job(self, tenant_id: str, job: Job) -> Job:
        job.updated_at = datetime.now()
        return self.job_repo.update(tenant_id, job)
    
    def delete_job(self, tenant_id: str, job_id: str) -> bool:
        return self.job_repo.delete(tenant_id, job_id)


class BaseApplicationService(ApplicationService):
    """Base implementation for ApplicationService."""
    
    def __init__(
        self,
        app_repo: ApplicationRepository,
        resume_repo: ResumeRepository,
        event_repo: EventRepository,
        rag_service: RAGService
    ):
        self.app_repo = app_repo
        self.resume_repo = resume_repo
        self.event_repo = event_repo
        self.rag_service = rag_service
    
    def list_applications(self, tenant_id: str, skip: int = 0, limit: int = 10) -> Tuple[List[Application], int]:
        return self.app_repo.get_by_tenant(tenant_id, skip, limit)
    
    def create_application(self, tenant_id: str, application: ApplicationCreate) -> Application:
        anonymized = lgpd_anonymize({"candidate_name": application.candidate_name})
        
        app_dict = application.model_dump()
        app_dict["id"] = f"app_{datetime.now().timestamp()}"
        app_dict["status"] = "active"
        app_dict["applied_at"] = datetime.now()
        app_dict["updated_at"] = datetime.now()
        app_dict["score"] = None  # Will be calculated by matching agent
        
        new_app = Application(**app_dict)
        result = self.app_repo.create(tenant_id, new_app)
        
        # Add initial event
        self.add_event(tenant_id, result.id, "created", "Application created")
        
        return result
    
    def update_application(self, tenant_id: str, application_id: str, updates: ApplicationUpdate) -> Application:
        current = self.app_repo.get_by_id(tenant_id, application_id)
        if not current:
            raise ValueError("Application not found")
        
        update_dict = updates.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(current, key, value)
        current.updated_at = datetime.now()
        
        result = self.app_repo.update(tenant_id, current)
        
        if updates.status and updates.status != current.status:
            self.add_event(tenant_id, application_id, "status_change", f"Status changed to {updates.status.value}")
        
        return result
    
    def delete_application(self, tenant_id: str, application_id: str) -> bool:
        return self.app_repo.delete(tenant_id, application_id)
    
    def match_application(self, tenant_id: str, application_id: str) -> Tuple[float, List[str]]:
        # This would be implemented by the Matching Agent
        # For now, returning placeholder
        return 75.0, ["Resume matches 60% of requirements", "Experience level matches", "Location is acceptable"]
    
    def generate_resume(self, tenant_id: str, application_id: str, original_text: str) -> ResumeVersion:
        # This would be implemented by the Resume Agent
        # For now, returning placeholder
        return ResumeVersion(
            id=f"resume_{datetime.now().timestamp()}",
            tenant_id=tenant_id,
            application_id=application_id,
            content=original_text,  # In production, this would be AI-optimized
            version=1,
            created_at=datetime.now(),
            created_by="resume_agent",
            ats_score=85.0
        )
    
    def add_event(self, tenant_id: str, application_id: str, event_type: str, description: str, created_by: Optional[str] = None) -> ApplicationEvent:
        event_dict = {
            "id": f"evt_{datetime.now().timestamp()}",
            "tenant_id": tenant_id,
            "application_id": application_id,
            "event_type": event_type,
            "description": description,
            "created_at": datetime.now(),
            "created_by": created_by
        }
        return self.event_repo.create(tenant_id, **event_dict)