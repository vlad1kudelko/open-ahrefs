from functools import lru_cache

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    KAFKA_URL: str

    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
