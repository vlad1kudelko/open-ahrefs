from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings
from .models import Base

engine = create_engine(
    url=settings.database_url_psycopg,
    #echo=True,
)
session_factory = sessionmaker(bind=engine)


def init_db() -> None:
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
