import time
import json
from typing import List, Dict, Any
from fastapi import APIRouter, \
    Depends, Path, Query, Body, Form, \
    status, HTTPException

from ...config.elasticsearch import get_search_client
from ...exceptions.search_except import \
    ClientException, NotFoundException, ServerException
from ..res.response import res_success, res_err
import logging as log


log.basicConfig(filemode='w', level=log.INFO)


router = APIRouter(
    prefix="/search/jobs",
    tags=["Search Jobs"],
    responses={404: {"description": "Not found"}},
)

INDEX_JOB = "jobs"


@router.post("")
def create_job(doc: Dict = Body(...), client: Any = Depends(get_search_client)):
    try:
        doc["views"] = 0
        client.index(index=INDEX_JOB, body=doc, id=doc["jid"])
        return res_success(data=doc)
    except Exception as e:
        log.error("create_job: %s", str(e))
        raise ServerException(msg="create job fail")


@router.get("")
def search_jobs(client: Any = Depends(get_search_client)):
    try:
        resp = client.search(index=INDEX_JOB, body={
            "query": {
                "match": {
                    "enable": True
                }
            },
            "_source": {
                "includes": [
                    "jid",
                    "cid",
                    "title",
                    "region",
                    "salary",
                    "job_desc",
                    "others",
                    "views",
                    "updated_at",
                    "created_at",
                ],
            }
        })
        data = resp['hits']['hits']
        data = list(map(lambda x: x["_source"], data))
        return res_success(data=data)
    except Exception as e:
        log.error("search_jobs: %s", str(e))
        raise ServerException(msg="no job found")


@router.get("/{jid}")
def find_job(jid: str, client: Any = Depends(get_search_client)):
    try:
        resp = client.search(index=INDEX_JOB, body={
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


@router.put("/{jid}")
def update_job(jid: str, doc: Dict = Body(...), client: Any = Depends(get_search_client)):
    try:
        client.update(index=INDEX_JOB, body={"doc": doc}, id=jid, refresh=True)
        return res_success(data=doc)
    except Exception as e:
        log.error("update_job: %s", str(e))
        raise ServerException(msg="update job fail")
