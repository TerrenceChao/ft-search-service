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
from ...domains.company.company_search_service import CompanySearchService
from ..res.response import res_success, res_err
import logging as log


log.basicConfig(filemode='w', level=log.INFO)


_company_search_service = CompanySearchService(es_client)


router = APIRouter(
    prefix="/jobs",
    tags=["Search Jobs"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
def create_job(doc: c.SearchJobDetailVO = Body(...)):
    data = _company_search_service.create(doc)
    return res_success(data=data)


@router.get("")
def search_jobs(
    size: int = Query(10, gt=0, le=100),
    sort_by: SortField = Query(SortField.UPDATED_AT),
    sort_dirction: SortDirection = Query(SortDirection.DESC),
    search_after: str = Query(None),
):
    query = c.SearchJobListVO(
        size=size,
        sort_by=sort_by,
        sort_dirction=sort_dirction,
        search_after=search_after,
    )
    result = _company_search_service.search(query)
    return res_success(data=result)


@router.put("")
def update_job(doc: c.SearchJobDetailVO = Body(...)):
    data = _company_search_service.update(doc)
    return res_success(data=data)


@router.put("/enable")
def enable_job(doc: c.SearchJobDetailVO = Body(...)):
    data = _company_search_service.enable(doc)
    return res_success(data=data)


@router.put("/remove")
def remove_job(doc: c.SearchJobDetailVO = Body(...)):
    data = _company_search_service.remove(doc)
    return res_success(data=data)
