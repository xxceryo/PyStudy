from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PyStudy API"
    debug: bool = True
    database_url: str = "mysql+asyncmy://root:123456@127.0.0.1:13306/pystudy"
    auto_create_tables: bool = False
    redis_url: str = "redis://:123456@127.0.0.1:16379/0"
    jwt_secret_key: str = "change-this-development-secret-before-production"
    access_token_expire_seconds: int = 86400

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PYSTUDY_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
