from datetime import datetime
import os
import databases
from sqlalchemy import DateTime, Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:////db.db"

metadata = MetaData()
database = databases.Database(DATABASE_URL)

urls = Table(
    "urls",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", String),
    Column("short_code", String, unique=True, index=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)

engine = create_engine(
    DATABASE_URL,
)
metadata.create_all(engine)
