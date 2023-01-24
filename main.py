import os
from mangum import Mangum
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from src.routers.v1 import search_resumes, search_jobs
from src.exceptions import search_except


STAGE = os.environ.get('STAGE')
root_path = '/' if not STAGE else f'/{STAGE}'
app = FastAPI(title="ForeignTeacher: Search Service", root_path=root_path)


class BusinessException(Exception):
    def __init__(self, term: str):
        self.term = term

@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return JSONResponse(
        status_code=418,
        content={
            "code": 1,
            "msg": f"Oops! {exc.term} is a wrong phrase. Guess again?"
        }
    )


search_except.include_app(app)


router_v1 = APIRouter(prefix="/api/v1")
router_v1.include_router(search_resumes.router)
router_v1.include_router(search_jobs.router)


app.include_router(router_v1)


@app.get("/search/{term}")
async def info(term: str):
    if term != "yolo":
        raise BusinessException(term=term)
    return {"mention": "You only live once"}


# Mangum Handler, this is so important
handler = Mangum(app)
