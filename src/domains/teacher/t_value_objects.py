from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from ...configs.constants import *
from ...infra.db.nosql.teachers import schemas as teacher


class SearchResumeDTO(BaseModel):
    rid: Optional[int] = None
    tid: Optional[int] = None
    avator: Optional[str] = None
    fullname: Optional[str] = None
    intro: Optional[str] = None
    tags: Optional[List[str]] = []
    views: Optional[int] = None
    updated_at: Optional[int] = None
    created_at: Optional[int] = None
    published_in: Optional[str] = None # must
    url_path: Optional[str] = None # must


class SearchResumeListVO(BaseModel):
    items: Optional[List[SearchResumeDTO]] = []
    next: Optional[str] = None

    def __init__(self, size: int, sort_by: SortField, items: List[Dict] = []):
        super().__init__()
        item_len = len(items)
        if item_len == 0:
            return
        
        if item_len > size:
            last_one = items[-1]
            if sort_by.value in last_one:
                self.next = str(last_one[sort_by.value])
        self.items = [SearchResumeDTO(**item) for item in items]


class SearchResumeListQueryDTO(BaseModel):
    size: int
    sort_by: SortField = SortField.UPDATED_AT
    sort_dirction: SortDirection = SortDirection.DESC
    search_after: Optional[str] = None


class SearchResumeDetailDTO(teacher.Resume):
    fullname: Optional[str] = None
    avator: Optional[str] = None
    url_path: Optional[str] = None
    views: int = 0

    # FIXME: it's not working when create & update resume
    def model(self):
        dictionary = self.dict()
        keys = set(SearchResumeDetailDTO.include_fields())
        dictionary = {key: value for key, value in dictionary.items() if key in keys}
        return dictionary

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
            "published_in", # must
            "url_path", # must
        ]
