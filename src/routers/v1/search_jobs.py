import time
import json
from typing import List, Dict, Any
from fastapi import APIRouter, \
    Query, Body
from ...configs.elasticsearch import client as es_client
from ...configs.conf import *
from ...configs.constants import *
from ...configs.exceptions import *
from ...domains.company import c_value_objects as c
from ...domains.company.job_search_service import JobSearchService
from ..res.response import res_success, res_err
import logging as log


log.basicConfig(filemode='w', level=log.INFO)


_job_search_service = JobSearchService(es_client)


router = APIRouter(
    prefix="/jobs",
    tags=["Search Jobs"],
    responses={404: {"description": "Not found"}},
)


@router.post("", status_code=201)
def create_job(doc: c.SearchJobDetailDTO = Body(...)):
    data = _job_search_service.create(doc)
    return res_success(data=data)


@router.get("")
def search_jobs(
    size: int = Query(10, gt=0, le=100),
    sort_by: SortField = Query(SortField.UPDATED_AT),
    sort_dirction: SortDirection = Query(SortDirection.DESC),
    search_after: str = Query(None),
    patterns: List[str] = Query([]),
):
    query = c.SearchJobListQueryDTO(
        size=size,
        sort_by=sort_by,
        sort_dirction=sort_dirction,
        search_after=search_after,
        patterns=patterns,
    )
    result = _job_search_service.search(query)
    return res_success(data=result)


@router.put("")
def update_job(doc: c.SearchJobDetailDTO = Body(...)):
    data = _job_search_service.update(doc)
    return res_success(data=data)


@router.put("/enable")
def enable_job(doc: c.SearchJobDetailDTO = Body(...)):
    data = _job_search_service.enable(doc)
    return res_success(data=data)


@router.put("/remove")
def remove_job(doc: c.SearchJobDetailDTO = Body(...)):
    data = _job_search_service.remove(doc)
    return res_success(data=data)


@router.delete("/delete-forever")
def delete_forever(confirm: str = Query(...)):
    if confirm != "im-sure":
        raise ClientException(msg="wrong phrase")

    _job_search_service.delete_job_index()
    return res_success()
