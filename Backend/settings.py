from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"

    secret_key: str = "change-this-secret-key"

    gemini_api_key: str | None = None

    gemini_model: str = "gemini-2.5-flash"

    database_path: str = "./pocketsmart.db"

    access_token_expire_minutes: int = 120

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()