from typing import List, Any, Dict
from . import t_value_objects as t
from ...configs.conf import INDEX_RESUME, ES_INDEX_REFRESH
from ...configs.exceptions import *
from ...infra.utils.time_util import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


class ResumeSearchService:
    
    def __init__(self, client: Any):
        self.client = client
        # TODO: read "time & es-cluster mapping" from db
        # and cache the mapping
        # 或是其他在 app 啟動時就會讀取資料的時機緩存 local 就好

    def __index_id(self, doc: t.SearchResumeDetailDTO):
        return f'{doc.region}-{doc.rid}'

    '''
    TODO:
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.updated_at]
    - create index in es-cluster-1 with rid
    '''
    def create(self, doc: t.SearchResumeDetailDTO):
        try:
            self.client.index(
                index=INDEX_RESUME, 
                id=self.__index_id(doc),
                body=doc.dict_for_create(), # FIXME: body=doc.model(),
                refresh=ES_INDEX_REFRESH,
            )
            return doc

        except Exception as e:
            log.error("create_resume, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="create resume fail")
        

    '''
    TODO:
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.updated_at]
    
    考慮銜接 跨 es-cluster 的搜尋
    '''
    def search(self, query: t.SearchResumeListQueryDTO):
        req_body = None
        resp = None
        
        try:
            req_body = {
                "size": query.size,
                "query": {
                    "term": {
                        "enable": {
                            "value": True,
                        },
                    },
                },
                "sort": [
                    {
                        query.sort_by.value: query.sort_dirction.value,
                    },
                ],
                "_source": {
                    "includes": t.SearchResumeDetailDTO.include_fields(),
                },
            }
            if query.search_after:
                req_body["search_after"] = [query.search_after]
            
            resp = self.client.search(
                index=INDEX_RESUME, 
                body=req_body,
            )
            items = resp['hits']['hits']
            items = list(map(lambda x: x["_source"], items))
            return t.SearchResumeListVO(
                size=query.size, 
                sort_by=query.sort_by, 
                items=items
            )
        
        except Exception as e:
            log.error("search_resumes, query: %s, req_body: %s, resp: %s, err: %s", 
                      query, req_body, resp, str(e))
            raise ServerException(msg="no resume found")


    '''
    TODO:
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.last_updated_at]
    - if [month of doc.last_updated_at] == [month of doc.updated_at]
        update index in es-cluster-1 with rid
        else
        TODO: get es-cluster-2 by [month of doc.updated_at]
        create index [month of doc.updated_at] in es-cluster-2 with rid
        delete index [month of doc.last_updated_at] in es-cluster-1 with rid
    '''
    def update(self, doc: t.SearchResumeDetailDTO):
        try:
            self.client.update(
                index=INDEX_RESUME,
                id=self.__index_id(doc),
                body={"doc": doc.dict_for_update()}, # FIXME: body={"doc": doc.model()},
                refresh=ES_INDEX_REFRESH,
            )
            return doc
        
        except Exception as e:
            log.error("update_resume, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="update resume fail")
        
        
    def enable(self, doc: t.SearchResumeDetailDTO):
        try:
            self.client.update(
                index=INDEX_RESUME, 
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
            log.error("enable_resume, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="enable resume fail")


    '''
    TODO:
    - read mapping from cache (or local cache)
    - get es-cluster-1 by [month of doc.updated_at]
    - delete index in es-cluster-1 with rid
    '''
    def remove(self, doc: t.SearchResumeDetailDTO):
        try:
            self.client.delete(
                index=INDEX_RESUME, 
                id=self.__index_id(doc),
                refresh=ES_INDEX_REFRESH,
            )
            return doc
        
        except Exception as e:
            log.error("remove_resume, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="remove resume fail")

    def delete_resume_index(self):
        try:
            self.client.indices.delete(index=INDEX_RESUME)
        
        except Exception as e:
            log.error("delete_resume_index, err: %s", str(e))
            raise ServerException(msg="delete_resume_index fail")
