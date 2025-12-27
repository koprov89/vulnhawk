"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    app_name: str = "VulnHawk API"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./vulnhawk.db"
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
