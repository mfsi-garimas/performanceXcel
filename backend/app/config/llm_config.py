from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Centralized application configuration.
    Loads values from .env automatically.
    """

    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL_NAME: str 
    OPENAI_TEMPERATURE: float 

    # Application
    MAX_ITERATIONS: int = 6

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    Ensures only one config object exists.
    """
    return Settings()