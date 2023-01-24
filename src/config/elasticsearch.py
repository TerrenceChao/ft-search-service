import os
import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import logging as log

log.basicConfig(filemode='w', level=log.INFO)

ES_REGION = os.getenv("ES_REGION")
ES_HOST = os.getenv("ES_HOST", "localhost")
# ES_ACCOUNT = os.getenv("ES_ACCOUNT", "admin")
# ES_PASSWORD = os.getenv("ES_PASSWORD", "admin")
ES_USE_SSL = os.getenv("ES_USE_SSL", "True")
ES_VERIFY_CERTS = os.getenv("ES_VERIFY_CERTS")
ES_SSL_ASSERT_HOSTNAME = os.getenv("ES_SSL_ASSERT_HOSTNAME")
ES_SSL_SHOW_WARN = os.getenv("ES_SSL_SHOW_WARN")

ES_USE_SSL = bool(ES_USE_SSL)
ES_VERIFY_CERTS = bool(ES_VERIFY_CERTS)
ES_SSL_ASSERT_HOSTNAME = bool(ES_SSL_ASSERT_HOSTNAME)
ES_SSL_SHOW_WARN = bool(ES_SSL_SHOW_WARN)

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, ES_REGION, service, session_token=credentials.token)


client = OpenSearch(
    hosts = [{"host": ES_HOST, "port": 443}],
    http_auth = awsauth,
    use_ssl = ES_USE_SSL,
    verify_certs = ES_VERIFY_CERTS,
    ssl_assert_hostname = ES_SSL_ASSERT_HOSTNAME,
    ssl_show_warn = ES_SSL_SHOW_WARN,
    connection_class = RequestsHttpConnection
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