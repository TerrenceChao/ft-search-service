import os
import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from .conf import *
import logging as log

log.basicConfig(filemode='w', level=log.INFO)


if ES_ACCOUNT is None or ES_PASSWORD is None:
    service = 'es'
    credentials = boto3.Session().get_credentials()
    http_auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        ES_REGION,
        service,
        session_token=credentials.token
    )
else:
    http_auth = (ES_ACCOUNT, ES_PASSWORD)

client = OpenSearch(
    hosts=[{"host": ES_HOST, "port": ES_PORT}],
    http_auth=http_auth,
    use_ssl=ES_USE_SSL,
    verify_certs=ES_VERIFY_CERTS,
    ssl_assert_hostname=ES_SSL_ASSERT_HOSTNAME,
    ssl_show_warn=ES_SSL_SHOW_WARN,
    connection_class=RequestsHttpConnection
)
client.info()


def get_search_client():
    try:
        yield client
    except Exception as e:
        log.error(e.__str__())
        raise
    finally:
        pass
