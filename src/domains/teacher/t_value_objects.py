from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from ...configs.conf import *
from ...configs.constants import *
from ...infra.db.nosql.teachers import schemas as teacher
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class SearchResumeDTO(BaseModel):
    rid: Optional[int] = None  # index
    tid: Optional[int] = None  # index
    avator: Optional[str] = None
    fullname: Optional[str] = None
    intro: Optional[str] = None
    tags: Optional[List[str]] = []
    views: Optional[int] = None
    updated_at: Optional[int] = None
    created_at: Optional[int] = None
    region: Optional[str] = None  # index
    enable: Optional[bool] = None


class SearchResumeListVO(BaseModel):
    items: Optional[List[SearchResumeDTO]] = []
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
        self.items = [SearchResumeDTO(**item) for item in items]


class SearchResumeListQueryDTO(BaseModel):
    size: int
    sort_by: SortField = SortField.UPDATED_AT
    sort_dirction: SortDirection = SortDirection.DESC
    search_after: Optional[str] = None


class SearchResumeDetailDTO(teacher.Resume):
    fullname: Optional[str] = None
    avator: Optional[str] = None
    views: int = 0

    # FIXME: it's not working when create & update resume
    def model(self):
        dictionary = self.dict()
        keys = set(SearchResumeDetailDTO.include_fields())
        dictionary = {key: value for key,
                      value in dictionary.items() if key in keys}
        return dictionary

    @staticmethod
    def include_fields():
        return [
            "rid",  # index
            "tid",  # index
            "avator",
            "fullname",
            "intro",
            "tags",
            "views",
            "updated_at",
            "created_at",
            "region",  # index
            "enable",
        ]

    '''
    create a doc schema
    '''

    def dict_for_create(self):
        profile_resume_dict = self.dict()
        # all fields are required for creating a doc schema,
        # besides 'sections', cuz the nested field 'sections' is not supported by elasticsearch
        sections = profile_resume_dict.pop('sections', [])
        log.warn('[create] sections: %s', sections)
        for field in RESUME_EXCLUDED_FIELDS:
            profile_resume_dict.pop(field, None)

        profile_resume_dict.update(self.gen_extra_tags(sections))
        log.warn('[create] profile_resume_dict: %s', profile_resume_dict)
        return profile_resume_dict

    '''
    update the non-empty fields of a doc schema
    '''

    def dict_for_update(self):
        profile_resume_dict = self.dict()
        # the nested field 'sections' is not supported by elasticsearch
        sections = profile_resume_dict.pop('sections', [])
        log.warn('[update] sections: %s', sections)
        for field in RESUME_EXCLUDED_FIELDS:
            profile_resume_dict.pop(field, None)

        profile_resume_dict.update(self.gen_extra_tags(sections))
        log.warn('[update] step 1: profile_resume_dict: %s',
                 profile_resume_dict)
        new_profile_resume_dict = {}
        for field, value in profile_resume_dict.items():
            if self.valid(value):
                new_profile_resume_dict[field] = value
        log.warn('[update] step 2: new_profile_resume_dict: %s',
                 new_profile_resume_dict)
        return new_profile_resume_dict

    def valid(self, value: Any):
        value_type = type(value)
        if value_type == int:
            return value > 0

        if value_type == str:
            return value != ''

        if value_type == list or value_type == dict:
            return len(value) > 0

        return value is not None

    def gen_extra_tags(self, resume_sections: List[Dict]) -> (Dict):
        extra_tags = \
            {f'{field}_tags': set() for field in RESUME_TRANSFORM_FIELDS}

        for section in resume_sections:
            for field in RESUME_TRANSFORM_FIELDS:
                if section.get(field) is not None:
                    extra_tags[f'{field}_tags'].add(section[field])
                extra_tags[f'{field}_tags'] = list(extra_tags[f'{field}_tags'])

        return extra_tags
