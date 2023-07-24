import uuid
from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse
from sqlalchemy import select

from .config import urls, database
from .models import UrlIn, Url

router = APIRouter()


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


async def create_url(url):
    short_code = str(uuid.uuid4())[
        :8
    ]  # Using UUID for a more unique short_code
    query = urls.insert().values(url=url, short_code=short_code)
    try:
        _id = await database.execute(query)
        return Url(id=_id, url=url, short_code=short_code)
    except IntegrityError:
        return HTTPException(500, "An error occurred, please try again later")


@router.post("/generate", response_model=Url)
async def generate_url(data: UrlIn):
    if not data.url or not is_valid_url(data.url):
        raise HTTPException(400, "Invalid URL provided")

    return await create_url(data.url)


@router.get("/{short_code}")
async def redirect_by_hash(short_code: str):
    query = select([urls]).where(urls.c.short_code == short_code)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(404, "URL not found")

    return RedirectResponse(url=result["url"])
