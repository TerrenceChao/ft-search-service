from typing import Dict, List, Optional
from ..public_schemas import BaseEntity


class ResumeSection(BaseEntity):
    sid: Optional[int] = None  # Sort Key
    tid: int  # Partition Key
    rid: int
    order: Optional[int] = None
    category: Optional[str] = None
    logo: Optional[str] = None
    name: Optional[str] = None  # School, Company, Certificate Name, Skill Name
    title: Optional[str] = None  # Degree, Job Title
    location: Optional[str] = None  # School Location, Company Location
    start_year: Optional[int] = None
    start_month: Optional[int] = None
    end_year: Optional[int] = None
    end_month: Optional[int] = None
    # Study Subject, Company Industry, Description, image/file urls, others
    context: Optional[Dict] = None


class Resume(BaseEntity):
    rid: Optional[int] = None
    tid: int
    intro: Optional[str] = None
    sections: Optional[List[ResumeSection]] = []
    tags: Optional[List[str]] = []
    enable: Optional[bool] = True
    last_updated_at: Optional[int] = None
    # it's optional in gateway
    region: Optional[str] = None
