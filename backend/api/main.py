from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import database
from .routes import router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(
    router,
    responses={404: {"description": "Not found"}},
)
