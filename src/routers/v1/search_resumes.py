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
    prefix="/search/resumes",
    tags=["Search Resumes"],
    responses={404: {"description": "Not found"}},
)

INDEX_RESUME = "resumes"


@router.post("")
def create_resume(doc: Dict = Body(...), client: Any = Depends(get_search_client)):
    try:
        doc["views"] = 0
        client.index(index=INDEX_RESUME, body=doc, id=doc["rid"])
        return res_success(data=doc)
    except Exception as e:
        log.error("create_resume: %s", str(e))
        raise ServerException(msg="create resume fail")


@router.get("")
def search_resumes(client: Any = Depends(get_search_client)):
    try:
        resp = client.search(index=INDEX_RESUME, body={
            "query": {
                "match": {
                    "enable": True
                }
            },
            "_source": {
                "includes": [
                    "rid",
                    "tid",
                    "avator",
                    "fullname",
                    "email",
                    "intro",
                    "updated_at",
                    "created_at",
                ],
            }
        })
        data = resp['hits']['hits']
        data = list(map(lambda x: x["_source"], data))
        return res_success(data=data)
    except Exception as e:
        log.error("search_resumes: %s", str(e))
        raise ServerException(msg="no resume found")


@router.get("/{rid}")
def find_resume(rid: str, client: Any = Depends(get_search_client)):
    try:
        resp = client.search(index=INDEX_RESUME, body={
            "query": {
                "match": {
                    "rid": rid
                }
            }
        })
        data = resp['hits']['hits']
        data = list(map(lambda x: x["_source"], data))
        return res_success(data=data)
    except Exception as e:
        log.error("search_resumes: %s", str(e))
        raise ServerException(msg="no resume found")


@router.put("/{rid}")
def update_resume(rid: str, doc: Dict = Body(...), client: Any = Depends(get_search_client)):
    try:
        client.update(index=INDEX_RESUME, body={"doc": doc}, id=rid, refresh=True)
        return res_success(data=doc)
    except Exception as e:
        log.error("update_resume: %s", str(e))
        raise ServerException(msg="update resume fail")
