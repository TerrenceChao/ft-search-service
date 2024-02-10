from typing import List, Any, Dict
from . import c_value_objects as c
from ...configs.conf import \
    INDEX_JOB, ES_INDEX_REFRESH, JOB_SEARCH_FIELDS
from ...configs.exceptions import *
from ...infra.utils.time_util import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class JobSearchService:

    def __init__(self, client: Any):
        self.client = client
        # TODO: read "time & es-cluster mapping" from db
        # and cache the mapping
        # 或是其他在 app 啟動時就會讀取資料的時機緩存 local 就好

    def __index_id(self, doc: c.SearchJobDetailDTO):
        return f'{doc.region}-{doc.jid}'

    '''
    TODO:
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.updated_at]
    - create index in es-cluster-1 with jid
    '''

    def create(self, doc: c.SearchJobDetailDTO):
        try:
            doc_dict = doc.dict_for_create()
            self.client.index(
                index=INDEX_JOB,
                id=self.__index_id(doc),
                body=doc_dict,  # FIXME: body=doc.model(),
                refresh=ES_INDEX_REFRESH,
            )
            return doc

        except Exception as e:
            log.error("create_job, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="create job fail")


    def __match_search(self, must: List[Dict[str, Any]], query: c.SearchJobListQueryDTO):
        if query.continent_code is not None and query.continent_code.strip():
            must.append({
                "match": {
                    "continent_code": query.continent_code,
                }
            })

        if query.country_code is not None and query.country_code.strip():
            must.append({
                "match": {
                    "country_code": query.country_code,
                }
            })

        return must


    def __should_search(self, must: List[Dict[str, Any]], patterns: List[str]):
        if len(patterns) > 0:
            search_patterns = list(map(self.__job_search, patterns))
            must.append({
                "bool": {
                    "should": search_patterns,
                },
            })
        return must


    def __job_search(self, pattern: str):
        return {
            'multi_match': {
                'query': pattern,
                'fields': list(JOB_SEARCH_FIELDS),
                'type': 'phrase',
            }
        }


    '''
    TODO:
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.updated_at]
    
    考慮銜接 跨 es-cluster 的搜尋
    '''

    def search(self, query: c.SearchJobListQueryDTO):
        req_body = None
        resp = None
        try:
            must = [
                {
                    "term": {
                        "enable": True
                    },
                },
            ]
            must = self.__match_search(must, query)
            must = self.__should_search(must, query.patterns)
            req_body = {
                "size": query.size,
                "query": {
                    "bool": {
                        "must": must,
                    },
                },
                "sort": [
                    {
                        query.sort_by.value: query.sort_dirction.value,
                    },
                ],
                "_source": {
                    "includes": c.SearchJobDetailDTO.include_fields(),
                },
            }
            if query.search_after:
                req_body["search_after"] = [query.search_after]

            resp = self.client.search(
                index=INDEX_JOB,
                body=req_body,
            )
            items = resp['hits']['hits']
            items = list(map(lambda x: x["_source"], items))
            return c.SearchJobListVO(
                size=query.size,
                sort_by=query.sort_by,
                items=items
            )

        except Exception as e:
            log.error("search_jobs, query: %s, req_body: %s, resp: %s, err: %s",
                      query, req_body, resp, str(e))
            raise ServerException(msg="no job found")

    '''
    TODO:
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.last_updated_at]
    - if [month of doc.last_updated_at] == [month of doc.updated_at]
        update index in es-cluster-1 with jid
        else
        TODO: get es-cluster-2 by [month of doc.updated_at]
        create index by [month of doc.updated_at] in es-cluster-2 with jid
        delete index in [month of doc.last_updated_at] es-cluster-1 with jid
    '''

    def update(self, doc: c.SearchJobDetailDTO):
        try:
            doc_dict = doc.dict_for_update()
            self.client.update(
                index=INDEX_JOB,
                id=self.__index_id(doc),
                body={"doc": doc_dict},  # FIXME: body={"doc": doc.model()},
                refresh=ES_INDEX_REFRESH,
            )
            return doc

        except Exception as e:
            log.error("update_job, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="update job fail")

    def enable(self, doc: c.SearchJobDetailDTO):
        try:
            self.client.update(
                index=INDEX_JOB,
                id=self.__index_id(doc),
                body={
                    "doc": {
                        "enable": doc.enable
                    }
                },
                refresh=ES_INDEX_REFRESH,
            )
            return doc

        except Exception as e:
            log.error("enable_job, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="enable job fail")

    '''
    TODO:
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.updated_at]
    - delete index in es-cluster-1 with jid
    '''

    def remove(self, doc: c.SearchJobDetailDTO):
        try:
            self.client.delete(
                index=INDEX_JOB,
                id=self.__index_id(doc),
                refresh=ES_INDEX_REFRESH,
            )
            return doc

        except Exception as e:
            log.error("remove_job, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="remove job fail")

    def delete_job_index(self):
        try:
            self.client.indices.delete(index=INDEX_JOB)

        except Exception as e:
            log.error("delete_job_index, err: %s", str(e))
            raise ServerException(msg="delete_job_index fail")
