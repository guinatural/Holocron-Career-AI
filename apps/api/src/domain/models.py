"""Domain models for Holocron Career AI."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class Status(str, Enum):
    """Application status enum."""
    DRAFT = "draft"
    ACTIVE = "active"
    IN_REVIEW = "in_review"
    INTERVIEW = "interview"
    OFFER = "offer"
    DECLINED = "declined"
    HIRED = "hired"
    ARCHIVED = "archived"


class ExperienceLevel(str, Enum):
    """Experience level enum."""
    JUNIOR = "junior"
    PLENO = "pleno"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    DIRECTOR = "director"


# Jobs
class Job(BaseModel):
    """Job posting model."""
    id: str
    tenant_id: str
    title: str
    company_id: str
    description: str
    requirements: List[str]
    benefits: List[str]
    location: str
    remote: bool
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    currency: str = "BRL"
    level: ExperienceLevel
    stack: List[str]
    status: str = "active"
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime] = None


class JobCreate(BaseModel):
    """Create job request."""
    title: str
    company_id: str
    description: str
    requirements: List[str]
    benefits: List[str]
    location: str
    remote: bool
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    level: ExperienceLevel
    stack: List[str]


class JobList(BaseModel):
    """Paginated job list."""
    items: List[Job]
    total: int
    page: int
    pages: int


# Companies
class Company(BaseModel):
    """Company model."""
    id: str
    tenant_id: str
    name: str
    description: str
    website: str
    logo_url: Optional[str] = None
    size: str
    industry: str
    created_at: datetime
    updated_at: datetime


class CompanyCreate(BaseModel):
    """Create company request."""
    name: str
    description: str
    website: str
    size: str
    industry: str


# Applications
class Application(BaseModel):
    """Job application model."""
    id: str
    tenant_id: str
    job_id: str
    candidate_name: str
    candidate_email: EmailStr
    status: Status
    score: Optional[float] = None  # AI matching score
    notes: Optional[str] = None
    resume_url: Optional[str] = None
    applied_at: datetime
    updated_at: datetime
    interview_date: Optional[datetime] = None
    offer_letter_url: Optional[str] = None


class ApplicationCreate(BaseModel):
    """Create application request."""
    job_id: str
    candidate_name: str
    candidate_email: EmailStr
    resume_text: Optional[str] = None


class ApplicationUpdate(BaseModel):
    """Update application request."""
    status: Optional[Status] = None
    notes: Optional[str] = None
    interview_date: Optional[datetime] = None
    offer_letter_url: Optional[str] = None


# Resume versions
class ResumeVersion(BaseModel):
    """Resume version model."""
    id: str
    tenant_id: str
    application_id: str
    content: str
    ats_score: Optional[float] = None
    version: int
    created_at: datetime
    created_by: str  # Agent ID


# Events (audit trail)
class ApplicationEvent(BaseModel):
    """Application event for timeline."""
    id: str
    tenant_id: str
    application_id: str
    event_type: str  # status_change, interview, offer, etc.
    description: str
    created_at: datetime
    created_by: Optional[str] = None


# Recruiters
class Recruiter(BaseModel):
    """Recruiter model."""
    id: str
    tenant_id: str
    name: str
    email: EmailStr
    team: str
    created_at: datetime
    updated_at: datetime


class ApplicationRecruiter(BaseModel):
    """Recruiter assignment for application."""
    id: str
    tenant_id: str
    application_id: str
    recruiter_id: str
    assigned_at: datetime