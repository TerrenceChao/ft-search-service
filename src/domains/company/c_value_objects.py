from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from ...configs.constants import *
from ...infra.db.nosql.companies import schemas as company


class BaseJobVO(BaseModel):
    jid: Optional[int] = None
    cid: Optional[int] = None
    name: Optional[str] = None  # school/company/organization name
    logo: Optional[str] = None
    title:  Optional[str] = None  # job title
    region: Optional[str] = None
    salary: Optional[str] = None
    job_desc: Optional[str] = None
    others: Optional[str] = None
    tags: Optional[List[str]] = []
    views: Optional[int] = None
    updated_at: Optional[int] = None
    created_at: Optional[int] = None
    published_in: Optional[str] = None  # must
    url_path: Optional[str] = None  # must


class JobListVO(BaseModel):
    items: Optional[List[BaseJobVO]] = []
    next: Optional[str] = None

    def __init__(self, sort_by: SortField, items: List[Dict] = []):
        super().__init__()
        if len(items) == 0:
            return
        
        last_one = items[-1]
        if sort_by.value in last_one:
            self.next = str(last_one[sort_by.value])
        self.items = [BaseJobVO(**item) for item in items]


class SearchJobListVO(BaseModel):
    size: int
    sort_by: SortField = SortField.UPDATED_AT
    sort_dirction: SortDirection = SortDirection.DESC
    search_after: Optional[int] = None


class SearchJobDetailVO(company.Job, company.CompanyProfile):
    url_path: Optional[str] = None
    views: int = 0

    def model(self):
        return {
            "jid": self.jid,
            "cid": self.cid,
            "name": self.name,  # school/company/organization name
            "logo": self.logo,
            "title": self.title,  # job title
            "region": self.region,
            "salary": self.salary,
            "job_desc": self.job_desc,
            "others": self.others,
            "tags": self.tags,
            "views": self.views,
            "updated_at": self.updated_at,
            "created_at": self.created_at,
            "published_in": self.published_in,  # must
            "url_path": self.url_path,  # must
        }

    @staticmethod
    def include_fields():
        return [
            "jid",
            "cid",
            "name",  # school/company/organization name
            "logo",
            "title",  # job title
            "region",
            "salary",
            "job_desc",
            "others",
            "tags",
            "views",
            "updated_at",
            "created_at",
            "published_in",  # must
            "url_path",  # must
        ]
