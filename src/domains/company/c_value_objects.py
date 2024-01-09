from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from ...configs.constants import *
from ...infra.db.nosql.companies import schemas as company


class SearchJobDTO(BaseModel):
    jid: Optional[int] = None
    cid: Optional[int] = None
    name: Optional[str] = None # school/company/organization name
    logo: Optional[str] = None
    title:  Optional[str] = None # job title
    location: Optional[str] = None
    salary: Optional[str] = None
    job_desc: Optional[Dict] = None
    others: Optional[Dict] = None
    tags: Optional[List[str]] = []
    views: Optional[int] = None
    updated_at: Optional[int] = None
    created_at: Optional[int] = None
    region: Optional[str] = None # must
    url_path: Optional[str] = None # must


class SearchJobListVO(BaseModel):
    items: Optional[List[SearchJobDTO]] = []
    next: Optional[str] = None

    def __init__(self, size: int, sort_by: SortField, items: List[Dict] = []):
        super().__init__()
        item_len = len(items)
        if item_len == 0:
            return
        
        if item_len >= size:
            last_one = items[-1]
            if sort_by.value in last_one:
                self.next = str(last_one[sort_by.value])
        self.items = [SearchJobDTO(**item) for item in items]


class SearchJobListQueryDTO(BaseModel):
    size: int
    sort_by: SortField = SortField.UPDATED_AT
    sort_dirction: SortDirection = SortDirection.DESC
    search_after: Optional[str] = None


class SearchJobDetailDTO(company.Job, company.CompanyProfile):
    url_path: Optional[str] = None
    views: int = 0

    # FIXME: it's not working when create & update job
    def model(self):
        dictionary = self.dict()
        keys = set(SearchJobDetailDTO.include_fields())
        dictionary = {key: value for key, value in dictionary.items() if key in keys}
        return dictionary

    @staticmethod
    def include_fields():
        return [
            "jid",
            "cid",
            "name", # school/company/organization name
            "logo",
            "title", # job title
            "location",
            "salary",
            "job_desc",
            "others",
            "tags",
            "views",
            "updated_at",
            "created_at",
            "region", # must
            "url_path", # must
        ]
