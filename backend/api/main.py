
from fastapi import FastAPI, Request
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from .config import database
from .routes import router

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(
    router,
    responses={404: {"description": "Not found"}}
)
