"""SQLAlchemy repository implementations."""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime

from ..domain.models import (
    Job, JobCreate, Company, CompanyCreate,
    Application, ApplicationCreate, ApplicationUpdate,
    ResumeVersion, ApplicationEvent
)
from ..domain.ports import (
    JobRepository, CompanyRepository, ApplicationRepository,
    ResumeRepository, EventRepository, RecruiterRepository
)
from .models import (
    Job as JobModel, Company as CompanyModel,
    Application as ApplicationModel, ResumeVersion as ResumeVersionModel,
    ApplicationEvent as EventModel, Recruiter as RecruiterModel,
    ApplicationRecruiter as ApplicationRecruiterModel
)


class SQLJobRepository(JobRepository):
    """SQLAlchemy implementation of JobRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, tenant_id: str, job_id: str) -> Optional[Job]:
        model = self.db.query(JobModel).filter(
            JobModel.tenant_id == tenant_id,
            JobModel.id == job_id
        ).first()
        return self._to_domain(model) if model else None
    
    def get_by_tenant(self, tenant_id: str, skip: int = 0, limit: int = 10) -> Tuple[List[Job], int]:
        query = self.db.query(JobModel).filter(JobModel.tenant_id == tenant_id)
        total = query.count()
        models = query.order_by(desc(JobModel.created_at)).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models], total
    
    def get_by_company(self, tenant_id: str, company_id: str) -> List[Job]:
        models = self.db.query(JobModel).filter(
            JobModel.tenant_id == tenant_id,
            JobModel.company_id == company_id
        ).all()
        return [self._to_domain(m) for m in models]
    
    def search(self, tenant_id: str, query: str, skip: int = 0, limit: int = 10) -> Tuple[List[Job], int]:
        search_term = f"%{query}%"
        query = self.db.query(JobModel).filter(
            JobModel.tenant_id == tenant_id,
            (JobModel.title.ilike(search_term)) |
            (JobModel.description.ilike(search_term))
        )
        total = query.count()
        models = query.offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models], total
    
    def create(self, tenant_id: str, job: JobCreate) -> Job:
        model = JobModel(
            id=job.id,
            tenant_id=tenant_id,
            title=job.title,
            company_id=job.company_id,
            description=job.description,
            requirements=job.requirements,
            benefits=job.benefits,
            location=job.location,
            remote=job.remote,
            salary_min=job.salary_min,
            salary_max=job.salary_max,
            level=job.level,
            stack=job.stack,
            created_at=job.created_at,
            updated_at=job.updated_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
    
    def update(self, tenant_id: str, job: Job) -> Job:
        model = self.db.query(JobModel).filter(
            JobModel.tenant_id == tenant_id,
            JobModel.id == job.id
        ).first()
        if not model:
            raise ValueError("Job not found")
        
        model.title = job.title
        model.description = job.description
        model.requirements = job.requirements
        model.benefits = job.benefits
        model.location = job.location
        model.remote = job.remote
        model.salary_min = job.salary_min
        model.salary_max = job.salary_max
        model.level = job.level
        model.stack = job.stack
        model.status = job.status
        model.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
    
    def delete(self, tenant_id: str, job_id: str) -> bool:
        model = self.db.query(JobModel).filter(
            JobModel.tenant_id == tenant_id,
            JobModel.id == job_id
        ).first()
        if not model:
            return False
        
        self.db.delete(model)
        self.db.commit()
        return True
    
    def _to_domain(self, model) -> Job:
        if not model:
            return None
        return Job(
            id=model.id,
            tenant_id=model.tenant_id,
            title=model.title,
            company_id=model.company_id,
            description=model.description,
            requirements=model.requirements,
            benefits=model.benefits,
            location=model.location,
            remote=model.remote,
            salary_min=model.salary_min,
            salary_max=model.salary_max,
            level=model.level,
            stack=model.stack,
            status=model.status,
            published_at=model.published_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )


class SQLCompanyRepository(CompanyRepository):
    """SQLAlchemy implementation of CompanyRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, tenant_id: str, company_id: str) -> Optional[Company]:
        model = self.db.query(CompanyModel).filter(
            CompanyModel.tenant_id == tenant_id,
            CompanyModel.id == company_id
        ).first()
        return self._to_domain(model) if model else None
    
    def get_by_tenant(self, tenant_id: str) -> List[Company]:
        models = self.db.query(CompanyModel).filter(
            CompanyModel.tenant_id == tenant_id
        ).all()
        return [self._to_domain(m) for m in models]
    
    def create(self, tenant_id: str, company: CompanyCreate) -> Company:
        model = CompanyModel(
            id=f"company_{datetime.utcnow().timestamp()}",
            tenant_id=tenant_id,
            name=company.name,
            description=company.description,
            website=company.website,
            size=company.size,
            industry=company.industry,
            created_at=datetime.utcnow()
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
    
    def update(self, tenant_id: str, company: Company) -> Company:
        model = self.db.query(CompanyModel).filter(
            CompanyModel.tenant_id == tenant_id,
            CompanyModel.id == company.id
        ).first()
        if not model:
            raise ValueError("Company not found")
        
        model.name = company.name
        model.description = company.description
        model.website = company.website
        model.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
    
    def _to_domain(self, model) -> Company:
        if not model:
            return None
        return Company(
            id=model.id,
            tenant_id=model.tenant_id,
            name=model.name,
            description=model.description,
            website=model.website,
            logo_url=model.logo_url,
            size=model.size,
            industry=model.industry,
            created_at=model.created_at,
            updated_at=model.updated_at
        )


class SQLApplicationRepository(ApplicationRepository):
    """SQLAlchemy implementation of ApplicationRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, tenant_id: str, application_id: str) -> Optional[Application]:
        model = self.db.query(ApplicationModel).filter(
            ApplicationModel.tenant_id == tenant_id,
            ApplicationModel.id == application_id
        ).first()
        return self._to_domain(model) if model else None
    
    def get_by_tenant(self, tenant_id: str, skip: int = 0, limit: int = 10) -> Tuple[List[Application], int]:
        query = self.db.query(ApplicationModel).filter(ApplicationModel.tenant_id == tenant_id)
        total = query.count()
        models = query.order_by(desc(ApplicationModel.applied_at)).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models], total
    
    def get_by_job(self, tenant_id: str, job_id: str) -> List[Application]:
        models = self.db.query(ApplicationModel).filter(
            ApplicationModel.tenant_id == tenant_id,
            ApplicationModel.job_id == job_id
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_status(self, tenant_id: str, status: str, skip: int = 0, limit: int = 10) -> Tuple[List[Application], int]:
        query = self.db.query(ApplicationModel).filter(
            ApplicationModel.tenant_id == tenant_id,
            ApplicationModel.status == status
        )
        total = query.count()
        models = query.offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models], total
    
    def create(self, tenant_id: str, application: ApplicationCreate) -> Application:
        model = ApplicationModel(
            id=application.id,
            tenant_id=tenant_id,
            job_id=application.job_id,
            candidate_name=application.candidate_name,
            candidate_email=application.candidate_email,
            status=application.status,
            score=application.score,
            applied_at=application.applied_at,
            updated_at=application.updated_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
    
    def update(self, tenant_id: str, application: Application) -> Application:
        model = self.db.query(ApplicationModel).filter(
            ApplicationModel.tenant_id == tenant_id,
            ApplicationModel.id == application.id
        ).first()
        if not model:
            raise ValueError("Application not found")
        
        model.status = application.status
        model.score = application.score
        model.notes = application.notes
        model.resume_url = application.resume_url
        model.interview_date = application.interview_date
        model.offer_letter_url = application.offer_letter_url
        model.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
    
    def delete(self, tenant_id: str, application_id: str) -> bool:
        model = self.db.query(ApplicationModel).filter(
            ApplicationModel.tenant_id == tenant_id,
            ApplicationModel.id == application_id
        ).first()
        if not model:
            return False
        
        self.db.delete(model)
        self.db.commit()
        return True
    
    def _to_domain(self, model) -> Application:
        if not model:
            return None
        return Application(
            id=model.id,
            tenant_id=model.tenant_id,
            job_id=model.job_id,
            candidate_name=model.candidate_name,
            candidate_email=model.candidate_email,
            status=model.status,
            score=model.score,
            notes=model.notes,
            resume_url=model.resume_url,
            applied_at=model.applied_at,
            updated_at=model.updated_at,
            interview_date=model.interview_date,
            offer_letter_url=model.offer_letter_url
        )


class SQLResumeRepository(ResumeRepository):
    """SQLAlchemy implementation of ResumeRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_application(self, tenant_id: str, application_id: str, limit: int = 10) -> List[ResumeVersion]:
        models = self.db.query(ResumeVersionModel).filter(
            ResumeVersionModel.tenant_id == tenant_id,
            ResumeVersionModel.application_id == application_id
        ).order_by(desc(ResumeVersionModel.version)).limit(limit).all()
        return [self._to_domain(m) for m in models]
    
    def create(self, tenant_id: str, application_id: str, content: str, version: int, created_by: str, ats_score: float = None) -> ResumeVersion:
        model = ResumeVersionModel(
            id=f"resume_{datetime.utcnow().timestamp()}",
            tenant_id=tenant_id,
            application_id=application_id,
            content=content,
            version=version,
            created_at=datetime.utcnow(),
            created_by=created_by,
            ats_score=ats_score
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
    
    def _to_domain(self, model) -> ResumeVersion:
        if not model:
            return None
        return ResumeVersion(
            id=model.id,
            tenant_id=model.tenant_id,
            application_id=model.application_id,
            content=model.content,
            ats_score=model.ats_score,
            version=model.version,
            created_at=model.created_at,
            created_by=model.created_by
        )


class SQLEventRepository(EventRepository):
    """SQLAlchemy implementation of EventRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_application(self, tenant_id: str, application_id: str) -> List[ApplicationEvent]:
        models = self.db.query(EventModel).filter(
            EventModel.tenant_id == tenant_id,
            EventModel.application_id == application_id
        ).order_by(EventModel.created_at).all()
        return [self._to_domain(m) for m in models]
    
    def create(self, tenant_id: str, application_id: str, event_type: str, description: str, created_by: str = None) -> ApplicationEvent:
        model = EventModel(
            id=f"evt_{datetime.utcnow().timestamp()}",
            tenant_id=tenant_id,
            application_id=application_id,
            event_type=event_type,
            description=description,
            created_at=datetime.utcnow(),
            created_by=created_by
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
    
    def _to_domain(self, model) -> ApplicationEvent:
        if not model:
            return None
        return ApplicationEvent(
            id=model.id,
            tenant_id=model.tenant_id,
            application_id=model.application_id,
            event_type=model.event_type,
            description=model.description,
            created_at=model.created_at,
            created_by=model.created_by
        )


class SQLRecruiterRepository(RecruiterRepository):
    """SQLAlchemy implementation of RecruiterRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_tenant(self, tenant_id: str) -> List[Recruiter]:
        models = self.db.query(RecruiterModel).filter(
            RecruiterModel.tenant_id == tenant_id
        ).all()
        return [self._to_domain(m) for m in models]
    
    def create(self, tenant_id: str, recruiter_data: dict) -> Recruiter:
        model = RecruiterModel(
            id=f"recruiter_{datetime.utcnow().timestamp()}",
            tenant_id=tenant_id,
            name=recruiter_data["name"],
            email=recruiter_data["email"],
            team=recruiter_data.get("team"),
            created_at=datetime.utcnow()
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
    
    def assign(self, tenant_id: str, application_id: str, recruiter_id: str) -> dict:
        model = ApplicationRecruiterModel(
            id=f"app_rec_{datetime.utcnow().timestamp()}",
            tenant_id=tenant_id,
            application_id=application_id,
            recruiter_id=recruiter_id,
            assigned_at=datetime.utcnow()
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return {
            "id": model.id,
            "tenant_id": model.tenant_id,
            "application_id": model.application_id,
            "recruiter_id": model.recruiter_id,
            "assigned_at": model.assigned_at
        }
    
    def _to_domain(self, model) -> dict:
        if not model:
            return None
        return {
            "id": model.id,
            "tenant_id": model.tenant_id,
            "name": model.name,
            "email": model.email,
            "team": model.team,
            "created_at": model.created_at,
            "updated_at": model.updated_at
        }