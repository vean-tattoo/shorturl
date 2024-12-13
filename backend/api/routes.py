import random
import string
from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from sqlalchemy import select
from urllib.parse import urlparse

from .config import database, urls
from .models import UrlIn, Url

router = APIRouter()

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def generate_short_code(min_length=4, max_length=9):
    """Генерация случайной строки с динамической длиной."""
    length = random.randint(min_length, max_length)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def find_unique_short_code():
    """Генерация и проверка уникальности short_code."""
    for attempt in range(200):
        short_code = generate_short_code()
        query = select(urls.c.short_code).where(urls.c.short_code == short_code)
        result = await database.fetch_one(query)
        if not result:
            return short_code
    raise HTTPException(500, "Could not generate a unique short code after multiple attempts")

async def create_url(url):
    """Создание новой записи с уникальным short_code."""
    short_code = await find_unique_short_code()
    query = urls.insert().values(
        url=url,
        short_code=short_code,
    )
    _id = await database.execute(query)
    return Url(id=_id, url=url, short_code=short_code)

@router.post("/generate", response_model=Url)
async def generate_url(data: UrlIn):
    if not data.url or not is_valid_url(data.url):
        raise HTTPException(400, "Invalid URL provided")
    return await create_url(data.url)

@router.get("/{short_code}")
async def redirect_by_hash(short_code: str):
    query = select(urls.c.url).where(urls.c.short_code == short_code)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(404, "URL not found")
    return RedirectResponse(url=result["url"])
