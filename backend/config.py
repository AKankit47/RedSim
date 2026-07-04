"""
RedSim - Application Configuration
Loads settings from environment variables / .env file.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    secret_key: str = "redsim-super-secret-jwt-key-2024-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    database_url: str = "sqlite:///./redsim.db"
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"
    app_env: str = "development"
    log_dir: str = "../logs"
    report_dir: str = "../reports"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
