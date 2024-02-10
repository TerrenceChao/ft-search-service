from fastapi import APIRouter
from ...configs.conf import *
from ...configs.constants import *
from ...configs.exceptions import *
# no resume_info_service
from ..res.response import res_success
import logging as log


log.basicConfig(filemode='w', level=log.INFO)


router = APIRouter(
    prefix='/resumes-info',
    tags=['Resume Related Info'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/tags')
def get_continents():
    return res_success(data={'tags': RESUME_TAGS})
