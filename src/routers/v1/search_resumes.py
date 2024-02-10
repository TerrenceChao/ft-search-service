import time
import json
from typing import List, Dict, Any
from fastapi import APIRouter, \
    Query, Body
from ...configs.elasticsearch import client as es_client
from ...configs.conf import *
from ...configs.constants import *
from ...configs.exceptions import *
from ...domains.teacher import t_value_objects as t
from ...domains.teacher.resume_search_service import ResumeSearchService
from ..res.response import res_success, res_err
import logging as log


log.basicConfig(filemode='w', level=log.INFO)


_resume_search_service = ResumeSearchService(es_client)


router = APIRouter(
    prefix="/resumes",
    tags=["Search Resumes"],
    responses={404: {"description": "Not found"}},
)


@router.post("", status_code=201)
def create_resume(doc: t.SearchResumeDetailDTO = Body(...)):
    data = _resume_search_service.create(doc)
    return res_success(data=data)


@router.get("")
def search_resumes(
    size: int = Query(10, gt=0, le=100),
    sort_by: SortField = Query(SortField.UPDATED_AT),
    sort_dirction: SortDirection = Query(SortDirection.DESC),
    search_after: str = Query(None),
    patterns: List[str] = Query([]),
    tags: List[str] = Query([]),
):
    query = t.SearchResumeListQueryDTO(
        size=size,
        sort_by=sort_by,
        sort_dirction=sort_dirction,
        search_after=search_after,
        patterns=patterns,
        tags=tags,
    )
    result = _resume_search_service.search(query)
    return res_success(data=result)


@router.put("")
def update_resume(doc: t.SearchResumeDetailDTO = Body(...)):
    data = _resume_search_service.update(doc)
    return res_success(data=data)


@router.put("/enable")
def enable_resume(doc: t.SearchResumeDetailDTO = Body(...)):
    data = _resume_search_service.enable(doc)
    return res_success(data=data)


@router.put("/remove")
def remove_resume(doc: t.SearchResumeDetailDTO = Body(...)):
    data = _resume_search_service.remove(doc)
    return res_success(data=data)


@router.delete("/delete-forever")
def delete_forever(confirm: str = Query(...)):
    if confirm != "im-sure":
        raise ClientException(msg="wrong phrase")

    _resume_search_service.delete_resume_index()
    return res_success()
