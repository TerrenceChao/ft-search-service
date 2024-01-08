from typing import List, Any, Dict
from ...domains.company import c_value_objects as c
from ...configs.conf import INDEX_JOB, ES_INDEX_REFRESH
from ...configs.exceptions import *
from ...infra.utils.time_util import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class CompanySearchService:
    
    def __init__(self, client: Any):
        self.client = client
        # TODO: read "time & es-cluster mapping" from db
        # and cache the mapping
        # 或是其他在 app 啟動時就會讀取資料的時機緩存 local 就好
        
    def __index_id(self, doc: c.SearchJobDetailVO):
        return f'{doc.published_in}-{doc.jid}'

    '''
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.updated_at]
    - create index in es-cluster-1 with jid
    '''
    def create(self, doc: c.SearchJobDetailVO):
        try:
            self.client.index(
                index=INDEX_JOB,
                id=self.__index_id(doc),
                body=doc.dict(), 
                refresh=ES_INDEX_REFRESH,
            )
            return doc
        
        except Exception as e:
            log.error("create_job, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="create job fail")


    '''
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.updated_at]
    
    考慮銜接 跨 es-cluster 的搜尋
    '''
    def search(self, query: c.SearchJobListVO):
        req_body = None
        resp = None
        
        try:
            req_body = {
                "size": query.size,
                "query": {
                    "match": {
                        "enable": True
                    }
                },
                "sort": [
                    {
                        query.sort_by.value: query.sort_dirction.value
                    }
                ],
                "_source": {
                    "includes": c.SearchJobDetailVO.include_fields(),
                }
            }
            if query.search_after:
                req_body["search_after"] = [query.search_after]
            
            resp = self.client.search(
                index=INDEX_JOB, 
                body=req_body,
            )
            items = resp['hits']['hits']
            items = list(map(lambda x: x["_source"], items))
            return c.JobListVO(sort_by=query.sort_by, items=items)
        
        except Exception as e:
            log.error("search_jobs, query: %s, req_body: %s, resp: %s, err: %s", 
                      query, req_body, resp, str(e))
            raise ServerException(msg="no job found")
    

    '''
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.last_updated_at]
    - if [month of doc.last_updated_at] == [month of doc.updated_at]
        update index in es-cluster-1 with jid
        else
        TODO: get es-cluster-2 by [month of doc.updated_at]
        create index by [month of doc.updated_at] in es-cluster-2 with jid
        delete index in [month of doc.last_updated_at] es-cluster-1 with jid
    '''
    def update(self, doc: c.SearchJobDetailVO):
        try:
            self.client.update(
                index=INDEX_JOB, 
                id=self.__index_id(doc),
                body={"doc": doc.dict()},
                refresh=ES_INDEX_REFRESH,
            )
            return doc
        
        except Exception as e:
            log.error("update_job, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="update job fail")
        
        
    def enable(self, doc: c.SearchJobDetailVO):
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
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.updated_at]
    - delete index in es-cluster-1 with jid
    '''
    def remove(self, doc: c.SearchJobDetailVO):
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
