from app.config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    url=settings.database_url_psycopg,
    echo=True,
)

session_factory = sessionmaker(bind=engine)
