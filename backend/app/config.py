"""Central configuration. Everything comes from environment variables.

Never hardcode secrets; see .env.example at the repo root.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Postgres (Supabase pooler URL works as-is)
    database_url: str

    # Auth
    secret_key: str
    token_ttl_hours: int = 72

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-5.6-luna"
    openai_reasoning_effort: str = "xhigh"

    # Storage for uploads and generated files
    data_dir: str = "./data"

    # Comma-separated list of allowed origins for CORS
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()
