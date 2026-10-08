"""SQLAlchemy ORM models for database tables."""
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, DateTime, Boolean, ForeignKey, Integer, Enum, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from ..domain.models import Status, ExperienceLevel

Base = declarative_base()


class Tenant(Base):
    """Tenant model for multi-tenancy."""
    __tablename__ = "tenants"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    jobs = relationship("Job", back_populates="tenant")
    companies = relationship("Company", back_populates="tenant")
    applications = relationship("Application", back_populates="tenant")
    recruiters = relationship("Recruiter", back_populates="tenant")


class Job(Base):
    """Job posting model."""
    __tablename__ = "jobs"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(JSON, nullable=False)
    benefits = Column(JSON, nullable=False)
    location = Column(String(255), nullable=False)
    remote = Column(Boolean, default=False)
    salary_min = Column(Float)
    salary_max = Column(Float)
    currency = Column(String(3), default="BRL")
    level = Column(Enum(ExperienceLevel), nullable=False)
    stack = Column(JSON, nullable=False)
    status = Column(String(50), default="active")
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_jobs_tenant_status", "tenant_id", "status"),
        Index("idx_jobs_tenant_level", "tenant_id", "level"),
        Index("idx_jobs_title", "title"),
    )
    
    # Relationships
    tenant = relationship("Tenant", back_populates="jobs")
    applications = relationship("Application", back_populates="job")


class Company(Base):
    """Company model."""
    __tablename__ = "companies"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    website = Column(String(255))
    logo_url = Column(String(500))
    size = Column(String(50))
    industry = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="companies")
    jobs = relationship("Job", back_populates="tenant")


class Application(Base):
    """Job application model."""
    __tablename__ = "applications"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    job_id = Column(String(36), ForeignKey("jobs.id"), nullable=False)
    candidate_name = Column(String(255), nullable=False)
    candidate_email = Column(String(255), nullable=False)
    status = Column(Enum(Status), default=Status.ACTIVE)
    score = Column(Float)
    notes = Column(Text)
    resume_url = Column(String(500))
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    interview_date = Column(DateTime)
    offer_letter_url = Column(String(500))
    
    # Indexes
    __table_args__ = (
        Index("idx_applications_tenant", "tenant_id"),
        Index("idx_applications_status", "status"),
        Index("idx_applications_job", "job_id"),
    )
    
    # Relationships
    tenant = relationship("Tenant", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    resume_versions = relationship("ResumeVersion", back_populates="application")
    events = relationship("ApplicationEvent", back_populates="application")
    recruiters = relationship("ApplicationRecruiter", back_populates="application")


class ResumeVersion(Base):
    """Resume version model."""
    __tablename__ = "resume_versions"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    application_id = Column(String(36), ForeignKey("applications.id"), nullable=False)
    content = Column(Text, nullable=False)
    ats_score = Column(Float)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(50), nullable=False)  # Agent ID
    
    # Relationships
    tenant = relationship("Tenant")
    application = relationship("Application", back_populates="resume_versions")


class ApplicationEvent(Base):
    """Application event for timeline."""
    __tablename__ = "application_events"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    application_id = Column(String(36), ForeignKey("applications.id"), nullable=False)
    event_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(36))
    
    # Relationships
    tenant = relationship("Tenant")
    application = relationship("Application", back_populates="events")


class Recruiter(Base):
    """Recruiter model."""
    __tablename__ = "recruiters"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    team = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="recruiters")


class ApplicationRecruiter(Base):
    """Recruiter assignment for application."""
    __tablename__ = "application_recruiters"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    application_id = Column(String(36), ForeignKey("applications.id"), nullable=False)
    recruiter_id = Column(String(36), ForeignKey("recruiters.id"), nullable=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant")
    application = relationship("Application", back_populates="recruiters")
    recruiter = relationship("Recruiter")
class UserProfile(Base):
    """User profile representing the candidate."""
    __tablename__ = "user_profiles"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    bio = Column(Text)
    years_of_experience = Column(Float)
    skills = Column(JSON) # List of skills
    work_history = Column(JSON) # List of past experiences
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tenant = relationship("Tenant")


class TargetJob(Base):
    """Target job the user is aiming for."""
    __tablename__ = "target_jobs"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    user_profile_id = Column(String(36), ForeignKey("user_profiles.id"), nullable=False)
    title = Column(String(255), nullable=False)
    level = Column(String(50), nullable=False) # e.g., Junior, Senior
    salary_range = Column(String(100))
    desired_skills = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tenant = relationship("Tenant")
    user_profile = relationship("UserProfile")


class AgentInteraction(Base):
    """History of interactions with AI Agents."""
    __tablename__ = "agent_interactions"
    
    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id"), nullable=False)
    agent_type = Column(String(100), nullable=False) # e.g., 'resume_tailor', 'mock_interview'
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    metadata_json = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    tenant = relationship("Tenant")
