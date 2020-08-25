import databases
import sqlalchemy


DATABASE_URL = "sqlite:////db.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

urls = sqlalchemy.Table(
    "urls",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("url", sqlalchemy.String),
    sqlalchemy.Column("short_code", sqlalchemy.String, unique=True),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
