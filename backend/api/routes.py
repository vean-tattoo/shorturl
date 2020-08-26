import datetime
from sqlalchemy import select
from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from sqlite3 import IntegrityError
from .config import urls, database
from .models import UrlIn, Url
from short_url import encode_url
from typing import List

router = APIRouter()

def get_current_time():
    return encode_url(int(datetime.datetime.now().timestamp()))

async def create_url(url):
    try:
        short_code = get_current_time()
        query = urls.insert().values(url=url, short_code=short_code)
        _id = await database.execute(query)
        return Url(id=_id, url=url, short_code=short_code)
    except IntegrityError:
        return await create_url(url)

@router.post('/generate', response_model=Url)
async def generate_url(data: UrlIn):
    if not data.url: raise HTTPException(400, "No url provided")
    return await create_url(data.url)


# @router.get('/list', response_model=List[Url])
# async def list_urls():
#     query = urls.select()
#     return await database.fetch_all(query)

@router.get('/{short_code}')
async def redirect_by_hash(short_code: str):
    result = await database.fetch_one(
        "SELECT urls.url FROM urls WHERE urls.short_code = :short_code", 
        {"short_code": short_code}
    )
    if result:
        return RedirectResponse(url=result[0])
    raise HTTPException(404)
