from typing import Dict, List, Optional
from ..public_schemas import BaseEntity


class ResumeSection(BaseEntity):
    sid: Optional[int] = None
    tid: int
    rid: Optional[int] = None  # NOT ForeignKey
    order: int
    subject: str
    context: Dict


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
