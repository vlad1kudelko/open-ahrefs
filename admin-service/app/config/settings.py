from functools import lru_cache

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str
    KAFKA_HOST: str
    KAFKA_PORT: str

    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
    )

    @property
    def database_url_psycopg(self) -> str:
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def database_url_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def kafka_url(self) -> str:
        return f"${self.KAFKA_HOST}:${self.KAFKA_PORT}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
