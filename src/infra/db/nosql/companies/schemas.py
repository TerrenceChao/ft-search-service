from typing import Dict, List, Optional
from ..public_schemas import BaseEntity


class Job(BaseEntity):
    jid: Optional[int] = None
    cid: int
    title: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None
    job_desc: Optional[Dict] = None
    # extra data, photos
    others: Optional[Dict] = None
    tags: Optional[List[str]] = []
    enable: Optional[bool] = True
    last_updated_at: Optional[int] = None
    # it's optional in gateway
    region: Optional[str] = None


class CompanyProfile(BaseEntity):
    cid: int
    name: Optional[str] = None
    intro: Optional[str] = None
    logo: Optional[str] = None
    # size, founded, revenue, ... etc (json)
    overview: Optional[Dict] = None
    # who, what, where, ... etc (json array)
    sections: Optional[List[Dict]] = []
    photos: Optional[List[Dict]] = []
