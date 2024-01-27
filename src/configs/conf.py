import os

ES_REGION = os.getenv("ES_REGION")
ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", "443")
# ES_ACCOUNT = os.getenv("ES_ACCOUNT", "admin")
# ES_PASSWORD = os.getenv("ES_PASSWORD", "admin")
ES_USE_SSL = os.getenv("ES_USE_SSL", "True")
ES_VERIFY_CERTS = os.getenv("ES_VERIFY_CERTS", "True")
ES_SSL_ASSERT_HOSTNAME = os.getenv("ES_SSL_ASSERT_HOSTNAME", "True")
ES_SSL_SHOW_WARN = os.getenv("ES_SSL_SHOW_WARN", "True")

ES_PORT = int(ES_PORT)
ES_USE_SSL = bool(ES_USE_SSL)
ES_VERIFY_CERTS = bool(ES_VERIFY_CERTS)
ES_SSL_ASSERT_HOSTNAME = bool(ES_SSL_ASSERT_HOSTNAME)
ES_SSL_SHOW_WARN = bool(ES_SSL_SHOW_WARN)


INDEX_JOB = os.getenv("INDEX_JOB", "jobs")
INDEX_RESUME = os.getenv("INDEX_RESUME", "resumes")
ES_INDEX_REFRESH = os.getenv("ES_INDEX_REFRESH", "False")
ES_INDEX_REFRESH = bool(ES_INDEX_REFRESH)

# job
# do some mapping in es
MAX_JOB_DICT_DEPTH = int(os.getenv("MAX_JOB_DICT_DEPTH", "3"))
JOB_EXCLUDED_FIELDS = os.getenv("JOB_EXCLUDED_FIELDS", None)
JOB_TRANSFORM_FIELDS = os.getenv("JOB_TRANSFORM_FIELDS", None)

# resume
RESUME_EXCLUDED_FIELDS = os.getenv("RESUME_EXCLUDED_FIELDS", None)
RESUME_TRANSFORM_FIELDS = os.getenv("RESUME_TRANSFORM_FIELDS", None)

if JOB_EXCLUDED_FIELDS is None:
    JOB_EXCLUDED_FIELDS = {
    }
else:
    JOB_EXCLUDED_FIELDS = \
        {field.strip() for field in JOB_EXCLUDED_FIELDS.split(',') if field.strip() != ''}

if JOB_TRANSFORM_FIELDS is None:
    JOB_TRANSFORM_FIELDS = {
        'overview',
        'job_desc',
        'others',
    }
else:
    JOB_TRANSFORM_FIELDS = \
        {field.strip() for field in JOB_TRANSFORM_FIELDS.split(',') if field.strip() != ''}


if RESUME_EXCLUDED_FIELDS is None:
    RESUME_EXCLUDED_FIELDS = {
        'avator',
    }
else:
    RESUME_EXCLUDED_FIELDS = \
        {field.strip() for field in RESUME_EXCLUDED_FIELDS.split(',') if field.strip() != ''}


if RESUME_TRANSFORM_FIELDS is None:
    RESUME_TRANSFORM_FIELDS = {
        'category',
        'name',
        'title',
        'location',
    }
else:
    RESUME_TRANSFORM_FIELDS = \
        {field.strip() for field in RESUME_TRANSFORM_FIELDS.split(',') if field.strip() != ''}
