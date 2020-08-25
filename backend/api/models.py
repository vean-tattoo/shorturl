from pydantic import BaseModel


class UrlIn(BaseModel):
    url: str


class Url(UrlIn):
    id: int
    short_code: str
