from config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    url=settings.database_url_psycopg,
    #  echo=True,
)

async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    #  echo=True,
)

session_factory = sessionmaker(engine)
async_session_factory = async_sessionmaker(async_engine)
