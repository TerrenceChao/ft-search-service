from typing import List, Any, Dict
from . import t_value_objects as t
from ...configs.conf import \
    INDEX_RESUME, ES_INDEX_REFRESH, RESUME_SEARCH_FIELDS
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
            doc_dict = doc.dict_for_create()
            self.client.index(
                index=INDEX_RESUME,
                id=self.__index_id(doc),
                body=doc_dict,  # FIXME: body=doc.model(),
                refresh=ES_INDEX_REFRESH,
            )
            return doc

        except Exception as e:
            log.error("create_resume, doc: %s, err: %s", doc, str(e))
            raise ServerException(msg="create resume fail")

    def __terms_search(self, must: List[Dict[str, Any]], query: t.SearchResumeListQueryDTO):
        if len(query.tags) > 0:
            query.tags = [tag.strip().lower() for tag in query.tags
                          if tag != None and tag.strip() != '']
            must.append({
                "terms": {
                    "tags": query.tags,
                }
            })

        return must

    def __should_search(self, must: List[Dict[str, Any]], patterns: List[str]):
        if len(patterns) > 0:
            search_patterns = list(map(self.__resume_search, patterns))
            must.append({
                "bool": {
                    "should": search_patterns,
                },
            })
        return must

    def __resume_search(self, pattern: str):
        return {
            'multi_match': {
                'query': pattern,
                'fields': list(RESUME_SEARCH_FIELDS),
                'type': 'phrase',
            }
        }

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
            must = [
                {
                    "term": {
                        "enable": True
                    },
                },
            ]
            must = self.__terms_search(must, query)
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
            doc_dict = doc.dict_for_update()
            self.client.update(
                index=INDEX_RESUME,
                id=self.__index_id(doc),
                # FIXME: body={"doc": doc.model()},
                body={"doc": doc_dict},
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
