import time
import json
from typing import List, Dict, Any
from fastapi import APIRouter, \
    Depends, Path, Query, Body, Form, status
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
    prefix="/search/jobs",
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
    search_after: int = Query(None, gt=0),
):
    query = c.SearchJobListVO(
        size=size,
        sort_by=sort_by,
        sort_dirction=sort_dirction,
        search_after=search_after,
    )
    result = _company_search_service.search(query)
    return res_success(data=result)


# TODO: 透過 match service 查詢
@router.get("/{jid}")
def find_job(jid: str):
    try:
        resp = es_client.search(index=INDEX_JOB, body={
            "query": {
                "match": {
                    "jid": jid
                }
            }
        })
        data = resp['hits']['hits']
        data = list(map(lambda x: x["_source"], data))
        return res_success(data=data)
    except Exception as e:
        log.error("search_jobs: %s", str(e))
        raise ServerException(msg="no job found")


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
