from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings

engine = create_engine(
    url=settings.database_url_psycopg,
    # echo=True,
)

session_factory = sessionmaker(bind=engine)
