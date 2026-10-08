"""FastAPI routes for the API."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..domain.models import (
    Job, JobCreate, JobList,
    Company, CompanyCreate,
    Application, ApplicationCreate, ApplicationUpdate,
    ResumeVersion
)
from ..application.use_cases import (
    JobService, CompanyService, ApplicationService
)
from ..infrastructure.repositories import (
    SQLJobRepository, SQLCompanyRepository, SQLApplicationRepository
)
from ..infrastructure.database import get_db

router = APIRouter(prefix="/api/v1", tags=["api"])


# Dependency injection for services
def get_job_service(db: Session = Depends(get_db)) -> JobService:
    return JobService(job_repo=SQLJobRepository(db))


def get_company_service(db: Session = Depends(get_db)) -> CompanyService:
    return CompanyService(company_repo=SQLCompanyRepository(db))


def get_application_service(db: Session = Depends(get_db)) -> ApplicationService:
    return ApplicationService(
        app_repo=SQLApplicationRepository(db),
        resume_repo=None,
        event_repo=None,
        rag_service=None
    )


# Jobs endpoints
@router.get("/jobs", response_model=JobList)
def list_jobs(
    skip: int = 0,
    limit: int = 10,
    service: JobService = Depends(get_job_service)
):
    """List jobs for tenant."""
    jobs, total = service.list_jobs(tenant_id="default_tenant", skip=skip, limit=limit)
    return {"items": jobs, "total": total, "page": skip // limit + 1, "pages": (total + limit - 1) // limit}


@router.get("/jobs/{job_id}", response_model=Job)
def get_job(
    job_id: str,
    service: JobService = Depends(get_job_service)
):
    """Get job by ID."""
    job = service.job_repo.get_by_id(tenant_id="default_tenant", job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/jobs", response_model=Job, status_code=status.HTTP_201_CREATED)
def create_job(
    job: JobCreate,
    service: JobService = Depends(get_job_service)
):
    """Create new job."""
    return service.create_job(tenant_id="default_tenant", job=job)


@router.put("/jobs/{job_id}", response_model=Job)
def update_job(
    job_id: str,
    job: Job,
    service: JobService = Depends(get_job_service)
):
    """Update job."""
    updated = service.update_job(tenant_id="default_tenant", job=job)
    if not updated:
        raise HTTPException(status_code=404, detail="Job not found")
    return updated


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: str,
    service: JobService = Depends(get_job_service)
):
    """Delete job."""
    if not service.delete_job(tenant_id="default_tenant", job_id=job_id):
        raise HTTPException(status_code=404, detail="Job not found")
    return None


# Companies endpoints
@router.get("/companies", response_model=List[Company])
def list_companies(
    service: CompanyService = Depends(get_company_service)
):
    """List companies for tenant."""
    return service.list_companies(tenant_id="default_tenant")


@router.post("/companies", response_model=Company, status_code=status.HTTP_201_CREATED)
def create_company(
    company: CompanyCreate,
    service: CompanyService = Depends(get_company_service)
):
    """Create new company."""
    return service.create_company(tenant_id="default_tenant", company=company)


# Applications endpoints
@router.get("/applications", response_model=List[Application])
def list_applications(
    skip: int = 0,
    limit: int = 10,
    service: ApplicationService = Depends(get_application_service)
):
    """List applications for tenant."""
    apps, _ = service.list_applications(tenant_id="default_tenant", skip=skip, limit=limit)
    return apps


@router.post("/applications", response_model=Application, status_code=status.HTTP_201_CREATED)
def create_application(
    application: ApplicationCreate,
    service: ApplicationService = Depends(get_application_service)
):
    """Create new application."""
    return service.create_application(tenant_id="default_tenant", application=application)


@router.put("/applications/{application_id}", response_model=Application)
def update_application(
    application_id: str,
    updates: ApplicationUpdate,
    service: ApplicationService = Depends(get_application_service)
):
    """Update application."""
    return service.update_application(
        tenant_id="default_tenant",
        application_id=application_id,
        updates=updates
    )


# Resume endpoints
@router.post("/resume/{application_id}", response_model=ResumeVersion)
def generate_resume(
    application_id: str,
    service: ApplicationService = Depends(get_application_service)
):
    """Generate optimized resume for application."""
    return service.generate_resume(
        tenant_id="default_tenant",
        application_id=application_id,
        original_text=""
    )


# Matching endpoints
@router.get("/match/{application_id}")
def match_application(
    application_id: str,
    service: ApplicationService = Depends(get_application_service)
):
    """Run AI matching on application."""
    score, breakdown = service.match_application(
        tenant_id="default_tenant",
        application_id=application_id
    )
    return {"score": score, "breakdown": breakdown}
from ..domain.models import UserProfile, TargetJob, AgentInteraction
from ..infrastructure.models import UserProfile as DBUserProfile, TargetJob as DBTargetJob, AgentInteraction as DBAgentInteraction
import uuid
from datetime import datetime

# Career AI User Routes
@router.post("/profiles", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile: UserProfile,
    db: Session = Depends(get_db)
):
    """Create a new user profile."""
    db_profile = DBUserProfile(
        id=profile.id or str(uuid.uuid4()),
        tenant_id=profile.tenant_id,
        name=profile.name,
        email=profile.email,
        bio=profile.bio,
        years_of_experience=profile.years_of_experience,
        skills=profile.skills,
        work_history=profile.work_history
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.post("/target-jobs", response_model=TargetJob, status_code=status.HTTP_201_CREATED)
def create_target_job(
    job: TargetJob,
    db: Session = Depends(get_db)
):
    """Create a new target job for the user."""
    db_job = DBTargetJob(
        id=job.id or str(uuid.uuid4()),
        tenant_id=job.tenant_id,
        user_profile_id=job.user_profile_id,
        title=job.title,
        level=job.level,
        salary_range=job.salary_range,
        desired_skills=job.desired_skills
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/interactions", response_model=List[AgentInteraction])
def list_interactions(
    tenant_id: str = "default_tenant",
    db: Session = Depends(get_db)
):
    """List all AI agent interactions."""
    return db.query(DBAgentInteraction).filter(DBAgentInteraction.tenant_id == tenant_id).all()
