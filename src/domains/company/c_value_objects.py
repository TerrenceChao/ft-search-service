from typing import Optional, List, Set, Dict, Any
from pydantic import BaseModel
from ...configs.conf import *
from ...configs.constants import *
from ...infra.db.nosql.companies import schemas as company
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class SearchJobDTO(BaseModel):
    jid: Optional[int] = None  # index
    cid: Optional[int] = None  # index
    name: Optional[str] = None  # school/company/organization name
    logo: Optional[str] = None
    title:  Optional[str] = None  # job title
    location: Optional[str] = None
    salary: Optional[str] = None
    job_desc: Optional[Dict] = None
    others: Optional[Dict] = None
    tags: Optional[List[str]] = []
    views: Optional[int] = None
    updated_at: Optional[int] = None
    created_at: Optional[int] = None
    region: Optional[str] = None  # index
    enable: Optional[bool] = None


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
    views: int = 0

    # FIXME: it's not working when create & update job
    def model(self):
        dictionary = self.dict()
        keys = set(SearchJobDetailDTO.include_fields())
        dictionary = {key: value for key,
                      value in dictionary.items() if key in keys}
        return dictionary

    @staticmethod
    def include_fields():
        return [
            "jid",  # index
            "cid",  # index
            "name",  # school/company/organization name
            "logo",
            "title",  # job title
            "location",
            "salary",
            "job_desc",
            "others",
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
        profile_job_dict = self.dict()
        for field in JOB_EXCLUDED_FIELDS:
            profile_job_dict.pop(field, None)

        profile_job_dict.update(self.gen_extra_tags(profile_job_dict))
        log.warn('[create] profile_job_dict: %s', profile_job_dict)
        return profile_job_dict

    '''
    update the non-empty fields of a doc schema
    '''

    def dict_for_update(self):
        profile_job_dict = self.dict()
        for field in JOB_EXCLUDED_FIELDS:
            profile_job_dict.pop(field, None)

        profile_job_dict.update(self.gen_extra_tags(profile_job_dict))
        log.warn('[update] step 1: profile_job_dict: %s', profile_job_dict)

        new_profile_job_dict = {}
        for field, value in profile_job_dict.items():
            if self.valid(value):
                new_profile_job_dict[field] = value

        log.warn('[update] step 2: new_profile_job_dict: %s',
                 new_profile_job_dict)
        return new_profile_job_dict

    def valid(self, value: Any):
        value_type = type(value)
        if value_type == int:
            return value > 0

        if value_type == str:
            return value != ''

        if value_type == list or value_type == dict:
            return len(value) > 0

        return value is not None

    def gen_extra_tags(self, profile_job_dict: Dict) -> (Dict):
        extra_tags = set()
        for field in JOB_TRANSFORM_FIELDS:
            if field in profile_job_dict:
                field_value = profile_job_dict[field]
                if isinstance(field_value, dict):
                    extra_tags = self.find_deep_strings(field_value, 0, extra_tags)

        return {'extra_tags': list(extra_tags)}

    def find_deep_strings(self, data: Dict, current_depth: int = 0, found_strings: Set = None):
        if found_strings is None:
            found_strings = []

        if current_depth >= MAX_JOB_DICT_DEPTH:
            return found_strings

        for key, value in data.items():
            if isinstance(value, dict):
                self.find_deep_strings(value, current_depth + 1, found_strings)
            elif isinstance(value, str):
                found_strings.add(value)

        return found_strings
