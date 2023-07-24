import os
import databases
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:////db.db"

metadata = MetaData()
database = databases.Database(DATABASE_URL)

urls = Table(
    "urls",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String),
    Column("short_code", String, unique=True),
)

engine = create_engine(
    DATABASE_URL,
)
metadata.create_all(engine)
