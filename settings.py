from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration.
    Environment variables are loaded automatically from a .env file.
    """

    # configuration
    PORT: int = Field(..., description="Server port")
    API_KEY: str = Field(..., description="API key for the service")
    FORCE_CACHE_INVOKE: bool = Field(...,
                                     description="When calling the interface, the cache_invoke parameter is mandatory to be True")

    # Load environment variables from .env file using UTF-8 encoding.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Optionally, for use in web frameworks, wrap settings retrieval in a function with caching:
from functools import lru_cache


@lru_cache()
def get_settings() -> Settings:
    return Settings()
