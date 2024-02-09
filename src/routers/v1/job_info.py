from fastapi import APIRouter
from ...configs.conf import *
from ...configs.constants import *
from ...configs.exceptions import *
from ...domains.company.job_info_service import JobInfoService
from ..res.response import res_success
import logging as log


log.basicConfig(filemode='w', level=log.INFO)

_job_info_service = JobInfoService()

router = APIRouter(
    prefix='/jobs-info',
    tags=['Job Related Info'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/continents')
def get_continents():
    data = _job_info_service.get_continents()
    return res_success(data=data)


# TODO: this route rule(get_all_continents_and_countries) is same as 'get_countries',
# so it has to be put before 'get_countries'
@router.get('/continents/all/countries')
def get_all_continents_and_countries():
    data = _job_info_service.get_all_continents_and_countries()
    return res_success(data=data)


@router.get('/continents/{continent_code}/countries')
def get_countries(continent_code: str):
    data = _job_info_service.get_countries(continent_code)
    return res_success(data=data)
