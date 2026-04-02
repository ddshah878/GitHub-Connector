from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    github_token: str
    github_api_base_url: str = "https://api.github.com"

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
