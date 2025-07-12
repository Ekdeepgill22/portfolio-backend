# Environment configuration
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # MongoDB Configuration
    mongodb_uri: str = "mongodb://localhost:27017/portfolio_db"
    database_name: str = "portfolio_db"
    
    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-portfolio.vercel.app"
    ]
    
    # Environment
    environment: str = "development"
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "Portfolio Backend"
    
    # Static files configuration
    static_files_path: str = "app/static"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def is_development(self) -> bool:
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()