from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from ...configs.constants import *
from ...infra.db.nosql.teachers import schemas as teacher


class BaseResumeVO(BaseModel):
    rid: Optional[int] = None
    tid: Optional[int] = None
    avator: Optional[str] = None
    fullname: Optional[str] = None
    intro: Optional[str] = None
    tags: Optional[List[str]] = []
    views: Optional[int] = None
    updated_at: Optional[int] = None
    created_at: Optional[int] = None
    published_in: Optional[str] = None  # must
    url_path: Optional[str] = None  # must


class ResumeListVO(BaseModel):
    items: Optional[List[BaseResumeVO]] = []
    next: Optional[str] = None

    def __init__(self, sort_by: SortField, items: List[Dict] = []):
        super().__init__()
        if len(items) == 0:
            return
        
        last_one = items[-1]
        if sort_by.value in last_one:
            self.next = str(last_one[sort_by.value])
        self.items = [BaseResumeVO(**item) for item in items]


class SearchResumeListVO(BaseModel):
    size: int
    sort_by: SortField = SortField.UPDATED_AT
    sort_dirction: SortDirection = SortDirection.DESC
    search_after: Optional[int] = None


class SearchResumeDetailVO(teacher.Resume):
    fullname: Optional[str] = None
    avator: Optional[str] = None
    url_path: Optional[str] = None
    views: int = 0

    def model(self):
        return {
            "rid": self.rid,
            "tid": self.tid,
            "avator": self.avator,
            "fullname": self.fullname,
            "intro": self.intro,
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
            "rid",
            "tid",
            "avator",
            "fullname",
            "intro",
            "tags",
            "views",
            "updated_at",
            "created_at",
            "published_in",  # must
            "url_path",  # must
        ]