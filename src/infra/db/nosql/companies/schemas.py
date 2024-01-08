from typing import Dict, List, Optional
from ..public_schemas import BaseEntity


class Job(BaseEntity):
    jid: Optional[int] = None
    cid: int
    title: Optional[str] = None
    region: Optional[str] = None
    salary: Optional[str] = None
    job_desc: Optional[Dict] = None
    # extra data, photos
    others: Optional[Dict] = None
    tags: Optional[List[str]] = []
    enable: Optional[bool] = True
    last_updated_at: Optional[int] = None
    # it's optional in gateway
    published_in: Optional[str] = None
    
    def ts(self):
        self.last_updated_at = self.updated_at if self.updated_at else self.created_at
        return self
    
    # get the old updated_at and overwrite old one with new data
    def parse_all_old_attr(self, all_old_attr: Dict):
        last_updated_at = all_old_attr['updated_at']
        new_data = self.dict()
        result_dict = {key: new_data[key] if new_data[key] is not None else all_old_attr[key] for key in all_old_attr.keys()}
        self = self.parse_obj(result_dict)
        self.last_updated_at = last_updated_at
        return self


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
    
