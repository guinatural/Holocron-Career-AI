"""Port interfaces for domain layer (Dependency Inversion)."""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from datetime import datetime
from .models import (
    Job, JobCreate, JobList,
    Company, CompanyCreate,
    Application, ApplicationCreate, ApplicationUpdate,
    ResumeVersion, ApplicationEvent, Recruiter, ApplicationRecruiter
)


# Job Repository Port
class JobRepository(ABC):
    """Interface for job persistence."""
    
    @abstractmethod
    def get_by_id(self, tenant_id: str, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        pass
    
    @abstractmethod
    def get_by_tenant(
        self, tenant_id: str, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Job], int]:
        """Get jobs for tenant with pagination."""
        pass
    
    @abstractmethod
    def get_by_company(self, tenant_id: str, company_id: str) -> List[Job]:
        """Get jobs by company."""
        pass
    
    @abstractmethod
    def search(
        self, tenant_id: str, query: str, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Job], int]:
        """Search jobs by text."""
        pass
    
    @abstractmethod
    def create(self, tenant_id: str, job: JobCreate) -> Job:
        """Create new job."""
        pass
    
    @abstractmethod
    def update(self, tenant_id: str, job: Job) -> Job:
        """Update existing job."""
        pass
    
    @abstractmethod
    def delete(self, tenant_id: str, job_id: str) -> bool:
        """Soft delete job."""
        pass


# Company Repository Port
class CompanyRepository(ABC):
    """Interface for company persistence."""
    
    @abstractmethod
    def get_by_id(self, tenant_id: str, company_id: str) -> Optional[Company]:
        """Get company by ID."""
        pass
    
    @abstractmethod
    def get_by_tenant(self, tenant_id: str) -> List[Company]:
        """Get companies for tenant."""
        pass
    
    @abstractmethod
    def create(self, tenant_id: str, company: CompanyCreate) -> Company:
        """Create new company."""
        pass
    
    @abstractmethod
    def update(self, tenant_id: str, company: Company) -> Company:
        """Update existing company."""
        pass


# Application Repository Port
class ApplicationRepository(ABC):
    """Interface for application persistence."""
    
    @abstractmethod
    def get_by_id(self, tenant_id: str, application_id: str) -> Optional[Application]:
        """Get application by ID."""
        pass
    
    @abstractmethod
    def get_by_tenant(
        self, tenant_id: str, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Application], int]:
        """Get applications for tenant with pagination."""
        pass
    
    @abstractmethod
    def get_by_job(self, tenant_id: str, job_id: str) -> List[Application]:
        """Get applications for job."""
        pass
    
    @abstractmethod
    def get_by_status(
        self, tenant_id: str, status: str, skip: int = 0, limit: int = 10
    ) -> Tuple[List[Application], int]:
        """Get applications by status."""
        pass
    
    @abstractmethod
    def create(self, tenant_id: str, application: ApplicationCreate) -> Application:
        """Create new application."""
        pass
    
    @abstractmethod
    def update(self, tenant_id: str, application: Application) -> Application:
        """Update existing application."""
        pass
    
    @abstractmethod
    def delete(self, tenant_id: str, application_id: str) -> bool:
        """Soft delete application."""
        pass


# Resume Repository Port
class ResumeRepository(ABC):
    """Interface for resume persistence."""
    
    @abstractmethod
    def get_by_application(
        self, tenant_id: str, application_id: str, limit: int = 10
    ) -> List[ResumeVersion]:
        """Get resume versions for application."""
        pass
    
    @abstractmethod
    def create(
        self, tenant_id: str, application_id: str, content: str, 
        version: int, created_by: str, ats_score: Optional[float] = None
    ) -> ResumeVersion:
        """Create new resume version."""
        pass


# Event Repository Port
class EventRepository(ABC):
    """Interface for event persistence."""
    
    @abstractmethod
    def get_by_application(
        self, tenant_id: str, application_id: str
    ) -> List[ApplicationEvent]:
        """Get events for application timeline."""
        pass
    
    @abstractmethod
    def create(
        self, tenant_id: str, application_id: str, event_type: str,
        description: str, created_by: Optional[str] = None
    ) -> ApplicationEvent:
        """Create new event."""
        pass


# Recruiter Repository Port
class RecruiterRepository(ABC):
    """Interface for recruiter persistence."""
    
    @abstractmethod
    def get_by_tenant(self, tenant_id: str) -> List[Recruiter]:
        """Get recruiters for tenant."""
        pass
    
    @abstractmethod
    def create(self, tenant_id: str, recruiter: dict) -> Recruiter:
        """Create new recruiter."""
        pass
    
    @abstractmethod
    def assign(
        self, tenant_id: str, application_id: str, recruiter_id: str
    ) -> ApplicationRecruiter:
        """Assign recruiter to application."""
        pass


# RAG Repository Port (for vector search)
class RAGRepository(ABC):
    """Interface for vector storage."""
    
    @abstractmethod
    def add_document(
        self, tenant_id: str, doc_type: str, doc_id: str, content: str,
        metadata: Optional[dict] = None
    ) -> str:
        """Add document to vector store."""
        pass
    
    @abstractmethod
    def search(
        self, tenant_id: str, query: str, doc_type: Optional[str] = None,
        limit: int = 5
    ) -> List[dict]:
        """Search documents."""
        pass
    
    @abstractmethod
    def get_embeddings(
        self, tenant_id: str, doc_type: str, doc_id: str
    ) -> Optional[List[float]]:
        """Get embeddings for document."""
        pass