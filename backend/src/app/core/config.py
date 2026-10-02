from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "AI Application Boilerplate"
    APP_ENV: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["*"]

    # Model Defaults
    DEFAULT_MODEL_PROVIDER: Literal["anthropic", "google", "ollama"] = "anthropic"
    DEFAULT_MODEL_NAME: str = "claude-3-5-sonnet-latest"
    DEFAULT_TEMPERATURE: float = Field(default=0.7, ge=0.0, le=2.0)

    # API Keys & URLs
    ANTHROPIC_API_KEY: str | None = None
    GOOGLE_API_KEY: str | None = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    # LangSmith / Observability
    LANGSMITH_TRACING: bool = False
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str = "fastapi-langgraph-boilerplate"

    # Checkpoint persistence
    CHECKPOINT_DB_PATH: str = "checkpoints.db"


@lru_cache
def get_settings() -> Settings:
    """Returns a cached instance of application settings.
    
    Using @lru_cache prevents reading the disk/.env on every request.
    In FastAPI tests, this can be overridden using app.dependency_overrides.
    """
    return Settings()
